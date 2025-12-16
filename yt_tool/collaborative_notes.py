"""
Collaborative Notes System - 协作注释系统
Enable multiple users to annotate the same video with timestamped notes
"""

import json
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional
from .ai_client import get_ai_client


class CollaborativeNotes:
    """Collaborative annotation system for videos"""

    def __init__(self, storage_path: str = ".collaborative_notes.json"):
        self.ai_client = get_ai_client()
        self.storage_path = storage_path
        self.data = self._load_data()

    def _load_data(self) -> Dict:
        """Load collaborative notes from file"""
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "videos": {},
                "users": {},
                "annotations": [],
                "discussions": []
            }

    def _save_data(self):
        """Save data to file"""
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2, default=str)

    def _generate_id(self, content: str) -> str:
        """Generate unique ID"""
        return hashlib.md5(f"{content}{datetime.now().isoformat()}".encode()).hexdigest()[:12]

    def register_video(self, video_id: str, title: str, transcript: str = "") -> Dict[str, Any]:
        """Register a video for collaborative annotation"""
        if video_id not in self.data["videos"]:
            self.data["videos"][video_id] = {
                "title": title,
                "transcript": transcript[:10000],  # Limit transcript size
                "registered_at": datetime.now().isoformat(),
                "collaborators": [],
                "annotation_count": 0
            }
            self._save_data()

        return self.data["videos"][video_id]

    def add_annotation(self, video_id: str, user_id: str, timestamp: str, content: str, annotation_type: str = "note") -> Dict[str, Any]:
        """Add a timestamped annotation to a video"""
        annotation = {
            "id": self._generate_id(content),
            "video_id": video_id,
            "user_id": user_id,
            "timestamp": timestamp,
            "content": content,
            "type": annotation_type,  # note, question, insight, correction, highlight
            "created_at": datetime.now().isoformat(),
            "reactions": {},
            "replies": []
        }

        self.data["annotations"].append(annotation)

        # Update video stats
        if video_id in self.data["videos"]:
            self.data["videos"][video_id]["annotation_count"] += 1
            if user_id not in self.data["videos"][video_id]["collaborators"]:
                self.data["videos"][video_id]["collaborators"].append(user_id)

        self._save_data()
        return annotation

    def reply_to_annotation(self, annotation_id: str, user_id: str, content: str) -> Dict[str, Any]:
        """Reply to an existing annotation"""
        reply = {
            "id": self._generate_id(content),
            "user_id": user_id,
            "content": content,
            "created_at": datetime.now().isoformat()
        }

        for annotation in self.data["annotations"]:
            if annotation["id"] == annotation_id:
                annotation["replies"].append(reply)
                self._save_data()
                return reply

        return {"error": "Annotation not found"}

    def react_to_annotation(self, annotation_id: str, user_id: str, reaction: str) -> Dict[str, Any]:
        """Add a reaction to an annotation"""
        valid_reactions = ["👍", "💡", "❓", "⭐", "🤔", "✅"]

        if reaction not in valid_reactions:
            return {"error": f"Invalid reaction. Use one of: {valid_reactions}"}

        for annotation in self.data["annotations"]:
            if annotation["id"] == annotation_id:
                if reaction not in annotation["reactions"]:
                    annotation["reactions"][reaction] = []
                if user_id not in annotation["reactions"][reaction]:
                    annotation["reactions"][reaction].append(user_id)
                self._save_data()
                return annotation["reactions"]

        return {"error": "Annotation not found"}

    def get_video_annotations(self, video_id: str, sort_by: str = "timestamp") -> List[Dict[str, Any]]:
        """Get all annotations for a video"""
        annotations = [a for a in self.data["annotations"] if a["video_id"] == video_id]

        if sort_by == "timestamp":
            annotations.sort(key=lambda x: x["timestamp"])
        elif sort_by == "newest":
            annotations.sort(key=lambda x: x["created_at"], reverse=True)
        elif sort_by == "popular":
            annotations.sort(key=lambda x: sum(len(r) for r in x["reactions"].values()), reverse=True)

        return annotations

    def get_annotations_by_timestamp(self, video_id: str, start_time: str, end_time: str) -> List[Dict[str, Any]]:
        """Get annotations within a time range"""
        annotations = self.get_video_annotations(video_id)

        def time_to_seconds(t):
            parts = t.split(":")
            if len(parts) == 2:
                return int(parts[0]) * 60 + int(parts[1])
            elif len(parts) == 3:
                return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
            return 0

        start_sec = time_to_seconds(start_time)
        end_sec = time_to_seconds(end_time)

        return [a for a in annotations if start_sec <= time_to_seconds(a["timestamp"]) <= end_sec]

    def generate_collaborative_summary(self, video_id: str, language: str = "中文") -> Dict[str, Any]:
        """Generate a summary from all collaborative annotations"""
        annotations = self.get_video_annotations(video_id)

        if not annotations:
            return {"error": "No annotations found for this video"}

        prompt = f"""根据以下协作注释生成综合总结。

注释内容：
{json.dumps(annotations[:30], ensure_ascii=False, indent=2)}

请生成：
1. 整体主题总结
2. 关键见解（来自用户注释）
3. 常见问题汇总
4. 讨论热点
5. 推荐关注的时间点

返回JSON格式，语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"summary": response}

    def find_related_annotations(self, annotation_id: str, language: str = "中文") -> List[Dict[str, Any]]:
        """Find annotations related to a specific one"""
        target = None
        for a in self.data["annotations"]:
            if a["id"] == annotation_id:
                target = a
                break

        if not target:
            return []

        same_video = [a for a in self.data["annotations"]
                     if a["video_id"] == target["video_id"] and a["id"] != annotation_id]

        prompt = f"""找出与目标注释最相关的注释。

