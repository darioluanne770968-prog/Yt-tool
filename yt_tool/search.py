"""
Keyword search within video transcript
"""

import re
from typing import Optional
from .extractor import format_timestamp


class TranscriptSearch:
    """Search keywords within video transcript"""

    def __init__(self, segments: list[dict], video_id: str = None):
        """
        Initialize search

        Args:
            segments: Transcript segments with 'text', 'start', 'duration'
            video_id: YouTube video ID for generating links
        """
        self.segments = segments
        self.video_id = video_id

    def search(
        self,
        keyword: str,
        case_sensitive: bool = False,
        context_chars: int = 50,
    ) -> list[dict]:
        """
        Search for keyword in transcript

        Args:
            keyword: Keyword or phrase to search
            case_sensitive: Whether search is case sensitive
            context_chars: Characters of context to include

        Returns:
            List of matches with timestamp and context
        """
        matches = []
        flags = 0 if case_sensitive else re.IGNORECASE

        # Escape special regex characters in keyword
        pattern = re.escape(keyword)

        for segment in self.segments:
            text = segment["text"]

            if re.search(pattern, text, flags):
                # Find all matches in this segment
                for match in re.finditer(pattern, text, flags):
                    start_pos = max(0, match.start() - context_chars)
                    end_pos = min(len(text), match.end() + context_chars)

                    context = text[start_pos:end_pos]
                    if start_pos > 0:
                        context = "..." + context
                    if end_pos < len(text):
                        context = context + "..."

                    # Highlight the match
                    highlighted = re.sub(
                        pattern,
                        lambda m: f"**{m.group()}**",
                        context,
                        flags=flags,
                    )

                    result = {
                        "timestamp": format_timestamp(segment["start"]),
                        "seconds": segment["start"],
                        "text": segment["text"],
                        "context": highlighted,
                        "match": match.group(),
                    }

                    if self.video_id:
                        result["link"] = (
                            f"https://youtube.com/watch?v={self.video_id}"
                            f"&t={int(segment['start'])}"
                        )

                    matches.append(result)

        return matches

    def search_regex(
        self,
        pattern: str,
        context_chars: int = 50,
    ) -> list[dict]:
        """
        Search using regex pattern

        Args:
            pattern: Regex pattern
            context_chars: Characters of context

        Returns:
            List of matches
        """
        matches = []

        try:
            compiled = re.compile(pattern, re.IGNORECASE)
        except re.error as e:
            raise ValueError(f"Invalid regex pattern: {e}")

        for segment in self.segments:
            text = segment["text"]

            for match in compiled.finditer(text):
                start_pos = max(0, match.start() - context_chars)
                end_pos = min(len(text), match.end() + context_chars)

                context = text[start_pos:end_pos]
                if start_pos > 0:
                    context = "..." + context
                if end_pos < len(text):
                    context = context + "..."

                result = {
                    "timestamp": format_timestamp(segment["start"]),
                    "seconds": segment["start"],
                    "text": segment["text"],
                    "context": context,
                    "match": match.group(),
                }

                if self.video_id:
                    result["link"] = (
                        f"https://youtube.com/watch?v={self.video_id}"
                        f"&t={int(segment['start'])}"
                    )

                matches.append(result)

        return matches

    def find_topics(self, topics: list[str]) -> dict[str, list[dict]]:
        """
        Find multiple topics in transcript

        Args:
            topics: List of topics to search

        Returns:
            Dictionary mapping topic to list of matches
        """
        results = {}

        for topic in topics:
            matches = self.search(topic)
            if matches:
                results[topic] = matches

        return results

    def get_segments_in_range(
        self,
        start_seconds: float,
        end_seconds: float,
    ) -> list[dict]:
        """
        Get transcript segments within a time range

        Args:
            start_seconds: Start time in seconds
            end_seconds: End time in seconds

        Returns:
            List of segments in the range
        """
        return [
            {
                **segment,
                "timestamp": format_timestamp(segment["start"]),
            }
            for segment in self.segments
            if start_seconds <= segment["start"] <= end_seconds
        ]

    def format_results(self, matches: list[dict], format_type: str = "text") -> str:
        """
        Format search results

        Args:
            matches: List of search matches
            format_type: 'text', 'markdown', or 'json'

        Returns:
            Formatted results string
        """
        if not matches:
            return "No matches found."

        if format_type == "markdown":
            lines = [f"## Search Results ({len(matches)} matches)\n"]
            for match in matches:
                timestamp = match["timestamp"]
                context = match["context"]
                if "link" in match:
                    lines.append(f"- [{timestamp}]({match['link']}): {context}")
                else:
                    lines.append(f"- **{timestamp}**: {context}")
            return "\n".join(lines)

        elif format_type == "json":
            import json
            return json.dumps(matches, ensure_ascii=False, indent=2)

        else:  # text
            lines = [f"Found {len(matches)} matches:\n"]
            for match in matches:
                timestamp = match["timestamp"]
                context = match["context"]
                lines.append(f"[{timestamp}] {context}")
            return "\n".join(lines)

    def get_statistics(self) -> dict:
        """
        Get transcript statistics

        Returns:
            Dictionary with statistics
        """
        if not self.segments:
            return {}

        total_duration = max(
            seg["start"] + seg.get("duration", 0)
            for seg in self.segments
        )

        total_words = sum(
            len(seg["text"].split())
            for seg in self.segments
        )

        total_chars = sum(
            len(seg["text"])
            for seg in self.segments
        )

        return {
            "total_segments": len(self.segments),
            "total_duration_seconds": total_duration,
            "total_duration_formatted": format_timestamp(total_duration),
            "total_words": total_words,
            "total_characters": total_chars,
            "average_segment_duration": total_duration / len(self.segments),
        }
