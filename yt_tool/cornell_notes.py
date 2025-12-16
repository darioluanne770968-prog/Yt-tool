"""
Cornell Notes Generator - 康奈尔笔记格式生成器
Generate notes in the Cornell note-taking system format
"""

import json
from typing import Dict, List, Any, Optional
from .ai_client import get_ai_client


class CornellNotesGenerator:
    """Generate Cornell-style notes from video content"""

    def __init__(self):
        self.ai_client = get_ai_client()

    def generate_cornell_notes(self, transcript: str, title: str = "", language: str = "中文") -> Dict[str, Any]:
        """Generate complete Cornell notes structure"""
        prompt = f"""将以下视频内容转换为康奈尔笔记格式。

康奈尔笔记系统包含：
1. 标题区：主题和日期
2. 笔记栏（右侧，占2/3）：主要内容记录
3. 提示栏（左侧，占1/3）：关键词、问题、提示
4. 总结区（底部）：内容总结

视频内容：
{transcript[:8000]}

返回JSON格式：
1. header:
   - title: 标题
   - topic: 主题
   - source: 来源

2. notes_column: 笔记栏内容数组，每项包含：
   - main_point: 主要观点
   - details: 细节要点列表
   - examples: 示例
   - diagrams_needed: 是否需要图表（描述）

3. cue_column: 提示栏数组，每项包含：
   - keywords: 关键词
   - questions: 相关问题
   - connections: 与其他知识的联系

4. summary:
   - main_summary: 主要总结（3-5句话）
   - key_takeaways: 关键要点（5个以内）
   - action_items: 行动项

5. review_questions: 复习问题列表

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                notes = json.loads(response[json_start:json_end])
                if title:
                    notes["header"]["title"] = title
                return notes
        except json.JSONDecodeError:
            pass

        return {"raw_notes": response}

    def generate_section_notes(self, transcript: str, section_duration: int = 5, language: str = "中文") -> List[Dict[str, Any]]:
        """Generate Cornell notes broken down by time sections"""
        prompt = f"""将以下视频内容按{section_duration}分钟的片段拆分，为每个片段生成康奈尔笔记。

内容：
{transcript[:8000]}

为每个片段返回JSON数组：
每个片段包含：
- segment_number: 片段编号
- estimated_time: 预估时间范围
- notes_column:
  - main_idea: 主要观点
  - supporting_points: 支持要点
  - examples: 示例
- cue_column:
  - keywords: 关键词
  - questions: 提问
- mini_summary: 片段小结

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return []

    def generate_cue_questions(self, notes: str, language: str = "中文") -> List[Dict[str, str]]:
        """Generate cue column questions from notes"""
        prompt = f"""根据以下笔记内容，生成康奈尔笔记的提示栏问题。

笔记内容：
{notes[:4000]}

生成问题要求：
1. 帮助回忆主要内容
2. 促进深入思考
3. 建立知识联系
4. 便于自测

返回JSON数组，每个问题包含：
- question: 问题
- type: 类型（recall/understanding/application/analysis）
- related_content: 对应的笔记内容摘要
- difficulty: 难度（1-5）

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return []

    def generate_summary_section(self, notes: str, max_sentences: int = 5, language: str = "中文") -> Dict[str, Any]:
        """Generate the summary section for Cornell notes"""
        prompt = f"""为以下笔记生成康奈尔笔记的总结部分（底部区域）。

笔记内容：
{notes[:4000]}

总结要求：
1. 不超过{max_sentences}句话
2. 涵盖所有核心要点
3. 使用自己的话重述
4. 突出最重要的信息

返回JSON格式：
1. summary: 总结文本
2. key_points: 关键要点列表（最多5个）
3. one_liner: 一句话概括
4. memory_hook: 记忆锚点（帮助记住整体内容的关键词或短语）

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"summary": response}

    def add_visual_cues(self, notes: Dict, language: str = "中文") -> Dict[str, Any]:
        """Add visual cues and diagram suggestions to notes"""
        prompt = f"""为以下康奈尔笔记添加视觉提示和图表建议。

笔记：
{json.dumps(notes, ensure_ascii=False)[:4000]}

请建议：
1. 适合添加的图表类型
2. 颜色编码方案
3. 符号/图标建议
4. 空间布局优化

返回JSON格式：
1. diagram_suggestions: 图表建议数组
   - location: 建议位置
   - type: 图表类型（flowchart/mindmap/table/timeline/venn）
   - description: 描述
   - content: 图表内容

2. color_coding:
   - scheme: 配色方案
   - meanings: 颜色含义

3. icons: 推荐使用的符号/图标

4. layout_tips: 布局建议

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                visual_cues = json.loads(response[json_start:json_end])
                notes["visual_cues"] = visual_cues
                return notes
        except json.JSONDecodeError:
            pass

        return notes

    def generate_review_plan(self, notes: Dict, language: str = "中文") -> Dict[str, Any]:
        """Generate a review plan using the Cornell method"""
        prompt = f"""根据康奈尔笔记方法，为以下笔记生成复习计划。

笔记：
{json.dumps(notes, ensure_ascii=False)[:4000]}

康奈尔复习法：
1. 覆盖笔记栏，用提示栏回忆
2. 用总结栏检查理解
3. 重复直到完全掌握

返回JSON格式：
1. immediate_review:
   - tasks: 立即复习任务
   - estimated_time: 预计时间

2. daily_review:
   - day_1: 第一天复习重点
   - day_3: 第三天复习重点
   - day_7: 第七天复习重点

