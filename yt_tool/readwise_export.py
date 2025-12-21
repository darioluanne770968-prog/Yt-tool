"""
Readwise Export - Export highlights to Readwise
Readwise导出 - 将视频金句导出到Readwise进行间隔复习
"""

import json
from typing import Dict, List, Optional
from .ai_client import get_ai_client


class ReadwiseExport:
    """Export video highlights to Readwise"""

    def __init__(self, api_token: str = None, provider: str = None):
        self.api_token = api_token
        self.ai = get_ai_client(provider)

    def extract_highlights(self, transcript: str, title: str, count: int = 20, language: str = "中文") -> str:
        """Extract highlights for Readwise"""
        prompt = f"""从视频中提取适合Readwise的高亮：

**视频标题**: {title}
**内容**: {self._truncate_text(transcript)}

请提取{count}条高亮：

## Readwise高亮

### 高亮 1
- **内容**: "[值得记住的句子]"
- **笔记**: [你的思考]
- **标签**: #标签1, #标签2
- **位置**: [大约时间]

### 高亮 2
...

## CSV导出格式
```csv
Highlight,Note,Title,Author,URL,Tags
"内容1","笔记1","{title}","作者","URL","标签"
...
```

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是高亮提取专家。", temperature=0.5)

    def format_for_api(self, transcript: str, title: str, author: str = "", url: str = "", language: str = "中文") -> Dict:
        """Format highlights for Readwise API"""
        prompt = f"""提取高亮并格式化为JSON：

**标题**: {title}
**作者**: {author}
**内容**: {self._truncate_text(transcript)}

请提取10-15条高亮，输出JSON格式：
```json
{{
  "highlights": [
    {{
      "text": "高亮内容",
      "note": "个人笔记",
      "location": 1,
      "location_type": "time"
    }}
  ]
}}
```

只输出JSON，用{language}写笔记。"""

        response = self.ai.chat(prompt=prompt, system_prompt="你是数据格式专家。", temperature=0.4)
        return response

    def generate_review_material(self, highlights: List[str], language: str = "中文") -> str:
        """Generate review material from highlights"""
        highlights_text = "\n".join([f"- {h}" for h in highlights])

        prompt = f"""基于以下高亮生成复习材料：

{highlights_text}

请生成：
## 间隔复习卡片
[每条高亮生成问答卡片]

## 主题总结
## 关联思考
## 应用场景

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是学习方法专家。", temperature=0.5)

    def create_book_entry(self, transcript: str, title: str, metadata: Dict = None, language: str = "中文") -> str:
        """Create a book-like entry for Readwise"""
        metadata = metadata or {}

        prompt = f"""将视频内容整理为书籍条目格式：

**标题**: {title}
**作者**: {metadata.get('channel', '未知')}
**内容**: {self._truncate_text(transcript)}

请生成：
## 书籍信息
- 标题: {title}
- 作者:
- 来源: YouTube
- 分类:

## 核心高亮 (10-15条)
每条包含：
1. 原文
2. 我的笔记
3. 章节/位置

## 书籍总结
## 阅读笔记
## 行动要点

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是阅读笔记专家。", temperature=0.5)

    def _truncate_text(self, text: str, max_chars: int = 15000) -> str:
        if len(text) <= max_chars:
            return text
        return text[:max_chars] + "..."
