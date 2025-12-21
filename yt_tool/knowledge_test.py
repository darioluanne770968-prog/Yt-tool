"""
Knowledge Test - Test understanding level after watching video
知识掌握度测试 - 看完视频后测试理解程度，生成个性化的薄弱点报告
"""

from typing import Dict, List, Optional
from .ai_client import get_ai_client


class KnowledgeTest:
    """Knowledge assessment and gap analysis"""

    def __init__(self, provider: str = None):
        self.ai = get_ai_client(provider)
        self.test_results: List[Dict] = []

    def generate_assessment(self, transcript: str, difficulty: str = "adaptive", language: str = "中文") -> str:
        """Generate knowledge assessment questions"""
        prompt = f"""基于以下视频内容生成知识掌握度测试：

{self._truncate_text(transcript)}

请生成：
## 基础理解题（3题）- 测试基本概念
## 应用分析题（3题）- 测试应用能力
## 综合思考题（2题）- 测试深度理解
## 创新拓展题（2题）- 测试迁移能力

每题标注：考察点、难度、预期答案要点。用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是教育评估专家。", temperature=0.6)

    def analyze_answers(self, transcript: str, questions: str, answers: str, language: str = "中文") -> str:
        """Analyze user answers and identify gaps"""
        prompt = f"""分析学生的答案，识别知识盲点：

**视频内容**: {self._truncate_text(transcript, 10000)}
**测试题目**: {questions}
**学生答案**: {answers}

请提供：
## 答案评估（每题得分和评语）
## 掌握程度分析
## 知识盲点识别
## 薄弱环节详解
## 针对性提升建议
## 推荐复习内容

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是学习诊断专家。", temperature=0.5)

    def generate_gap_report(self, transcript: str, test_performance: str, language: str = "中文") -> str:
        """Generate detailed knowledge gap report"""
        prompt = f"""基于测试表现生成知识盲点报告：

**视频内容**: {self._truncate_text(transcript, 10000)}
**测试表现**: {test_performance}

请生成：
## 知识掌握概览（雷达图数据）
## 已掌握知识点（✓）
## 待加强知识点（△）
## 未掌握知识点（✗）
## 知识关联分析
## 个性化学习路径
## 推荐练习题

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是学习分析专家。", temperature=0.5)

    def generate_remedial_content(self, weak_points: List[str], transcript: str, language: str = "中文") -> str:
        """Generate remedial content for weak points"""
        prompt = f"""针对以下薄弱点生成补救学习材料：

**薄弱点**: {', '.join(weak_points)}
**原视频内容**: {self._truncate_text(transcript, 10000)}

请生成：
## 概念重讲（更简单的解释）
## 类比说明
## 具体例子
## 练习题（由易到难）
## 记忆技巧
## 检验问题

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是因材施教的好老师。", temperature=0.6)

    def create_mastery_checklist(self, transcript: str, language: str = "中文") -> str:
        """Create mastery checklist"""
        prompt = f"""基于视频内容创建知识掌握检查清单：

{self._truncate_text(transcript)}

请生成：
## 学习目标清单
每个目标包含：
- [ ] 目标描述
- 检验方法
- 达标标准

## 自测问题
## 掌握程度自评表

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是学习目标设计专家。", temperature=0.5)

    def _truncate_text(self, text: str, max_chars: int = 20000) -> str:
        if len(text) <= max_chars:
            return text
        return text[:max_chars] + "\n[已截断...]"
