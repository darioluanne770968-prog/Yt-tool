"""
Accessibility Suite - 无障碍功能套件
Comprehensive accessibility features for video content
Including: Sign language, Audio description, Simplified language, Multisensory notes
"""

import json
from typing import Dict, List, Any, Optional
from .ai_client import get_ai_client


class AccessibilitySuite:
    """Comprehensive accessibility features for video content"""

    def __init__(self):
        self.ai_client = get_ai_client()

    # ============ Sign Language Generation ============

    def generate_sign_language_script(self, transcript: str, sign_language: str = "CSL", language: str = "中文") -> Dict[str, Any]:
        """Generate sign language translation script"""
        sign_systems = {
            "CSL": "中国手语",
            "ASL": "美国手语",
            "BSL": "英国手语",
            "JSL": "日本手语"
        }

        prompt = f"""将以下内容转换为{sign_systems.get(sign_language, sign_language)}翻译脚本。

内容：
{transcript[:6000]}

要求：
1. 分解为手语词汇序列
2. 标注表情和体态
3. 提供手势描述

返回JSON格式：
1. sign_system: 手语系统
2. segments: 段落数组，每段包含：
   - original_text: 原文
   - sign_sequence: 手语词汇序列
   - facial_expression: 面部表情指示
   - body_position: 体态说明
   - notes: 翻译注释

3. glossary: 关键手语词汇表
4. interpreter_notes: 译员注意事项

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"raw": response}

    # ============ Audio Description ============

    def generate_audio_description(self, transcript: str, visual_content: str = "", language: str = "中文") -> Dict[str, Any]:
        """Generate audio descriptions for visual content"""
        prompt = f"""为以下视频内容生成音频描述（为视障用户描述视觉元素）。

字幕/口述内容：
{transcript[:4000]}

{f"视觉内容描述：{visual_content}" if visual_content else "请根据内容推测可能的视觉元素"}

音频描述要求：
1. 描述重要视觉信息
2. 在对话间隙插入
3. 简洁但信息丰富
4. 不重复已说内容

返回JSON格式：
1. descriptions: 描述数组，每个包含：
   - timestamp: 时间点
   - description: 描述内容
   - priority: 优先级（必要/重要/补充）
   - duration: 描述时长（秒）

2. summary_description: 整体场景描述
3. key_visuals: 关键视觉元素列表
4. style_guide: 描述风格指南

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"raw": response}

    # ============ Simplified Language ============

    def simplify_content(self, transcript: str, reading_level: str = "elementary", language: str = "中文") -> Dict[str, Any]:
        """Simplify content for different reading levels"""
        levels = {
            "elementary": "小学水平（6-10岁）",
            "middle": "初中水平（11-14岁）",
            "basic": "基础成人水平",
            "easy_read": "易读版本（学习障碍友好）"
        }

        prompt = f"""将以下内容简化为{levels.get(reading_level, reading_level)}。

原内容：
{transcript[:6000]}

简化要求：
1. 使用简单词汇
2. 短句结构
3. 避免隐喻和习语
4. 清晰的逻辑连接
5. 一个段落一个主题

返回JSON格式：
1. simplified_text: 简化后的文本
2. vocabulary_changes: 词汇替换列表
3. structure_changes: 结构调整说明
4. reading_aids:
   - key_terms: 关键术语（带简单解释）
   - summary_points: 要点总结
5. accessibility_score: 可读性评分（1-10）

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"raw": response}

    def generate_plain_language_summary(self, transcript: str, language: str = "中文") -> str:
        """Generate a plain language summary"""
        prompt = f"""用最简单的语言总结以下内容。

内容：
{transcript[:6000]}

要求：
- 使用日常词汇
- 每句话不超过15个字
- 一段话说一件事
- 避免专业术语

语言使用{language}。"""

        return self.ai_client.chat(prompt)

    # ============ Multisensory Notes ============

    def generate_multisensory_notes(self, transcript: str, language: str = "中文") -> Dict[str, Any]:
        """Generate multisensory learning notes"""
        prompt = f"""为以下内容创建多感官学习笔记。

内容：
{transcript[:6000]}

多感官笔记要求：
1. 视觉元素（图表、颜色编码）
2. 听觉元素（节奏、韵律）
3. 动觉元素（动作、手势）
4. 触觉提示（质感描述）

返回JSON格式：
1. visual_notes:
   - color_coding: 颜色编码方案
   - diagram_suggestions: 图表建议
   - spatial_layout: 空间布局

2. auditory_notes:
   - rhythm_patterns: 节奏模式
   - mnemonic_songs: 记忆歌曲/韵律
   - verbal_associations: 语音联想

3. kinesthetic_notes:
   - gestures: 手势动作
   - physical_activities: 身体活动
   - movement_patterns: 动作模式

4. tactile_notes:
   - texture_associations: 质感联想
   - physical_materials: 可用材料

5. combined_activities: 综合活动建议

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"raw": response}

    # ============ WCAG Compliance ============

    def check_accessibility_compliance(self, content: Dict, language: str = "中文") -> Dict[str, Any]:
        """Check content for accessibility compliance"""
        prompt = f"""检查以下内容的无障碍合规性（参考WCAG标准）。

内容：
{json.dumps(content, ensure_ascii=False)[:4000]}

检查项目：
1. 文本替代（图像、视频）
2. 字幕/转录
3. 颜色对比度
4. 键盘可访问性
5. 屏幕阅读器兼容性

返回JSON格式：
1. compliance_score: 合规评分（0-100）
2. issues: 问题列表
   - severity: 严重程度（critical/major/minor）
   - description: 问题描述
   - recommendation: 修复建议
3. passed_criteria: 通过的标准
4. improvement_suggestions: 改进建议

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"raw": response}

    # ============ Export Functions ============

    def export_accessibility_package(self, transcript: str, language: str = "中文") -> Dict[str, Any]:
        """Generate complete accessibility package"""
        return {
            "sign_language": self.generate_sign_language_script(transcript, language=language),
            "audio_description": self.generate_audio_description(transcript, language=language),
            "simplified": self.simplify_content(transcript, language=language),
            "multisensory": self.generate_multisensory_notes(transcript, language=language)
        }

    def export_accessible_document(self, content: Dict, format: str = "markdown") -> str:
        """Export as accessible document"""
        if format == "markdown":
            md = "# 无障碍内容包\n\n"

            if content.get("simplified"):
                md += "## 简化版本\n\n"
                simplified = content["simplified"]
                if isinstance(simplified, dict):
                    md += simplified.get("simplified_text", "") + "\n\n"
                else:
                    md += str(simplified) + "\n\n"

            if content.get("audio_description"):
                md += "## 音频描述\n\n"
                ad = content["audio_description"]
                if isinstance(ad, dict) and "descriptions" in ad:
                    for desc in ad["descriptions"]:
                        md += f"- [{desc.get('timestamp', '')}] {desc.get('description', '')}\n"
                md += "\n"

            if content.get("multisensory"):
                md += "## 多感官笔记\n\n"
                ms = content["multisensory"]
                if isinstance(ms, dict):
                    if ms.get("visual_notes"):
                        md += f"### 视觉提示\n{json.dumps(ms['visual_notes'], ensure_ascii=False)}\n\n"
                    if ms.get("auditory_notes"):
                        md += f"### 听觉提示\n{json.dumps(ms['auditory_notes'], ensure_ascii=False)}\n\n"

            return md

        elif format == "json":
            return json.dumps(content, ensure_ascii=False, indent=2)

        return str(content)
