"""
Smart Playlist - 智能播放列表
Automatically curate and organize video playlists based on learning goals
"""

import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from .ai_client import get_ai_client


class SmartPlaylist:
    """Create and manage intelligent video playlists"""

    def __init__(self, storage_path: str = ".smart_playlists.json"):
        self.ai_client = get_ai_client()
        self.storage_path = storage_path
        self.data = self._load_data()

    def _load_data(self) -> Dict:
        """Load playlist data"""
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "playlists": {},
                "video_pool": [],
                "user_preferences": {}
            }

    def _save_data(self):
        """Save data"""
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2, default=str)

    def add_video_to_pool(self, video: Dict[str, Any]):
        """Add a video to the pool for playlist curation"""
        video_entry = {
            "video_id": video.get("video_id", ""),
            "title": video.get("title", ""),
            "channel": video.get("channel", ""),
            "duration": video.get("duration", 0),
            "topics": video.get("topics", []),
            "difficulty": video.get("difficulty", "intermediate"),
            "quality_score": video.get("quality_score", 5),
            "added_at": datetime.now().isoformat()
        }

        # Check if already in pool
        existing_ids = [v["video_id"] for v in self.data["video_pool"]]
        if video_entry["video_id"] not in existing_ids:
            self.data["video_pool"].append(video_entry)
            self._save_data()

        return video_entry

    def create_learning_playlist(self, goal: str, duration_minutes: int = 60, level: str = "intermediate", language: str = "中文") -> Dict[str, Any]:
        """Create a playlist based on learning goal"""
        # Filter videos from pool
        suitable_videos = [
            v for v in self.data["video_pool"]
            if v.get("difficulty", "intermediate") == level or level == "all"
        ]

        prompt = f"""根据学习目标创建一个智能播放列表。

学习目标: {goal}
目标时长: {duration_minutes}分钟
难度级别: {level}

可用视频库:
{json.dumps(suitable_videos[:20], ensure_ascii=False)}

请选择和排序视频，返回JSON格式：
1. playlist_name: 播放列表名称
2. description: 描述
3. videos: 视频数组（按推荐顺序）
   - video_id: 视频ID
   - title: 标题
   - reason: 选择原因
   - learning_focus: 学习重点
4. total_duration: 总时长
5. learning_objectives: 学习目标
6. suggested_schedule: 建议学习安排

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                playlist_data = json.loads(response[json_start:json_end])
            else:
                playlist_data = {"raw": response}
        except json.JSONDecodeError:
            playlist_data = {"raw": response}

        playlist_id = f"pl_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        playlist = {
            "id": playlist_id,
            "goal": goal,
            "level": level,
            "created_at": datetime.now().isoformat(),
            **playlist_data
        }

        self.data["playlists"][playlist_id] = playlist
        self._save_data()

        return playlist

    def create_daily_playlist(self, available_time: int = 30, interests: List[str] = None, language: str = "中文") -> Dict[str, Any]:
        """Create a daily learning playlist"""
        today = datetime.now().strftime("%Y-%m-%d")

        # Get unwatched videos
        watched_ids = self.data.get("user_preferences", {}).get("watched", [])
        unwatched = [v for v in self.data["video_pool"] if v["video_id"] not in watched_ids]

        if interests:
            unwatched = [
                v for v in unwatched
                if any(i.lower() in [t.lower() for t in v.get("topics", [])] for i in interests)
            ]

        # Select videos to fit time
        selected = []
        total_time = 0
        for v in unwatched:
            if total_time + v.get("duration", 0) <= available_time:
                selected.append(v)
                total_time += v.get("duration", 0)
            if total_time >= available_time:
                break

        playlist = {
            "id": f"daily_{today}",
            "name": f"今日学习 - {today}",
            "type": "daily",
            "date": today,
            "videos": selected,
            "total_duration": total_time,
            "target_duration": available_time,
            "created_at": datetime.now().isoformat()
        }

        self.data["playlists"][playlist["id"]] = playlist
        self._save_data()

        return playlist

    def create_topic_deep_dive(self, topic: str, depth: str = "comprehensive", language: str = "中文") -> Dict[str, Any]:
        """Create a deep-dive playlist for a specific topic"""
        topic_videos = [
            v for v in self.data["video_pool"]
            if topic.lower() in [t.lower() for t in v.get("topics", [])]
               or topic.lower() in v.get("title", "").lower()
        ]

        if not topic_videos:
            return {"error": f"No videos found for topic: {topic}"}

        prompt = f"""为话题"{topic}"创建深度学习播放列表。

深度级别: {depth}
可用视频:
{json.dumps(topic_videos[:15], ensure_ascii=False)}

请按学习路径排序（从基础到高级），返回JSON格式：
1. playlist_name: 播放列表名称
2. topic_overview: 话题概述
3. prerequisite_knowledge: 前置知识
4. videos: 视频数组（按学习顺序）
   - video_id, title, sequence_reason, key_concepts
