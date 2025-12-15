"""
Audio/Video download functionality using yt-dlp
"""

import os
from typing import Optional, Callable


class Downloader:
    """Download audio/video from YouTube"""

    def __init__(self, output_dir: str = "output"):
        """
        Initialize downloader

        Args:
            output_dir: Output directory for downloads
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def download_audio(
        self,
        video_id: str,
        format: str = "mp3",
        quality: str = "192",
        filename: str = None,
        progress_callback: Callable[[dict], None] = None,
    ) -> str:
        """
        Download audio from YouTube video

        Args:
            video_id: YouTube video ID
            format: Audio format ('mp3', 'm4a', 'wav', 'opus')
            quality: Audio quality/bitrate ('128', '192', '256', '320')
            filename: Custom filename (without extension)
            progress_callback: Progress callback function

        Returns:
            Path to downloaded file
        """
        try:
            import yt_dlp
        except ImportError:
            raise ImportError("yt-dlp is required. Install with: pip install yt-dlp")

        if filename is None:
            filename = video_id

        output_template = os.path.join(self.output_dir, f"{filename}.%(ext)s")

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": output_template,
            "quiet": True,
            "no_warnings": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": format,
                    "preferredquality": quality,
                }
            ],
        }

        if progress_callback:
            ydl_opts["progress_hooks"] = [progress_callback]

        url = f"https://www.youtube.com/watch?v={video_id}"

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Return the expected output path
        return os.path.join(self.output_dir, f"{filename}.{format}")

    def download_video(
        self,
        video_id: str,
        quality: str = "720",
        format: str = "mp4",
        filename: str = None,
        progress_callback: Callable[[dict], None] = None,
    ) -> str:
        """
        Download video from YouTube

        Args:
            video_id: YouTube video ID
            quality: Video quality ('360', '480', '720', '1080', 'best')
            format: Video format ('mp4', 'webm', 'mkv')
            filename: Custom filename
            progress_callback: Progress callback

        Returns:
            Path to downloaded file
        """
        try:
            import yt_dlp
        except ImportError:
            raise ImportError("yt-dlp is required. Install with: pip install yt-dlp")

        if filename is None:
            filename = video_id

        output_template = os.path.join(self.output_dir, f"{filename}.%(ext)s")

        # Format selection based on quality
        if quality == "best":
            format_str = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
        else:
            format_str = f"bestvideo[height<={quality}][ext=mp4]+bestaudio[ext=m4a]/best[height<={quality}][ext=mp4]/best"

        ydl_opts = {
            "format": format_str,
            "outtmpl": output_template,
            "quiet": True,
            "no_warnings": True,
            "merge_output_format": format,
        }

        if progress_callback:
            ydl_opts["progress_hooks"] = [progress_callback]

        url = f"https://www.youtube.com/watch?v={video_id}"

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return os.path.join(self.output_dir, f"{filename}.{format}")

    def download_thumbnail(
        self,
        video_id: str,
        filename: str = None,
    ) -> str:
        """
        Download video thumbnail

        Args:
            video_id: YouTube video ID
            filename: Custom filename

        Returns:
            Path to downloaded thumbnail
        """
        try:
            import yt_dlp
            import requests
        except ImportError:
            raise ImportError("yt-dlp and requests are required")

        if filename is None:
            filename = f"{video_id}_thumbnail"

        # Get video info to find thumbnail URL
        ydl_opts = {"quiet": True, "no_warnings": True}

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(
                f"https://www.youtube.com/watch?v={video_id}",
                download=False,
            )
            thumbnail_url = info.get("thumbnail", "")

        if not thumbnail_url:
            # Fallback to standard thumbnail URL
            thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"

        # Download thumbnail
        response = requests.get(thumbnail_url)
        response.raise_for_status()

        # Determine extension
        content_type = response.headers.get("content-type", "image/jpeg")
        ext = "jpg" if "jpeg" in content_type else "png" if "png" in content_type else "webp"

        filepath = os.path.join(self.output_dir, f"{filename}.{ext}")

        with open(filepath, "wb") as f:
            f.write(response.content)

        return filepath

    def get_available_formats(self, video_id: str) -> list[dict]:
        """
        Get available download formats for a video

        Args:
            video_id: YouTube video ID

        Returns:
            List of available formats
        """
        try:
            import yt_dlp
        except ImportError:
            raise ImportError("yt-dlp is required")

        ydl_opts = {"quiet": True, "no_warnings": True}

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(
                f"https://www.youtube.com/watch?v={video_id}",
                download=False,
            )

            formats = []
            for f in info.get("formats", []):
                formats.append({
                    "format_id": f.get("format_id"),
                    "ext": f.get("ext"),
                    "resolution": f.get("resolution", "audio only"),
                    "filesize": f.get("filesize"),
                    "vcodec": f.get("vcodec"),
                    "acodec": f.get("acodec"),
                    "tbr": f.get("tbr"),  # Total bitrate
                })

            return formats


def create_progress_bar():
    """Create a progress callback for downloads"""
    from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn

    progress = Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
    )

    task_id = None

    def callback(d):
        nonlocal task_id

        if d["status"] == "downloading":
            if task_id is None:
                task_id = progress.add_task("Downloading...", total=100)
                progress.start()

            # Calculate percentage
            if "total_bytes" in d and d["total_bytes"]:
                pct = (d["downloaded_bytes"] / d["total_bytes"]) * 100
            elif "total_bytes_estimate" in d and d["total_bytes_estimate"]:
                pct = (d["downloaded_bytes"] / d["total_bytes_estimate"]) * 100
            else:
                pct = 0

            progress.update(task_id, completed=pct)

        elif d["status"] == "finished":
            if task_id is not None:
                progress.update(task_id, completed=100)
                progress.stop()

    return callback, progress
