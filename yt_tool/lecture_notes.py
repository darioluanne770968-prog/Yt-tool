"""
Lecture Notes - Generate university-style lecture notes
课堂笔记生成 - 生成大学课堂风格的详细笔记，包含板书、例题、作业
"""

from typing import Dict, List, Optional
from .ai_client import get_ai_client


NOTE_STYLES = {
    "cornell": {"name": "康奈尔笔记", "description": "分为笔记栏、提示栏、总结栏"},
    "outline": {"name": "大纲笔记", "description": "层次分明的大纲结构"},
    "mindmap": {"name": "思维导图", "description": "放射状思维导图"},
    "charting": {"name": "图表笔记", "description": "表格对比形式"},
    "sentence": {"name": "句子笔记", "description": "逐句记录要点"},
}


class LectureNotes:
    """University-style lecture notes generator"""

    def __init__(self, provider: str = None):
        self.ai = get_ai_client(provider)

    def generate_lecture_notes(self, transcript: str, subject: str = "general", style: str = "outline", language: str = "中文") -> str:
        """Generate comprehensive lecture notes"""
        prompt = f"""将以下视频内容整理成大学课堂笔记：

**学科**: {subject}
**笔记风格**: {NOTE_STYLES.get(style, NOTE_STYLES['outline'])['name']}
**视频内容**: {self._truncate_text(transcript)}

请生成：
## 课程信息
- 主题：
- 关键词：

## 课堂笔记
[按{style}风格组织内容]

## 板书要点
```
[模拟板书的关键内容]
```

## 重点标注
⭐ 必考点
📝 需要记忆
💡 理解要点

## 课堂例题
[视频中的例题整理]

## 课后作业建议
## 延伸阅读

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是经验丰富的大学教授助教。", temperature=0.5)

    def generate_board_notes(self, transcript: str, language: str = "中文") -> str:
        """Generate simulated board/whiteboard notes"""
        prompt = f"""从视频内容提取板书要点：

{self._truncate_text(transcript)}

请生成模拟板书：
```
┌─────────────────────────────────────┐
│           [主题标题]                 │
├─────────────────────────────────────┤
│ 一、核心概念                         │
│    1.                               │
│    2.                               │
├─────────────────────────────────────┤
│ 二、公式/定理                        │
│                                     │
├─────────────────────────────────────┤
│ 三、例题                            │
│                                     │
├─────────────────────────────────────┤
│ ★ 重点 │ ※ 难点 │ ○ 考点          │
└─────────────────────────────────────┘
```

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你擅长提炼板书要点。", temperature=0.5)

    def generate_examples(self, transcript: str, count: int = 5, language: str = "中文") -> str:
        """Extract and organize examples from lecture"""
        prompt = f"""从视频内容整理例题和练习：

{self._truncate_text(transcript)}

请整理{count}道例题：

### 例题1
**题目**:
**解题思路**:
**详细解答**:
**知识点**:
**举一反三**:

[继续其他例题...]

## 课后练习（附答案）

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是善于出题的老师。", temperature=0.6)

    def generate_formula_sheet(self, transcript: str, language: str = "中文") -> str:
        """Generate formula/theorem reference sheet"""
        prompt = f"""从视频内容提取公式和定理：

{self._truncate_text(transcript)}

请生成公式速查表：
## 公式列表
| 公式名称 | 公式内容 | 适用条件 | 备注 |
|----------|----------|----------|------|

## 定理总结

## 推导过程（重要的）

## 记忆技巧

用{language}输出，数学公式使用LaTeX格式。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是学科专家。", temperature=0.5)

    def generate_homework(self, transcript: str, difficulty: str = "medium", count: int = 10, language: str = "中文") -> str:
        """Generate homework assignments"""
        prompt = f"""基于视频内容布置作业：

{self._truncate_text(transcript)}

难度: {difficulty}
数量: {count}题

请生成：
## 作业题目
[包含基础题、提高题、挑战题]

## 参考答案
## 评分标准
## 常见错误提醒

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是认真负责的老师。", temperature=0.6)

    def _truncate_text(self, text: str, max_chars: int = 20000) -> str:
        if len(text) <= max_chars:
            return text
        return text[:max_chars] + "\n[已截断...]"

    @staticmethod
    def get_note_styles() -> Dict:
        return NOTE_STYLES
