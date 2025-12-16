"""
Channel monitoring and notifications
"""

import os
import json
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class ChannelMonitor:
    """Monitor YouTube channels for new videos"""

    def __init__(self, data_file: str = None):
        """
        Initialize channel monitor

        Args:
            data_file: Path to data file
        """
        self.data_file = data_file or os.path.expanduser("~/.yt-tool/monitor.json")
        self.data = self._load_data()

    def _load_data(self) -> Dict:
        """Load monitor data from file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass

        return {
            "channels": {},
            "last_check": None,
            "new_videos": [],
        }

    def _save_data(self):
        """Save monitor data to file"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def add_channel(
        self,
        channel_url: str,
        name: str = None,
        keywords: List[str] = None,
    ) -> Dict:
        """
        Add channel to monitor

        Args:
            channel_url: YouTube channel URL
            name: Friendly name for channel
            keywords: Keywords to filter videos

        Returns:
            Added channel info
        """
        channel_id = self._extract_channel_id(channel_url)

        if not channel_id:
            return {"error": "Invalid channel URL"}

        self.data["channels"][channel_id] = {
            "id": channel_id,
            "url": channel_url,
            "name": name or channel_id,
            "keywords": keywords or [],
            "added_at": datetime.now().isoformat(),
            "last_video_id": None,
        }

        self._save_data()
        return self.data["channels"][channel_id]

    def remove_channel(self, channel_id: str) -> bool:
        """Remove channel from monitoring"""
        if channel_id in self.data["channels"]:
            del self.data["channels"][channel_id]
            self._save_data()
            return True
        return False

    def get_channels(self) -> List[Dict]:
        """Get all monitored channels"""
        return list(self.data["channels"].values())

    def check_new_videos(self) -> List[Dict]:
        """
        Check all channels for new videos

        Returns:
            List of new videos found
        """
        new_videos = []

        for channel_id, channel in self.data["channels"].items():
            channel_videos = self._get_channel_videos(channel["url"])

            for video in channel_videos:
                video_id = video.get("id")

                # Skip if we've seen this video
                if video_id == channel["last_video_id"]:
                    break

                # Check keyword filter
                if channel["keywords"]:
                    title = video.get("title", "").lower()
                    if not any(kw.lower() in title for kw in channel["keywords"]):
                        continue

                new_videos.append({
                    "channel": channel["name"],
                    "channel_id": channel_id,
                    "video_id": video_id,
                    "title": video.get("title"),
                    "url": f"https://youtube.com/watch?v={video_id}",
                    "upload_date": video.get("upload_date"),
                })

            # Update last video ID
            if channel_videos:
                self.data["channels"][channel_id]["last_video_id"] = channel_videos[0].get("id")

        self.data["last_check"] = datetime.now().isoformat()
        self.data["new_videos"] = new_videos
        self._save_data()

        return new_videos

    def _get_channel_videos(self, channel_url: str) -> List[Dict]:
        """Get recent videos from channel"""
        cmd = [
            "yt-dlp",
            "--dump-json",
            "--flat-playlist",
            "--playlist-items", "1:10",
            channel_url,
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
            )

            videos = []
            for line in result.stdout.strip().split("\n"):
                if line:
                    try:
                        videos.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue

            return videos

        except Exception:
            return []

    def _extract_channel_id(self, url: str) -> Optional[str]:
        """Extract channel ID from URL"""
        import re

        patterns = [
            r"youtube\.com/channel/([^/\?]+)",
            r"youtube\.com/c/([^/\?]+)",
            r"youtube\.com/@([^/\?]+)",
            r"youtube\.com/user/([^/\?]+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)

        return None

    def auto_process_new(
        self,
        actions: List[str] = None,
        language: str = "中文",
    ) -> List[Dict]:
        """
        Automatically process new videos

        Args:
            actions: Actions to perform (transcript, summary, etc.)
            language: Output language

        Returns:
            Processing results
        """
        if actions is None:
            actions = ["summary"]

        new_videos = self.check_new_videos()
        results = []

        from .extractor import TranscriptExtractor
        from .summarizer import Summarizer

        for video in new_videos:
            result = {
                "video": video,
                "outputs": {},
            }

            try:
                extractor = TranscriptExtractor(video["video_id"])
                extractor.extract()
                transcript = extractor.get_plain_text()

                if "transcript" in actions:
                    result["outputs"]["transcript"] = transcript

                if "summary" in actions:
                    summarizer = Summarizer()
                    result["outputs"]["summary"] = summarizer.summarize(transcript, language)

            except Exception as e:
                result["error"] = str(e)

            results.append(result)

        return results

    def get_status(self) -> Dict:
        """Get monitor status"""
        return {
            "channels_count": len(self.data["channels"]),
            "channels": [
                {"name": c["name"], "url": c["url"]}
                for c in self.data["channels"].values()
            ],
            "last_check": self.data["last_check"],
            "pending_videos": len(self.data.get("new_videos", [])),
        }

    def export_feed(self, format: str = "json") -> str:
        """
        Export new videos as feed

        Args:
            format: json or markdown

        Returns:
            Feed content
        """
        videos = self.data.get("new_videos", [])

        if format == "json":
            return json.dumps(videos, ensure_ascii=False, indent=2)

        # Markdown format
        md = "# New Videos\n\n"
        md += f"Last checked: {self.data.get('last_check', 'Never')}\n\n"

        for video in videos:
            md += f"## {video.get('title', 'Unknown')}\n"
            md += f"- Channel: {video.get('channel')}\n"
            md += f"- URL: {video.get('url')}\n"
            md += f"- Date: {video.get('upload_date', 'Unknown')}\n\n"

        return md

    def create_digest(
        self,
        language: str = "中文",
    ) -> str:
        """
        Create digest of new videos

        Args:
            language: Output language

        Returns:
            Digest content
        """
        videos = self.data.get("new_videos", [])

        if not videos:
            return "没有新视频"

        from .ai_client import get_ai_client

        ai = get_ai_client()

        video_list = "\n".join([
            f"- {v['title']} (by {v['channel']})"
            for v in videos
        ])

        prompt = f"""Create a digest summary of these new videos:

{video_list}

## 新视频摘要

### 概览
[Overview of new content]

### 推荐观看
[Which to watch first and why]

### 主题分类
[Group videos by topic]
"""

        return ai.chat(prompt, max_tokens=1500)


def get_monitor(data_file: str = None) -> ChannelMonitor:
    """Factory function to get channel monitor"""
    return ChannelMonitor(data_file)
