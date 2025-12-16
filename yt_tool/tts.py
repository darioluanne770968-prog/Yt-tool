"""
Text-to-Speech for generating audio summaries
"""

import os
from typing import Dict, Optional


class TTSGenerator:
    """Generate audio from text using TTS"""

    def __init__(self, output_dir: str = "."):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_audio(
        self,
        text: str,
        output_name: str = "audio_summary",
        voice: str = "alloy",
        provider: str = "openai",
    ) -> Dict:
        """
        Generate audio from text

        Args:
            text: Text to convert to speech
            output_name: Output filename (without extension)
            voice: Voice to use
            provider: TTS provider (openai, edge, gtts)

        Returns:
            Result with audio path
        """
        if provider == "openai":
            return self._generate_openai(text, output_name, voice)
        elif provider == "edge":
            return self._generate_edge(text, output_name, voice)
        elif provider == "gtts":
            return self._generate_gtts(text, output_name)
        else:
            return {"error": f"Unknown provider: {provider}"}

    def _generate_openai(
        self,
        text: str,
        output_name: str,
        voice: str = "alloy",
    ) -> Dict:
        """Generate using OpenAI TTS"""
        try:
            from openai import OpenAI
            from .config import Config

            client = OpenAI(api_key=Config.OPENAI_API_KEY)

            output_path = os.path.join(self.output_dir, f"{output_name}.mp3")

            response = client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text[:4096],  # OpenAI limit
            )

            response.stream_to_file(output_path)

            return {
                "success": True,
                "output_path": output_path,
                "provider": "openai",
                "voice": voice,
            }

        except ImportError:
            return {"error": "OpenAI not installed. Run: pip install openai"}
        except Exception as e:
            return {"error": str(e)}

    def _generate_edge(
        self,
        text: str,
        output_name: str,
        voice: str = "zh-CN-XiaoxiaoNeural",
    ) -> Dict:
        """Generate using Edge TTS (free)"""
        try:
            import edge_tts
            import asyncio

            output_path = os.path.join(self.output_dir, f"{output_name}.mp3")

            async def generate():
                communicate = edge_tts.Communicate(text, voice)
                await communicate.save(output_path)

            asyncio.run(generate())

            if os.path.exists(output_path):
                return {
                    "success": True,
                    "output_path": output_path,
                    "provider": "edge",
                    "voice": voice,
                }
            else:
                return {"error": "Failed to generate audio"}

        except ImportError:
            return {"error": "edge-tts not installed. Run: pip install edge-tts"}
        except Exception as e:
            return {"error": str(e)}

    def _generate_gtts(
        self,
        text: str,
        output_name: str,
    ) -> Dict:
        """Generate using Google TTS (free)"""
        try:
            from gtts import gTTS

            output_path = os.path.join(self.output_dir, f"{output_name}.mp3")

            tts = gTTS(text=text, lang="zh-CN")
            tts.save(output_path)

            return {
                "success": True,
                "output_path": output_path,
                "provider": "gtts",
            }

        except ImportError:
            return {"error": "gTTS not installed. Run: pip install gTTS"}
        except Exception as e:
            return {"error": str(e)}

    def generate_summary_audio(
        self,
        transcript: str,
        language: str = "中文",
        provider: str = "edge",
    ) -> Dict:
        """
        Generate audio summary from transcript

        Args:
            transcript: Video transcript
            language: Language for summary
            provider: TTS provider

        Returns:
            Result with audio path
        """
        from .summarizer import Summarizer

        # Generate summary first
        summarizer = Summarizer()
        summary = summarizer.summarize(transcript, language, style="brief")

        # Generate audio
        return self.generate_audio(summary, "summary_audio", provider=provider)

    def generate_podcast_audio(
        self,
        transcript: str,
        language: str = "中文",
        provider: str = "edge",
    ) -> Dict:
        """
        Generate podcast-style audio

        Args:
            transcript: Video transcript
            language: Language
            provider: TTS provider

        Returns:
            Result with audio path
        """
        from .generator import ContentGenerator

        # Generate podcast script
        generator = ContentGenerator()
        script = generator.generate_podcast_script(transcript, language)

        # Generate audio
        return self.generate_audio(script, "podcast_audio", provider=provider)

    @staticmethod
    def get_available_voices(provider: str = "edge") -> list:
        """Get available voices for provider"""
        if provider == "openai":
            return [
                {"id": "alloy", "name": "Alloy", "gender": "neutral"},
                {"id": "echo", "name": "Echo", "gender": "male"},
                {"id": "fable", "name": "Fable", "gender": "neutral"},
                {"id": "onyx", "name": "Onyx", "gender": "male"},
                {"id": "nova", "name": "Nova", "gender": "female"},
                {"id": "shimmer", "name": "Shimmer", "gender": "female"},
            ]
        elif provider == "edge":
            return [
                {"id": "zh-CN-XiaoxiaoNeural", "name": "Xiaoxiao", "lang": "Chinese"},
                {"id": "zh-CN-YunxiNeural", "name": "Yunxi", "lang": "Chinese"},
                {"id": "zh-CN-YunjianNeural", "name": "Yunjian", "lang": "Chinese"},
                {"id": "en-US-JennyNeural", "name": "Jenny", "lang": "English"},
                {"id": "en-US-GuyNeural", "name": "Guy", "lang": "English"},
                {"id": "ja-JP-NanamiNeural", "name": "Nanami", "lang": "Japanese"},
                {"id": "ko-KR-SunHiNeural", "name": "SunHi", "lang": "Korean"},
            ]
        else:
            return []

    def generate_multilingual(
        self,
        text: str,
        languages: list,
        output_name: str = "multilingual",
    ) -> Dict:
        """
        Generate audio in multiple languages

        Args:
            text: Text to convert (will be translated)
            languages: List of target languages
            output_name: Base output name

        Returns:
            Results for each language
        """
        from .translator import Translator

        results = {}
        translator = Translator()

        for lang in languages:
            # Translate text
            translated = translator.translate(text, lang)

            # Determine voice based on language
            voice_map = {
                "中文": "zh-CN-XiaoxiaoNeural",
                "English": "en-US-JennyNeural",
                "日本語": "ja-JP-NanamiNeural",
                "한국어": "ko-KR-SunHiNeural",
            }
            voice = voice_map.get(lang, "en-US-JennyNeural")

            # Generate audio
            result = self._generate_edge(
                translated,
                f"{output_name}_{lang}",
                voice,
            )
            results[lang] = result

        return results
