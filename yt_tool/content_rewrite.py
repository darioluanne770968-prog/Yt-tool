"""
Content Rewrite - Stylized content rewriting
风格化改写 - 将视频内容改写成不同风格
"""

from typing import Dict, List, Optional
from .ai_client import get_ai_client


# Rewrite styles configuration
REWRITE_STYLES = {
    "children": {
        "name": "儿童版",
        "description": "适合儿童理解的简化版本",
        "prompt": """请将以下内容改写成适合8-12岁儿童阅读的版本：

要求：
1. 使用简单的词汇和短句
2. 添加有趣的比喻和例子
3. 可以加入一些趣味性的元素
4. 保持核心信息不变
5. 避免复杂的专业术语"""
    },
    "professional": {
        "name": "专业版",
        "description": "正式专业的商务风格",
        "prompt": """请将以下内容改写成专业商务风格：

要求：
1. 使用正式、专业的语言
2. 结构清晰，逻辑严谨
3. 数据和事实准确
4. 适合在工作场合使用
5. 保持客观中立的语气"""
    },
    "humorous": {
        "name": "幽默版",
        "description": "轻松幽默的风格",
        "prompt": """请将以下内容改写成幽默有趣的风格：

要求：
1. 添加适当的幽默元素
2. 可以使用俏皮的比喻
3. 保持内容的核心信息
4. 让人看了会心一笑
5. 不要过于浮夸或低俗"""
    },
    "storytelling": {
        "name": "故事版",
        "description": "用故事的方式讲述",
        "prompt": """请将以下内容改写成故事形式：

要求：
1. 创造引人入胜的开头
2. 添加人物或角色
3. 有情节发展和转折
4. 将知识点融入故事中
5. 有一个有意义的结尾"""
    },
    "classical_chinese": {
        "name": "文言文版",
        "description": "古典文言文风格",
        "prompt": """请将以下内容改写成文言文风格：

要求：
1. 使用文言文句式和词汇
2. 保持古典韵味
3. 内容准确传达原意
4. 可加入适当的典故
5. 注意音韵和节奏"""
    },
    "poetic": {
        "name": "诗意版",
        "description": "富有诗意和美感的风格",
        "prompt": """请将以下内容改写成富有诗意的风格：

要求：
1. 使用优美的语言
2. 添加意象和修辞
3. 注重节奏和韵律
4. 传达情感和美感
5. 保留核心信息"""
    },
    "socratic": {
        "name": "苏格拉底式",
        "description": "通过提问引导思考",
        "prompt": """请将以下内容改写成苏格拉底式对话：

要求：
1. 以问答形式呈现
2. 通过层层追问引导思考
3. 让读者主动发现答案
4. 保持逻辑递进
5. 每个问题都有意义"""
    },
    "news": {
        "name": "新闻报道版",
        "description": "新闻稿风格",
        "prompt": """请将以下内容改写成新闻报道风格：

要求：
1. 采用倒金字塔结构
2. 开头概括要点
3. 客观中立的语气
4. 使用新闻写作惯用语
5. 事实清晰，层次分明"""
    },
    "academic": {
        "name": "学术论文版",
        "description": "学术论文风格",
        "prompt": """请将以下内容改写成学术论文风格：

要求：
1. 使用学术语言和术语
2. 结构严谨（摘要、正文、结论）
3. 客观、精确的表述
4. 适当引用和论证
5. 保持学术规范"""
    },
    "tiktok": {
        "name": "短视频脚本版",
        "description": "适合短视频的口语化脚本",
        "prompt": """请将以下内容改写成适合短视频的脚本：

要求：
1. 开头要有吸引力（hook）
2. 语言口语化、接地气
3. 节奏紧凑，信息密度高
4. 适合在60秒内讲述
5. 加入互动元素（如提问）"""
    },
    "rap": {
        "name": "说唱版",
        "description": "说唱歌词风格",
        "prompt": """请将以下内容改写成说唱歌词：

要求：
1. 押韵（尾韵或内韵）
2. 节奏感强
3. 朗朗上口
4. 保留核心信息
5. 可加入流行说唱元素"""
    },
    "motivational": {
        "name": "励志版",
        "description": "充满正能量的励志风格",
        "prompt": """请将以下内容改写成励志风格：

要求：
1. 充满正能量
2. 鼓励和激励读者
3. 使用有力的语言
4. 可引用名言警句
5. 让人读后有行动的动力"""
    },
    "dialogue": {
        "name": "对话版",
        "description": "两人对话形式",
        "prompt": """请将以下内容改写成两人对话形式：

要求：
1. 设定两个有特点的角色
2. 对话自然流畅
3. 通过对话传递信息
4. 可以有适当的讨论和争辩
5. 保持内容完整性"""
    },
    "telegram": {
        "name": "电报版",
        "description": "极简电报风格",
        "prompt": """请将以下内容改写成电报风格：

要求：
1. 极度精简
2. 只保留关键信息
3. 省略虚词和修饰
4. 类似电报的短句
5. 信息密度最大化"""
    },
    "eli5": {
        "name": "ELI5版",
        "description": "像解释给5岁小孩听一样",
        "prompt": """请将以下内容改写成"像解释给5岁小孩听"的版本（ELI5）：

要求：
1. 使用最简单的词汇
2. 用日常生活中的例子
3. 多用"就像..."这样的比喻
4. 短句为主
5. 去除所有专业术语"""
    }
}


