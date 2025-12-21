"""
Shorts Generator - Generate short video scripts from long videos
短视频脚本生成 - 从长视频中提取精华，生成适合抖音/Shorts/Reels的60秒脚本
"""

from typing import Dict, List, Optional
from .ai_client import get_ai_client


# Platform specifications
PLATFORM_SPECS = {
    "tiktok": {
        "name": "抖音/TikTok",
        "max_duration": 60,
        "optimal_duration": "15-30秒",
        "aspect_ratio": "9:16",
        "style": "快节奏、接地气、有梗",
        "features": ["duet", "stitch", "音乐", "特效"]
    },
    "youtube_shorts": {
        "name": "YouTube Shorts",
        "max_duration": 60,
        "optimal_duration": "30-60秒",
        "aspect_ratio": "9:16",
        "style": "信息密集、教育性强",
        "features": ["remix", "shorts音频"]
    },
    "instagram_reels": {
        "name": "Instagram Reels",
        "max_duration": 90,
        "optimal_duration": "15-30秒",
        "aspect_ratio": "9:16",
        "style": "美观、创意、潮流",
        "features": ["remix", "特效", "滤镜"]
    },
    "kuaishou": {
        "name": "快手",
        "max_duration": 60,
        "optimal_duration": "15-30秒",
        "aspect_ratio": "9:16",
        "style": "真实、接地气、有温度",
        "features": ["合拍", "K歌"]
    },
    "bilibili": {
        "name": "B站",
        "max_duration": 180,
        "optimal_duration": "60-120秒",
        "aspect_ratio": "16:9或9:16",
        "style": "有深度、有趣味、二次元友好",
        "features": ["投币", "一键三连"]
    }
}


