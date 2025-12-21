"""
Obsidian Vault - Export notes to Obsidian with backlinks
Obsidian知识库集成 - 将视频笔记自动整理到Obsidian，创建双向链接和知识图谱
"""

import os
import re
import json
from typing import Dict, List, Optional
from .ai_client import get_ai_client


class ObsidianVault:
    """Obsidian vault integration for video notes"""

    def __init__(self, vault_path: str = None, provider: str = None):
        self.vault_path = vault_path
        self.ai = get_ai_client(provider)

    def generate_note(self, transcript: str, title: str, metadata: Dict = None, language: str = "中文") -> str:
        """Generate Obsidian-formatted note"""
        metadata = metadata or {}

        prompt = f"""将视频内容转换为Obsidian笔记格式：

**标题**: {title}
**内容**: {self._truncate_text(transcript)}

请生成Obsidian笔记：

---
tags: [视频笔记, 待分类]
source: youtube
date: {metadata.get('date', '[[日期]]')}
author: {metadata.get('channel', '未知')}
url: {metadata.get('url', '')}
---

# {title}

## 摘要
[简短摘要]

## 核心要点
- [[概念1]]
- [[概念2]]

## 详细笔记
[使用Obsidian语法：
- [[双向链接]]
- #标签
- > 引用
- ==高亮==
]

## 相关概念
[列出可以链接的概念，使用[[]]语法]

## 问题与思考
- [ ] 待解决的问题

## 参考资料
- [原视频](URL)

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是Obsidian笔记专家。", temperature=0.5)

    def extract_concepts(self, transcript: str, language: str = "中文") -> List[str]:
        """Extract concepts for backlinking"""
        prompt = f"""从以下内容提取可以作为Obsidian双向链接的概念：

{self._truncate_text(transcript)}

请提取：
## 核心概念（必须链接）
- 概念1
- 概念2

## 相关概念（可选链接）
- 概念A
- 概念B

## 人物/组织
## 工具/技术
## 方法/框架

只输出概念列表，每行一个。用{language}输出。"""

        response = self.ai.chat(prompt=prompt, system_prompt="你是知识管理专家。", temperature=0.4)
        return response

    def generate_moc(self, notes: List[Dict], topic: str, language: str = "中文") -> str:
        """Generate Map of Content (MOC)"""
        notes_text = "\n".join([f"- {n.get('title', '未知')}" for n in notes])

        prompt = f"""创建主题索引笔记（MOC）：

**主题**: {topic}
**相关笔记**:
{notes_text}

请生成MOC：

# {topic} MOC

## 概述
[主题简介]

## 核心笔记
- [[笔记1]] - 简介
- [[笔记2]] - 简介

## 子主题
### 子主题1
- [[相关笔记]]

### 子主题2
- [[相关笔记]]

## 学习路径
1. 入门 → [[笔记]]
2. 进阶 → [[笔记]]
3. 精通 → [[笔记]]

## 待探索
- [ ] 话题1
- [ ] 话题2

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是知识组织专家。", temperature=0.5)

    def generate_daily_note_entry(self, transcript: str, title: str, language: str = "中文") -> str:
        """Generate daily note entry"""
        prompt = f"""生成Obsidian日记条目：

**视频**: {title}
**内容摘要**: {self._truncate_text(transcript, 5000)}

请生成：
## 今日学习

### 📺 视频: [[{title}]]
- 主要收获:
  -
- 值得记住的:
  >
- 行动项:
  - [ ]
- 相关链接: [[概念1]], [[概念2]]

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是日记整理助手。", temperature=0.5)

    def create_knowledge_graph_data(self, transcript: str, title: str, language: str = "中文") -> str:
        """Create data for Obsidian graph view"""
        prompt = f"""分析内容，生成知识图谱数据：

**标题**: {title}
**内容**: {self._truncate_text(transcript)}

请生成：
## 节点（Nodes）
| 概念 | 类型 | 重要性 |
|------|------|--------|

## 连接（Edges）
| 源 | 目标 | 关系 |
|-----|------|------|

## Obsidian链接建议
[如何在笔记中创建这些链接]

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是知识图谱专家。", temperature=0.5)

    def export_note(self, content: str, filename: str) -> bool:
        """Export note to vault"""
        if not self.vault_path:
            return False

        filepath = os.path.join(self.vault_path, f"{filename}.md")
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