class ContentRewriter:
    """Content rewriter for stylized transformations"""

    def __init__(self, provider: str = None):
        """
        Initialize content rewriter

        Args:
            provider: AI provider ('openai', 'anthropic', or 'gemini')
        """
        self.ai = get_ai_client(provider)

    def rewrite(
        self,
        content: str,
        style: str = "professional",
        language: str = "中文",
        preserve_length: bool = False
    ) -> str:
        """
        Rewrite content in specified style

        Args:
            content: Original content
            style: Rewrite style
            language: Output language
            preserve_length: Try to preserve original length

        Returns:
            Rewritten content
        """
        if style not in REWRITE_STYLES:
            style = "professional"

        style_config = REWRITE_STYLES[style]
        length_instruction = "保持与原文相近的长度" if preserve_length else ""

        prompt = f"""{style_config['prompt']}

{length_instruction}

原内容：
{content}

请用{language}输出改写后的内容："""

        system_prompt = f"""你是一个专业的内容改写专家，擅长将内容转换成不同的风格，
同时保持核心信息的准确性。当前任务是将内容改写成{style_config['name']}风格。"""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.7
        )

        return response

    def rewrite_multi_style(
        self,
        content: str,
        styles: List[str],
        language: str = "中文"
    ) -> Dict[str, str]:
        """
        Rewrite content in multiple styles

        Args:
            content: Original content
            styles: List of styles
            language: Output language

        Returns:
            Dictionary of style -> rewritten content
        """
        results = {}
        for style in styles:
            if style in REWRITE_STYLES:
                results[style] = self.rewrite(content, style, language)
        return results

    def custom_rewrite(
        self,
        content: str,
        custom_prompt: str,
        language: str = "中文"
    ) -> str:
        """
        Rewrite with custom instructions

        Args:
            content: Original content
            custom_prompt: Custom rewriting instructions
            language: Output language

        Returns:
            Rewritten content
        """
        prompt = f"""{custom_prompt}

原内容：
{content}

请用{language}输出："""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt="你是一个专业的内容改写专家。",
            temperature=0.7
        )

        return response

    def adapt_for_audience(
        self,
        content: str,
        audience: str,
        language: str = "中文"
    ) -> str:
        """
        Adapt content for specific audience

        Args:
            content: Original content
            audience: Target audience description
            language: Output language

        Returns:
            Adapted content
        """
        prompt = f"""请将以下内容改写，使其适合以下受众：

目标受众：{audience}

要求：
1. 使用该受众熟悉的语言和术语
2. 关注该受众关心的点
3. 采用该受众偏好的表达方式
4. 保持内容的核心信息

原内容：
{content}

请用{language}输出："""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt="你是一个擅长针对不同受众调整内容的专家。",
            temperature=0.6
        )

        return response

    def tone_shift(
        self,
        content: str,
        from_tone: str,
        to_tone: str,
        language: str = "中文"
    ) -> str:
        """
        Shift the tone of content

        Args:
            content: Original content
            from_tone: Original tone
            to_tone: Target tone
            language: Output language

        Returns:
            Content with shifted tone
        """
        prompt = f"""请将以下内容的语气从「{from_tone}」转换为「{to_tone}」：

原内容：
{content}

要求：
1. 保持核心信息不变
2. 只改变语气和表达方式
3. 确保转换自然流畅

请用{language}输出："""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt="你是一个语气转换专家，擅长在保持内容不变的情况下改变表达的语气。",
            temperature=0.6
        )

        return response

    def expand_content(
        self,
        content: str,
        factor: float = 2.0,
        language: str = "中文"
    ) -> str:
        """
        Expand content with more details

        Args:
            content: Original content
            factor: Expansion factor (e.g., 2.0 = double length)
            language: Output language

        Returns:
            Expanded content
        """
        prompt = f"""请将以下内容扩展，使其长度约为原来的{factor}倍：

原内容：
{content}

扩展要求：
1. 添加更多细节和例子
2. 补充相关背景信息
3. 增加解释和说明
4. 保持逻辑连贯
5. 不要添加不相关的内容

请用{language}输出："""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt="你是一个内容扩展专家，擅长在保持质量的同时丰富内容。",
            temperature=0.7
        )

        return response

    def condense_content(
        self,
        content: str,
        target_length: str = "50%",
        language: str = "中文"
    ) -> str:
        """
        Condense content to shorter version

        Args:
            content: Original content
            target_length: Target length (e.g., "50%", "100字")
            language: Output language

        Returns:
            Condensed content
        """
        prompt = f"""请将以下内容精简至{target_length}：

原内容：
{content}

精简要求：
1. 保留核心信息
2. 删除冗余和次要内容
3. 保持逻辑完整
4. 语言简洁有力

请用{language}输出："""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt="你是一个内容精简专家，擅长在保留核心信息的同时减少篇幅。",
            temperature=0.5
        )

        return response

    def localize_content(
        self,
        content: str,
        target_region: str,
        language: str = "中文"
    ) -> str:
        """
        Localize content for specific region/culture

        Args:
            content: Original content
            target_region: Target region (e.g., "中国大陆", "台湾", "美国")
            language: Output language

        Returns:
            Localized content
        """
        prompt = f"""请将以下内容本地化，使其适合{target_region}的读者：

原内容：
{content}

本地化要求：
1. 调整文化相关的例子和引用
2. 使用该地区习惯的表达方式
3. 转换度量单位和货币（如适用）
4. 注意避免文化敏感内容
5. 保持内容的核心信息

请用{language}输出："""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt="你是一个内容本地化专家，擅长为不同地区调整内容。",
            temperature=0.6
        )

        return response

    @staticmethod
    def get_available_styles() -> Dict:
        """Get available rewrite styles"""
        return {
            key: {"name": val["name"], "description": val["description"]}
            for key, val in REWRITE_STYLES.items()
        }


def rewrite_video_content(
    transcript: str,
    style: str = "professional",
    language: str = "中文",
    provider: str = None
) -> str:
    """
    Convenience function to rewrite video transcript

    Args:
        transcript: Video transcript
        style: Rewrite style
        language: Output language
        provider: AI provider

    Returns:
        Rewritten content
    """
    rewriter = ContentRewriter(provider)
    return rewriter.rewrite(transcript, style, language)