class ShortsGenerator:
    """Generator for short video scripts from long-form content"""

    def __init__(self, provider: str = None):
        """
        Initialize shorts generator

        Args:
            provider: AI provider ('openai', 'anthropic', or 'gemini')
        """
        self.ai = get_ai_client(provider)

    def extract_highlights(
        self,
        transcript: str,
        count: int = 5,
        language: str = "中文"
    ) -> str:
        """
        Extract potential short video highlights from transcript

        Args:
            transcript: Video transcript
            count: Number of highlights to extract
            language: Output language

        Returns:
            List of highlight segments
        """
        prompt = f"""从以下长视频内容中提取{count}个适合制作短视频的精华片段：

{self._truncate_text(transcript)}

请提取{count}个最有潜力的片段：

每个片段请提供：

### 精华片段 1
- **核心话题**:
- **时间范围**: [估计位置]
- **原文内容**: [相关原文]
- **爆款潜力**: ⭐⭐⭐⭐⭐ (1-5星)
- **适合平台**:
- **推荐理由**:

### 精华片段 2
...

## 片段排名
按爆款潜力排序：

## 组合建议
哪些片段可以组合成系列短视频

请用{language}输出。"""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt=self._get_system_prompt(),
            temperature=0.6
        )

        return response

    def generate_script(
        self,
        transcript: str,
        platform: str = "tiktok",
        duration: int = 30,
        style: str = "informative",
        language: str = "中文"
    ) -> str:
        """
        Generate a short video script

        Args:
            transcript: Source transcript
            platform: Target platform
            duration: Target duration in seconds
            style: Content style
            language: Output language

        Returns:
            Short video script
        """
        platform_info = PLATFORM_SPECS.get(platform, PLATFORM_SPECS["tiktok"])

        prompt = f"""基于以下长视频内容，生成一个{duration}秒的短视频脚本：

**目标平台**: {platform_info['name']}
**时长**: {duration}秒
**风格**: {style}
**平台特点**: {platform_info['style']}

**原视频内容**:
{self._truncate_text(transcript)}

请生成完整脚本：

## 短视频脚本

### 基本信息
- **时长**: {duration}秒
- **平台**: {platform_info['name']}
- **风格**: {style}

### Hook (0-3秒)
[开场hook，必须在3秒内抓住注意力]

### 正文 (3-{duration-5}秒)
[分段落的主体内容，标注每段大概时长]

**第1段 (X秒)**:
[内容]

**第2段 (X秒)**:
[内容]

**第3段 (X秒)**:
[内容]

### 结尾 (最后3-5秒)
[收尾和CTA]

### 画面建议
- 开场画面：
- 主体画面：
- 结尾画面：

### 字幕/文字
- 需要添加的关键字幕

### 音效/配乐建议
- 推荐背景音乐类型
- 关键音效点

### 互动引导
- 评论引导：
- 点赞引导：
- 关注引导：

请用{language}输出。"""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt=self._get_system_prompt(),
            temperature=0.7
        )

        return response

    def generate_series(
        self,
        transcript: str,
        platform: str = "tiktok",
        count: int = 5,
        language: str = "中文"
    ) -> str:
        """
        Generate a series of short videos from one long video

        Args:
            transcript: Source transcript
            platform: Target platform
            count: Number of shorts in series
            language: Output language

        Returns:
            Series of short video scripts
        """
        platform_info = PLATFORM_SPECS.get(platform, PLATFORM_SPECS["tiktok"])

        prompt = f"""将以下长视频内容拆分成{count}个系列短视频：

**目标平台**: {platform_info['name']}
**系列数量**: {count}个
**每个时长**: {platform_info['optimal_duration']}

**原视频内容**:
{self._truncate_text(transcript)}

请生成完整系列规划：

## 系列主题
[系列的统一主题和命名]

## 系列结构

### 第1集：[标题]
- **核心内容**:
- **Hook**:
- **时长**:
- **发布顺序**: 1
- **简要脚本**:

### 第2集：[标题]
...

### 第3集：[标题]
...

(继续到第{count}集)

## 系列策略

### 发布节奏
- 推荐发布频率
- 最佳发布时间

### 系列钩子
- 如何在每集末尾引导看下一集
- 系列预告文案

### 互动策略
- 系列专属互动话题
- 评论区运营建议

### 数据预期
- 预期播放趋势
- 关键指标

请用{language}输出。"""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt=self._get_system_prompt(),
            temperature=0.7
        )

        return response

    def optimize_for_platform(
        self,
        script: str,
        platform: str,
        language: str = "中文"
    ) -> str:
        """
        Optimize existing script for specific platform

        Args:
            script: Existing script
            platform: Target platform
            language: Output language

        Returns:
            Optimized script
        """
        platform_info = PLATFORM_SPECS.get(platform, PLATFORM_SPECS["tiktok"])

        prompt = f"""将以下脚本优化为适合{platform_info['name']}的版本：

**目标平台**: {platform_info['name']}
**平台特点**: {platform_info['style']}
**最佳时长**: {platform_info['optimal_duration']}
**平台功能**: {', '.join(platform_info['features'])}

**原脚本**:
{script}

请优化：

### 优化后的脚本

#### Hook优化
[针对平台优化的开场]

#### 内容优化
[针对平台风格调整的内容]

#### 互动优化
[利用平台功能的互动设计]

#### 画面建议优化
[适合平台的画面风格]

### 优化说明
- 做了哪些调整
- 为什么这样调整
- 预期效果

请用{language}输出。"""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt=self._get_system_prompt(),
            temperature=0.6
        )

        return response

    def generate_hooks(
        self,
        topic: str,
        count: int = 10,
        platform: str = "tiktok",
        language: str = "中文"
    ) -> str:
        """
        Generate hook options for a topic

        Args:
            topic: Video topic
            count: Number of hooks
            platform: Target platform
            language: Output language

        Returns:
            List of hook options
        """
        platform_info = PLATFORM_SPECS.get(platform, PLATFORM_SPECS["tiktok"])

        prompt = f"""为以下主题生成{count}个短视频开场hook：

**主题**: {topic}
**平台**: {platform_info['name']}
**平台风格**: {platform_info['style']}

请生成{count}个不同风格的hook：

### 悬念型
1.
2.

### 痛点型
3.
4.

### 反常识型
5.
6.

### 数据型
7.
8.

### 情绪型
9.
10.

每个hook标注：
- 预期效果
- 适合的内容类型
- 搭配建议

请用{language}输出。"""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt=self._get_system_prompt(),
            temperature=0.8
        )

        return response

    def generate_captions(
        self,
        script: str,
        style: str = "dynamic",
        language: str = "中文"
    ) -> str:
        """
        Generate caption/subtitle suggestions for short video

        Args:
            script: Video script
            style: Caption style (dynamic, minimal, bold)
            language: Output language

        Returns:
            Caption suggestions
        """
        prompt = f"""为以下短视频脚本生成字幕建议：

**字幕风格**: {style}

**脚本内容**:
{script}

请生成：

### 字幕方案

#### 主要字幕
[按时间顺序列出需要显示的文字]

#### 强调字幕
[需要特殊效果突出的关键词]

#### 动态效果建议
- 入场动画：
- 停留时长：
- 退场动画：

#### 排版建议
- 位置：
- 字体：
- 颜色：
- 大小：

#### 特殊效果
- 需要特效的文字
- 建议的特效类型

请用{language}输出。"""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt=self._get_system_prompt(),
            temperature=0.6
        )

        return response

    def suggest_music(
        self,
        script: str,
        mood: str = "auto",
        language: str = "中文"
    ) -> str:
        """
        Suggest background music for short video

        Args:
            script: Video script
            mood: Desired mood or 'auto'
            language: Output language

        Returns:
            Music suggestions
        """
        prompt = f"""为以下短视频脚本推荐背景音乐：

**期望情绪**: {mood}

**脚本内容**:
{script}

请推荐：

### 音乐推荐

#### 首选推荐
- 曲风：
- 节奏：
- 情绪：
- 参考歌曲/类型：

#### 备选方案
1. [方案1]
2. [方案2]

### 音效建议
- 开场音效：
- 转折点音效：
- 结尾音效：

### 音乐使用建议
- 音乐开始时机：
- 音量变化：
- 高潮匹配：

### 版权提醒
- 使用注意事项
- 平台音乐库推荐

请用{language}输出。"""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt=self._get_system_prompt(),
            temperature=0.7
        )

        return response

    def create_content_calendar(
        self,
        topics: List[str],
        platform: str = "tiktok",
        days: int = 7,
        language: str = "中文"
    ) -> str:
        """
        Create a content calendar for short videos

        Args:
            topics: List of topics
            platform: Target platform
            days: Number of days to plan
            language: Output language

        Returns:
            Content calendar
        """
        platform_info = PLATFORM_SPECS.get(platform, PLATFORM_SPECS["tiktok"])

        prompt = f"""创建{days}天的短视频内容日历：

**平台**: {platform_info['name']}
**主题列表**: {', '.join(topics)}

请生成：

## {days}天内容日历

### 第1天
- **发布时间**:
- **主题**:
- **内容类型**:
- **Hook预告**:
- **预期效果**:

### 第2天
...

(继续到第{days}天)

## 发布策略

### 最佳发布时间
- 工作日：
- 周末：

### 内容组合建议
- 教育类占比：
- 娱乐类占比：
- 互动类占比：

### 系列规划
- 可以形成系列的主题

### 数据追踪
- 需要关注的指标
- 调整依据

请用{language}输出。"""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt=self._get_system_prompt(),
            temperature=0.7
        )

        return response

    def _get_system_prompt(self) -> str:
        """Get system prompt for shorts generation"""
        return """你是一个专业的短视频内容策划师和脚本作家。
你精通抖音、快手、YouTube Shorts、Instagram Reels等平台的内容创作。
你了解各平台的推荐算法和用户偏好。
你的脚本要有爆款潜力，能够抓住用户注意力。
输出要具体、可执行、有创意。"""

    def _truncate_text(self, text: str, max_chars: int = 20000) -> str:
        """Truncate text if too long"""
        if len(text) <= max_chars:
            return text
        return text[:max_chars] + "\n\n[内容过长，已截断...]"

    @staticmethod
    def get_platform_specs() -> Dict:
        """Get available platform specifications"""
        return PLATFORM_SPECS


def generate_shorts_script(
    transcript: str,
    platform: str = "tiktok",
    duration: int = 30,
    language: str = "中文",
    provider: str = None
) -> str:
    """
    Convenience function to generate a short video script

    Args:
        transcript: Source transcript
        platform: Target platform
        duration: Target duration
        language: Output language
        provider: AI provider

    Returns:
        Short video script
    """
    generator = ShortsGenerator(provider)
    return generator.generate_script(transcript, platform, duration, language=language)
