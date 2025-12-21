"""
YouTube subtitle/transcript extraction module
"""

import re
from typing import Optional
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
)


def extract_video_id(url: str) -> Optional[str]:
    """
    Extract video ID from various YouTube URL formats

    Supported formats:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/embed/VIDEO_ID
    - https://www.youtube.com/v/VIDEO_ID
    """
    patterns = [
        r"(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/|youtube\.com\/v\/)([a-zA-Z0-9_-]{11})",
        r"^([a-zA-Z0-9_-]{11})$",  # Direct video ID
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None


def get_transcript(
    video_id: str, languages: list[str] = None
) -> tuple[list[dict], str]:
    """
    Get transcript for a YouTube video

    Args:
        video_id: YouTube video ID
        languages: Preferred languages in order of preference

    Returns:
        Tuple of (transcript_list, language_code)
    """
    if languages is None:
        languages = ["zh-Hans", "zh-Hant", "zh", "en", "ja", "ko"]

    try:
        # youtube-transcript-api 1.x uses instance method
        ytt_api = YouTubeTranscriptApi()
        transcript_list = ytt_api.list(video_id)

        # Try to find a transcript in preferred languages
        for lang in languages:
            try:
                transcript = transcript_list.find_transcript([lang])
                fetched = transcript.fetch()
                # Convert FetchedTranscript to list of dicts
                return [{"text": item.text, "start": item.start, "duration": item.duration} for item in fetched], lang
            except NoTranscriptFound:
                continue

        # If no preferred language found, try to get any available transcript
        try:
            # Try manually created transcripts first
            for transcript in transcript_list:
                if not transcript.is_generated:
                    fetched = transcript.fetch()
                    return [{"text": item.text, "start": item.start, "duration": item.duration} for item in fetched], transcript.language_code
        except Exception:
            pass

        # Fall back to auto-generated
        for transcript in transcript_list:
            fetched = transcript.fetch()
            return [{"text": item.text, "start": item.start, "duration": item.duration} for item in fetched], transcript.language_code

    except TranscriptsDisabled:
        raise Exception("Transcripts are disabled for this video")
    except VideoUnavailable:
        raise Exception("Video is unavailable")
    except Exception as e:
        raise Exception(f"Failed to get transcript: {str(e)}")


def format_transcript(transcript: list[dict], include_timestamps: bool = True) -> str:
    """
    Format transcript into readable text

    Args:
        transcript: List of transcript segments
        include_timestamps: Whether to include timestamps

    Returns:
        Formatted transcript text
    """
    lines = []

    for segment in transcript:
        text = segment["text"].strip()
        if not text:
            continue

        if include_timestamps:
            start_time = segment["start"]
            timestamp = format_timestamp(start_time)
            lines.append(f"[{timestamp}] {text}")
        else:
            lines.append(text)

    return "\n".join(lines)


def format_timestamp(seconds: float) -> str:
    """Convert seconds to HH:MM:SS or MM:SS format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def get_plain_text(transcript: list[dict]) -> str:
    """
    Get plain text without timestamps

    Args:
        transcript: List of transcript segments

    Returns:
        Plain text content
    """
    return " ".join(segment["text"].strip() for segment in transcript if segment["text"].strip())


class TranscriptExtractor:
    """Main class for extracting transcripts"""

    def __init__(self, url_or_id: str):
        self.video_id = extract_video_id(url_or_id)
        if not self.video_id:
            raise ValueError(f"Invalid YouTube URL or video ID: {url_or_id}")

        self.transcript = None
        self.language = None

    def extract(self, languages: list[str] = None) -> "TranscriptExtractor":
        """Extract transcript from video"""
        self.transcript, self.language = get_transcript(self.video_id, languages)
        return self

    def get_formatted(self, include_timestamps: bool = True) -> str:
        """Get formatted transcript"""
        if not self.transcript:
            raise ValueError("No transcript extracted. Call extract() first.")
        return format_transcript(self.transcript, include_timestamps)

    def get_plain_text(self) -> str:
        """Get plain text without timestamps"""
        if not self.transcript:
            raise ValueError("No transcript extracted. Call extract() first.")
        return get_plain_text(self.transcript)

    def get_segments(self) -> list[dict]:
        """Get raw transcript segments"""
        if not self.transcript:
            raise ValueError("No transcript extracted. Call extract() first.")
        return self.transcript
