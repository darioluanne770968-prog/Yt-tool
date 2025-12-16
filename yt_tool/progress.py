"""
Learning progress tracking
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional


class ProgressTracker:
    """Track learning progress across videos"""

    def __init__(self, data_file: str = None):
        """
        Initialize progress tracker

        Args:
            data_file: Path to data file
        """
        self.data_file = data_file or os.path.expanduser("~/.yt-tool/progress.json")
        self.data = self._load_data()

    def _load_data(self) -> Dict:
        """Load progress data from file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass

        return {
            "videos": {},
            "playlists": {},
            "notes": {},
            "stats": {
                "total_videos": 0,
                "total_watch_time": 0,
                "notes_count": 0,
            },
        }

    def _save_data(self):
        """Save progress data to file"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def add_video(
        self,
        video_id: str,
        title: str = "",
        duration: int = 0,
        status: str = "to_watch",
        notes: str = "",
        tags: List[str] = None,
    ) -> Dict:
        """
        Add or update video in tracking

        Args:
            video_id: YouTube video ID
            title: Video title
            duration: Video duration in seconds
            status: to_watch, watching, completed
            notes: Personal notes
            tags: Tags for categorization

        Returns:
            Updated video entry
        """
        if video_id not in self.data["videos"]:
            self.data["videos"][video_id] = {
                "id": video_id,
                "title": title,
                "duration": duration,
                "status": status,
                "notes": notes,
                "tags": tags or [],
                "added_at": datetime.now().isoformat(),
                "completed_at": None,
                "progress_percent": 0,
            }
            self.data["stats"]["total_videos"] += 1
        else:
            entry = self.data["videos"][video_id]
            if title:
                entry["title"] = title
            if duration:
                entry["duration"] = duration
            if status:
                entry["status"] = status
                if status == "completed" and not entry["completed_at"]:
                    entry["completed_at"] = datetime.now().isoformat()
                    self.data["stats"]["total_watch_time"] += entry["duration"]
            if notes:
                entry["notes"] = notes
            if tags:
                entry["tags"] = tags

        self._save_data()
        return self.data["videos"][video_id]

    def update_progress(
        self,
        video_id: str,
        progress_percent: int,
    ) -> Dict:
        """
        Update video watch progress

        Args:
            video_id: YouTube video ID
            progress_percent: Watch progress (0-100)

        Returns:
            Updated video entry
        """
        if video_id in self.data["videos"]:
            self.data["videos"][video_id]["progress_percent"] = progress_percent

            if progress_percent >= 90:
                self.data["videos"][video_id]["status"] = "completed"
                if not self.data["videos"][video_id]["completed_at"]:
                    self.data["videos"][video_id]["completed_at"] = datetime.now().isoformat()
            elif progress_percent > 0:
                self.data["videos"][video_id]["status"] = "watching"

            self._save_data()
            return self.data["videos"][video_id]

        return {}

    def add_note(
        self,
        video_id: str,
        note: str,
        timestamp: str = None,
    ) -> Dict:
        """
        Add note for video

        Args:
            video_id: YouTube video ID
            note: Note content
            timestamp: Video timestamp for note

        Returns:
            Created note
        """
        if video_id not in self.data["notes"]:
            self.data["notes"][video_id] = []

        note_entry = {
            "content": note,
            "timestamp": timestamp,
            "created_at": datetime.now().isoformat(),
        }

        self.data["notes"][video_id].append(note_entry)
        self.data["stats"]["notes_count"] += 1
        self._save_data()

        return note_entry

    def get_video(self, video_id: str) -> Optional[Dict]:
        """Get video entry"""
        return self.data["videos"].get(video_id)

    def get_all_videos(
        self,
        status: str = None,
        tag: str = None,
    ) -> List[Dict]:
        """
        Get all tracked videos

        Args:
            status: Filter by status
            tag: Filter by tag

        Returns:
            List of video entries
        """
        videos = list(self.data["videos"].values())

        if status:
            videos = [v for v in videos if v["status"] == status]

        if tag:
            videos = [v for v in videos if tag in v.get("tags", [])]

        return videos

    def get_stats(self) -> Dict:
        """Get progress statistics"""
        videos = list(self.data["videos"].values())

        completed = [v for v in videos if v["status"] == "completed"]
        watching = [v for v in videos if v["status"] == "watching"]
        to_watch = [v for v in videos if v["status"] == "to_watch"]

        total_duration = sum(v.get("duration", 0) for v in videos)
        watched_duration = sum(v.get("duration", 0) for v in completed)

        return {
            "total_videos": len(videos),
            "completed": len(completed),
            "watching": len(watching),
            "to_watch": len(to_watch),
            "total_duration_hours": round(total_duration / 3600, 1),
            "watched_duration_hours": round(watched_duration / 3600, 1),
            "completion_rate": f"{round(len(completed) / max(len(videos), 1) * 100)}%",
            "notes_count": self.data["stats"]["notes_count"],
        }

    def get_notes(self, video_id: str = None) -> Dict:
        """Get notes for video or all notes"""
        if video_id:
            return self.data["notes"].get(video_id, [])
        return self.data["notes"]

    def add_playlist(
        self,
        playlist_id: str,
        name: str,
        video_ids: List[str],
    ) -> Dict:
        """Add playlist to tracking"""
        self.data["playlists"][playlist_id] = {
            "id": playlist_id,
            "name": name,
            "video_ids": video_ids,
            "added_at": datetime.now().isoformat(),
        }
        self._save_data()
        return self.data["playlists"][playlist_id]

    def get_playlist_progress(self, playlist_id: str) -> Dict:
        """Get progress for playlist"""
        playlist = self.data["playlists"].get(playlist_id)
        if not playlist:
            return {}

        video_ids = playlist.get("video_ids", [])
        videos = [self.data["videos"].get(vid, {}) for vid in video_ids]

        completed = sum(1 for v in videos if v.get("status") == "completed")

        return {
            "playlist": playlist,
            "total_videos": len(video_ids),
            "completed": completed,
            "progress_percent": round(completed / max(len(video_ids), 1) * 100),
        }

    def export_data(self, format: str = "json") -> str:
        """Export progress data"""
        if format == "json":
            return json.dumps(self.data, ensure_ascii=False, indent=2)
        elif format == "markdown":
            return self._export_markdown()
        else:
            return json.dumps(self.data, ensure_ascii=False, indent=2)

    def _export_markdown(self) -> str:
        """Export as markdown"""
        stats = self.get_stats()

        md = "# Learning Progress Report\n\n"
        md += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"

        md += "## Statistics\n\n"
        md += f"- Total Videos: {stats['total_videos']}\n"
        md += f"- Completed: {stats['completed']}\n"
        md += f"- Watching: {stats['watching']}\n"
        md += f"- To Watch: {stats['to_watch']}\n"
        md += f"- Watch Time: {stats['watched_duration_hours']} hours\n"
        md += f"- Completion Rate: {stats['completion_rate']}\n\n"

        md += "## Videos\n\n"
        md += "| Title | Status | Progress | Tags |\n"
        md += "|-------|--------|----------|------|\n"

        for video in self.data["videos"].values():
            title = video.get("title", video["id"])[:30]
            status = video.get("status", "unknown")
            progress = f"{video.get('progress_percent', 0)}%"
            tags = ", ".join(video.get("tags", []))
            md += f"| {title} | {status} | {progress} | {tags} |\n"

        return md

    def clear_data(self):
        """Clear all progress data"""
        self.data = {
            "videos": {},
            "playlists": {},
            "notes": {},
            "stats": {
                "total_videos": 0,
                "total_watch_time": 0,
                "notes_count": 0,
            },
        }
        self._save_data()


def get_tracker(data_file: str = None) -> ProgressTracker:
    """Factory function to get progress tracker"""
    return ProgressTracker(data_file)
