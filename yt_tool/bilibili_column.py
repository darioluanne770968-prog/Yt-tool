"""
Bilibili Column Generator - Generate Bilibili column articles from video content
B站专栏生成 - 专门针对B站专栏的格式和风格生成文章
"""

from typing import Dict, List, Optional
from .ai_client import get_ai_client


# Bilibili content categories
BILIBILI_CATEGORIES = {
    "technology": {
        "name": "科技数码",
        "style": "专业但不枯燥，适当玩梗",
        "audience": "数码爱好者、程序员、科技关注者"
    },
    "gaming": {
        "name": "游戏",
        "style": "轻松活泼，可以有游戏梗",
        "audience": "游戏玩家、电竞爱好者"
    },
    "anime": {
        "name": "动画/番剧",
        "style": "二次元风格，可用日语梗",
        "audience": "动漫爱好者、二次元用户"
    },
    "knowledge": {
        "name": "知识科普",
        "style": "深入浅出，有干货",
        "audience": "求知欲强的用户"
    },
    "lifestyle": {
        "name": "生活",
        "style": "接地气，有温度",
        "audience": "年轻用户群体"
    },
    "entertainment": {
        "name": "娱乐",
        "style": "有趣好玩，节目效果",
        "audience": "追求娱乐内容的用户"
    },
    "food": {
        "name": "美食",
        "style": "烟火气，垂涎欲滴",
        "audience": "吃货、美食爱好者"
    },
    "tutorial": {
        "name": "教程",
        "style": "清晰实用，步骤详细",
        "audience": "想要学习技能的用户"
    }
}


