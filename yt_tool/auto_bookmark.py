"""
Auto Bookmark - Automatically identify key moments in video
智能书签 - 自动识别视频中的"精彩时刻"、"重点"、"转折点"并生成书签
"""

from typing import Dict, List, Optional
from .ai_client import get_ai_client


BOOKMARK_TYPES = {
    "highlight": {"name": "精彩时刻", "emoji": "⭐"},
    "key_point": {"name": "重点内容", "emoji": "📌"},
    "turning_point": {"name": "转折点", "emoji": "🔄"},
    "example": {"name": "案例/例子", "emoji": "💡"},
    "quote": {"name": "金句", "emoji": "💬"},
    "action": {"name": "行动建议", "emoji": "✅"},
    "warning": {"name": "注意事项", "emoji": "⚠️"},
    "summary": {"name": "总结", "emoji": "📋"},
}


class AutoBookmark:
    """Automatic video bookmark generator"""

    def __init__(self, provider: str = None):
        self.ai = get_ai_client(provider)

    def generate_bookmarks(self, transcript: str, include_timestamps: bool = True, language: str = "中文") -> str:
        """Generate smart bookmarks for video"""
        prompt = f"""为以下视频内容生成智能书签：

{self._truncate_text(transcript)}

请生成书签：
## 智能书签

### ⭐ 精彩时刻
| 时间点 | 内容描述 | 重要程度 |
|--------|----------|----------|

### 📌 重点内容
| 时间点 | 内容描述 | 重要程度 |
|--------|----------|----------|

### 🔄 转折点
### 💡 案例/例子
### 💬 金句
### ✅ 行动建议

## 书签索引
[按时间顺序排列的完整书签列表]

## YouTube时间戳格式
```
0:00 开场
X:XX [书签1]
X:XX [书签2]
...
```

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是视频内容分析师。", temperature=0.5)

    def extract_highlights(self, transcript: str, count: int = 10, language: str = "中文") -> str:
        """Extract top highlights"""
        prompt = f"""提取视频的{count}个最精彩时刻：

{self._truncate_text(transcript)}

请提取：
## Top {count} 精彩时刻

### 1. [精彩时刻标题]
- **时间点**: [估计时间]
- **内容**: [具体内容]
- **精彩原因**: [为什么精彩]

### 2. [精彩时刻标题]
...

## 剪辑建议
[适合作为短视频的片段]

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是视频剪辑顾问。", temperature=0.6)

    def identify_chapters(self, transcript: str, language: str = "中文") -> str:
        """Identify logical chapters"""
        prompt = f"""为视频识别逻辑章节：

{self._truncate_text(transcript)}

请识别：
## 视频章节

### 第1章: [章节标题]
- 时间范围: X:XX - X:XX
- 主要内容: [概述]
- 关键点: [列出]

### 第2章: [章节标题]
...

## YouTube章节格式
```
0:00 章节1
X:XX 章节2
...
```

## 章节关系图

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是内容结构分析师。", temperature=0.5)

    def find_quotable_moments(self, transcript: str, count: int = 10, language: str = "中文") -> str:
        """Find quotable moments"""
        prompt = f"""找出视频中{count}个值得引用的金句：

{self._truncate_text(transcript)}

请找出：
## 金句集锦

### 金句 1
> "[金句内容]"
- 时间点:
- 上下文:
- 适用场景:

### 金句 2
...

## 社交媒体引用版
[适合分享的格式]

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是金句提取专家。", temperature=0.6)

    def create_navigation_guide(self, transcript: str, language: str = "中文") -> str:
        """Create video navigation guide"""
        prompt = f"""创建视频导航指南：

{self._truncate_text(transcript)}

请创建：
## 视频导航指南

### 快速跳转
- 想了解[主题1]? 跳转到 X:XX
- 想看[主题2]? 跳转到 X:XX
...

### 按兴趣导航
**新手推荐路径**:
**进阶路径**:
**快速回顾**:

### 避免章节
[可跳过的部分及原因]

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是用户体验专家。", temperature=0.5)

    def _truncate_text(self, text: str, max_chars: int = 20000) -> str:
        if len(text) <= max_chars:
            return text
        return text[:max_chars] + "\n[已截断...]"

    @staticmethod
    def get_bookmark_types() -> Dict:
        return BOOKMARK_TYPES
