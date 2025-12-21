"""
Meeting Notes - Generate professional meeting minutes from video
会议纪要生成 - 针对会议录像/直播回放，生成专业会议纪要
"""

from typing import Dict, List, Optional
from .ai_client import get_ai_client


class MeetingNotes:
    """Professional meeting notes generator"""

    def __init__(self, provider: str = None):
        self.ai = get_ai_client(provider)

    def generate_minutes(self, transcript: str, meeting_info: Dict = None, language: str = "中文") -> str:
        """Generate formal meeting minutes"""
        info = meeting_info or {}

        prompt = f"""将以下会议录像内容整理成正式会议纪要：

**会议信息**:
- 主题: {info.get('topic', '待识别')}
- 日期: {info.get('date', '待填写')}
- 参会人: {info.get('attendees', '待识别')}

**会议内容**: {self._truncate_text(transcript)}

请生成会议纪要：

# 会议纪要

## 基本信息
- **会议主题**:
- **会议时间**:
- **会议地点**:
- **主持人**:
- **记录人**:
- **参会人员**:

## 会议议程

## 讨论要点
### 议题1
- 讨论内容：
- 各方观点：
- 结论：

## 决议事项
| 序号 | 决议内容 | 责任人 | 完成时间 |
|------|----------|--------|----------|

## 待办事项 (Action Items)
- [ ] 事项1 - 负责人 - 截止日期
- [ ] 事项2 - 负责人 - 截止日期

## 下次会议安排

## 附注

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是专业的会议记录员。", temperature=0.4)

    def extract_action_items(self, transcript: str, language: str = "中文") -> str:
        """Extract action items from meeting"""
        prompt = f"""从会议内容中提取待办事项：

{self._truncate_text(transcript)}

请提取：
## 行动项清单

| 序号 | 待办事项 | 负责人 | 优先级 | 截止时间 | 依赖项 |
|------|----------|--------|--------|----------|--------|

## 按负责人分组
## 按优先级排序
## 关键路径分析

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是项目管理专家。", temperature=0.4)

    def identify_decisions(self, transcript: str, language: str = "中文") -> str:
        """Identify key decisions made"""
        prompt = f"""从会议内容中识别决策要点：

{self._truncate_text(transcript)}

请识别：
## 正式决议
[已通过的决策]

## 待定事项
[需要进一步讨论的]

## 否决事项
[已否决的提议]

## 决策依据
## 后续影响

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是决策分析师。", temperature=0.4)

    def generate_summary_email(self, transcript: str, recipients: str = "team", language: str = "中文") -> str:
        """Generate summary email"""
        prompt = f"""将会议内容整理成会后邮件：

{self._truncate_text(transcript)}

**收件人**: {recipients}

请生成：

---
**主题**: [会议名称] 会议纪要

各位好，

以下是本次会议的要点总结：

**主要讨论内容**:
1.
2.
3.

**决议事项**:
-

**待办事项**:
-

**下次会议**:

如有问题，请随时沟通。

---

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是商务写作专家。", temperature=0.5)

    def analyze_participation(self, transcript: str, language: str = "中文") -> str:
        """Analyze meeting participation"""
        prompt = f"""分析会议参与情况：

{self._truncate_text(transcript)}

请分析：
## 发言统计
| 参会者 | 发言次数 | 发言时长占比 | 主要观点 |
|--------|----------|--------------|----------|

## 互动分析
## 会议效率评估
## 改进建议

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是会议效能顾问。", temperature=0.5)

    def _truncate_text(self, text: str, max_chars: int = 20000) -> str:
        if len(text) <= max_chars:
            return text
        return text[:max_chars] + "\n[已截断...]"
