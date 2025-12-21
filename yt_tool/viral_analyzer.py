"""
Viral Analyzer - Analyze why videos go viral and extract viral elements
爆款视频分析 - 分析视频为什么能火，提取爆款元素
"""

from typing import Dict, List, Optional
from .ai_client import get_ai_client


# Viral factors framework
VIRAL_FACTORS = {
    "hook": {
        "name": "开场钩子",
        "description": "开头3秒内吸引注意力的元素",
        "weight": 0.20
    },
    "emotion": {
        "name": "情感共鸣",
        "description": "触发观众情感反应的能力",
        "weight": 0.18
    },
    "value": {
        "name": "价值密度",
        "description": "信息价值与时长的比例",
        "weight": 0.15
    },
    "uniqueness": {
        "name": "独特视角",
        "description": "内容的独特性和新颖性",
        "weight": 0.12
    },
    "shareability": {
        "name": "可分享性",
        "description": "观众分享给他人的意愿",
        "weight": 0.12
    },
    "controversy": {
        "name": "争议性",
        "description": "引发讨论和辩论的潜力",
        "weight": 0.08
    },
    "relatability": {
        "name": "相关性",
        "description": "与观众日常生活的关联程度",
        "weight": 0.08
    },
    "timing": {
        "name": "时效性",
        "description": "与当前热点或趋势的契合度",
        "weight": 0.07
    }
}


