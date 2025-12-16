"""
Multi-video summary and synthesis
"""

from typing import List, Dict, Optional
from .ai_client import get_ai_client
from .extractor import TranscriptExtractor


class MultiVideoSummarizer:
    """Summarize and synthesize multiple videos"""

    def __init__(self):
        self.ai_client = get_ai_client()

    def summarize_multiple(
        self,
        video_urls: List[str],
        language: str = "中文",
    ) -> str:
        """
        Create combined summary from multiple videos

        Args:
            video_urls: List of YouTube video URLs
            language: Output language

        Returns:
            Combined summary
        """
        transcripts = []

        for url in video_urls:
            try:
                video_id = self._extract_video_id(url)
                if video_id:
                    extractor = TranscriptExtractor(video_id)
                    extractor.extract()
                    transcripts.append({
                        "url": url,
                        "transcript": extractor.get_plain_text()[:4000],
                    })
            except Exception as e:
                transcripts.append({
                    "url": url,
                    "transcript": f"[Error: {e}]",
                })

        return self._synthesize(transcripts, language)

    def _synthesize(
        self,
        transcripts: List[Dict],
        language: str = "中文",
    ) -> str:
        """Synthesize transcripts into unified summary"""
        system_prompt = f"""You are an expert at synthesizing information from multiple sources.
Create comprehensive, unified summaries in {language}."""

        videos_content = ""
        for i, t in enumerate(transcripts, 1):
            videos_content += f"\n### Video {i}\n{t['transcript']}\n"

        prompt = f"""Synthesize these video transcripts into a unified summary:

{videos_content}

Create:

## 综合摘要

### 主题概述
[What all videos collectively cover]

### 核心观点
[Key insights from all videos combined]

### 共同主题
[Themes that appear across videos]

### 独特见解
[Unique insights from each video]

### 知识整合
[How the information connects and builds on each other]

### 行动建议
[Actionable takeaways from all videos]

### 进一步学习
[What to explore next based on all videos]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=4096)

    def _extract_video_id(self, url: str) -> Optional[str]:
        """Extract video ID from URL"""
        import re

        patterns = [
            r"(?:v=|\/)([0-9A-Za-z_-]{11}).*",
            r"(?:embed\/)([0-9A-Za-z_-]{11})",
            r"(?:youtu\.be\/)([0-9A-Za-z_-]{11})",
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)

        return url if len(url) == 11 else None

    def create_topic_deep_dive(
        self,
        video_urls: List[str],
        topic: str,
        language: str = "中文",
    ) -> str:
        """
        Create deep dive on specific topic from multiple videos

        Args:
            video_urls: List of video URLs
            topic: Topic to focus on
            language: Output language

        Returns:
            Topic deep dive
        """
        transcripts = []

        for url in video_urls:
            try:
                video_id = self._extract_video_id(url)
                if video_id:
                    extractor = TranscriptExtractor(video_id)
                    extractor.extract()
                    transcripts.append(extractor.get_plain_text()[:4000])
            except:
                pass

        system_prompt = f"Create topic deep dives in {language}."

        combined = "\n\n---\n\n".join(transcripts)

        prompt = f"""Create a deep dive on "{topic}" based on these video transcripts:

{combined}

## 深度分析: {topic}

### 定义与背景
[What is this topic and why it matters]

### 各视频观点汇总
[What each video says about this topic]

### 综合分析
[Synthesized understanding from all sources]

### 实践应用
[How to apply this knowledge]

### 争议与不同观点
[Any disagreements or different perspectives]

### 专家建议
[Expert recommendations from the videos]

