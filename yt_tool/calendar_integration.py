"""
Calendar Integration - Extract dates and events for calendar
日历集成 - 将视频中提到的日期、事件自动添加到日历
"""

import re
from typing import Dict, List, Optional
from datetime import datetime
from .ai_client import get_ai_client


class CalendarIntegration:
    """Extract and format calendar events from video"""

    def __init__(self, provider: str = None):
        self.ai = get_ai_client(provider)

    def extract_events(self, transcript: str, language: str = "中文") -> str:
        """Extract calendar events from video"""
        prompt = f"""从视频内容中提取可以添加到日历的事件：

{self._truncate_text(transcript)}

请提取：
## 提到的日期/事件

### 事件 1
- **事件名称**:
- **日期/时间**: [如提到]
- **类型**: [会议/截止日期/活动/提醒]
- **详情**:
- **重复**: [一次性/每日/每周/每月]

### 事件 2
...

## 推荐日历提醒
[基于内容建议的学习/复习提醒]

## iCal格式
```ics
BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
SUMMARY:事件名称
DTSTART:20240101T090000
DTEND:20240101T100000
DESCRIPTION:详情
END:VEVENT
END:VCALENDAR
```

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是时间管理专家。", temperature=0.4)

    def create_study_schedule(self, transcript: str, duration_days: int = 7, language: str = "中文") -> str:
        """Create study schedule based on content"""
        prompt = f"""基于视频内容创建{duration_days}天学习计划：

{self._truncate_text(transcript)}

请生成：
## {duration_days}天学习计划

### Day 1 - [主题]
- 09:00 学习任务1
- 14:00 复习任务
- 19:00 练习任务

### Day 2 - [主题]
...

## Google Calendar导入格式
```csv
Subject,Start Date,Start Time,End Date,End Time,Description
"任务1","2024/01/01","09:00","2024/01/01","10:00","描述"
...
```

## 提醒设置建议

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是学习规划师。", temperature=0.5)

    def extract_deadlines(self, transcript: str, language: str = "中文") -> str:
        """Extract deadlines and important dates"""
        prompt = f"""从内容中提取截止日期和重要时间点：

{self._truncate_text(transcript)}

请提取：
## 截止日期
| 事项 | 日期 | 紧急程度 | 备注 |
|------|------|----------|------|

## 重要时间节点
## 周期性事件
## 提醒建议

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是时间管理顾问。", temperature=0.4)

    def generate_reminders(self, transcript: str, video_title: str, language: str = "中文") -> str:
        """Generate reminder suggestions"""
        prompt = f"""基于视频内容生成提醒建议：

**视频**: {video_title}
**内容**: {self._truncate_text(transcript, 10000)}

请生成：
## 推荐提醒

### 立即提醒
- [ ] 行动项1

### 明天提醒
- [ ] 复习要点

### 一周后提醒
- [ ] 检查掌握程度

### 一月后提醒
- [ ] 间隔复习

## 苹果提醒事项格式
## Todoist格式
## Things格式

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是提醒系统专家。", temperature=0.5)

    def format_ical(self, events: List[Dict]) -> str:
        """Format events to iCal format"""
        ical = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//YT-Tool//EN"]

        for event in events:
            ical.append("BEGIN:VEVENT")
            ical.append(f"SUMMARY:{event.get('title', 'Event')}")
            if 'start' in event:
                ical.append(f"DTSTART:{event['start']}")
            if 'end' in event:
                ical.append(f"DTEND:{event['end']}")
            if 'description' in event:
                ical.append(f"DESCRIPTION:{event['description']}")
            ical.append("END:VEVENT")

        ical.append("END:VCALENDAR")
        return "\n".join(ical)

    def _truncate_text(self, text: str, max_chars: int = 15000) -> str:
        if len(text) <= max_chars:
            return text
        return text[:max_chars] + "..."
