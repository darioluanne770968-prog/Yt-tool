"""
AI-powered video content summarization
"""

from typing import Optional
from .ai_client import get_ai_client


# Summary styles configuration
SUMMARY_STYLES = {
    "default": {
        "name": "标准摘要",
        "description": "平衡的详细程度，适合一般用途",
        "system_prompt": """你是一个专业的视频内容分析师。你的任务是分析YouTube视频的字幕内容，并生成高质量的摘要。

要求：
1. 使用清晰、简洁的语言
2. 保持客观，准确反映视频内容
3. 突出重要信息和关键观点
4. 使用用户指定的语言输出""",
        "prompt_template": """请分析以下YouTube视频字幕内容，并生成一个详细的摘要。

字幕内容：
{transcript}

请提供：
1. **视频概述**（2-3句话总结视频主题）
2. **主要内容**（详细介绍视频讨论的主要话题）
3. **关键要点**（用列表形式列出3-7个关键要点）
4. **结论/总结**（视频的主要结论或takeaway）

请用{language}输出。""",
    },
    "brief": {
        "name": "简短摘要",
        "description": "简洁的一段话摘要，适合快速了解",
        "system_prompt": "你是一个专业的内容摘要专家。用最简洁的语言总结视频核心内容。",
        "prompt_template": """请用一段话（100-150字）简要总结以下视频内容的核心要点：

{transcript}

要求：只输出摘要内容，不需要标题或格式。用{language}输出。""",
    },
    "detailed": {
        "name": "详细摘要",
        "description": "深入详细的分析，适合学习笔记",
        "system_prompt": """你是一个专业的学习内容分析师。你的任务是深入分析视频内容，生成详细的学习笔记。

要求：
1. 深入分析每个主要话题
2. 提取所有重要细节
3. 保留具体的例子和数据
4. 组织结构清晰，便于复习""",
        "prompt_template": """请深入分析以下YouTube视频字幕内容，生成详细的学习笔记。

字幕内容：
{transcript}

请提供：
1. **视频概述**（3-5句话详细介绍视频主题和背景）
2. **内容大纲**（列出视频的结构和各部分内容）
3. **详细分析**（对每个主要话题进行深入分析）
4. **重要细节**（具体的例子、数据、引用）
5. **核心概念**（解释视频中的关键概念）
6. **实践要点**（可以实际应用的建议和方法）
7. **总结与反思**（主要收获和思考）

请用{language}输出，使用清晰的Markdown格式。""",
    },
    "bullets": {
        "name": "要点列表",
        "description": "纯要点列表形式，便于快速浏览",
        "system_prompt": "你是一个专业的内容提炼专家。用要点列表形式总结视频内容。",
        "prompt_template": """请将以下视频内容提炼成要点列表：

{transcript}

要求：
- 每个要点一行，使用 "•" 开头
- 提取10-20个核心要点
- 每个要点简洁明了（15字以内）
- 按照内容出现顺序或重要性排列

用{language}输出，只输出要点列表。""",
    },
    "academic": {
        "name": "学术风格",
        "description": "学术论文风格，适合研究和引用",
        "system_prompt": """你是一个学术研究助手。你的任务是以学术风格分析和总结视频内容。

要求：
1. 使用正式、客观的学术语言
2. 清晰区分事实和观点
3. 注意逻辑结构和论证
4. 可以指出内容的局限性""",
        "prompt_template": """请以学术风格分析以下视频内容：

视频内容：
{transcript}

请提供：
1. **摘要** (Abstract)：简要概述视频主题和主要论点
2. **背景** (Background)：介绍相关背景信息
3. **主要内容** (Main Content)：系统梳理视频的核心论述
4. **论证分析** (Analysis)：分析视频的论证逻辑和证据
5. **局限性** (Limitations)：指出可能的局限或需要进一步探讨的问题
6. **结论** (Conclusion)：总结主要发现和贡献

请用{language}输出。""",
    },
    "casual": {
        "name": "口语化",
        "description": "轻松口语化风格，像朋友聊天一样",
        "system_prompt": "你是一个友好的内容分享者。用轻松口语化的方式分享视频内容。",
        "prompt_template": """请用轻松口语化的方式，像给朋友介绍一样，总结以下视频内容：

{transcript}

要求：
- 用自然、亲切的语气
- 可以加入一些个人感受
- 突出有趣或实用的点
- 300-500字左右

用{language}输出。""",
    },
    "twitter": {
        "name": "推文风格",
        "description": "适合社交媒体分享的简短内容",
        "system_prompt": "你是一个社交媒体内容创作者。生成适合分享的简短内容。",
        "prompt_template": """请为以下视频内容创作3条可以发布在社交媒体上的推文：

{transcript}

要求：
- 每条推文不超过280字符
- 突出视频最吸引人的点
- 可以使用emoji增加表现力
- 适合引发讨论和分享

用{language}输出。格式：
🧵 推文1：...
🧵 推文2：...
🧵 推文3：...""",
    },
}

SUMMARY_SYSTEM_PROMPT = SUMMARY_STYLES["default"]["system_prompt"]

SUMMARY_PROMPT_TEMPLATE = SUMMARY_STYLES["default"]["prompt_template"]


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
        self,
        transcript: str,
        language: str = "中文",
        style: str = "default",
    ) -> str:
        """
        Generate a summary of the video content

        Args:
            transcript: Video transcript text
            language: Output language
            style: Summary style ('default', 'brief', 'detailed', 'bullets',
                   'academic', 'casual', 'twitter')

        Returns:
            Summary text
        """
        if style not in SUMMARY_STYLES:
            style = "default"

        style_config = SUMMARY_STYLES[style]

        prompt = style_config["prompt_template"].format(
            transcript=self._truncate_text(transcript),
            language=language,
        )

        return self.ai.chat(
            prompt=prompt,
            system_prompt=style_config["system_prompt"],
            temperature=0.5,
        )

    @staticmethod
    def get_available_styles() -> dict:
        """Get available summary styles"""
        return {
            key: {"name": val["name"], "description": val["description"]}
            for key, val in SUMMARY_STYLES.items()
        }

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
