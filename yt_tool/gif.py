"""
GIF generation from video clips
"""

import os
import subprocess
from typing import Dict, Optional


class GifGenerator:
    """Generate GIFs from video"""

    def __init__(self, output_dir: str = "."):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def create_gif(
        self,
        video_url: str,
        start_time: str,
        duration: float = 5.0,
        output_name: str = None,
        width: int = 480,
        fps: int = 15,
    ) -> Dict:
        """
        Create GIF from video segment

        Args:
            video_url: YouTube video URL
            start_time: Start time (HH:MM:SS)
            duration: Duration in seconds
            output_name: Output filename
            width: GIF width in pixels
            fps: Frames per second

        Returns:
            Result with output path
        """
        if output_name is None:
            output_name = f"gif_{start_time.replace(':', '-')}"

        output_path = os.path.join(self.output_dir, f"{output_name}.gif")
        palette_path = os.path.join(self.output_dir, "palette.png")

        # First download the segment
        video_segment = os.path.join(self.output_dir, "temp_segment.mp4")

        download_cmd = [
            "yt-dlp",
            "--download-sections", f"*{start_time}-{self._add_duration(start_time, duration)}",
            "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "-o", video_segment,
            "--force-keyframes-at-cuts",
            video_url,
        ]

        try:
            subprocess.run(download_cmd, capture_output=True, timeout=120)

            if not os.path.exists(video_segment):
                return {"success": False, "error": "Failed to download video segment"}

            # Generate palette for better quality
            palette_cmd = [
                "ffmpeg",
                "-i", video_segment,
                "-vf", f"fps={fps},scale={width}:-1:flags=lanczos,palettegen",
                "-y",
                palette_path,
            ]
            subprocess.run(palette_cmd, capture_output=True, timeout=60)

            # Create GIF with palette
            gif_cmd = [
                "ffmpeg",
                "-i", video_segment,
                "-i", palette_path,
                "-lavfi", f"fps={fps},scale={width}:-1:flags=lanczos[x];[x][1:v]paletteuse",
                "-y",
                output_path,
            ]
            subprocess.run(gif_cmd, capture_output=True, timeout=120)

            # Cleanup
            if os.path.exists(video_segment):
                os.remove(video_segment)
            if os.path.exists(palette_path):
                os.remove(palette_path)

            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path) / 1024  # KB
                return {
                    "success": True,
                    "output_path": output_path,
                    "size_kb": round(file_size, 2),
                    "width": width,
                    "fps": fps,
                    "duration": duration,
                }
            else:
                return {"success": False, "error": "Failed to create GIF"}

        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Operation timed out"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def create_multiple_gifs(
        self,
        video_url: str,
        timestamps: list,
        duration: float = 3.0,
        width: int = 480,
    ) -> list:
        """
        Create multiple GIFs from different timestamps

        Args:
            video_url: YouTube video URL
            timestamps: List of start times
            duration: Duration for each GIF
            width: GIF width

        Returns:
            List of results
        """
        results = []

        for i, timestamp in enumerate(timestamps):
            result = self.create_gif(
                video_url,
                timestamp,
                duration,
                f"gif_{i+1}",
                width,
            )
            result["timestamp"] = timestamp
            results.append(result)

        return results

    def create_thumbnail_gif(
        self,
        video_url: str,
        output_name: str = "thumbnail",
    ) -> Dict:
        """
        Create a thumbnail GIF from video preview

        Args:
            video_url: YouTube video URL
            output_name: Output filename

        Returns:
            Result with output path
        """
        # Get video duration first
        info_cmd = [
            "yt-dlp",
            "--print", "duration",
            video_url,
        ]

        try:
            result = subprocess.run(info_cmd, capture_output=True, text=True, timeout=30)
            duration = float(result.stdout.strip() or 60)

            # Create GIF from middle section
            start_seconds = max(0, duration * 0.3)  # Start at 30%
            start_time = self._seconds_to_timestamp(start_seconds)

            return self.create_gif(
                video_url,
                start_time,
                duration=3.0,
                output_name=output_name,
                width=320,
                fps=10,
            )

        except Exception as e:
            return {"success": False, "error": str(e)}

    def create_reaction_gif(
        self,
        video_url: str,
        start_time: str,
        text: str = None,
        duration: float = 3.0,
        output_name: str = "reaction",
    ) -> Dict:
        """
        Create reaction GIF with optional text overlay

        Args:
            video_url: YouTube video URL
            start_time: Start time
            text: Text to overlay (optional)
            duration: Duration in seconds
            output_name: Output filename

        Returns:
            Result with output path
        """
        # First create base GIF
        base_result = self.create_gif(
            video_url,
            start_time,
            duration,
            f"{output_name}_base",
            width=480,
        )

        if not base_result.get("success"):
            return base_result

        if not text:
            # Rename and return
            final_path = os.path.join(self.output_dir, f"{output_name}.gif")
            os.rename(base_result["output_path"], final_path)
            base_result["output_path"] = final_path
            return base_result

        # Add text overlay
        base_gif = base_result["output_path"]
        final_path = os.path.join(self.output_dir, f"{output_name}.gif")

        cmd = [
            "ffmpeg",
            "-i", base_gif,
            "-vf", f"drawtext=text='{text}':fontsize=24:fontcolor=white:borderw=2:bordercolor=black:x=(w-text_w)/2:y=h-th-10",
            "-y",
            final_path,
        ]

        try:
            subprocess.run(cmd, capture_output=True, timeout=60)

            # Cleanup base
            os.remove(base_gif)

            if os.path.exists(final_path):
                return {
                    "success": True,
                    "output_path": final_path,
                    "text": text,
                }
            else:
                return {"success": False, "error": "Failed to add text"}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def optimize_gif(
        self,
        gif_path: str,
        max_size_kb: int = 500,
    ) -> Dict:
        """
        Optimize GIF to reduce file size

        Args:
            gif_path: Path to GIF file
            max_size_kb: Target max size in KB

        Returns:
            Result with optimized path
        """
        if not os.path.exists(gif_path):
            return {"success": False, "error": "GIF file not found"}

        current_size = os.path.getsize(gif_path) / 1024

        if current_size <= max_size_kb:
            return {
                "success": True,
                "output_path": gif_path,
                "size_kb": round(current_size, 2),
                "optimized": False,
            }

        # Try different optimization levels
        output_path = gif_path.replace(".gif", "_optimized.gif")

        # Use gifsicle if available
        try:
            cmd = [
                "gifsicle",
                "-O3",
                "--colors", "128",
                "--lossy=80",
                "-o", output_path,
                gif_path,
            ]
            subprocess.run(cmd, capture_output=True, timeout=60)

            if os.path.exists(output_path):
                new_size = os.path.getsize(output_path) / 1024
                return {
                    "success": True,
                    "output_path": output_path,
                    "original_size_kb": round(current_size, 2),
                    "size_kb": round(new_size, 2),
                    "reduction": f"{round((1 - new_size/current_size) * 100)}%",
                    "optimized": True,
                }

        except FileNotFoundError:
            # gifsicle not installed, try ffmpeg
            pass

        # FFmpeg optimization
        cmd = [
            "ffmpeg",
            "-i", gif_path,
            "-vf", "scale=320:-1:flags=lanczos,fps=10",
            "-y",
            output_path,
        ]

        try:
            subprocess.run(cmd, capture_output=True, timeout=60)

            if os.path.exists(output_path):
                new_size = os.path.getsize(output_path) / 1024
                return {
                    "success": True,
                    "output_path": output_path,
                    "original_size_kb": round(current_size, 2),
                    "size_kb": round(new_size, 2),
                    "optimized": True,
                }

        except Exception as e:
            return {"success": False, "error": str(e)}

        return {"success": False, "error": "Optimization failed"}

    def _add_duration(self, timestamp: str, duration: float) -> str:
        """Add duration to timestamp"""
        parts = timestamp.split(":")
        if len(parts) == 2:
            minutes, seconds = int(parts[0]), int(parts[1])
            total_seconds = minutes * 60 + seconds + duration
        elif len(parts) == 3:
            hours, minutes, seconds = int(parts[0]), int(parts[1]), int(parts[2])
            total_seconds = hours * 3600 + minutes * 60 + seconds + duration
        else:
            total_seconds = float(timestamp) + duration

        return self._seconds_to_timestamp(total_seconds)

    def _seconds_to_timestamp(self, seconds: float) -> str:
        """Convert seconds to timestamp format"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)

        if hours > 0:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        return f"{minutes}:{secs:02d}"
