"""
YouTube video information retrieval
"""

import re
from typing import Optional
from datetime import datetime


def get_video_info(video_id: str) -> dict:
    """
    Get video metadata using yt-dlp

    Args:
        video_id: YouTube video ID

    Returns:
        Dictionary with video information
    """
    try:
        import yt_dlp

        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": False,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(
                f"https://www.youtube.com/watch?v={video_id}",
                download=False,
            )

            return {
                "video_id": video_id,
                "title": info.get("title", ""),
                "description": info.get("description", ""),
                "channel": info.get("channel", info.get("uploader", "")),
                "channel_id": info.get("channel_id", ""),
                "channel_url": info.get("channel_url", ""),
                "duration": info.get("duration", 0),
                "duration_formatted": format_duration(info.get("duration", 0)),
                "view_count": info.get("view_count", 0),
                "like_count": info.get("like_count", 0),
                "comment_count": info.get("comment_count", 0),
                "upload_date": format_date(info.get("upload_date", "")),
                "thumbnail": info.get("thumbnail", ""),
                "tags": info.get("tags", []),
                "categories": info.get("categories", []),
                "language": info.get("language", ""),
                "url": f"https://www.youtube.com/watch?v={video_id}",
            }

    except ImportError:
        raise ImportError("yt-dlp is required. Install with: pip install yt-dlp")
    except Exception as e:
        raise Exception(f"Failed to get video info: {str(e)}")


def format_duration(seconds: int) -> str:
    """Format duration in seconds to HH:MM:SS"""
    if not seconds:
        return "00:00"

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def format_date(date_str: str) -> str:
    """Format YYYYMMDD to YYYY-MM-DD"""
    if not date_str or len(date_str) != 8:
        return date_str

    try:
        return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
    except Exception:
        return date_str


def format_number(num: int) -> str:
    """Format number with K/M suffix"""
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    return str(num)


class VideoInfo:
    """Class for retrieving and managing video information"""

    def __init__(self, url_or_id: str):
        """
        Initialize with video URL or ID

        Args:
            url_or_id: YouTube URL or video ID
        """
        from .extractor import extract_video_id

        self.video_id = extract_video_id(url_or_id)
        if not self.video_id:
            raise ValueError(f"Invalid YouTube URL or video ID: {url_or_id}")

        self._info = None

    def fetch(self) -> "VideoInfo":
        """Fetch video information"""
        self._info = get_video_info(self.video_id)
        return self

    @property
    def info(self) -> dict:
        """Get video info dictionary"""
        if not self._info:
            self.fetch()
        return self._info

    @property
    def title(self) -> str:
        return self.info.get("title", "")

    @property
    def channel(self) -> str:
        return self.info.get("channel", "")

    @property
    def duration(self) -> int:
        return self.info.get("duration", 0)

    @property
    def duration_formatted(self) -> str:
        return self.info.get("duration_formatted", "")

    @property
    def description(self) -> str:
        return self.info.get("description", "")

    @property
    def view_count(self) -> int:
        return self.info.get("view_count", 0)

    def format_summary(self) -> str:
        """Format video info as summary text"""
        info = self.info
        lines = [
            f"Title: {info['title']}",
            f"Channel: {info['channel']}",
            f"Duration: {info['duration_formatted']}",
            f"Views: {format_number(info['view_count'])}",
            f"Likes: {format_number(info.get('like_count', 0))}",
            f"Upload Date: {info['upload_date']}",
            f"URL: {info['url']}",
        ]

        if info.get("tags"):
            lines.append(f"Tags: {', '.join(info['tags'][:10])}")

        return "\n".join(lines)

    def format_markdown(self) -> str:
        """Format video info as Markdown"""
        info = self.info
        lines = [
            f"# {info['title']}",
            "",
            f"**Channel:** [{info['channel']}]({info.get('channel_url', '')})",
            f"**Duration:** {info['duration_formatted']}",
            f"**Views:** {format_number(info['view_count'])}",
            f"**Likes:** {format_number(info.get('like_count', 0))}",
            f"**Upload Date:** {info['upload_date']}",
            "",
            f"[Watch on YouTube]({info['url']})",
            "",
        ]

        if info.get("description"):
            lines.extend([
                "## Description",
                "",
                info["description"][:1000] + ("..." if len(info["description"]) > 1000 else ""),
                "",
            ])

        if info.get("tags"):
            lines.extend([
                "## Tags",
                "",
                ", ".join(f"`{tag}`" for tag in info["tags"][:15]),
            ])

        return "\n".join(lines)
