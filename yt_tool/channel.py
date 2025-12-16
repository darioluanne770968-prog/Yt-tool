"""
YouTube channel analysis
"""

import subprocess
import json
from typing import Dict, List, Optional
from .ai_client import get_ai_client


class ChannelAnalyzer:
    """Analyze YouTube channel content and patterns"""

    def __init__(self):
        self.ai_client = get_ai_client()

    def get_channel_info(self, channel_url: str) -> Dict:
        """
        Get channel information using yt-dlp

        Args:
            channel_url: YouTube channel URL

        Returns:
            Channel metadata
        """
        cmd = [
            "yt-dlp",
            "--dump-json",
            "--playlist-items", "1:20",
            "--flat-playlist",
            channel_url,
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
            )

            videos = []
            for line in result.stdout.strip().split("\n"):
                if line:
                    try:
                        videos.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue

            return {
                "videos": videos,
                "video_count": len(videos),
            }
        except Exception as e:
            return {"error": str(e), "videos": []}

    def analyze_channel(
        self,
        channel_url: str,
        language: str = "中文",
    ) -> str:
        """
        Analyze channel content themes and patterns

        Args:
            channel_url: YouTube channel URL
            language: Output language

        Returns:
            Channel analysis report
        """
        channel_info = self.get_channel_info(channel_url)
        videos = channel_info.get("videos", [])

        if not videos:
            return "无法获取频道视频信息"

        # Prepare video list for analysis
        video_list = "\n".join([
            f"- {v.get('title', 'Unknown')} (views: {v.get('view_count', 'N/A')})"
            for v in videos[:20]
        ])

        system_prompt = f"Analyze YouTube channel content in {language}."

        prompt = f"""Analyze this YouTube channel based on recent videos:

Recent Videos:
{video_list}

Provide:

## 频道概览
- 主要内容领域
- 目标受众
- 内容风格

## 主题分析
### 热门主题
[Most common topics]

### 内容类型分布
- 教程: X%
- 评测: X%
- 访谈: X%
- 其他: X%

## 发布规律
- 发布频率估计
- 内容趋势

## 频道特色
- 独特卖点
- 与同类频道对比

## 推荐观看
[Top 3-5 must-watch videos based on titles]

## 改进建议
[Suggestions for the channel]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=2500)

    def analyze_topics(
        self,
        video_titles: List[str],
        language: str = "中文",
    ) -> str:
        """Analyze topics from video titles"""
        system_prompt = f"Analyze content topics in {language}."

        titles = "\n".join([f"- {t}" for t in video_titles])

        prompt = f"""Analyze the main topics covered by this channel based on video titles:

{titles}

Provide:
1. Main topic categories
2. Subtopics within each category
3. Topic frequency analysis
4. Content gaps (topics not covered)
5. Trending topics
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=2000)

    def find_best_videos(
        self,
        channel_url: str,
        topic: str = None,
        language: str = "中文",
    ) -> str:
        """Find best videos on a channel"""
        channel_info = self.get_channel_info(channel_url)
        videos = channel_info.get("videos", [])

        if not videos:
            return "无法获取频道视频信息"

        # Sort by view count
        sorted_videos = sorted(
            videos,
            key=lambda x: x.get("view_count", 0) or 0,
            reverse=True,
        )

        video_list = "\n".join([
            f"- {v.get('title', 'Unknown')} (views: {v.get('view_count', 'N/A')}, duration: {v.get('duration', 'N/A')}s)"
            for v in sorted_videos[:20]
        ])

        system_prompt = f"Recommend videos in {language}."

        topic_filter = f"\nFocus on videos related to: {topic}" if topic else ""

        prompt = f"""Based on these channel videos, recommend the best ones to watch:

{video_list}
{topic_filter}

Provide:
## 必看视频 (Top 5)
[Best videos to start with]

## 入门推荐
[Best for beginners]

## 进阶推荐
[Best for advanced viewers]

## 观看顺序建议
[Suggested viewing order]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=2000)

    def compare_channels(
        self,
        channel_urls: List[str],
        language: str = "中文",
    ) -> str:
        """Compare multiple channels"""
        channels_info = []
        for url in channel_urls:
            info = self.get_channel_info(url)
            channels_info.append({
                "url": url,
                "videos": info.get("videos", [])[:10],
            })

        channel_descriptions = ""
        for i, ch in enumerate(channels_info, 1):
            titles = "\n  ".join([v.get("title", "")[:50] for v in ch["videos"]])
            channel_descriptions += f"\n### Channel {i}\nRecent videos:\n  {titles}\n"

        system_prompt = f"Compare YouTube channels in {language}."

        prompt = f"""Compare these YouTube channels:

{channel_descriptions}

Provide:
## 频道对比

| 方面 | Channel 1 | Channel 2 | ... |
|------|-----------|-----------|-----|
| 内容领域 | | | |
| 更新频率 | | | |
| 内容深度 | | | |
| 目标受众 | | | |

## 各频道优势
[Unique strengths of each]

## 推荐选择
[Which channel for which needs]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=2500)
