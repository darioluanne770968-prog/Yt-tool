"""
Export video analysis to various formats
"""

import os
import json
from datetime import datetime
from typing import Optional


class Exporter:
    """Export video analysis results to various formats"""

    def __init__(self, output_dir: str = "output"):
        """
        Initialize exporter

        Args:
            output_dir: Directory to save exported files
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def export_markdown(
        self,
        video_id: str,
        title: str = None,
        transcript: str = None,
        summary: str = None,
        key_points: str = None,
        chapters: list[dict] = None,
        translation: str = None,
    ) -> str:
        """
        Export analysis to Markdown format

        Returns:
            Path to exported file
        """
        lines = []

        # Header
        lines.append(f"# {title or 'YouTube Video Analysis'}")
        lines.append("")
        lines.append(f"**Video ID:** {video_id}")
        lines.append(f"**Link:** https://youtube.com/watch?v={video_id}")
        lines.append(f"**Exported:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")

        # Table of Contents
        lines.append("## 目录")
        lines.append("")
        if summary:
            lines.append("- [视频摘要](#视频摘要)")
        if key_points:
            lines.append("- [关键要点](#关键要点)")
        if chapters:
            lines.append("- [章节时间戳](#章节时间戳)")
        if transcript:
            lines.append("- [完整字幕](#完整字幕)")
        if translation:
            lines.append("- [翻译内容](#翻译内容)")
        lines.append("")

        # Summary
        if summary:
            lines.append("---")
            lines.append("")
            lines.append("## 视频摘要")
            lines.append("")
            lines.append(summary)
            lines.append("")

        # Key Points
        if key_points:
            lines.append("---")
            lines.append("")
            lines.append("## 关键要点")
            lines.append("")
            lines.append(key_points)
            lines.append("")

        # Chapters
        if chapters:
            lines.append("---")
            lines.append("")
            lines.append("## 章节时间戳")
            lines.append("")
            for chapter in chapters:
                time_str = chapter["time"]
                title = chapter["title"]
                seconds = self._time_to_seconds(time_str)
                link = f"https://youtube.com/watch?v={video_id}&t={seconds}"
                lines.append(f"- [{time_str}]({link}) {title}")
            lines.append("")

        # Transcript
        if transcript:
            lines.append("---")
            lines.append("")
            lines.append("## 完整字幕")
            lines.append("")
            lines.append("```")
            lines.append(transcript)
            lines.append("```")
            lines.append("")

        # Translation
        if translation:
            lines.append("---")
            lines.append("")
            lines.append("## 翻译内容")
            lines.append("")
            lines.append(translation)
            lines.append("")

        # Write file
        content = "\n".join(lines)
        filename = f"{video_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        return filepath

    def export_json(
        self,
        video_id: str,
        title: str = None,
        transcript: str = None,
        transcript_segments: list[dict] = None,
        summary: str = None,
        key_points: str = None,
        chapters: list[dict] = None,
        translation: str = None,
    ) -> str:
        """
        Export analysis to JSON format

        Returns:
            Path to exported file
        """
        data = {
            "video_id": video_id,
            "url": f"https://youtube.com/watch?v={video_id}",
            "title": title,
            "exported_at": datetime.now().isoformat(),
            "transcript": transcript,
            "transcript_segments": transcript_segments,
            "summary": summary,
            "key_points": key_points,
            "chapters": chapters,
            "translation": translation,
        }

        # Remove None values
        data = {k: v for k, v in data.items() if v is not None}

        filename = f"{video_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return filepath

    def export_notion(
        self,
        video_id: str,
        title: str = None,
        summary: str = None,
        key_points: str = None,
        chapters: list[dict] = None,
    ) -> str:
        """
        Export in Notion-compatible format

        Returns:
            Path to exported file
        """
        lines = []

        # Notion page header with properties
        lines.append("---")
        lines.append(f"title: {title or 'YouTube Video Analysis'}")
        lines.append(f"video_id: {video_id}")
        lines.append(f"url: https://youtube.com/watch?v={video_id}")
        lines.append(f"date: {datetime.now().strftime('%Y-%m-%d')}")
        lines.append("tags: [youtube, video-notes]")
        lines.append("---")
        lines.append("")

        # Callout for video link
        lines.append("> [!video] Video Link")
        lines.append(f"> https://youtube.com/watch?v={video_id}")
        lines.append("")

        # Summary in toggle
        if summary:
            lines.append("## 📝 Summary")
            lines.append("")
            lines.append(summary)
            lines.append("")

        # Key Points
        if key_points:
            lines.append("## 💡 Key Points")
            lines.append("")
            lines.append(key_points)
            lines.append("")

        # Chapters as table
        if chapters:
            lines.append("## 📑 Chapters")
            lines.append("")
            lines.append("| Time | Chapter |")
            lines.append("|------|---------|")
            for chapter in chapters:
                lines.append(f"| {chapter['time']} | {chapter['title']} |")
            lines.append("")

        content = "\n".join(lines)
        filename = f"{video_id}_notion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        return filepath

    def export_obsidian(
        self,
        video_id: str,
        title: str = None,
        summary: str = None,
        key_points: str = None,
        chapters: list[dict] = None,
    ) -> str:
        """
        Export in Obsidian-compatible format with wikilinks

        Returns:
            Path to exported file
        """
        lines = []

        # Obsidian YAML frontmatter
        lines.append("---")
        lines.append(f"title: \"{title or 'YouTube Video'}\"")
        lines.append(f"video_id: {video_id}")
        lines.append(f"source: https://youtube.com/watch?v={video_id}")
        lines.append(f"created: {datetime.now().strftime('%Y-%m-%d')}")
        lines.append("type: video-note")
        lines.append("tags:")
        lines.append("  - youtube")
        lines.append("  - video")
        lines.append("---")
        lines.append("")

        # Link to video
        lines.append(f"# {title or 'YouTube Video'}")
        lines.append("")
        lines.append(f"🔗 [Watch on YouTube](https://youtube.com/watch?v={video_id})")
        lines.append("")

        # Summary
        if summary:
            lines.append("## Summary")
            lines.append("")
            lines.append(summary)
            lines.append("")

        # Key Points
        if key_points:
            lines.append("## Key Points")
            lines.append("")
            lines.append(key_points)
            lines.append("")

        # Chapters with timestamps
        if chapters:
            lines.append("## Chapters")
            lines.append("")
            for chapter in chapters:
                time_str = chapter["time"]
                title_text = chapter["title"]
                seconds = self._time_to_seconds(time_str)
                lines.append(
                    f"- `{time_str}` [{title_text}](https://youtube.com/watch?v={video_id}&t={seconds})"
                )
            lines.append("")

        content = "\n".join(lines)
        filename = f"{video_id}_obsidian_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        return filepath

    def export_txt(self, video_id: str, content: str, suffix: str = "") -> str:
        """
        Export plain text

        Returns:
            Path to exported file
        """
        suffix_str = f"_{suffix}" if suffix else ""
        filename = f"{video_id}{suffix_str}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        return filepath

    def _time_to_seconds(self, time_str: str) -> int:
        """Convert time string to seconds"""
        parts = time_str.split(":")
        if len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
        elif len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        return 0
