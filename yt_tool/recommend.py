"""
Smart video recommendations
"""

from typing import List, Dict, Optional
from .ai_client import get_ai_client
from .progress import ProgressTracker


class VideoRecommender:
    """Recommend videos based on viewing history and preferences"""

    def __init__(self):
        self.ai_client = get_ai_client()
        self.tracker = ProgressTracker()

    def recommend_next(
        self,
        current_video_transcript: str,
        language: str = "中文",
    ) -> str:
        """
        Recommend what to learn next based on current video

        Args:
            current_video_transcript: Transcript of current video
            language: Output language

        Returns:
            Recommendations
        """
        system_prompt = f"Provide learning recommendations in {language}."

        prompt = f"""Based on this video content, recommend what to learn next:

{current_video_transcript[:6000]}

## 学习推荐

### 立即学习
[Topics to learn immediately after this video]
1. [Topic] - [Why]
2. [Topic] - [Why]

### 深入学习
[Topics to dive deeper into]
1. [Topic] - [Why]
2. [Topic] - [Why]

### 相关领域
[Related areas to explore]
1. [Area] - [How it connects]
2. [Area] - [How it connects]

### 实践项目
[Projects to apply what was learned]
1. [Project idea] - [What you'll practice]
2. [Project idea] - [What you'll practice]

### 搜索关键词
[Keywords to search for more videos]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=2000)

    def recommend_from_history(
        self,
        language: str = "中文",
    ) -> str:
        """
        Recommend based on viewing history

        Args:
            language: Output language

        Returns:
            Personalized recommendations
        """
        # Get watched videos
        completed = self.tracker.get_all_videos(status="completed")
        watching = self.tracker.get_all_videos(status="watching")

        if not completed and not watching:
            return "没有足够的观看历史来生成推荐。请先观看一些视频。"

        # Build history summary
        watched_titles = [v.get("title", v["id"]) for v in completed[:10]]
        watched_tags = []
        for v in completed + watching:
            watched_tags.extend(v.get("tags", []))

        system_prompt = f"Provide personalized recommendations in {language}."

        prompt = f"""Based on this viewing history, recommend what to watch next:

Watched Videos:
{chr(10).join(['- ' + t for t in watched_titles])}

Common Tags: {', '.join(set(watched_tags))}

## 个性化推荐

### 基于你的兴趣
[Recommendations based on viewing patterns]

### 填补知识空白
[Topics you might be missing]

### 热门相关内容
[Popular content in your interest areas]

### 挑战性内容
[More advanced content to grow]

### 搜索建议
[Specific search queries to find relevant content]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=2000)

    def find_similar_videos(
        self,
        transcript: str,
        language: str = "中文",
    ) -> str:
        """
        Find similar video topics

        Args:
            transcript: Video transcript
            language: Output language

        Returns:
            Similar video suggestions
        """
        system_prompt = f"Suggest similar content in {language}."

        prompt = f"""Based on this video content, suggest similar videos to find:

{transcript[:5000]}

## 相似视频推荐

### 同类型视频
[Videos covering similar topics]
- 搜索: "[search query]"
- 频道: [Channel type to look for]

### 不同角度
[Videos covering same topic from different perspectives]
- 搜索: "[search query]"

### 进阶内容
[More advanced videos on the topic]
- 搜索: "[search query]"

### 入门内容
[Beginner-friendly videos on the topic]
- 搜索: "[search query]"

### 相关话题
[Related but different topics]
- 搜索: "[search query]"
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=1500)

    def create_learning_path(
        self,
        goal: str,
        current_level: str = "beginner",
        language: str = "中文",
    ) -> str:
        """
        Create learning path for a goal

        Args:
            goal: Learning goal
            current_level: beginner, intermediate, advanced
            language: Output language

        Returns:
            Learning path
        """
        system_prompt = f"Create learning paths in {language}."

        prompt = f"""Create a YouTube learning path for:

Goal: {goal}
Current Level: {current_level}

## 学习路径: {goal}

### 阶段 1: 基础
**时长:** X周
**目标:** [What you'll achieve]

搜索这些视频:
1. "[Search query]" - [What to look for]
2. "[Search query]" - [What to look for]

### 阶段 2: 核心技能
**时长:** X周
**目标:** [What you'll achieve]

搜索这些视频:
1. "[Search query]"
2. "[Search query]"

### 阶段 3: 进阶
**时长:** X周
**目标:** [What you'll achieve]

搜索这些视频:
1. "[Search query]"
2. "[Search query]"

### 阶段 4: 实战
**时长:** X周
**目标:** [What you'll achieve]

搜索这些视频:
1. "[Search query]"
2. "[Search query]"

### 推荐频道
[Channels to subscribe to]

### 学习建议
[Tips for this learning path]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=2500)

    def recommend_for_topic(
        self,
        topic: str,
        language: str = "中文",
    ) -> str:
        """
        Recommend videos for a topic

        Args:
            topic: Topic of interest
            language: Output language

        Returns:
            Topic-based recommendations
        """
        system_prompt = f"Recommend YouTube content in {language}."

        prompt = f"""Recommend YouTube videos for learning about: {topic}

## {topic} 学习推荐

### 入门视频
[Videos for beginners]
- 搜索: "[query]"
- 类型: [What kind of video]

### 核心概念
[Videos covering core concepts]
- 搜索: "[query]"

### 实践教程
[Hands-on tutorials]
- 搜索: "[query]"

### 深度讲解
[In-depth explanations]
- 搜索: "[query]"

### 热门创作者
[Popular channels for this topic]

### 最新内容
[How to find recent content]
- 搜索: "[query] 2024" 或 "[query] latest"

### 不同语言资源
[Resources in different languages]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=2000)

    def analyze_gaps(
        self,
        transcripts: List[str],
        target_skill: str,
        language: str = "中文",
    ) -> str:
        """
        Analyze knowledge gaps based on watched content

        Args:
            transcripts: List of watched video transcripts
            target_skill: Skill you want to master
            language: Output language

        Returns:
            Gap analysis
        """
        system_prompt = f"Analyze learning gaps in {language}."

        combined = "\n---\n".join([t[:2000] for t in transcripts[:5]])

        prompt = f"""Analyze knowledge gaps for mastering: {target_skill}

Based on these watched videos:
{combined}

## 知识差距分析

### 已掌握
[What you've likely learned]

### 需要补充
[What's missing for {target_skill}]

### 优先学习
[Most important gaps to fill first]

### 推荐视频
[Videos to fill these gaps]
- Gap 1: 搜索 "[query]"
- Gap 2: 搜索 "[query]"

### 学习建议
[How to fill these gaps efficiently]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=2000)
