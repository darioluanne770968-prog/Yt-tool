"""
AI-powered subtitle translation
"""

from typing import Optional
from .ai_client import get_ai_client


TRANSLATION_SYSTEM_PROMPT = """你是一个专业的翻译专家，精通多种语言。你的任务是翻译视频字幕。

要求：
1. 保持原文的意思和语气
2. 使用自然流畅的目标语言表达
3. 保留专业术语（如有必要可在括号中保留原文）
4. 保持段落结构
5. 如果有时间戳，保留时间戳格式"""


TRANSLATION_PROMPT_TEMPLATE = """请将以下视频字幕翻译成{target_language}。

原文：
{text}

要求：
1. 保持自然流畅
2. 如有时间戳格式 [MM:SS]，请保留
3. 保持段落分隔

请直接输出翻译结果，不要添加额外说明。"""


# Language code mapping
LANGUAGE_NAMES = {
    "zh": "中文",
    "zh-CN": "简体中文",
    "zh-TW": "繁体中文",
    "en": "English",
    "ja": "日本語",
    "ko": "한국어",
    "es": "Español",
    "fr": "Français",
    "de": "Deutsch",
    "ru": "Русский",
    "pt": "Português",
    "it": "Italiano",
    "ar": "العربية",
    "hi": "हिन्दी",
    "th": "ไทย",
    "vi": "Tiếng Việt",
}


class Translator:
    """Translate video subtitles using AI"""

    def __init__(self, provider: str = None):
        """
        Initialize translator

        Args:
            provider: AI provider ('openai' or 'anthropic')
        """
        self.ai = get_ai_client(provider)

    def translate(
        self,
        text: str,
        target_language: str = "中文",
        source_language: str = None,
    ) -> str:
        """
        Translate text to target language

        Args:
            text: Text to translate
            target_language: Target language (name or code)
            source_language: Source language (optional, for context)

        Returns:
            Translated text
        """
        # Resolve language code to name if needed
        target_lang_name = LANGUAGE_NAMES.get(target_language, target_language)

        # Split long text into chunks to avoid token limits
        chunks = self._split_text(text)
        translated_chunks = []

        for chunk in chunks:
            prompt = TRANSLATION_PROMPT_TEMPLATE.format(
                target_language=target_lang_name,
                text=chunk,
            )

            translated = self.ai.chat(
                prompt=prompt,
                system_prompt=TRANSLATION_SYSTEM_PROMPT,
                temperature=0.3,
            )

            translated_chunks.append(translated)

        return "\n\n".join(translated_chunks)

    def translate_segments(
        self,
        segments: list[dict],
        target_language: str = "中文",
    ) -> list[dict]:
        """
        Translate transcript segments while preserving timestamps

        Args:
            segments: List of transcript segments with 'text', 'start', 'duration'
            target_language: Target language

        Returns:
            List of translated segments
        """
        # Combine segments into batches for efficient translation
        batch_size = 50
        translated_segments = []

        for i in range(0, len(segments), batch_size):
            batch = segments[i : i + batch_size]

            # Create numbered text for translation
            numbered_text = "\n".join(
                f"[{j}] {seg['text']}" for j, seg in enumerate(batch)
            )

            # Translate batch
            translated_text = self._translate_batch(numbered_text, target_language)

            # Parse translated text back to segments
            translated_lines = self._parse_numbered_translation(
                translated_text, len(batch)
            )

            for j, seg in enumerate(batch):
                translated_segments.append(
                    {
                        "text": translated_lines[j] if j < len(translated_lines) else seg["text"],
                        "start": seg["start"],
                        "duration": seg.get("duration", 0),
                    }
                )

        return translated_segments

    def _translate_batch(self, text: str, target_language: str) -> str:
        """Translate a batch of numbered text"""
        target_lang_name = LANGUAGE_NAMES.get(target_language, target_language)

        prompt = f"""请将以下编号文本翻译成{target_lang_name}。保留编号格式 [数字]。

{text}

直接输出翻译结果，保持编号格式。"""

        return self.ai.chat(
            prompt=prompt,
            system_prompt=TRANSLATION_SYSTEM_PROMPT,
            temperature=0.3,
        )

    def _parse_numbered_translation(
        self, translated_text: str, expected_count: int
    ) -> list[str]:
        """Parse numbered translation back to list"""
        import re

        lines = []
        pattern = r"\[(\d+)\]\s*(.+?)(?=\[\d+\]|$)"
        matches = re.findall(pattern, translated_text, re.DOTALL)

        # Create a dict for easier lookup
        translations = {int(m[0]): m[1].strip() for m in matches}

        # Build result list
        for i in range(expected_count):
            lines.append(translations.get(i, ""))

        return lines

    def _split_text(self, text: str, max_chars: int = 8000) -> list[str]:
        """Split text into chunks for translation"""
        if len(text) <= max_chars:
            return [text]

        chunks = []
        lines = text.split("\n")
        current_chunk = []
        current_length = 0

        for line in lines:
            if current_length + len(line) > max_chars and current_chunk:
                chunks.append("\n".join(current_chunk))
                current_chunk = []
                current_length = 0

            current_chunk.append(line)
            current_length += len(line) + 1

        if current_chunk:
            chunks.append("\n".join(current_chunk))

        return chunks

    @staticmethod
    def get_supported_languages() -> dict:
        """Get list of supported languages"""
        return LANGUAGE_NAMES.copy()
