"""
Thread Generator - Generate Twitter/X thread posts from video content
Twitter长帖生成 - 将视频内容转换为Twitter长帖（Thread）格式
"""

from typing import Dict, List, Optional
from .ai_client import get_ai_client


# Thread styles
THREAD_STYLES = {
    "educational": {
        "name": "教育科普型",
        "description": "分享知识和见解，有结构地讲解概念",
        "emoji_use": "moderate",
        "tone": "professional but accessible"
    },
    "storytelling": {
        "name": "故事叙述型",
        "description": "用故事的方式讲述，有开头、发展、高潮、结尾",
        "emoji_use": "moderate",
        "tone": "engaging and personal"
    },
    "listicle": {
        "name": "清单型",
        "description": "列出要点、技巧或建议",
        "emoji_use": "heavy",
        "tone": "concise and actionable"
    },
    "analysis": {
        "name": "深度分析型",
        "description": "深入分析某个话题或现象",
        "emoji_use": "light",
        "tone": "thoughtful and analytical"
    },
    "controversial": {
        "name": "观点型",
        "description": "提出有争议性的观点引发讨论",
        "emoji_use": "moderate",
        "tone": "bold and provocative"
    },
    "howto": {
        "name": "教程型",
        "description": "一步步教授如何做某事",
        "emoji_use": "moderate",
        "tone": "helpful and clear"
    }
}


