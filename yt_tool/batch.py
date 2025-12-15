"""
Batch processing for multiple videos or playlists
"""

import re
import time
from typing import Optional, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed

from .extractor import TranscriptExtractor, extract_video_id
from .summarizer import Summarizer
from .timestamp import TimestampGenerator
from .exporter import Exporter


def extract_playlist_id(url: str) -> Optional[str]:
    """Extract playlist ID from YouTube URL"""
    pattern = r"[?&]list=([a-zA-Z0-9_-]+)"
    match = re.search(pattern, url)
    return match.group(1) if match else None


def get_playlist_videos(playlist_id: str) -> list[str]:
    """
    Get video IDs from a YouTube playlist

    Note: This is a simplified implementation. For full support,
    consider using yt-dlp or YouTube Data API.
    """
    try:
        import yt_dlp

        ydl_opts = {
            "quiet": True,
            "extract_flat": True,
            "force_generic_extractor": False,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(
                f"https://www.youtube.com/playlist?list={playlist_id}",
                download=False,
            )

            if result and "entries" in result:
                return [
                    entry["id"]
                    for entry in result["entries"]
                    if entry and "id" in entry
                ]
    except ImportError:
        raise ImportError("yt-dlp is required for playlist support. Install with: pip install yt-dlp")
    except Exception as e:
        raise Exception(f"Failed to get playlist videos: {str(e)}")

    return []


class BatchProcessor:
    """Process multiple videos in batch"""

    def __init__(
        self,
        provider: str = None,
        output_dir: str = "output",
        max_workers: int = 3,
    ):
        """
        Initialize batch processor

        Args:
            provider: AI provider
            output_dir: Output directory for exports
            max_workers: Maximum parallel workers
        """
        self.provider = provider
        self.output_dir = output_dir
        self.max_workers = max_workers
        self.exporter = Exporter(output_dir)

    def process_videos(
        self,
        video_urls: list[str],
        operations: list[str] = None,
        language: str = "中文",
        progress_callback: Callable[[str, int, int], None] = None,
    ) -> list[dict]:
        """
        Process multiple videos

        Args:
            video_urls: List of YouTube URLs or video IDs
            operations: List of operations ('summary', 'keypoints', 'chapters', 'transcript')
            language: Output language
            progress_callback: Callback function(video_id, current, total)

        Returns:
            List of results for each video
        """
        if operations is None:
            operations = ["summary", "transcript"]

        results = []
        total = len(video_urls)

        for i, url in enumerate(video_urls):
            video_id = extract_video_id(url)
            if not video_id:
                results.append({
                    "url": url,
                    "success": False,
                    "error": "Invalid video URL",
                })
                continue

            if progress_callback:
                progress_callback(video_id, i + 1, total)

            try:
                result = self._process_single_video(
                    video_id, operations, language
                )
                results.append(result)

                # Small delay to avoid rate limiting
                if i < total - 1:
                    time.sleep(1)

            except Exception as e:
                results.append({
                    "video_id": video_id,
                    "url": url,
                    "success": False,
                    "error": str(e),
                })

        return results

    def process_playlist(
        self,
        playlist_url: str,
        operations: list[str] = None,
        language: str = "中文",
        max_videos: int = None,
        progress_callback: Callable[[str, int, int], None] = None,
    ) -> list[dict]:
        """
        Process all videos in a playlist

        Args:
            playlist_url: YouTube playlist URL
            operations: Operations to perform
            language: Output language
            max_videos: Maximum number of videos to process
            progress_callback: Progress callback

        Returns:
            List of results
        """
        playlist_id = extract_playlist_id(playlist_url)
        if not playlist_id:
            raise ValueError("Invalid playlist URL")

        video_ids = get_playlist_videos(playlist_id)

        if max_videos:
            video_ids = video_ids[:max_videos]

        return self.process_videos(
            video_ids, operations, language, progress_callback
        )

    def _process_single_video(
        self,
        video_id: str,
        operations: list[str],
        language: str,
    ) -> dict:
        """Process a single video"""
        result = {
            "video_id": video_id,
            "url": f"https://youtube.com/watch?v={video_id}",
            "success": True,
        }

        # Extract transcript
        extractor = TranscriptExtractor(video_id)
        extractor.extract()

        transcript_text = extractor.get_plain_text()
        transcript_formatted = extractor.get_formatted(include_timestamps=True)

        result["transcript_language"] = extractor.language

        if "transcript" in operations:
            result["transcript"] = transcript_formatted

        # Summary
        if "summary" in operations:
            summarizer = Summarizer(self.provider)
            result["summary"] = summarizer.summarize(transcript_text, language)

        # Key points
        if "keypoints" in operations:
            summarizer = Summarizer(self.provider)
            result["key_points"] = summarizer.extract_key_points(
                transcript_text, language
            )

        # Chapters
        if "chapters" in operations:
            generator = TimestampGenerator(self.provider)
            chapters = generator.generate(transcript_formatted, language)
            result["chapters"] = chapters

        # Export
        export_path = self.exporter.export_markdown(
            video_id=video_id,
            transcript=result.get("transcript"),
            summary=result.get("summary"),
            key_points=result.get("key_points"),
            chapters=result.get("chapters"),
        )
        result["export_path"] = export_path

        return result

    def process_videos_parallel(
        self,
        video_urls: list[str],
        operations: list[str] = None,
        language: str = "中文",
        progress_callback: Callable[[str, int, int], None] = None,
    ) -> list[dict]:
        """
        Process multiple videos in parallel

        Note: Be careful with rate limits when using parallel processing.

        Args:
            video_urls: List of video URLs
            operations: Operations to perform
            language: Output language
            progress_callback: Progress callback

        Returns:
            List of results
        """
        if operations is None:
            operations = ["summary", "transcript"]

        results = []
        total = len(video_urls)
        completed = 0

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_url = {
                executor.submit(
                    self._process_single_video,
                    extract_video_id(url),
                    operations,
                    language,
                ): url
                for url in video_urls
                if extract_video_id(url)
            }

            for future in as_completed(future_to_url):
                url = future_to_url[future]
                completed += 1

                try:
                    result = future.result()
                    results.append(result)

                    if progress_callback:
                        progress_callback(result["video_id"], completed, total)

                except Exception as e:
                    results.append({
                        "url": url,
                        "success": False,
                        "error": str(e),
                    })

        return results
