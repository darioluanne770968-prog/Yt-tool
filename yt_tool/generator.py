"""
AI-powered content generation from video transcripts
"""

from typing import Optional
from .ai_client import get_ai_client


# Flashcard generation
FLASHCARD_SYSTEM_PROMPT = """你是一个专业的学习卡片设计师。你的任务是从视频内容中创建高效的学习卡片（闪卡）。

要求：
1. 每张卡片包含一个问题和答案
2. 问题应该简洁明确
3. 答案应该准确完整但不冗长
4. 覆盖视频的核心概念和知识点
5. 适合间隔重复学习"""

FLASHCARD_PROMPT_TEMPLATE = """请从以下视频内容中创建学习卡片（闪卡）。

视频内容：
{transcript}

请生成15-25张学习卡片，使用以下格式：

Q: [问题]
A: [答案]

---

Q: [问题]
A: [答案]

请用{language}输出。每张卡片用 --- 分隔。"""


# Blog post generation
BLOG_SYSTEM_PROMPT = """你是一个专业的博客作者。你的任务是将视频内容转换为高质量的博客文章。

要求：
1. 文章结构清晰，有引人入胜的开头
2. 内容丰富，有深度
3. 使用适当的标题和子标题
4. 包含实用的见解和建议
5. 结尾有总结或行动号召"""

BLOG_PROMPT_TEMPLATE = """请将以下视频内容转换为一篇高质量的博客文章。

视频内容：
{transcript}

要求：
1. 写一个吸引人的标题
2. 开头引人入胜
3. 主体内容分多个小节
4. 包含实用的见解
5. 结尾有总结

请用{language}输出，使用Markdown格式。"""


# Vocabulary extraction
VOCABULARY_SYSTEM_PROMPT = """你是一个专业的语言学专家。你的任务是从内容中提取重要的专业术语和词汇。

要求：
1. 识别专业术语和关键概念
2. 提供准确的定义或解释
3. 如有必要，提供英文对照
4. 按照重要性或主题分类"""

VOCABULARY_PROMPT_TEMPLATE = """请从以下视频内容中提取重要的专业术语和词汇。

视频内容：
{transcript}

请提供：
1. **核心术语**（视频中最重要的专业词汇）
2. **概念解释**（每个术语的简明定义）
3. **相关词汇**（相关的专业词汇）
4. **英文对照**（如适用）

格式示例：
### 术语名称
- **定义**: 简明解释
- **英文**: English term
- **上下文**: 在视频中如何使用

请用{language}输出。"""


# Podcast script generation
PODCAST_SYSTEM_PROMPT = """你是一个专业的播客脚本作家。你的任务是将视频内容转换为播客脚本风格。

要求：
1. 口语化、自然的表达
2. 适合朗读的节奏
3. 包含过渡语和连接词
4. 保持听众的注意力
5. 有开场和结尾"""

PODCAST_PROMPT_TEMPLATE = """请将以下视频内容转换为播客脚本。

视频内容：
{transcript}

要求：
1. 写一个吸引人的开场白
2. 用口语化的方式讲述内容
3. 添加适当的过渡语
4. 包含与听众的互动（如提问）
5. 写一个有力的结尾

请用{language}输出。用 [停顿] 标记需要停顿的地方。"""


class ContentGenerator:
    """Generate various content formats from video transcripts"""

    def __init__(self, provider: str = None):
        """
        Initialize content generator

        Args:
            provider: AI provider ('openai' or 'anthropic')
        """
        self.ai = get_ai_client(provider)

    def generate_flashcards(
        self, transcript: str, language: str = "中文"
    ) -> list[dict]:
        """
        Generate flashcards from transcript

        Args:
            transcript: Video transcript
            language: Output language

        Returns:
            List of flashcard dictionaries with 'question' and 'answer'
        """
        prompt = FLASHCARD_PROMPT_TEMPLATE.format(
            transcript=self._truncate_text(transcript),
            language=language,
        )

        response = self.ai.chat(
            prompt=prompt,
            system_prompt=FLASHCARD_SYSTEM_PROMPT,
            temperature=0.5,
        )

        return self._parse_flashcards(response)

    def _parse_flashcards(self, response: str) -> list[dict]:
        """Parse flashcards from response"""
        cards = []
        current_q = None
        current_a = None

        for line in response.split("\n"):
            line = line.strip()
            if line.startswith("Q:") or line.startswith("问:"):
                if current_q and current_a:
                    cards.append({"question": current_q, "answer": current_a})
                current_q = line[2:].strip()
                current_a = None
            elif line.startswith("A:") or line.startswith("答:"):
                current_a = line[2:].strip()

        if current_q and current_a:
            cards.append({"question": current_q, "answer": current_a})

        return cards

    def generate_blog_post(
        self, transcript: str, language: str = "中文"
    ) -> str:
        """
        Generate blog post from transcript

        Args:
            transcript: Video transcript
            language: Output language

        Returns:
            Blog post in Markdown format
        """
        prompt = BLOG_PROMPT_TEMPLATE.format(
            transcript=self._truncate_text(transcript),
            language=language,
        )

        return self.ai.chat(
            prompt=prompt,
            system_prompt=BLOG_SYSTEM_PROMPT,
            temperature=0.7,
        )

    def extract_vocabulary(
        self, transcript: str, language: str = "中文"
    ) -> str:
        """
        Extract vocabulary and terminology from transcript

        Args:
            transcript: Video transcript
            language: Output language

        Returns:
            Vocabulary list in Markdown format
        """
        prompt = VOCABULARY_PROMPT_TEMPLATE.format(
            transcript=self._truncate_text(transcript),
            language=language,
        )

        return self.ai.chat(
            prompt=prompt,
            system_prompt=VOCABULARY_SYSTEM_PROMPT,
            temperature=0.5,
        )

    def generate_podcast_script(
        self, transcript: str, language: str = "中文"
    ) -> str:
        """
        Generate podcast script from transcript

        Args:
            transcript: Video transcript
            language: Output language

        Returns:
            Podcast script
        """
        prompt = PODCAST_PROMPT_TEMPLATE.format(
            transcript=self._truncate_text(transcript),
            language=language,
        )

        return self.ai.chat(
            prompt=prompt,
            system_prompt=PODCAST_SYSTEM_PROMPT,
            temperature=0.7,
        )

    def export_flashcards_anki(self, cards: list[dict]) -> str:
        """
        Export flashcards in Anki import format (TSV)

        Args:
            cards: List of flashcard dictionaries

        Returns:
            TSV formatted string for Anki import
        """
        lines = []
        for card in cards:
            q = card["question"].replace("\t", " ").replace("\n", "<br>")
            a = card["answer"].replace("\t", " ").replace("\n", "<br>")
            lines.append(f"{q}\t{a}")
        return "\n".join(lines)

    def export_flashcards_markdown(self, cards: list[dict]) -> str:
        """
        Export flashcards as Markdown

        Args:
            cards: List of flashcard dictionaries

        Returns:
            Markdown formatted flashcards
        """
        lines = ["# 学习卡片\n"]
        for i, card in enumerate(cards, 1):
            lines.append(f"## 卡片 {i}\n")
            lines.append(f"**问题:** {card['question']}\n")
            lines.append(f"<details>")
            lines.append(f"<summary>查看答案</summary>\n")
            lines.append(f"{card['answer']}")
            lines.append(f"</details>\n")
            lines.append("---\n")
        return "\n".join(lines)

    def _truncate_text(self, text: str, max_chars: int = 25000) -> str:
        """Truncate text if too long"""
        if len(text) <= max_chars:
            return text
        return text[:max_chars] + "\n\n[内容已截断...]"