class BilibiliColumnGenerator:
    """Generator for Bilibili column articles"""

    def __init__(self, provider: str = None):
        """
        Initialize Bilibili column generator

        Args:
            provider: AI provider ('openai', 'anthropic', or 'gemini')
        """
        self.ai = get_ai_client(provider)

    def generate_column(
        self,
        transcript: str,
        title: str = "",
        category: str = "knowledge",
        language: str = "中文"
    ) -> str:
        """
        Generate a Bilibili column article

        Args:
            transcript: Video transcript
            title: Video title
            category: Content category
            language: Output language

        Returns:
            Bilibili column article
        """
        category_info = BILIBILI_CATEGORIES.get(category, BILIBILI_CATEGORIES["knowledge"])

        prompt = f"""将以下视频内容转换为B站专栏文章：

**原视频标题**: {title or '未知'}
**内容分区**: {category_info['name']}
**目标受众**: {category_info['audience']}
**风格要求**: {category_info['style']}

**视频内容**:
{self._truncate_text(transcript)}

请生成B站专栏文章：

## 文章标题
[吸引眼球的标题，可以包含B站常用的标题技巧]

## 头图建议
[描述适合作为专栏头图的画面]

## 正文

### 开场
[B站风格的开场，可以有梗、有互动]

### 主体内容
[结构清晰的正文，分段落和小标题]
[适当使用表情、加粗、引用等排版]

### 总结
[干货总结，核心要点]

### 互动环节
[引导评论、收藏、投币的文案]

---

## 发布建议

### 标签推荐
[推荐5-8个相关标签]

### 发布时间
[推荐发布时间段]

### 关联视频
[是否可以关联视频，如何引流]

请用{language}输出，符合B站专栏的排版规范。"""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt=self._get_system_prompt(),
            temperature=0.7
        )

        return response

    def generate_title_options(
        self,
        content: str,
        category: str = "knowledge",
        count: int = 10,
        language: str = "中文"
    ) -> str:
        """
        Generate title options for Bilibili column

        Args:
            content: Article content or topic
            category: Content category
            count: Number of titles
            language: Output language

        Returns:
            Title options
        """
        category_info = BILIBILI_CATEGORIES.get(category, BILIBILI_CATEGORIES["knowledge"])

        prompt = f"""为B站专栏生成{count}个标题选项：

**内容简介**: {content[:500]}
**分区**: {category_info['name']}
**受众**: {category_info['audience']}

B站标题技巧：
1. 可以用【】突出关键词
2. 数字往往很吸引眼球
3. 适当的悬念或疑问
4. 蹭热点但不过度
5. 二次元用户喜欢玩梗

请生成{count}个标题：

### 严肃型
1.
2.

### 悬念型
3.
4.

### 数据型
5.
6.

### 玩梗型
7.
8.

### 反常识型
9.
10.

## 推荐排名
按预期点击率排序，说明理由

请用{language}输出。"""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt=self._get_system_prompt(),
            temperature=0.8
        )

        return response

    def add_bilibili_elements(
        self,
        article: str,
        language: str = "中文"
    ) -> str:
        """
        Add Bilibili-specific elements to article

        Args:
            article: Existing article
            language: Output language

        Returns:
            Article with Bilibili elements
        """
        prompt = f"""为以下文章添加B站特色元素：

**原文章**:
{article}

请添加：

### 1. B站风格的开场白
[符合B站文化的打招呼方式]

### 2. 适当的表情和颜文字
[在合适的位置添加B站常用表情]

### 3. 互动引导
[引导三连、评论、关注的文案]

### 4. 梗和流行语
[适当融入B站流行的梗]

### 5. 投票/互动话题
[可以引发讨论的话题]

---

## 完整优化版文章

[输出添加了以上元素的完整文章]

请用{language}输出。"""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt=self._get_system_prompt(),
            temperature=0.7
        )

        return response

    def generate_summary_card(
        self,
        article: str,
        language: str = "中文"
    ) -> str:
        """
        Generate a summary card for the article

        Args:
            article: Article content
            language: Output language

        Returns:
            Summary card content
        """
        prompt = f"""为以下B站专栏生成总结卡片：

**文章内容**:
{self._truncate_text(article)}

请生成：

## 一图读懂版

### 核心要点 (3-5点)
-
-
-

### 一句话总结


### 适合做成图片的排版
```
┌─────────────────────────────┐
│         [标题]              │
├─────────────────────────────┤
│ ✓ 要点1                     │
│ ✓ 要点2                     │
│ ✓ 要点3                     │
├─────────────────────────────┤
│    [金句/总结]              │
└─────────────────────────────┘
```

### 朋友圈/微博分享文案


请用{language}输出。"""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt=self._get_system_prompt(),
            temperature=0.6
        )

        return response

    def generate_comment_replies(
        self,
        article_topic: str,
        comment_types: List[str] = None,
        language: str = "中文"
    ) -> str:
        """
        Generate template replies for common comments

        Args:
            article_topic: Topic of the article
            comment_types: Types of comments to prepare for
            language: Output language

        Returns:
            Comment reply templates
        """
        comment_types = comment_types or ["praise", "question", "criticism", "discussion"]

        prompt = f"""为关于「{article_topic}」的B站专栏准备评论回复模板：

请准备以下类型评论的回复：

### 1. 夸赞型评论
**常见评论**: "写得太好了"、"干货满满"
**回复模板**:

### 2. 提问型评论
**常见问题**: [预测可能的问题]
**回复模板**:

### 3. 质疑型评论
**可能的质疑**: [预测可能的质疑]
**回复模板**:

### 4. 讨论型评论
**讨论方向**: [可能的讨论话题]
**回复模板**:

### 5. 抬杠型评论
**如何应对**:
**回复模板**:

### 6. 求更新型评论
**回复模板**:

## 评论区运营建议
- 最佳回复时机
- 需要重点回复的评论类型
- 可以置顶的评论

请用{language}输出。"""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt=self._get_system_prompt(),
            temperature=0.7
        )

        return response

    def convert_to_series(
        self,
        transcript: str,
        series_count: int = 3,
        language: str = "中文"
    ) -> str:
        """
        Convert content to a series of columns

        Args:
            transcript: Source content
            series_count: Number of articles in series
            language: Output language

        Returns:
            Series plan
        """
        prompt = f"""将以下内容规划为{series_count}篇系列B站专栏：

**原内容**:
{self._truncate_text(transcript)}

请规划：

## 系列专栏规划

### 系列名称
[吸引人的系列名]

### 系列简介
[整体介绍，吸引读者追完整个系列]

---

### 第1篇：[标题]
- **核心内容**:
- **亮点**:
- **字数估计**:
- **与下篇的衔接**:

### 第2篇：[标题]
- **核心内容**:
- **亮点**:
- **字数估计**:
- **与上下篇的关联**:

### 第3篇：[标题]
...

---

## 发布策略

### 发布间隔
推荐间隔天数及原因

### 预告方式
每篇末尾如何预告下一篇

### 系列收尾
最后一篇如何收尾和引导

### 数据预期
系列的预期阅读趋势

请用{language}输出。"""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt=self._get_system_prompt(),
            temperature=0.7
        )

        return response

    def generate_cover_ideas(
        self,
        article_content: str,
        count: int = 5,
        language: str = "中文"
    ) -> str:
        """
        Generate cover image ideas for column

        Args:
            article_content: Article content
            count: Number of ideas
            language: Output language

        Returns:
            Cover image ideas
        """
        prompt = f"""为以下B站专栏生成{count}个封面图创意：

**文章内容**:
{self._truncate_text(article_content, 5000)}

请生成{count}个封面创意：

### 创意 1
- **风格**:
- **画面描述**:
- **文字内容**:
- **配色建议**:
- **预期效果**:

### 创意 2
...

## 封面设计建议

### 尺寸规格
B站专栏头图推荐尺寸

### 排版建议
- 文字位置
- 字体建议
- 避免区域

### 工具推荐
可以用来制作封面的工具

请用{language}输出。"""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt=self._get_system_prompt(),
            temperature=0.7
        )

        return response

    def optimize_for_seo(
        self,
        article: str,
        target_keywords: List[str] = None,
        language: str = "中文"
    ) -> str:
        """
        Optimize article for Bilibili search

        Args:
            article: Article content
            target_keywords: Target keywords
            language: Output language

        Returns:
            SEO-optimized article
        """
        keywords_text = ', '.join(target_keywords) if target_keywords else "自动识别"

        prompt = f"""优化以下B站专栏的搜索表现：

**目标关键词**: {keywords_text}

**原文章**:
{article}

请优化：

### SEO分析

#### 当前关键词密度


#### 标题优化建议


#### 标签优化建议
推荐标签:

### 优化后的文章

[输出SEO优化后的完整文章]

### 优化说明
- 做了哪些调整
- 预期搜索排名提升

请用{language}输出。"""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt=self._get_system_prompt(),
            temperature=0.5
        )

        return response

    def _get_system_prompt(self) -> str:
        """Get system prompt for Bilibili content"""
        return """你是一个资深的B站UP主和专栏作者。
你深谙B站的内容文化，知道什么内容能获得用户的喜爱。
你的文章既有干货又有趣味，懂得适当玩梗但不尴尬。
你了解B站的推荐机制和用户习惯。
输出符合B站专栏的排版规范和阅读习惯。"""

    def _truncate_text(self, text: str, max_chars: int = 20000) -> str:
        """Truncate text if too long"""
        if len(text) <= max_chars:
            return text
        return text[:max_chars] + "\n\n[内容过长，已截断...]"

    @staticmethod
    def get_categories() -> Dict:
        """Get available Bilibili categories"""
        return {
            key: {"name": val["name"], "audience": val["audience"]}
            for key, val in BILIBILI_CATEGORIES.items()
        }


def generate_bilibili_column(
    transcript: str,
    title: str = "",
    category: str = "knowledge",
    language: str = "中文",
    provider: str = None
) -> str:
    """
    Convenience function to generate Bilibili column

    Args:
        transcript: Video transcript
        title: Video title
        category: Content category
        language: Output language
        provider: AI provider

    Returns:
        Bilibili column article
    """
    generator = BilibiliColumnGenerator(provider)
    return generator.generate_column(transcript, title, category, language)