class ThreadGenerator:
    """Generator for Twitter/X threads from video content"""

    def __init__(self, provider: str = None):
        """
        Initialize thread generator

        Args:
            provider: AI provider ('openai', 'anthropic', or 'gemini')
        """
        self.ai = get_ai_client(provider)

    def generate_thread(
        self,
        transcript: str,
        style: str = "educational",
        tweet_count: int = 10,
        language: str = "中文",
        include_hook: bool = True,
        include_cta: bool = True
    ) -> str:
        """
        Generate a Twitter thread from video content

        Args:
            transcript: Video transcript
            style: Thread style
            tweet_count: Number of tweets in thread
            language: Output language
            include_hook: Include engaging hook
            include_cta: Include call-to-action

        Returns:
            Twitter thread
        """
        style_config = THREAD_STYLES.get(style, THREAD_STYLES["educational"])

        prompt = f"""将以下视频内容转换为Twitter长帖（Thread）：

**风格**: {style_config['name']} - {style_config['description']}
**推文数量**: {tweet_count}条
**语气**: {style_config['tone']}
**Emoji使用**: {style_config['emoji_use']}

**视频内容**:
{self._truncate_text(transcript)}

请生成Twitter Thread：

## Twitter 长帖

### 🧵 Tweet 1 (Hook)
[开场推文，吸引注意力，点明主题]
[留出悬念让人想往下看]

### Tweet 2
[第一个要点或故事开始]

### Tweet 3
[继续展开]

...

### Tweet {tweet_count-1}
[总结或高潮]

### Tweet {tweet_count} (CTA)
[行动号召，互动引导]

---

**格式要求**：
1. 每条推文不超过280字符（中文约140字）
2. 每条推文要能独立成立，又有连续性
3. 使用数字编号如 1/、2/ 开头
4. 适当使用emoji增加表现力
5. 第一条要有强hook
6. 最后一条要有互动引导

请用{language}输出。"""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt=self._get_system_prompt(),
            temperature=0.7
        )

        return response

    def generate_hook_variations(
        self,
        topic: str,
        count: int = 5,
        language: str = "中文"
    ) -> str:
        """
        Generate multiple hook variations for thread

        Args:
            topic: Thread topic
            count: Number of variations
            language: Output language

        Returns:
            Hook variations
        """
        prompt = f"""为以下主题生成{count}个Twitter Thread开场hook：

**主题**: {topic}

要求：
1. 每个hook不超过280字符
2. 必须引发好奇心
3. 暗示后续有干货
4. 让人想点开看完整thread

请生成{count}个不同风格的hook：

### Hook 1 - 悬念型
[内容]
**预期效果**:

### Hook 2 - 数据型
[内容]
**预期效果**:

### Hook 3 - 反常识型
[内容]
**预期效果**:

### Hook 4 - 故事型
[内容]
**预期效果**:

### Hook 5 - 痛点型
[内容]
**预期效果**:

## 推荐组合
最佳hook与后续内容的搭配建议

请用{language}输出。"""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt=self._get_system_prompt(),
            temperature=0.8
        )

        return response

    def optimize_thread(
        self,
        thread: str,
        optimization_focus: str = "engagement",
        language: str = "中文"
    ) -> str:
        """
        Optimize existing thread for better engagement

        Args:
            thread: Existing thread
            optimization_focus: Focus area (engagement, clarity, virality)
            language: Output language

        Returns:
            Optimized thread
        """
        prompt = f"""优化以下Twitter Thread，重点提升{optimization_focus}：

**原Thread**:
{thread}

**优化重点**: {optimization_focus}

请提供：

### 优化后的Thread

[完整的优化版本]

---

### 优化说明

#### 修改点
1. [修改1及原因]
2. [修改2及原因]
...

#### 优化效果
- 预期提升的指标
- 优化的核心逻辑

#### A/B测试建议
- 可以测试的变量
- 测试方法

请用{language}输出。"""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt=self._get_system_prompt(),
            temperature=0.6
        )

        return response

    def generate_quote_tweets(
        self,
        transcript: str,
        count: int = 5,
        language: str = "中文"
    ) -> str:
        """
        Generate standalone quote tweets from content

        Args:
            transcript: Video transcript
            count: Number of quotes
            language: Output language

        Returns:
            Quote tweets
        """
        prompt = f"""从以下内容中提取{count}条可以独立发布的金句推文：

**内容**:
{self._truncate_text(transcript)}

要求：
1. 每条不超过280字符
2. 可以独立成立，有传播价值
3. 能引发共鸣或讨论
4. 适合被转发

请提取：

### Quote Tweet 1
[内容]
**传播价值**:
**适合配图**:

### Quote Tweet 2
[内容]
**传播价值**:
**适合配图**:

...

### Quote Tweet {count}
[内容]
**传播价值**:
**适合配图**:

## 最佳发布时机
每条推文的最佳发布时间建议

请用{language}输出。"""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt=self._get_system_prompt(),
            temperature=0.7
        )

        return response

    def create_thread_series(
        self,
        transcript: str,
        series_count: int = 3,
        language: str = "中文"
    ) -> str:
        """
        Create a series of related threads from long content

        Args:
            transcript: Video transcript
            series_count: Number of threads in series
            language: Output language

        Returns:
            Thread series plan
        """
        prompt = f"""将以下长内容规划为{series_count}个系列Thread：

**内容**:
{self._truncate_text(transcript)}

请规划：

## Thread系列规划

### 系列主题
[整体系列的统一主题]

### Thread 1: [标题]
- **核心内容**:
- **Hook预览**:
- **推文数量**:
- **关键要点**:
- **发布顺序**: 1

### Thread 2: [标题]
- **核心内容**:
- **Hook预览**:
- **推文数量**:
- **关键要点**:
- **发布顺序**: 2
- **与Thread 1的关联**:

### Thread 3: [标题]
...

## 发布策略

### 发布间隔
- 推荐间隔时间
- 最佳发布日期/时间

### 互联策略
- 如何在每个thread中引导到其他thread
- 系列预告文案

### 内容升级
- 系列完成后可以汇总成什么

请用{language}输出。"""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt=self._get_system_prompt(),
            temperature=0.7
        )

        return response

    def add_visuals_suggestions(
        self,
        thread: str,
        language: str = "中文"
    ) -> str:
        """
        Add visual content suggestions to thread

        Args:
            thread: Existing thread
            language: Output language

        Returns:
            Thread with visual suggestions
        """
        prompt = f"""为以下Thread添加视觉内容建议：

**Thread**:
{thread}

请为每条推文建议视觉内容：

### 视觉内容建议

#### Tweet 1
- **图片类型**: [截图/图表/插画/照片]
- **图片描述**:
- **替代方案**:

#### Tweet 2
...

### 整体视觉风格
- 推荐的配色方案
- 字体建议
- 品牌元素

### 图片制作建议
- 推荐工具
- 尺寸规格 (1200x675 for Twitter)
- 模板建议

请用{language}输出。"""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt=self._get_system_prompt(),
            temperature=0.6
        )

        return response

    def generate_engagement_prompts(
        self,
        thread_topic: str,
        language: str = "中文"
    ) -> str:
        """
        Generate engagement prompts for end of thread

        Args:
            thread_topic: Topic of the thread
            language: Output language

        Returns:
            Engagement prompts
        """
        prompt = f"""为关于「{thread_topic}」的Thread生成互动引导：

请生成多种类型的结尾互动引导：

### 1. 问题型
[引发讨论的问题]

### 2. 投票型
[适合做投票的话题]
- 选项A:
- 选项B:

### 3. 分享型
[引导分享的文案]

### 4. 关注型
[引导关注的文案]

### 5. 行动型
[引导具体行动的文案]

### 6. 预告型
[预告后续内容的文案]

## 使用建议
- 哪种类型最适合这个话题
- 如何组合使用

请用{language}输出。"""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt=self._get_system_prompt(),
            temperature=0.7
        )

        return response

    def analyze_thread_structure(
        self,
        transcript: str,
        language: str = "中文"
    ) -> str:
        """
        Analyze and suggest optimal thread structure

        Args:
            transcript: Source content
            language: Output language

        Returns:
            Structure analysis and suggestion
        """
        prompt = f"""分析以下内容，建议最佳Thread结构：

**内容**:
{self._truncate_text(transcript)}

请分析：

### 内容分析
- **核心主题**:
- **关键信息点**:
- **内容类型**:
- **目标受众**:

### 推荐结构

#### 方案1: [结构名称]
- 推文数量:
- 结构:
  1. [第1条作用]
  2. [第2-3条作用]
  ...
- 适合原因:

#### 方案2: [结构名称]
...

### 最佳推荐
- 推荐方案及原因
- 预期效果

### 避免事项
- 不应该做的事情
- 常见错误

请用{language}输出。"""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt=self._get_system_prompt(),
            temperature=0.5
        )

        return response

    def _get_system_prompt(self) -> str:
        """Get system prompt for thread generation"""
        return """你是一个专业的Twitter/X内容创作者和社交媒体运营专家。
你精通Thread的写作技巧，知道如何创作高互动率的长帖。
你了解Twitter的最佳实践，包括字符限制、hook技巧、互动引导等。
你的Thread要有洞察力、可读性强、能引发讨论和转发。"""

    def _truncate_text(self, text: str, max_chars: int = 20000) -> str:
        """Truncate text if too long"""
        if len(text) <= max_chars:
            return text
        return text[:max_chars] + "\n\n[内容过长，已截断...]"

    @staticmethod
    def get_available_styles() -> Dict:
        """Get available thread styles"""
        return {
            key: {"name": val["name"], "description": val["description"]}
            for key, val in THREAD_STYLES.items()
        }


def generate_thread(
    transcript: str,
    style: str = "educational",
    tweet_count: int = 10,
    language: str = "中文",
    provider: str = None
) -> str:
    """
    Convenience function to generate a Twitter thread

    Args:
        transcript: Video transcript
        style: Thread style
        tweet_count: Number of tweets
        language: Output language
        provider: AI provider

    Returns:
        Twitter thread
    """
    generator = ThreadGenerator(provider)
    return generator.generate_thread(transcript, style, tweet_count, language)
