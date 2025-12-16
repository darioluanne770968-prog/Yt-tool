"""
Multi-video comparison and analysis
"""

from typing import List, Dict, Optional
from .ai_client import get_ai_client
from .extractor import TranscriptExtractor


class VideoComparator:
    """Compare multiple videos on the same topic"""

    def __init__(self):
        self.ai_client = get_ai_client()

    def compare_videos(
        self,
        transcripts: List[Dict],
        language: str = "中文",
    ) -> str:
        """
        Compare multiple video transcripts

        Args:
            transcripts: List of dicts with 'title' and 'transcript' keys
            language: Output language

        Returns:
            Comparison analysis
        """
        system_prompt = f"""You are an expert analyst comparing content from multiple sources.
Provide balanced, objective comparisons in {language}."""

        videos_text = ""
        for i, t in enumerate(transcripts, 1):
            title = t.get("title", f"Video {i}")
            content = t.get("transcript", "")[:4000]
            videos_text += f"\n### Video {i}: {title}\n{content}\n"

        prompt = f"""Compare the following videos on the same topic:

{videos_text}

Provide a comprehensive comparison:

## 视频概览
| 视频 | 主要观点 | 目标受众 | 风格 |
|------|----------|----------|------|
| ... | ... | ... | ... |

## 观点对比

### 共同观点
- [Points all videos agree on]

### 不同观点
- [Where videos differ and why]

### 独特见解
- Video 1: [Unique insights]
- Video 2: [Unique insights]
- ...

## 深度分析

### 最全面的讲解
[Which video covers the topic most thoroughly]

### 最适合初学者
[Which video is best for beginners]

### 最适合进阶学习
[Which video is best for advanced learners]

## 综合推荐
[Overall recommendation based on different needs]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=4096)

    def compare_by_urls(
        self,
        video_urls: List[str],
        language: str = "中文",
    ) -> str:
        """Compare videos by their URLs"""
        transcripts = []

        for url in video_urls:
            try:
                # Extract video ID from URL
                video_id = self._extract_video_id(url)
                if video_id:
                    extractor = TranscriptExtractor(video_id)
                    extractor.extract()
                    transcripts.append({
                        "title": url,
                        "transcript": extractor.get_plain_text(),
                    })
            except Exception as e:
                transcripts.append({
                    "title": url,
                    "transcript": f"[Error extracting transcript: {e}]",
                })

        return self.compare_videos(transcripts, language)

    def _extract_video_id(self, url: str) -> Optional[str]:
        """Extract video ID from YouTube URL"""
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

    def find_contradictions(
        self,
        transcripts: List[Dict],
        language: str = "中文",
    ) -> str:
        """Find contradictions between videos"""
        system_prompt = f"Identify contradictions and conflicting information in {language}."

        videos_text = ""
        for i, t in enumerate(transcripts, 1):
            title = t.get("title", f"Video {i}")
            content = t.get("transcript", "")[:3000]
            videos_text += f"\n### Video {i}: {title}\n{content}\n"

        prompt = f"""Analyze these videos for contradictions and conflicting claims:

{videos_text}

Identify:

## 矛盾点分析

### 直接矛盾
[Claims that directly contradict each other]

### 事实差异
[Factual differences between videos]

### 观点冲突
[Differing opinions on same topic]

### 信息缺失
[Important information missing from some videos]

## 可信度评估
[Assessment of which claims seem more credible and why]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=3000)

    def merge_insights(
        self,
        transcripts: List[Dict],
        language: str = "中文",
    ) -> str:
        """Merge unique insights from all videos"""
        system_prompt = f"Synthesize information from multiple sources in {language}."

        videos_text = ""
        for i, t in enumerate(transcripts, 1):
            title = t.get("title", f"Video {i}")
            content = t.get("transcript", "")[:3000]
            videos_text += f"\n### Video {i}: {title}\n{content}\n"

        prompt = f"""Merge and synthesize insights from these videos into a comprehensive summary:

{videos_text}

Create a unified summary that:

## 综合摘要
[Merged summary of all key points]

## 核心知识点
[All unique insights combined]

## 最佳实践
[Best practices mentioned across videos]

## 完整学习路径
[Suggested learning path based on all videos]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=3500)

    def generate_debate(
        self,
        transcripts: List[Dict],
        language: str = "中文",
    ) -> str:
        """Generate a debate format comparing viewpoints"""
        system_prompt = f"Create engaging debate-style comparisons in {language}."

        videos_text = ""
        for i, t in enumerate(transcripts, 1):
            title = t.get("title", f"Video {i}")
            content = t.get("transcript", "")[:3000]
            videos_text += f"\n### Video {i}: {title}\n{content}\n"

        prompt = f"""Create a debate-style comparison of these videos:

{videos_text}

Format as a debate:

## 辩论主题
[Main topic being debated]

## 各方立场

### 正方观点 (Video 1)
- 主要论点: ...
- 支持证据: ...

### 反方观点 (Video 2)
- 主要论点: ...
- 支持证据: ...

## 关键交锋点
[Key points of disagreement]

## 裁判点评
[Balanced analysis of both sides]

## 结论
[What viewers should take away]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=3000)
