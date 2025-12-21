"""
Poetry Converter - Convert video content to poetry and lyrics
诗歌转换 - 将视频内容转换为诗歌、说唱歌词、顺口溜
"""

from typing import Dict, List, Optional
from .ai_client import get_ai_client


POETRY_STYLES = {
    "modern": {"name": "现代诗", "description": "自由体现代诗"},
    "classical": {"name": "古诗", "description": "五言/七言古诗"},
    "haiku": {"name": "俳句", "description": "5-7-5音节俳句"},
    "rap": {"name": "说唱", "description": "押韵说唱歌词"},
    "jingle": {"name": "顺口溜", "description": "朗朗上口的顺口溜"},
    "song": {"name": "歌词", "description": "流行歌曲歌词"},
    "limerick": {"name": "打油诗", "description": "幽默打油诗"},
}


class PoetryConverter:
    """Convert content to various poetic forms"""

    def __init__(self, provider: str = None):
        self.ai = get_ai_client(provider)

    def convert(self, transcript: str, style: str = "modern", language: str = "中文") -> str:
        """Convert content to poetry"""
        style_info = POETRY_STYLES.get(style, POETRY_STYLES["modern"])

        prompt = f"""将以下内容转换为{style_info['name']}：

{self._truncate_text(transcript)}

风格: {style_info['description']}

请创作：
## {style_info['name']}

[诗歌内容]

## 创作说明
- 主题解读
- 使用的技巧
- 情感表达

用{language}创作。"""

        return self.ai.chat(prompt=prompt, system_prompt=f"你是一位才华横溢的{style_info['name']}创作者。", temperature=0.8)

    def generate_rap(self, transcript: str, beats_per_bar: int = 4, language: str = "中文") -> str:
        """Generate rap lyrics"""
        prompt = f"""将内容转换为说唱歌词：

{self._truncate_text(transcript)}

要求:
- 每bar {beats_per_bar}拍
- 押韵
- flow顺畅

请创作：
## 说唱歌词

### Verse 1
[第一段，8-16 bars]

### Hook
[副歌，朗朗上口]

### Verse 2
[第二段]

### Outro
[结尾]

## 押韵分析
## 建议BPM
## 参考风格

用{language}创作。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是专业说唱词作者。", temperature=0.8)

    def generate_jingle(self, transcript: str, topic: str = "", language: str = "中文") -> str:
        """Generate catchy jingle"""
        prompt = f"""将内容转换为顺口溜/口号：

{self._truncate_text(transcript)}
主题: {topic or '根据内容确定'}

请创作：
## 顺口溜

### 完整版
[4-8行的顺口溜]

### 精简版
[2-4行的核心版本]

### 超精简版
[1-2行的口号版]

## 使用场景
## 记忆技巧

用{language}创作。"""

        return self.ai.chat(prompt=prompt, system_prompt="你擅长创作朗朗上口的顺口溜。", temperature=0.7)

    def generate_song_lyrics(self, transcript: str, genre: str = "pop", language: str = "中文") -> str:
        """Generate song lyrics"""
        prompt = f"""将内容转换为{genre}风格歌词：

{self._truncate_text(transcript)}

请创作：
## 歌词

### 前奏/引子

### Verse 1 (主歌1)

### Pre-Chorus (导歌)

### Chorus (副歌)

### Verse 2 (主歌2)

### Bridge (桥段)

### Chorus (副歌重复)

### Outro (尾奏)

## 歌曲信息
- 建议曲风:
- 建议速度:
- 情感基调:

用{language}创作。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是专业作词人。", temperature=0.8)

    def generate_classical_poem(self, transcript: str, form: str = "七言", language: str = "中文") -> str:
        """Generate classical Chinese poem"""
        prompt = f"""将内容转换为{form}古诗：

{self._truncate_text(transcript)}

请创作：
## {form}诗

[诗歌正文]

## 注释
[重要词语解释]

## 赏析
[诗歌赏析]

用{language}创作，遵循格律。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是精通格律的古典诗人。", temperature=0.7)

    def _truncate_text(self, text: str, max_chars: int = 15000) -> str:
        if len(text) <= max_chars:
            return text
        return text[:max_chars] + "..."

    @staticmethod
    def get_styles() -> Dict:
        return POETRY_STYLES
