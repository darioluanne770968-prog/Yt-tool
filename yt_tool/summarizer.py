"""
AI-powered video content summarization
"""

from typing import Optional
from .ai_client import get_ai_client


SUMMARY_SYSTEM_PROMPT = """你是一个专业的视频内容分析师。你的任务是分析YouTube视频的字幕内容，并生成高质量的摘要。

要求：
1. 使用清晰、简洁的语言
2. 保持客观，准确反映视频内容
3. 突出重要信息和关键观点
4. 使用用户指定的语言输出"""


SUMMARY_PROMPT_TEMPLATE = """请分析以下YouTube视频字幕内容，并生成一个详细的摘要。

字幕内容：
{transcript}

请提供：
1. **视频概述**（2-3句话总结视频主题）
2. **主要内容**（详细介绍视频讨论的主要话题）
3. **关键要点**（用列表形式列出3-7个关键要点）
4. **结论/总结**（视频的主要结论或takeaway）

请用{language}输出。"""


KEY_POINTS_SYSTEM_PROMPT = """你是一个专业的内容分析师。你的任务是从视频字幕中提取关键信息和亮点。

要求：
1. 识别最重要的信息点
2. 提取具有实际价值的建议或见解
3. 突出数据、事实和引用
4. 使用用户指定的语言输出"""


KEY_POINTS_PROMPT_TEMPLATE = """请从以下YouTube视频字幕中提取关键要点和亮点。

字幕内容：
{transcript}

请提供：
1. **核心观点**（视频的核心论点或主题）
2. **关键要点**（5-10个最重要的信息点，每个用1-2句话说明）
3. **重要数据/事实**（如有提到具体数据、统计或事实）
4. **实用建议**（如有任何可操作的建议或技巧）
5. **金句/亮点**（令人印象深刻的表述或观点）

请用{language}输出，使用Markdown格式。"""


class Summarizer:
    """Video content summarizer using AI"""

    def __init__(self, provider: str = None):
        """
        Initialize summarizer

        Args:
            provider: AI provider ('openai' or 'anthropic')
        """
        self.ai = get_ai_client(provider)

    def summarize(
        self, transcript: str, language: str = "中文", detailed: bool = False
    ) -> str:
        """
        Generate a summary of the video content

        Args:
            transcript: Video transcript text
            language: Output language
            detailed: Whether to generate detailed summary

        Returns:
            Summary text
        """
        prompt = SUMMARY_PROMPT_TEMPLATE.format(
            transcript=self._truncate_text(transcript),
            language=language,
        )

        return self.ai.chat(
            prompt=prompt,
            system_prompt=SUMMARY_SYSTEM_PROMPT,
            temperature=0.5,
        )

    def extract_key_points(self, transcript: str, language: str = "中文") -> str:
        """
        Extract key points and highlights from video

        Args:
            transcript: Video transcript text
            language: Output language

        Returns:
            Key points text
        """
        prompt = KEY_POINTS_PROMPT_TEMPLATE.format(
            transcript=self._truncate_text(transcript),
            language=language,
        )

        return self.ai.chat(
            prompt=prompt,
            system_prompt=KEY_POINTS_SYSTEM_PROMPT,
            temperature=0.5,
        )

    def _truncate_text(self, text: str, max_chars: int = 30000) -> str:
        """Truncate text if too long"""
        if len(text) <= max_chars:
            return text

        # Try to truncate at a sentence boundary
        truncated = text[:max_chars]
        last_period = max(
            truncated.rfind("。"),
            truncated.rfind("."),
            truncated.rfind("！"),
            truncated.rfind("!"),
        )

        if last_period > max_chars * 0.8:
            return truncated[: last_period + 1] + "\n\n[内容过长，已截断...]"

        return truncated + "\n\n[内容过长，已截断...]"
