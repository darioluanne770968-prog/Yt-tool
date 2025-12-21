"""
Logseq Sync - Export notes to Logseq format
Logseq同步 - 与Logseq笔记软件集成
"""

import os
from typing import Dict, List, Optional
from .ai_client import get_ai_client


class LogseqSync:
    """Logseq integration for video notes"""

    def __init__(self, graph_path: str = None, provider: str = None):
        self.graph_path = graph_path
        self.ai = get_ai_client(provider)

    def generate_page(self, transcript: str, title: str, metadata: Dict = None, language: str = "中文") -> str:
        """Generate Logseq page format"""
        metadata = metadata or {}

        prompt = f"""将视频内容转换为Logseq页面格式：

**标题**: {title}
**内容**: {self._truncate_text(transcript)}

请生成Logseq格式的笔记（使用大纲/bullet格式）：

title:: {title}
tags:: 视频笔记
source:: YouTube
date:: [[{metadata.get('date', '日期')}]]
url:: {metadata.get('url', '')}

- # 摘要
  - [简短摘要]
- # 核心要点
  - [[概念1]]
    - 解释
  - [[概念2]]
    - 解释
- # 详细笔记
  - 要点1
    - 细节
    - 细节
  - 要点2
    - 细节
- # 问题与思考
  - TODO 问题1
  - TODO 问题2
- # 相关页面
  - [[相关主题1]]
  - [[相关主题2]]

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是Logseq笔记专家。", temperature=0.5)

    def generate_journal_entry(self, transcript: str, title: str, language: str = "中文") -> str:
        """Generate journal entry"""
        prompt = f"""生成Logseq日志条目：

**视频**: {title}
**内容**: {self._truncate_text(transcript, 5000)}

请生成（大纲格式）：

- 📺 观看视频 [[{title}]]
  - 主要收获
    -
  - 金句记录
    - >
  - TODO 后续行动
  - 相关页面: [[概念1]], [[概念2]]

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是日志整理助手。", temperature=0.5)

    def create_flashcards(self, transcript: str, count: int = 10, language: str = "中文") -> str:
        """Create Logseq flashcards"""
        prompt = f"""创建Logseq闪卡：

{self._truncate_text(transcript)}

请生成{count}张闪卡（使用Logseq闪卡语法）：

- 问题1 #card
  - 答案1
- 问题2 #card
  - 答案2
...

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是学习卡片专家。", temperature=0.5)

    def generate_queries(self, topic: str, language: str = "中文") -> str:
        """Generate Logseq queries"""
        prompt = f"""为主题生成Logseq查询：

**主题**: {topic}

请生成有用的查询：

## 相关页面查询
#+BEGIN_QUERY
{{:title "相关 {topic}"
 :query [:find (pull ?b [*])
         :where
         [?b :block/refs ?r]
         [?r :block/name "{topic.lower()}"]]}}
#+END_QUERY

## 待办事项查询
## 最近修改查询
## 标签查询

用{language}说明每个查询的用途。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是Logseq高级用户。", temperature=0.5)

    def export_page(self, content: str, filename: str) -> bool:
        """Export page to graph"""
        if not self.graph_path:
            return False

        pages_path = os.path.join(self.graph_path, "pages")
        os.makedirs(pages_path, exist_ok=True)

        filepath = os.path.join(pages_path, f"{filename}.md")
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception:
            return False

    def _truncate_text(self, text: str, max_chars: int = 15000) -> str:
        if len(text) <= max_chars:
            return text
        return text[:max_chars] + "..."