class ViralAnalyzer:
    """Analyzer for viral video elements and potential"""

    def __init__(self, provider: str = None):
        """
        Initialize viral analyzer

        Args:
            provider: AI provider ('openai', 'anthropic', or 'gemini')
        """
        self.ai = get_ai_client(provider)

    def analyze_viral_potential(
        self,
        transcript: str,
        title: str = "",
        metadata: dict = None,
        language: str = "中文"
    ) -> str:
        """
        Analyze video's viral potential

        Args:
            transcript: Video transcript
            title: Video title
            metadata: Video metadata (views, likes, etc.)
            language: Output language

        Returns:
            Viral potential analysis
        """
        metadata = metadata or {}

        prompt = f"""分析以下视频的爆款潜力：

**视频标题**: {title or '未知'}
**视频数据**: 播放量 {metadata.get('views', '未知')}, 点赞 {metadata.get('likes', '未知')}

**视频内容**:
{self._truncate_text(transcript)}

请从以下维度进行分析：

### 1. 开场钩子分析 (Hook)
- 开场是否抓人
- 前3秒的吸引力
- 评分：/10

### 2. 情感共鸣分析
- 触发的情感类型
- 情感强度
- 评分：/10

### 3. 价值密度分析
- 干货含量
- 信息密度
- 评分：/10

### 4. 独特视角分析
- 内容新颖度
- 差异化程度
- 评分：/10

### 5. 可分享性分析
- 观众分享意愿
- 社交货币价值
- 评分：/10

### 6. 争议性分析
- 话题争议度
- 讨论空间
- 评分：/10

### 7. 相关性分析
- 目标受众共鸣
- 痛点匹配度
- 评分：/10

### 8. 时效性分析
- 热点契合度
- 持续价值
- 评分：/10

## 综合评估
- **爆款指数**: XX/100
- **最强元素**:
- **最弱环节**:
- **爆款概率**:

请用{language}输出。"""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt=self._get_system_prompt(),
            temperature=0.6
        )

        return response

    def extract_viral_elements(
        self,
        transcript: str,
        language: str = "中文"
    ) -> str:
        """
        Extract specific viral elements from video

        Args:
            transcript: Video transcript
            language: Output language

        Returns:
            Extracted viral elements
        """
        prompt = f"""从以下视频内容中提取可复用的爆款元素：

{self._truncate_text(transcript)}

请提取：

### 1. 金句/爆点语录
- 列出视频中最有传播力的句子
- 分析为什么这些句子有传播力

### 2. Hook技巧
- 开场使用的吸引技巧
- 可以借鉴的hook模板

### 3. 结构模板
- 视频的内容结构
- 可复用的结构框架

### 4. 情感触发点
- 使用的情感触发技巧
- 情感曲线设计

### 5. 转折与高潮
- 内容中的转折点
- 高潮时刻的设计

### 6. Call to Action
- 引导互动的方式
- CTA的设计技巧

### 7. 可复制元素清单
以模板形式列出可直接复用的元素

请用{language}输出。"""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt=self._get_system_prompt(),
            temperature=0.6
        )

        return response

    def analyze_title_thumbnail(
        self,
        title: str,
        description: str = "",
        language: str = "中文"
    ) -> str:
        """
        Analyze title and thumbnail potential

        Args:
            title: Video title
            description: Video description
            language: Output language

        Returns:
            Title/thumbnail analysis
        """
        prompt = f"""分析视频标题的爆款潜力：

**标题**: {title}
**描述**: {description or '无'}

请分析：

### 1. 标题分析
- **点击欲望**: /10
- **好奇心激发**: /10
- **清晰度**: /10
- **情感触发**: /10

### 2. 标题技巧识别
- 使用的标题技巧（数字、疑问、对比等）
- 关键词选择分析
- 情感词使用

### 3. 优化建议
提供3-5个优化后的标题版本：
1. [更吸引眼球版]
2. [更有价值感版]
3. [更有争议性版]
4. [更接地气版]
5. [SEO优化版]

### 4. 封面建议
- 推荐的封面元素
- 推荐的文字叠加
- 配色建议
- 表情/人物建议

请用{language}输出。"""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt=self._get_system_prompt(),
            temperature=0.7
        )

        return response

    def compare_viral_videos(
        self,
        transcripts: List[Dict],
        language: str = "中文"
    ) -> str:
        """
        Compare multiple videos for viral elements

        Args:
            transcripts: List of dicts with 'title' and 'transcript'
            language: Output language

        Returns:
            Comparative analysis
        """
        video_sections = []
        for i, video in enumerate(transcripts[:5], 1):  # Max 5 videos
            video_sections.append(f"""
### 视频{i}: {video.get('title', '未知')}
{self._truncate_text(video.get('transcript', ''), 3000)}
""")

        prompt = f"""对比分析以下视频的爆款元素：

{chr(10).join(video_sections)}

请分析：

### 1. 共同爆款元素
- 这些视频共有的成功元素

### 2. 差异化特点
- 每个视频的独特成功因素

### 3. 爆款公式提炼
- 从这些视频中提炼出的爆款公式

### 4. 可借鉴策略
- 内容策略
- 呈现策略
- 互动策略

### 5. 排名分析
按爆款潜力排序并说明理由

请用{language}输出。"""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt=self._get_system_prompt(),
            temperature=0.6
        )

        return response

    def generate_viral_hooks(
        self,
        topic: str,
        style: str = "general",
        count: int = 10,
        language: str = "中文"
    ) -> str:
        """
        Generate viral hooks for a topic

        Args:
            topic: Video topic
            style: Content style
            count: Number of hooks to generate
            language: Output language

        Returns:
            List of viral hooks
        """
        prompt = f"""为以下主题生成{count}个爆款开场hook：

**主题**: {topic}
**风格**: {style}

要求：
1. 每个hook不超过2句话
2. 开场就要抓住注意力
3. 激发好奇心或情感
4. 适合短视频平台

请生成{count}个不同类型的hook：

### 悬念型 Hook
1. ...
2. ...

### 痛点型 Hook
3. ...
4. ...

### 反常识型 Hook
5. ...
6. ...

### 数据型 Hook
7. ...
8. ...

### 情感型 Hook
9. ...
10. ...

每个hook后说明其使用的技巧和适用场景。

请用{language}输出。"""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt=self._get_system_prompt(),
            temperature=0.8
        )

        return response

    def analyze_engagement_triggers(
        self,
        transcript: str,
        language: str = "中文"
    ) -> str:
        """
        Analyze engagement triggers in video

        Args:
            transcript: Video transcript
            language: Output language

        Returns:
            Engagement trigger analysis
        """
        prompt = f"""分析视频中的互动触发点：

{self._truncate_text(transcript)}

请分析：

### 1. 点赞触发点
- 能引发点赞的时刻
- 使用的技巧

### 2. 评论触发点
- 能引发评论的话题
- 问题设置技巧

### 3. 分享触发点
- 能引发分享的内容
- 社交货币元素

### 4. 关注触发点
- 能转化关注的理由
- 人设和价值传递

### 5. 完播触发点
- 保持观看的元素
- 节奏控制技巧

### 6. 互动优化建议
具体可以添加的互动引导

请用{language}输出。"""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt=self._get_system_prompt(),
            temperature=0.6
        )

        return response

    def predict_performance(
        self,
        transcript: str,
        title: str,
        niche: str = "general",
        language: str = "中文"
    ) -> str:
        """
        Predict video performance

        Args:
            transcript: Video transcript
            title: Video title
            niche: Content niche
            language: Output language

        Returns:
            Performance prediction
        """
        prompt = f"""预测视频表现：

**标题**: {title}
**领域**: {niche}
**内容**:
{self._truncate_text(transcript)}

请预测：

### 1. 预期数据范围
- 播放量预估:
- 点赞率预估:
- 评论率预估:
- 完播率预估:

### 2. 表现预测依据
- 有利因素
- 不利因素

### 3. 目标受众画像
- 核心受众
- 潜在受众

### 4. 最佳发布时机
- 推荐发布时间
- 推荐发布日期

### 5. 优化建议
如何提高各项指标

### 6. 风险提示
可能影响表现的风险因素

请用{language}输出。"""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt=self._get_system_prompt(),
            temperature=0.6
        )

        return response

    def _get_system_prompt(self) -> str:
        """Get system prompt for viral analysis"""
        return """你是一个资深的视频内容运营专家和爆款分析师。
你深谙各大短视频平台的推荐机制和用户心理。
你的分析应该专业、具体、可操作。
基于数据和经验提供洞察，而非泛泛而谈。"""

    def _truncate_text(self, text: str, max_chars: int = 20000) -> str:
        """Truncate text if too long"""
        if len(text) <= max_chars:
            return text
        return text[:max_chars] + "\n\n[内容过长，已截断...]"


def analyze_viral_potential(
    transcript: str,
    title: str = "",
    language: str = "中文",
    provider: str = None
) -> str:
    """
    Convenience function to analyze viral potential

    Args:
        transcript: Video transcript
        title: Video title
        language: Output language
        provider: AI provider

    Returns:
        Viral potential analysis
    """
    analyzer = ViralAnalyzer(provider)
    return analyzer.analyze_viral_potential(transcript, title, language=language)
