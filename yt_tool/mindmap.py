"""
AI-powered mind map generation from video content
"""

import json
import re
from typing import Optional
from .ai_client import get_ai_client


MINDMAP_SYSTEM_PROMPT = """你是一个专业的知识整理专家。你的任务是将视频内容整理成清晰的思维导图结构。

要求：
1. 提取核心主题和关键概念
2. 建立层次化的知识结构
3. 保持简洁，每个节点不超过10个字
4. 最多3-4层深度
5. 每个父节点下最多5-7个子节点"""


MINDMAP_PROMPT_TEMPLATE = """请将以下视频内容整理成思维导图结构。

视频内容：
{transcript}

请严格按照以下JSON格式输出：
{{
    "title": "视频主题",
    "children": [
        {{
            "title": "主要话题1",
            "children": [
                {{"title": "要点1"}},
                {{"title": "要点2"}}
            ]
        }},
        {{
            "title": "主要话题2",
            "children": [
                {{"title": "要点1"}},
                {{"title": "要点2"}}
            ]
        }}
    ]
}}

请用{language}输出。只输出JSON，不要有其他文字。"""


class MindmapGenerator:
    """Generate mind maps from video content"""

    def __init__(self, provider: str = None):
        """
        Initialize mind map generator

        Args:
            provider: AI provider ('openai' or 'anthropic')
        """
        self.ai = get_ai_client(provider)

    def generate(self, transcript: str, language: str = "中文") -> dict:
        """
        Generate mind map structure from transcript

        Args:
            transcript: Video transcript text
            language: Output language

        Returns:
            Mind map structure as dictionary
        """
        # Truncate if needed
        if len(transcript) > 15000:
            transcript = transcript[:15000] + "\n\n[内容已截断...]"

        prompt = MINDMAP_PROMPT_TEMPLATE.format(
            transcript=transcript,
            language=language,
        )

        response = self.ai.chat(
            prompt=prompt,
            system_prompt=MINDMAP_SYSTEM_PROMPT,
            temperature=0.5,
        )

        return self._parse_response(response)

    def _parse_response(self, response: str) -> dict:
        """Parse AI response to extract mind map structure"""
        try:
            # Try to find JSON in the response
            json_match = re.search(r"\{[\s\S]*\}", response)
            if json_match:
                return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass

        # Fallback: create simple structure
        return {
            "title": "Video Content",
            "children": [{"title": "Unable to parse content"}],
        }

    def to_markdown(self, mindmap: dict, indent: int = 0) -> str:
        """
        Convert mind map to Markdown format

        Args:
            mindmap: Mind map dictionary
            indent: Current indentation level

        Returns:
            Markdown formatted mind map
        """
        lines = []
        prefix = "  " * indent

        if indent == 0:
            lines.append(f"# {mindmap.get('title', 'Mind Map')}\n")
        else:
            bullet = "-" if indent == 1 else "  " * (indent - 1) + "-"
            lines.append(f"{bullet} {mindmap.get('title', '')}")

        for child in mindmap.get("children", []):
            lines.append(self.to_markdown(child, indent + 1))

        return "\n".join(lines)

    def to_mermaid(self, mindmap: dict) -> str:
        """
        Convert mind map to Mermaid diagram format

        Args:
            mindmap: Mind map dictionary

        Returns:
            Mermaid diagram code
        """
        lines = ["```mermaid", "mindmap"]
        lines.append(f"  root(({self._escape_mermaid(mindmap.get('title', 'Mind Map'))}))")

        def add_children(node: dict, level: int):
            indent = "    " * level
            for child in node.get("children", []):
                title = self._escape_mermaid(child.get("title", ""))
                lines.append(f"{indent}{title}")
                add_children(child, level + 1)

        add_children(mindmap, 1)
        lines.append("```")

        return "\n".join(lines)

    def _escape_mermaid(self, text: str) -> str:
        """Escape special characters for Mermaid"""
        # Remove or replace special characters
        text = text.replace("(", "（").replace(")", "）")
        text = text.replace("[", "【").replace("]", "】")
        text = text.replace("{", "｛").replace("}", "｝")
        return text

    def to_markmap(self, mindmap: dict) -> str:
        """
        Convert mind map to Markmap format (Markdown-based mind map)

        Args:
            mindmap: Mind map dictionary

        Returns:
            Markmap compatible Markdown
        """
        lines = ["---", "markmap:", "  colorFreezeLevel: 2", "---", ""]
        lines.append(f"# {mindmap.get('title', 'Mind Map')}\n")

        def add_children(node: dict, level: int):
            prefix = "#" * (level + 1)
            for child in node.get("children", []):
                title = child.get("title", "")
                if child.get("children"):
                    lines.append(f"\n{prefix} {title}\n")
                    add_children(child, level + 1)
                else:
                    lines.append(f"- {title}")

        add_children(mindmap, 1)

        return "\n".join(lines)

    def to_xmind(self, mindmap: dict) -> str:
        """
        Convert mind map to XMind compatible format (simplified)

        Args:
            mindmap: Mind map dictionary

        Returns:
            Plain text outline format
        """
        lines = []

        def add_node(node: dict, level: int):
            indent = "\t" * level
            lines.append(f"{indent}{node.get('title', '')}")
            for child in node.get("children", []):
                add_node(child, level + 1)

        add_node(mindmap, 0)

        return "\n".join(lines)

    def to_json(self, mindmap: dict) -> str:
        """Convert mind map to JSON string"""
        return json.dumps(mindmap, ensure_ascii=False, indent=2)
