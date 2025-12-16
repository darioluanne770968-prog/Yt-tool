"""
Study guide generation from video content
"""

from typing import Dict, Optional
from .ai_client import get_ai_client


class StudyGuideGenerator:
    """Generate comprehensive study guides from video transcripts"""

    def __init__(self):
        self.ai_client = get_ai_client()

    def generate_study_guide(
        self,
        transcript: str,
        title: str = "",
        language: str = "中文",
        include_exercises: bool = True,
    ) -> str:
        """
        Generate a comprehensive study guide

        Args:
            transcript: Video transcript text
            title: Video title
            language: Output language
            include_exercises: Whether to include practice exercises

        Returns:
            Formatted study guide
        """
        system_prompt = f"""You are an expert educator creating study materials.
Generate comprehensive, well-structured study guides in {language}.
Focus on learning objectives, key concepts, and practical application."""

        exercises_section = """
## 练习题
- 提供3-5个练习题
- 包含答案和解析
""" if include_exercises else ""

        prompt = f"""Create a comprehensive study guide based on this video transcript.

Video Title: {title}

Include the following sections:
## 学习目标
- 列出3-5个具体的学习目标

## 核心概念
- 详细解释每个核心概念
- 使用简单易懂的语言

## 知识框架
- 构建知识结构图
- 展示概念之间的关系

## 重点笔记
- 提取最重要的信息点
- 使用要点格式

## 学习建议
- 如何有效学习这些内容
- 推荐的学习步骤

## 延伸阅读
- 相关主题建议
- 进阶学习方向
{exercises_section}

Transcript:
{transcript[:12000]}
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=4096)

    def generate_learning_objectives(
        self,
        transcript: str,
        language: str = "中文",
    ) -> str:
        """Extract learning objectives from video"""
        system_prompt = f"Extract clear, actionable learning objectives in {language}."

        prompt = f"""Based on this video transcript, identify 5-7 specific learning objectives.

Format each objective as:
- [ ] [Objective] - [Brief description of what learner will be able to do]

Transcript:
{transcript[:8000]}
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=1024)

    def generate_outline(
        self,
        transcript: str,
        language: str = "中文",
    ) -> str:
        """Generate a structured outline"""
        system_prompt = f"Create well-organized outlines in {language}."

        prompt = f"""Create a detailed outline of this video content.

Use this format:
I. Main Topic
   A. Subtopic
      1. Detail
      2. Detail
   B. Subtopic
II. Main Topic
   ...

Transcript:
{transcript[:10000]}
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=2048)

    def generate_summary_notes(
        self,
        transcript: str,
        language: str = "中文",
    ) -> str:
        """Generate Cornell-style notes"""
        system_prompt = f"Create Cornell-style study notes in {language}."

        prompt = f"""Create Cornell-style notes from this video transcript.

Format:
┌─────────────────┬────────────────────────────────────┐
│   关键词/问题    │              笔记内容               │
├─────────────────┼────────────────────────────────────┤
│                 │                                    │
│                 │                                    │
└─────────────────┴────────────────────────────────────┘
                    总结
                    ────
                    [Summary section]

Transcript:
{transcript[:10000]}
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=3000)