3. self_test_questions: 自测问题
4. mastery_checklist: 掌握程度检查清单
5. weak_areas: 可能的薄弱环节
6. reinforcement_activities: 强化活动建议

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"raw_plan": response}

    def export_cornell_template(self, notes: Dict, format: str = "markdown") -> str:
        """Export Cornell notes in various formats"""
        if format == "markdown":
            header = notes.get("header", {})
            md = f"# {header.get('title', '康奈尔笔记')}\n\n"
            md += f"**主题:** {header.get('topic', '')}\n"
            md += f"**来源:** {header.get('source', '')}\n\n"
            md += "---\n\n"

            # Two-column layout simulation
            md += "## 📝 笔记栏 | 💡 提示栏\n\n"

            notes_col = notes.get("notes_column", [])
            cue_col = notes.get("cue_column", [])

            md += "| 主要内容 | 提示/问题 |\n"
            md += "|----------|----------|\n"

            for i in range(max(len(notes_col), len(cue_col))):
                note_content = ""
                cue_content = ""

                if i < len(notes_col):
                    note = notes_col[i]
                    note_content = f"**{note.get('main_point', '')}**<br>"
                    if note.get('details'):
                        note_content += "<br>".join(f"• {d}" for d in note.get('details', []))

                if i < len(cue_col):
                    cue = cue_col[i]
                    if cue.get('keywords'):
                        cue_content += f"🔑 {', '.join(cue.get('keywords', []))}<br>"
                    if cue.get('questions'):
                        cue_content += "<br>".join(f"❓ {q}" for q in cue.get('questions', []))

                md += f"| {note_content} | {cue_content} |\n"

            md += "\n---\n\n"

            # Summary section
            md += "## 📋 总结\n\n"
            summary = notes.get("summary", {})
            if isinstance(summary, dict):
                md += f"{summary.get('main_summary', '')}\n\n"
                if summary.get('key_takeaways'):
                    md += "**关键要点:**\n"
                    for point in summary.get('key_takeaways', []):
                        md += f"- {point}\n"
            else:
                md += f"{summary}\n"

            # Review questions
            if notes.get("review_questions"):
                md += "\n## ❓ 复习问题\n\n"
                for i, q in enumerate(notes["review_questions"], 1):
                    if isinstance(q, dict):
                        md += f"{i}. {q.get('question', q)}\n"
                    else:
                        md += f"{i}. {q}\n"

            return md

        elif format == "html":
            header = notes.get("header", {})
            html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{header.get('title', '康奈尔笔记')}</title>
    <style>
        .cornell-container {{ display: grid; grid-template-columns: 1fr 2fr; gap: 10px; border: 2px solid #333; }}
        .cue-column {{ background: #f0f0f0; padding: 10px; border-right: 2px solid #333; }}
        .notes-column {{ padding: 10px; }}
        .summary {{ grid-column: 1 / -1; border-top: 2px solid #333; padding: 10px; background: #e8f4e8; }}
        .header {{ grid-column: 1 / -1; background: #333; color: white; padding: 10px; }}
    </style>
</head>
<body>
    <div class="cornell-container">
        <div class="header">
            <h1>{header.get('title', '')}</h1>
            <p>主题: {header.get('topic', '')} | 来源: {header.get('source', '')}</p>
        </div>
        <div class="cue-column">
            <h3>提示栏</h3>
"""
            for cue in notes.get("cue_column", []):
                html += f"<p><strong>关键词:</strong> {', '.join(cue.get('keywords', []))}</p>"
                for q in cue.get('questions', []):
                    html += f"<p>❓ {q}</p>"

            html += """
        </div>
        <div class="notes-column">
            <h3>笔记栏</h3>
"""
            for note in notes.get("notes_column", []):
                html += f"<h4>{note.get('main_point', '')}</h4>"
                html += "<ul>"
                for detail in note.get('details', []):
                    html += f"<li>{detail}</li>"
                html += "</ul>"

            summary = notes.get("summary", {})
            summary_text = summary.get('main_summary', '') if isinstance(summary, dict) else str(summary)
            html += f"""
        </div>
        <div class="summary">
            <h3>总结</h3>
            <p>{summary_text}</p>
        </div>
    </div>
</body>
</html>"""
            return html

        elif format == "json":
            return json.dumps(notes, ensure_ascii=False, indent=2)

        return str(notes)

    def merge_notes(self, notes_list: List[Dict], language: str = "中文") -> Dict[str, Any]:
        """Merge multiple Cornell notes into one comprehensive note"""
        all_notes = []
        all_cues = []
        all_summaries = []

        for notes in notes_list:
            all_notes.extend(notes.get("notes_column", []))
            all_cues.extend(notes.get("cue_column", []))
            summary = notes.get("summary", {})
            if isinstance(summary, dict):
                all_summaries.append(summary.get("main_summary", ""))
            else:
                all_summaries.append(str(summary))

        prompt = f"""合并以下内容为一份综合康奈尔笔记。

笔记内容：
{json.dumps(all_notes[:20], ensure_ascii=False)}

提示栏：
{json.dumps(all_cues[:20], ensure_ascii=False)}

原总结：
{json.dumps(all_summaries, ensure_ascii=False)}

请整合并去重，生成一份完整的康奈尔笔记JSON格式，语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {
            "notes_column": all_notes,
            "cue_column": all_cues,
            "summary": {"main_summary": " ".join(all_summaries)}
        }