### 延伸主题
[Related topics to explore]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=4096)

    def create_learning_synthesis(
        self,
        video_urls: List[str],
        language: str = "中文",
    ) -> str:
        """
        Create comprehensive learning synthesis

        Args:
            video_urls: List of video URLs
            language: Output language

        Returns:
            Learning synthesis document
        """
        transcripts = []

        for url in video_urls:
            try:
                video_id = self._extract_video_id(url)
                if video_id:
                    extractor = TranscriptExtractor(video_id)
                    extractor.extract()
                    transcripts.append({
                        "url": url,
                        "text": extractor.get_plain_text()[:3000],
                    })
            except:
                pass

        system_prompt = f"Create learning synthesis documents in {language}."

        videos_text = "\n\n---\n\n".join([t["text"] for t in transcripts])

        prompt = f"""Create a comprehensive learning synthesis from these videos:

{videos_text}

## 学习综合报告

### 学习概览
- 视频数量: {len(transcripts)}
- 主要主题: [Identify main topics]

### 知识地图
[Hierarchical view of all concepts covered]

### 核心概念清单
| 概念 | 定义 | 视频来源 |
|------|------|----------|
| ... | ... | ... |

### 技能清单
[Skills that can be learned from these videos]

### 学习路径建议
[Suggested order for learning]

### 练习建议
[Practical exercises based on content]

### 知识检验问题
[Questions to test understanding]

### 资源汇总
[All resources mentioned across videos]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=4096)

    def create_comparison_matrix(
        self,
        video_urls: List[str],
        aspects: List[str] = None,
        language: str = "中文",
    ) -> str:
        """
        Create comparison matrix for videos

        Args:
            video_urls: List of video URLs
            aspects: Aspects to compare
            language: Output language

        Returns:
            Comparison matrix
        """
        if aspects is None:
            aspects = ["主要观点", "目标受众", "深度", "实用性", "优点", "缺点"]

        transcripts = []

        for url in video_urls:
            try:
                video_id = self._extract_video_id(url)
                if video_id:
                    extractor = TranscriptExtractor(video_id)
                    extractor.extract()
                    transcripts.append({
                        "url": url,
                        "text": extractor.get_plain_text()[:3000],
                    })
            except:
                pass

        system_prompt = f"Create comparison matrices in {language}."

        videos_text = ""
        for i, t in enumerate(transcripts, 1):
            videos_text += f"\n### Video {i}\n{t['text']}\n"

        aspects_str = ", ".join(aspects)

        prompt = f"""Create a comparison matrix for these videos:

{videos_text}

Compare on these aspects: {aspects_str}

## 对比矩阵

| 方面 | Video 1 | Video 2 | ... |
|------|---------|---------|-----|
| {aspects[0]} | | | |
| ... | | | |

## 详细对比

### {aspects[0]}
[Detailed comparison]

### {aspects[1]}
[Detailed comparison]

...

## 综合评估
[Which video is best for what purpose]

## 推荐
[Recommendations based on different needs]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=3500)

    def extract_all_resources(
        self,
        video_urls: List[str],
        language: str = "中文",
    ) -> str:
        """
        Extract all resources mentioned across videos

        Args:
            video_urls: List of video URLs
            language: Output language

        Returns:
            Consolidated resource list
        """
        transcripts = []

        for url in video_urls:
            try:
                video_id = self._extract_video_id(url)
                if video_id:
                    extractor = TranscriptExtractor(video_id)
                    extractor.extract()
                    transcripts.append(extractor.get_plain_text()[:4000])
            except:
                pass

        system_prompt = f"Extract and categorize resources in {language}."

        combined = "\n\n---\n\n".join(transcripts)

        prompt = f"""Extract all resources mentioned in these videos:

{combined}

## 资源汇总

### 书籍
| 书名 | 作者 | 描述 |
|------|------|------|
| ... | ... | ... |

### 工具/软件
| 名称 | 类型 | 用途 |
|------|------|------|
| ... | ... | ... |

### 网站/平台
| 名称 | URL | 描述 |
|------|-----|------|
| ... | ... | ... |

### 课程/教程
| 名称 | 平台 | 描述 |
|------|------|------|
| ... | ... | ... |

### 其他资源
[Any other resources mentioned]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=2500)
