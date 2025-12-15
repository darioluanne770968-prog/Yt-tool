"""
Subtitle file generation (SRT, VTT, TXT formats)
"""

import os
from typing import Optional
from datetime import datetime


def format_srt_timestamp(seconds: float) -> str:
    """Convert seconds to SRT timestamp format (HH:MM:SS,mmm)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)

    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def format_vtt_timestamp(seconds: float) -> str:
    """Convert seconds to VTT timestamp format (HH:MM:SS.mmm)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)

    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"


def segments_to_srt(segments: list[dict]) -> str:
    """
    Convert transcript segments to SRT format

    Args:
        segments: List of segments with 'text', 'start', 'duration'

    Returns:
        SRT formatted string
    """
    lines = []

    for i, segment in enumerate(segments, 1):
        start = segment["start"]
        duration = segment.get("duration", 2.0)
        end = start + duration
        text = segment["text"].strip()

        if not text:
            continue

        lines.append(str(i))
        lines.append(f"{format_srt_timestamp(start)} --> {format_srt_timestamp(end)}")
        lines.append(text)
        lines.append("")

    return "\n".join(lines)


def segments_to_vtt(segments: list[dict], title: str = None) -> str:
    """
    Convert transcript segments to WebVTT format

    Args:
        segments: List of segments with 'text', 'start', 'duration'
        title: Optional video title

    Returns:
        VTT formatted string
    """
    lines = ["WEBVTT", ""]

    if title:
        lines.extend([f"NOTE {title}", ""])

    for i, segment in enumerate(segments, 1):
        start = segment["start"]
        duration = segment.get("duration", 2.0)
        end = start + duration
        text = segment["text"].strip()

        if not text:
            continue

        lines.append(f"{i}")
        lines.append(f"{format_vtt_timestamp(start)} --> {format_vtt_timestamp(end)}")
        lines.append(text)
        lines.append("")

    return "\n".join(lines)


def segments_to_txt(segments: list[dict], include_timestamps: bool = False) -> str:
    """
    Convert transcript segments to plain text

    Args:
        segments: List of segments
        include_timestamps: Whether to include timestamps

    Returns:
        Plain text string
    """
    lines = []

    for segment in segments:
        text = segment["text"].strip()
        if not text:
            continue

        if include_timestamps:
            from .extractor import format_timestamp
            timestamp = format_timestamp(segment["start"])
            lines.append(f"[{timestamp}] {text}")
        else:
            lines.append(text)

    return "\n".join(lines)


class SubtitleExporter:
    """Export subtitles to various formats"""

    def __init__(self, segments: list[dict], video_id: str = None, title: str = None):
        """
        Initialize subtitle exporter

        Args:
            segments: Transcript segments
            video_id: YouTube video ID
            title: Video title
        """
        self.segments = segments
        self.video_id = video_id
        self.title = title

    def to_srt(self) -> str:
        """Convert to SRT format"""
        return segments_to_srt(self.segments)

    def to_vtt(self) -> str:
        """Convert to VTT format"""
        return segments_to_vtt(self.segments, self.title)

    def to_txt(self, include_timestamps: bool = False) -> str:
        """Convert to plain text"""
        return segments_to_txt(self.segments, include_timestamps)

    def save(
        self,
        output_dir: str = "output",
        format: str = "srt",
        filename: str = None,
    ) -> str:
        """
        Save subtitle file

        Args:
            output_dir: Output directory
            format: 'srt', 'vtt', or 'txt'
            filename: Custom filename (without extension)

        Returns:
            Path to saved file
        """
        os.makedirs(output_dir, exist_ok=True)

        if filename is None:
            filename = self.video_id or datetime.now().strftime("%Y%m%d_%H%M%S")

        if format == "srt":
            content = self.to_srt()
            ext = "srt"
        elif format == "vtt":
            content = self.to_vtt()
            ext = "vtt"
        else:
            content = self.to_txt(include_timestamps=True)
            ext = "txt"

        filepath = os.path.join(output_dir, f"{filename}.{ext}")

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        return filepath

    def save_all_formats(self, output_dir: str = "output", filename: str = None) -> dict:
        """
        Save in all formats

        Returns:
            Dictionary of format -> filepath
        """
        results = {}
        for fmt in ["srt", "vtt", "txt"]:
            results[fmt] = self.save(output_dir, fmt, filename)
        return results
