"""
Video clip extraction based on timestamps
"""

import os
import subprocess
from typing import List, Dict, Optional, Tuple


class ClipExtractor:
    """Extract video clips based on timestamps"""

    def __init__(self, output_dir: str = "."):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def extract_clip(
        self,
        video_url: str,
        start_time: str,
        end_time: str,
        output_name: str = None,
    ) -> Dict:
        """
        Extract a single clip from video

        Args:
            video_url: YouTube video URL
            start_time: Start time (HH:MM:SS or seconds)
            end_time: End time (HH:MM:SS or seconds)
            output_name: Output filename (without extension)

        Returns:
            Result with output path
        """
        if output_name is None:
            output_name = f"clip_{start_time.replace(':', '-')}_{end_time.replace(':', '-')}"

        output_path = os.path.join(self.output_dir, f"{output_name}.mp4")

        # Use yt-dlp with ffmpeg for extraction
        cmd = [
            "yt-dlp",
            "--download-sections", f"*{start_time}-{end_time}",
            "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "-o", output_path,
            "--force-keyframes-at-cuts",
            video_url,
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,
            )

            if os.path.exists(output_path):
                return {
                    "success": True,
                    "output_path": output_path,
                    "start": start_time,
                    "end": end_time,
                }
            else:
                return {
                    "success": False,
                    "error": result.stderr,
                }

        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Extraction timed out"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def extract_multiple_clips(
        self,
        video_url: str,
        clips: List[Dict],
    ) -> List[Dict]:
        """
        Extract multiple clips from video

        Args:
            video_url: YouTube video URL
            clips: List of dicts with 'start', 'end', 'name' keys

        Returns:
            List of results
        """
        results = []

        for clip in clips:
            result = self.extract_clip(
                video_url,
                clip.get("start", "0:00"),
                clip.get("end", "0:30"),
                clip.get("name"),
            )
            result["clip_info"] = clip
            results.append(result)

        return results

    def extract_highlights(
        self,
        video_url: str,
        transcript_segments: List[Dict],
        keywords: List[str],
        context_seconds: int = 5,
    ) -> List[Dict]:
        """
        Extract clips around keyword mentions

        Args:
            video_url: YouTube video URL
            transcript_segments: Transcript with timestamps
            keywords: Keywords to find
            context_seconds: Seconds before/after keyword

        Returns:
            List of extracted clips
        """
        clips_to_extract = []

        for segment in transcript_segments:
            text = segment.get("text", "").lower()
            start = segment.get("start", 0)

            for keyword in keywords:
                if keyword.lower() in text:
                    clip_start = max(0, start - context_seconds)
                    clip_end = start + context_seconds + 5  # Extra 5s for content

                    clips_to_extract.append({
                        "start": self._seconds_to_timestamp(clip_start),
                        "end": self._seconds_to_timestamp(clip_end),
                        "name": f"highlight_{keyword}_{int(start)}",
                        "keyword": keyword,
                    })

        return self.extract_multiple_clips(video_url, clips_to_extract)

    def extract_chapters(
        self,
        video_url: str,
        chapters: List[Dict],
    ) -> List[Dict]:
        """
        Extract clips for each chapter

        Args:
            video_url: YouTube video URL
            chapters: List of chapter dicts with 'start', 'end', 'title'

        Returns:
            List of extracted clips
        """
        clips = []

        for chapter in chapters:
            clips.append({
                "start": chapter.get("start", "0:00"),
                "end": chapter.get("end", "1:00"),
                "name": self._sanitize_filename(chapter.get("title", "chapter")),
            })

        return self.extract_multiple_clips(video_url, clips)

    def create_compilation(
        self,
        clip_paths: List[str],
        output_name: str = "compilation",
    ) -> Dict:
        """
        Combine multiple clips into one video

        Args:
            clip_paths: List of clip file paths
            output_name: Output filename

        Returns:
            Result with output path
        """
        output_path = os.path.join(self.output_dir, f"{output_name}.mp4")

        # Create file list
        list_path = os.path.join(self.output_dir, "clips_list.txt")
        with open(list_path, "w") as f:
            for clip in clip_paths:
                f.write(f"file '{os.path.abspath(clip)}'\n")

        cmd = [
            "ffmpeg",
            "-f", "concat",
            "-safe", "0",
            "-i", list_path,
            "-c", "copy",
            "-y",
            output_path,
        ]

        try:
            subprocess.run(cmd, capture_output=True, timeout=300)

            if os.path.exists(output_path):
                os.remove(list_path)
                return {
                    "success": True,
                    "output_path": output_path,
                    "clips_count": len(clip_paths),
                }
            else:
                return {"success": False, "error": "Failed to create compilation"}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def extract_best_moments(
        self,
        video_url: str,
        transcript: str,
        num_clips: int = 5,
        clip_duration: int = 30,
    ) -> List[Dict]:
        """
        Use AI to identify and extract best moments

        Args:
            video_url: YouTube video URL
            transcript: Full transcript
            num_clips: Number of clips to extract
            clip_duration: Duration of each clip in seconds

        Returns:
            List of extracted clips
        """
        from .ai_client import get_ai_client

        ai = get_ai_client()

        prompt = f"""Identify the {num_clips} most interesting/important moments in this video transcript.

For each moment, provide:
1. Approximate timestamp (MM:SS format)
2. Why it's important
3. A short title for the clip

Transcript:
{transcript[:10000]}

Format:
Moment 1:
- Timestamp: MM:SS
- Title: [title]
- Reason: [why important]

Moment 2:
...
"""

        response = ai.chat(prompt, max_tokens=1500)

        # Parse response to extract timestamps
        clips = self._parse_moments(response, clip_duration)

        return self.extract_multiple_clips(video_url, clips)

    def _parse_moments(self, response: str, clip_duration: int) -> List[Dict]:
        """Parse AI response to extract clip timestamps"""
        import re

        clips = []
        timestamp_pattern = r"(\d{1,2}):(\d{2})"

        # Find all timestamps
        matches = re.finditer(timestamp_pattern, response)

        for i, match in enumerate(matches):
            minutes = int(match.group(1))
            seconds = int(match.group(2))
            start_seconds = minutes * 60 + seconds

            clips.append({
                "start": self._seconds_to_timestamp(max(0, start_seconds - 5)),
                "end": self._seconds_to_timestamp(start_seconds + clip_duration),
                "name": f"best_moment_{i+1}",
            })

        return clips[:10]  # Limit to 10 clips

    def _seconds_to_timestamp(self, seconds: float) -> str:
        """Convert seconds to HH:MM:SS format"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)

        if hours > 0:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        return f"{minutes}:{secs:02d}"

    def _sanitize_filename(self, name: str) -> str:
        """Sanitize string for use as filename"""
        import re
        # Remove invalid characters
        name = re.sub(r'[<>:"/\\|?*]', '', name)
        # Replace spaces with underscores
        name = name.replace(' ', '_')
        # Limit length
        return name[:50]
