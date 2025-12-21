"""
Language Learning - Extract language learning materials from video
语言学习助手 - 从视频中提取语言学习材料（生词、语法、例句、练习）
"""

from typing import Dict, List, Optional
from .ai_client import get_ai_client


LANGUAGE_LEVELS = {
    "beginner": {"name": "初级", "cefr": "A1-A2"},
    "intermediate": {"name": "中级", "cefr": "B1-B2"},
    "advanced": {"name": "高级", "cefr": "C1-C2"},
}


class LanguageLearning:
    """Language learning material extractor"""

    def __init__(self, provider: str = None):
        self.ai = get_ai_client(provider)

    def extract_vocabulary(self, transcript: str, target_language: str = "English", level: str = "intermediate", language: str = "中文") -> str:
        """Extract vocabulary list from video"""
        prompt = f"""从以下{target_language}视频内容提取词汇表：

{self._truncate_text(transcript)}

目标水平: {LANGUAGE_LEVELS.get(level, LANGUAGE_LEVELS['intermediate'])['name']}

请生成：
## 核心词汇（必学）
| 单词 | 音标 | 词性 | 释义 | 例句 | 记忆技巧 |
|------|------|------|------|------|----------|

## 进阶词汇
## 习语/固定搭配
## 词汇练习

用{language}解释，保留原文单词。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是专业的语言教师。", temperature=0.5)

    def analyze_grammar(self, transcript: str, target_language: str = "English", language: str = "中文") -> str:
        """Analyze grammar points in video"""
        prompt = f"""分析以下{target_language}视频的语法点：

{self._truncate_text(transcript)}

请分析：
## 语法点列表
### 语法点1
- **语法结构**:
- **使用场景**:
- **原文例句**:
- **更多例句**:
- **常见错误**:
- **练习题**:

## 语法总结表
## 语法练习

用{language}解释。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是语法分析专家。", temperature=0.5)

    def generate_listening_exercise(self, transcript: str, target_language: str = "English", language: str = "中文") -> str:
        """Generate listening comprehension exercises"""
        prompt = f"""基于视频内容生成听力练习：

{self._truncate_text(transcript)}

请生成：
## 听力填空
[选取关键句子，挖空让学生填写]
1. The speaker mentioned that ___ is important for ___.
...

## 听力选择题
## 听力判断题
## 听力问答题
## 答案及听力技巧

用{language}出题，原文保留{target_language}。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是听力教学专家。", temperature=0.6)

    def generate_speaking_practice(self, transcript: str, target_language: str = "English", language: str = "中文") -> str:
        """Generate speaking practice materials"""
        prompt = f"""基于视频内容生成口语练习：

{self._truncate_text(transcript)}

请生成：
## 跟读练习
[选取适合跟读的句子，标注重音和语调]

## 口语表达句型
| 场景 | 句型 | 例句 | 替换练习 |
|------|------|------|----------|

## 话题讨论
[基于视频内容的讨论话题]

## 角色扮演
## 发音要点

用{language}说明，练习内容用{target_language}。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是口语教练。", temperature=0.6)

    def create_study_materials(self, transcript: str, target_language: str = "English", level: str = "intermediate", language: str = "中文") -> str:
        """Create comprehensive study materials"""
        prompt = f"""创建完整的{target_language}学习材料：

{self._truncate_text(transcript)}

水平: {level}

请生成：
## 学习目标
## 词汇表（20个核心词）
## 语法点（3-5个）
## 重点句型
## 听力练习
## 口语练习
## 阅读理解
## 写作任务
## 文化知识点
## 学习建议

用{language}编写。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是语言课程设计师。", temperature=0.5)

    def generate_translation_exercise(self, transcript: str, target_language: str = "English", language: str = "中文") -> str:
        """Generate translation exercises"""
        prompt = f"""基于视频内容生成翻译练习：

{self._truncate_text(transcript)}

请生成：
## {target_language} → {language} 翻译
1. [原句]
   参考译文：

## {language} → {target_language} 翻译
1. [中文句子]
   参考译文：

## 翻译技巧
## 常见翻译错误

"""

        return self.ai.chat(prompt=prompt, system_prompt="你是翻译教学专家。", temperature=0.5)

    def _truncate_text(self, text: str, max_chars: int = 20000) -> str:
        if len(text) <= max_chars:
            return text
        return text[:max_chars] + "\n[已截断...]"

    @staticmethod
    def get_language_levels() -> Dict:
        return LANGUAGE_LEVELS
