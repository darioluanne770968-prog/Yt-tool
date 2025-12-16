"""
Whisper-based transcription for videos without subtitles
"""

import os
import subprocess
import tempfile
from typing import Dict, Optional
from .downloader import Downloader


class WhisperTranscriber:
    """Transcribe videos using OpenAI Whisper"""

    def __init__(self, model: str = "base"):
        """
        Initialize Whisper transcriber

        Args:
            model: Whisper model size (tiny, base, small, medium, large)
        """
        self.model = model
        self.downloader = Downloader()

    def transcribe(
        self,
        video_url: str,
        language: str = None,
        output_dir: str = ".",
    ) -> Dict:
        """
        Transcribe video using Whisper

        Args:
            video_url: YouTube video URL
            language: Language code (auto-detect if None)
            output_dir: Output directory

        Returns:
            Transcription result
        """
        # Create temp directory for audio
        with tempfile.TemporaryDirectory() as temp_dir:
            # Download audio
            audio_path = self._download_audio(video_url, temp_dir)

            if not audio_path:
                return {"error": "Failed to download audio"}

            # Transcribe with Whisper
            result = self._run_whisper(audio_path, language, output_dir)

            return result

    def _download_audio(self, video_url: str, output_dir: str) -> Optional[str]:
        """Download audio from video"""
        try:
            cmd = [
                "yt-dlp",
                "-x",
                "--audio-format", "mp3",
                "--audio-quality", "0",
                "-o", os.path.join(output_dir, "audio.%(ext)s"),
                video_url,
            ]

            subprocess.run(cmd, capture_output=True, timeout=300)

            audio_path = os.path.join(output_dir, "audio.mp3")
            if os.path.exists(audio_path):
                return audio_path

            # Try other extensions
            for ext in ["m4a", "wav", "webm"]:
                path = os.path.join(output_dir, f"audio.{ext}")
                if os.path.exists(path):
                    return path

            return None
        except Exception as e:
            return None

    def _run_whisper(
        self,
        audio_path: str,
        language: str = None,
        output_dir: str = ".",
    ) -> Dict:
        """Run Whisper transcription"""
        try:
            # Try OpenAI Whisper CLI
            cmd = [
                "whisper",
                audio_path,
                "--model", self.model,
                "--output_dir", output_dir,
                "--output_format", "all",
            ]

            if language:
                cmd.extend(["--language", language])

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=1800,  # 30 minutes timeout
            )

            # Find output files
            base_name = os.path.splitext(os.path.basename(audio_path))[0]

            outputs = {
                "txt": os.path.join(output_dir, f"{base_name}.txt"),
                "vtt": os.path.join(output_dir, f"{base_name}.vtt"),
                "srt": os.path.join(output_dir, f"{base_name}.srt"),
                "json": os.path.join(output_dir, f"{base_name}.json"),
            }

            transcript = ""
            if os.path.exists(outputs["txt"]):
                with open(outputs["txt"], "r", encoding="utf-8") as f:
                    transcript = f.read()

            return {
                "success": True,
                "transcript": transcript,
                "files": {k: v for k, v in outputs.items() if os.path.exists(v)},
                "model": self.model,
            }

        except FileNotFoundError:
            return self._run_whisper_python(audio_path, language, output_dir)
        except subprocess.TimeoutExpired:
            return {"error": "Transcription timed out"}
        except Exception as e:
            return {"error": str(e)}

    def _run_whisper_python(
        self,
        audio_path: str,
        language: str = None,
        output_dir: str = ".",
    ) -> Dict:
        """Run Whisper using Python library"""
        try:
            import whisper

            model = whisper.load_model(self.model)

            options = {}
            if language:
                options["language"] = language

            result = model.transcribe(audio_path, **options)

            transcript = result.get("text", "")

            # Save outputs
            base_name = os.path.splitext(os.path.basename(audio_path))[0]

            txt_path = os.path.join(output_dir, f"{base_name}.txt")
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(transcript)

            # Generate SRT
            srt_path = os.path.join(output_dir, f"{base_name}.srt")
            srt_content = self._segments_to_srt(result.get("segments", []))
            with open(srt_path, "w", encoding="utf-8") as f:
                f.write(srt_content)

            return {
                "success": True,
                "transcript": transcript,
                "segments": result.get("segments", []),
                "language": result.get("language", ""),
                "files": {
                    "txt": txt_path,
                    "srt": srt_path,
                },
                "model": self.model,
            }

        except ImportError:
            return {
                "error": "Whisper not installed. Run: pip install openai-whisper",
                "install_command": "pip install openai-whisper",
            }
        except Exception as e:
            return {"error": str(e)}

    def _segments_to_srt(self, segments: list) -> str:
        """Convert Whisper segments to SRT format"""
        srt_lines = []

        for i, segment in enumerate(segments, 1):
            start = self._format_timestamp_srt(segment["start"])
            end = self._format_timestamp_srt(segment["end"])
            text = segment["text"].strip()

            srt_lines.append(f"{i}")
            srt_lines.append(f"{start} --> {end}")
            srt_lines.append(text)
            srt_lines.append("")

        return "\n".join(srt_lines)

    def _format_timestamp_srt(self, seconds: float) -> str:
        """Format seconds to SRT timestamp"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds - int(seconds)) * 1000)

        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

    def transcribe_with_openai_api(
        self,
        video_url: str,
        output_dir: str = ".",
    ) -> Dict:
        """Transcribe using OpenAI API (for shorter videos)"""
        try:
            from openai import OpenAI
            from .config import Config

            client = OpenAI(api_key=Config.OPENAI_API_KEY)

            # Download audio
            with tempfile.TemporaryDirectory() as temp_dir:
                audio_path = self._download_audio(video_url, temp_dir)

                if not audio_path:
                    return {"error": "Failed to download audio"}

                # Check file size (API limit is 25MB)
                file_size = os.path.getsize(audio_path)
                if file_size > 25 * 1024 * 1024:
                    return {
                        "error": "File too large for API. Use local Whisper instead.",
                        "file_size_mb": file_size / (1024 * 1024),
                    }

                with open(audio_path, "rb") as audio_file:
                    response = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file,
                        response_format="verbose_json",
                    )

                transcript = response.text

                # Save output
                txt_path = os.path.join(output_dir, "transcript.txt")
                with open(txt_path, "w", encoding="utf-8") as f:
                    f.write(transcript)

                return {
                    "success": True,
                    "transcript": transcript,
                    "language": getattr(response, "language", ""),
                    "duration": getattr(response, "duration", 0),
                    "files": {"txt": txt_path},
                    "method": "openai_api",
                }

        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_available_models() -> list:
        """Get available Whisper models"""
        return [
            {"name": "tiny", "size": "39M", "vram": "~1GB", "speed": "~32x"},
            {"name": "base", "size": "74M", "vram": "~1GB", "speed": "~16x"},
            {"name": "small", "size": "244M", "vram": "~2GB", "speed": "~6x"},
            {"name": "medium", "size": "769M", "vram": "~5GB", "speed": "~2x"},
            {"name": "large", "size": "1550M", "vram": "~10GB", "speed": "~1x"},
        ]
