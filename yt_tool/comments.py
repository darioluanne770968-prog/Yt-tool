"""
YouTube comments extraction and analysis
"""

from typing import Optional
from .ai_client import get_ai_client


def get_video_comments(video_id: str, max_comments: int = 100) -> list[dict]:
    """
    Get comments from a YouTube video using yt-dlp

    Args:
        video_id: YouTube video ID
        max_comments: Maximum number of comments to retrieve

    Returns:
        List of comment dictionaries
    """
    try:
        import yt_dlp
    except ImportError:
        raise ImportError("yt-dlp is required. Install with: pip install yt-dlp")

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "getcomments": True,
        "extractor_args": {
            "youtube": {
                "max_comments": [str(max_comments)],
                "comment_sort": ["top"],
            }
        },
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(
                f"https://www.youtube.com/watch?v={video_id}",
                download=False,
            )

            comments = info.get("comments", [])

            return [
                {
                    "text": c.get("text", ""),
                    "author": c.get("author", ""),
                    "likes": c.get("like_count", 0),
                    "timestamp": c.get("timestamp", 0),
                    "is_reply": c.get("parent", "root") != "root",
                }
                for c in comments
                if c.get("text")
            ]

    except Exception as e:
        raise Exception(f"Failed to get comments: {str(e)}")


COMMENTS_ANALYSIS_SYSTEM_PROMPT = """你是一个专业的社交媒体分析师。你的任务是分析YouTube视频的评论内容，提取有价值的信息。

要求：
1. 识别评论中的主要话题和情感
2. 找出有价值的反馈和建议
3. 分析观众的反应和态度
4. 使用用户指定的语言输出"""


COMMENTS_ANALYSIS_PROMPT_TEMPLATE = """请分析以下YouTube视频评论，总结观众的反馈和看法。

评论内容：
{comments}

请提供：
1. **整体情感** - 评论的整体态度是正面、负面还是中立
2. **主要话题** - 评论中讨论最多的话题（3-5个）
3. **观众反馈** - 观众对视频内容的主要反馈
4. **有价值的建议** - 评论中提出的有价值的建议或问题
5. **热门观点** - 获赞最多或最有代表性的观点
6. **争议话题** - 如有争议性讨论，简要说明

请用{language}输出。"""


class CommentsAnalyzer:
    """Analyze YouTube video comments"""

    def __init__(self, provider: str = None):
        """
        Initialize comments analyzer

        Args:
            provider: AI provider ('openai' or 'anthropic')
        """
        self.ai = get_ai_client(provider)

    def get_comments(self, video_id: str, max_comments: int = 100) -> list[dict]:
        """
        Get comments from a video

        Args:
            video_id: YouTube video ID
            max_comments: Maximum comments to retrieve

        Returns:
            List of comments
        """
        return get_video_comments(video_id, max_comments)

    def analyze(
        self,
        comments: list[dict],
        language: str = "中文",
    ) -> str:
        """
        Analyze comments with AI

        Args:
            comments: List of comment dictionaries
            language: Output language

        Returns:
            Analysis result
        """
        # Format comments for analysis
        formatted_comments = self._format_comments(comments)

        prompt = COMMENTS_ANALYSIS_PROMPT_TEMPLATE.format(
            comments=formatted_comments,
            language=language,
        )

        return self.ai.chat(
            prompt=prompt,
            system_prompt=COMMENTS_ANALYSIS_SYSTEM_PROMPT,
            temperature=0.5,
        )

    def analyze_video(
        self,
        video_id: str,
        max_comments: int = 100,
        language: str = "中文",
    ) -> dict:
        """
        Get and analyze comments for a video

        Args:
            video_id: YouTube video ID
            max_comments: Maximum comments to analyze
            language: Output language

        Returns:
            Dictionary with comments and analysis
        """
        comments = self.get_comments(video_id, max_comments)

        if not comments:
            return {
                "video_id": video_id,
                "comments_count": 0,
                "comments": [],
                "analysis": "No comments found for this video.",
            }

        analysis = self.analyze(comments, language)

        return {
            "video_id": video_id,
            "comments_count": len(comments),
            "comments": comments,
            "analysis": analysis,
        }

    def _format_comments(self, comments: list[dict], max_chars: int = 15000) -> str:
        """Format comments for AI analysis"""
        lines = []
        total_chars = 0

        # Sort by likes
        sorted_comments = sorted(
            comments, key=lambda x: x.get("likes", 0), reverse=True
        )

        for comment in sorted_comments:
            text = comment["text"].strip()
            likes = comment.get("likes", 0)

            line = f"[{likes} likes] {text}"

            if total_chars + len(line) > max_chars:
                break

            lines.append(line)
            total_chars += len(line) + 1

        return "\n".join(lines)

    def get_sentiment_summary(self, comments: list[dict]) -> dict:
        """
        Get quick sentiment summary without AI

        Args:
            comments: List of comments

        Returns:
            Sentiment statistics
        """
        positive_keywords = ["好", "棒", "赞", "喜欢", "支持", "感谢", "great", "good", "love", "amazing", "awesome", "helpful"]
        negative_keywords = ["差", "烂", "不好", "讨厌", "失望", "bad", "hate", "terrible", "boring", "waste"]

        positive_count = 0
        negative_count = 0
        neutral_count = 0

        for comment in comments:
            text = comment["text"].lower()

            has_positive = any(kw in text for kw in positive_keywords)
            has_negative = any(kw in text for kw in negative_keywords)

            if has_positive and not has_negative:
                positive_count += 1
            elif has_negative and not has_positive:
                negative_count += 1
            else:
                neutral_count += 1

        total = len(comments)
        return {
            "total_comments": total,
            "positive": positive_count,
            "negative": negative_count,
            "neutral": neutral_count,
            "positive_ratio": round(positive_count / total * 100, 1) if total else 0,
            "negative_ratio": round(negative_count / total * 100, 1) if total else 0,
        }

    def get_top_comments(
        self, comments: list[dict], limit: int = 10
    ) -> list[dict]:
        """
        Get top comments by likes

        Args:
            comments: List of comments
            limit: Maximum comments to return

        Returns:
            Top comments sorted by likes
        """
        sorted_comments = sorted(
            comments, key=lambda x: x.get("likes", 0), reverse=True
        )
        return sorted_comments[:limit]