目标注释：
{json.dumps(target, ensure_ascii=False)}

其他注释：
{json.dumps(same_video[:20], ensure_ascii=False)}

返回最相关的5个注释ID及相关原因，JSON数组格式，语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return []

    def generate_discussion_prompts(self, video_id: str, language: str = "中文") -> List[Dict[str, str]]:
        """Generate discussion prompts based on annotations"""
        annotations = self.get_video_annotations(video_id)

        if not annotations:
            return []

        prompt = f"""基于以下视频注释，生成讨论话题引导。

注释：
{json.dumps(annotations[:20], ensure_ascii=False)}

生成5-10个讨论话题，返回JSON数组：
- topic: 话题
- trigger_annotation: 触发这个话题的注释ID
- discussion_angle: 讨论角度
- expected_insights: 期望的见解

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return []

    def get_user_contributions(self, user_id: str) -> Dict[str, Any]:
        """Get all contributions by a user"""
        user_annotations = [a for a in self.data["annotations"] if a["user_id"] == user_id]

        videos_contributed = set(a["video_id"] for a in user_annotations)

        total_reactions = sum(
            sum(len(users) for users in a["reactions"].values())
            for a in user_annotations
        )

        return {
            "user_id": user_id,
            "total_annotations": len(user_annotations),
            "videos_contributed": len(videos_contributed),
            "total_reactions_received": total_reactions,
            "annotation_types": dict(
                (t, len([a for a in user_annotations if a["type"] == t]))
                for t in set(a["type"] for a in user_annotations)
            )
        }

    def export_annotations(self, video_id: str, format: str = "markdown") -> str:
        """Export video annotations"""
        annotations = self.get_video_annotations(video_id)
        video_info = self.data["videos"].get(video_id, {})

        if format == "markdown":
            md = f"# 协作注释: {video_info.get('title', video_id)}\n\n"
            md += f"**协作者:** {len(video_info.get('collaborators', []))}人\n"
            md += f"**注释数:** {len(annotations)}\n\n"
            md += "---\n\n"

            current_minute = -1
            for a in annotations:
                # Group by minute
                try:
                    minute = int(a["timestamp"].split(":")[0])
                    if minute != current_minute:
                        current_minute = minute
                        md += f"\n## {a['timestamp'][:5]}+\n\n"
                except:
                    pass

                type_emoji = {
                    "note": "📝",
                    "question": "❓",
                    "insight": "💡",
                    "correction": "⚠️",
                    "highlight": "⭐"
                }.get(a["type"], "📌")

                md += f"### {type_emoji} [{a['timestamp']}] @{a['user_id']}\n\n"
                md += f"{a['content']}\n\n"

                if a.get("reactions"):
                    reactions_str = " ".join(f"{r}×{len(users)}" for r, users in a["reactions"].items())
                    md += f"*反应: {reactions_str}*\n\n"

                for reply in a.get("replies", []):
                    md += f"> **@{reply['user_id']}回复:** {reply['content']}\n\n"

            return md

        elif format == "json":
            return json.dumps({
                "video": video_info,
                "annotations": annotations
            }, ensure_ascii=False, indent=2)

        elif format == "srt":
            # Export as subtitle format
            srt_lines = []
            for i, a in enumerate(annotations, 1):
                srt_lines.append(f"{i}")
                srt_lines.append(f"{a['timestamp']},000 --> {a['timestamp']},000")
                srt_lines.append(f"[{a['user_id']}] {a['content']}")
                srt_lines.append("")
            return "\n".join(srt_lines)

        return str(annotations)

    def merge_annotations_to_transcript(self, video_id: str, transcript: str) -> str:
        """Merge annotations inline with transcript"""
        annotations = self.get_video_annotations(video_id)

        # Create annotation markers
        markers = {}
        for a in annotations:
            ts = a["timestamp"]
            if ts not in markers:
                markers[ts] = []
            markers[ts].append(f"[{a['type'].upper()}@{a['user_id']}]: {a['content']}")

        # This is a simplified version - actual implementation would need
        # proper timestamp matching with transcript
        result = transcript
        for ts, notes in sorted(markers.items(), reverse=True):
            marker = f"\n\n📌 **[{ts}]** " + " | ".join(notes) + "\n\n"
            result = result.replace(ts, ts + marker, 1)

        return result
