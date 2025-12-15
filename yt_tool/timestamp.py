"""
AI-powered timestamp/chapter generation
"""

import json
import re
from typing import Optional
from .ai_client import get_ai_client
from .extractor import format_timestamp


TIMESTAMP_SYSTEM_PROMPT = """你是一个专业的视频编辑助手。你的任务是分析视频字幕，自动生成章节时间戳。

要求：
1. 识别视频内容的主要话题转换点
2. 为每个章节创建简洁但描述性的标题
3. 确保时间戳准确对应内容变化
4. 生成5-15个章节（根据视频长度）
5. 时间戳必须按时间顺序排列"""


TIMESTAMP_PROMPT_TEMPLATE = """请分析以下带时间戳的视频字幕，生成YouTube风格的章节时间戳。

字幕内容：
{transcript}

请严格按照以下JSON格式输出，不要添加任何其他内容：
{{
    "chapters": [
        {{"time": "00:00", "title": "开场介绍"}},
        {{"time": "01:23", "title": "章节标题"}}
    ]
}}

注意：
1. 时间格式为 MM:SS 或 HH:MM:SS
2. 第一个章节通常从 00:00 开始
3. 章节标题用{language}
4. 只输出JSON，不要有其他文字"""


class TimestampGenerator:
    """Generate video chapters/timestamps using AI"""

    def __init__(self, provider: str = None):
        """
        Initialize timestamp generator

        Args:
            provider: AI provider ('openai' or 'anthropic')
        """
        self.ai = get_ai_client(provider)

    def generate(
        self, transcript_with_timestamps: str, language: str = "中文"
    ) -> list[dict]:
        """
        Generate chapter timestamps from transcript

        Args:
            transcript_with_timestamps: Transcript with timestamps
            language: Output language for chapter titles

        Returns:
            List of chapters with time and title
        """
        prompt = TIMESTAMP_PROMPT_TEMPLATE.format(
            transcript=self._truncate_transcript(transcript_with_timestamps),
            language=language,
        )

        response = self.ai.chat(
            prompt=prompt,
            system_prompt=TIMESTAMP_SYSTEM_PROMPT,
            temperature=0.3,
        )

        return self._parse_response(response)

    def _truncate_transcript(self, transcript: str, max_chars: int = 25000) -> str:
        """Truncate transcript while keeping timestamps visible"""
        if len(transcript) <= max_chars:
            return transcript

        lines = transcript.split("\n")
        result_lines = []
        current_length = 0

        for line in lines:
            if current_length + len(line) > max_chars:
                break
            result_lines.append(line)
            current_length += len(line) + 1

        return "\n".join(result_lines)

    def _parse_response(self, response: str) -> list[dict]:
        """Parse AI response to extract chapters"""
        try:
            # Try to find JSON in the response
            json_match = re.search(r"\{[\s\S]*\}", response)
            if json_match:
                data = json.loads(json_match.group())
                return data.get("chapters", [])
        except json.JSONDecodeError:
            pass

        # Fallback: try to parse line by line
        chapters = []
        lines = response.strip().split("\n")

        for line in lines:
            # Match patterns like "00:00 - Title" or "00:00 Title"
            match = re.match(r"(\d{1,2}:\d{2}(?::\d{2})?)\s*[-–—]?\s*(.+)", line)
            if match:
                chapters.append({"time": match.group(1), "title": match.group(2).strip()})

        return chapters

    def format_chapters(self, chapters: list[dict]) -> str:
        """
        Format chapters for YouTube description

        Args:
            chapters: List of chapter dictionaries

        Returns:
            Formatted string for YouTube description
        """
        lines = []
        for chapter in chapters:
            lines.append(f"{chapter['time']} {chapter['title']}")
        return "\n".join(lines)

    def format_chapters_markdown(self, chapters: list[dict], video_id: str = None) -> str:
        """
        Format chapters as Markdown with optional YouTube links

        Args:
            chapters: List of chapter dictionaries
            video_id: YouTube video ID for creating links

        Returns:
            Markdown formatted chapters
        """
        lines = ["## 视频章节\n"]

        for chapter in chapters:
            time_str = chapter["time"]
            title = chapter["title"]

            if video_id:
                # Convert time to seconds for YouTube link
                seconds = self._time_to_seconds(time_str)
                link = f"https://youtube.com/watch?v={video_id}&t={seconds}"
                lines.append(f"- [{time_str}]({link}) {title}")
            else:
                lines.append(f"- **{time_str}** {title}")

        return "\n".join(lines)

    def _time_to_seconds(self, time_str: str) -> int:
        """Convert time string to seconds"""
        parts = time_str.split(":")
        if len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
        elif len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        return 0