5. milestones: 学习里程碑
6. mastery_checklist: 掌握检查清单

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                playlist_data = json.loads(response[json_start:json_end])
            else:
                playlist_data = {"videos": topic_videos}
        except json.JSONDecodeError:
            playlist_data = {"videos": topic_videos}

        playlist_id = f"topic_{topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}"
        playlist = {
            "id": playlist_id,
            "type": "topic_deep_dive",
            "topic": topic,
            "depth": depth,
            "created_at": datetime.now().isoformat(),
            **playlist_data
        }

        self.data["playlists"][playlist_id] = playlist
        self._save_data()

        return playlist

    def create_spaced_playlist(self, topic: str, total_days: int = 7, daily_time: int = 30, language: str = "中文") -> Dict[str, Any]:
        """Create a spaced learning playlist over multiple days"""
        topic_videos = [
            v for v in self.data["video_pool"]
            if topic.lower() in [t.lower() for t in v.get("topics", [])]
        ]

        # Distribute videos across days
        days_schedule = []
        video_index = 0

        for day in range(total_days):
            day_videos = []
            day_time = 0

            while video_index < len(topic_videos) and day_time < daily_time:
                video = topic_videos[video_index]
                if day_time + video.get("duration", 0) <= daily_time:
                    day_videos.append(video)
                    day_time += video.get("duration", 0)
                video_index += 1

            days_schedule.append({
                "day": day + 1,
                "videos": day_videos,
                "total_time": day_time,
                "review_previous": day > 0
            })

        playlist = {
            "id": f"spaced_{topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}",
            "name": f"{topic} - {total_days}天学习计划",
            "type": "spaced_learning",
            "topic": topic,
            "total_days": total_days,
            "daily_target": daily_time,
            "schedule": days_schedule,
            "created_at": datetime.now().isoformat()
        }

        self.data["playlists"][playlist["id"]] = playlist
        self._save_data()

        return playlist

    def reorder_playlist(self, playlist_id: str, criteria: str = "difficulty", language: str = "中文") -> Dict[str, Any]:
        """Reorder playlist based on criteria"""
        if playlist_id not in self.data["playlists"]:
            return {"error": "Playlist not found"}

        playlist = self.data["playlists"][playlist_id]
        videos = playlist.get("videos", [])

        if criteria == "difficulty":
            difficulty_order = {"beginner": 0, "easy": 1, "intermediate": 2, "advanced": 3, "expert": 4}
            videos.sort(key=lambda v: difficulty_order.get(v.get("difficulty", "intermediate"), 2))
        elif criteria == "duration":
            videos.sort(key=lambda v: v.get("duration", 0))
        elif criteria == "quality":
            videos.sort(key=lambda v: v.get("quality_score", 5), reverse=True)

        playlist["videos"] = videos
        playlist["last_reordered"] = datetime.now().isoformat()
        playlist["order_criteria"] = criteria

        self._save_data()
        return playlist

    def get_next_video(self, playlist_id: str) -> Dict[str, Any]:
        """Get next unwatched video in playlist"""
        if playlist_id not in self.data["playlists"]:
            return {"error": "Playlist not found"}

        playlist = self.data["playlists"][playlist_id]
        watched = self.data.get("user_preferences", {}).get("watched", [])

        for video in playlist.get("videos", []):
            if video.get("video_id") not in watched:
                return video

        return {"message": "All videos watched", "completed": True}

    def mark_video_watched(self, video_id: str):
        """Mark a video as watched"""
        if "user_preferences" not in self.data:
            self.data["user_preferences"] = {}
        if "watched" not in self.data["user_preferences"]:
            self.data["user_preferences"]["watched"] = []

        if video_id not in self.data["user_preferences"]["watched"]:
            self.data["user_preferences"]["watched"].append(video_id)
            self._save_data()

    def get_playlist_progress(self, playlist_id: str) -> Dict[str, Any]:
        """Get progress for a playlist"""
        if playlist_id not in self.data["playlists"]:
            return {"error": "Playlist not found"}

        playlist = self.data["playlists"][playlist_id]
        videos = playlist.get("videos", [])
        watched = self.data.get("user_preferences", {}).get("watched", [])

        watched_count = sum(1 for v in videos if v.get("video_id") in watched)
        total_count = len(videos)

        return {
            "playlist_id": playlist_id,
            "total_videos": total_count,
            "watched_videos": watched_count,
            "progress_percent": round(watched_count / total_count * 100, 1) if total_count > 0 else 0,
            "remaining": total_count - watched_count
        }

    def list_playlists(self) -> List[Dict[str, Any]]:
        """List all playlists"""
        return [
            {
                "id": p["id"],
                "name": p.get("name", p.get("playlist_name", p["id"])),
                "type": p.get("type", "custom"),
                "video_count": len(p.get("videos", [])),
                "created_at": p.get("created_at")
            }
            for p in self.data["playlists"].values()
        ]

    def export_playlist(self, playlist_id: str, format: str = "markdown") -> str:
        """Export playlist"""
        if playlist_id not in self.data["playlists"]:
            return "Playlist not found"

        playlist = self.data["playlists"][playlist_id]

        if format == "markdown":
            md = f"# {playlist.get('name', playlist.get('playlist_name', playlist_id))}\n\n"
            md += f"**类型:** {playlist.get('type', 'custom')}\n"
            md += f"**创建时间:** {playlist.get('created_at', 'N/A')}\n\n"

            if playlist.get("description"):
                md += f"{playlist['description']}\n\n"

            md += "## 视频列表\n\n"
            for i, v in enumerate(playlist.get("videos", []), 1):
                md += f"{i}. **{v.get('title', v.get('video_id'))}**\n"
                if v.get("reason"):
                    md += f"   - 原因: {v['reason']}\n"
                if v.get("duration"):
                    md += f"   - 时长: {v['duration']}分钟\n"
                md += "\n"

            return md

        elif format == "json":
            return json.dumps(playlist, ensure_ascii=False, indent=2)

        return str(playlist)
