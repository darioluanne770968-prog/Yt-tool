"""
Exam Prep - Exam preparation assistant based on video content
考试备考助手 - 针对教育类视频，生成考试要点、易错题、考前速记卡片
"""

from typing import Dict, List, Optional
from .ai_client import get_ai_client


EXAM_TYPES = {
    "multiple_choice": {"name": "选择题", "description": "单选或多选题"},
    "true_false": {"name": "判断题", "description": "判断正误"},
    "fill_blank": {"name": "填空题", "description": "填写关键词"},
    "short_answer": {"name": "简答题", "description": "简要回答"},
    "essay": {"name": "论述题", "description": "详细论述"},
}


class ExamPrep:
    """Exam preparation assistant"""

    def __init__(self, provider: str = None):
        self.ai = get_ai_client(provider)

    def generate_exam_points(self, transcript: str, subject: str = "general", language: str = "中文") -> str:
        """Generate key exam points from video content"""
        prompt = f"""从以下教育视频内容中提取考试要点：

**学科**: {subject}
**视频内容**: {self._truncate_text(transcript)}

请生成：
## 核心概念（定义+关键特征）
## 重要知识点（按重要性⭐排序）
## 公式/定理/规律
## 易错点
## 记忆口诀
## 真题预测

请用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是经验丰富的考试辅导老师。", temperature=0.5)

    def generate_practice_exam(self, transcript: str, question_count: int = 20, difficulty: str = "medium", language: str = "中文") -> str:
        """Generate practice exam"""
        prompt = f"""基于以下内容生成{question_count}题模拟考试（难度：{difficulty}）：

{self._truncate_text(transcript)}

请生成完整试卷（选择题、判断题、简答题）和参考答案。用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是专业的命题老师。", temperature=0.6)

    def generate_flashcards(self, transcript: str, count: int = 20, language: str = "中文") -> str:
        """Generate exam flashcards"""
        prompt = f"""从以下内容生成{count}张考前速记卡片：

{self._truncate_text(transcript)}

每张卡片包含：正面（问题）、背面（答案）、记忆提示、重要程度。
最后提供Anki导入格式。用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是记忆方法专家。", temperature=0.5)

    def identify_common_mistakes(self, transcript: str, language: str = "中文") -> str:
        """Identify common mistakes"""
        prompt = f"""分析以下内容的易错点：

{self._truncate_text(transcript)}

请分析：概念混淆、常见错误、陷阱题型、边界条件、答题技巧。用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是教学经验丰富的老师。", temperature=0.5)

    def generate_quick_review(self, transcript: str, time_limit: int = 30, language: str = "中文") -> str:
        """Generate quick review guide"""
        prompt = f"""生成{time_limit}分钟考前速览材料：

{self._truncate_text(transcript)}

按时间分配：核心框架、必背要点、关键公式、易错提醒、典型例题、记忆口诀。用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是高效复习专家。", temperature=0.5)

    def _truncate_text(self, text: str, max_chars: int = 20000) -> str:
        if len(text) <= max_chars:
            return text
        return text[:max_chars] + "\n[已截断...]"

    @staticmethod
    def get_exam_types() -> Dict:
        return EXAM_TYPES
