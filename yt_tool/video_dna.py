"""
Video DNA Fingerprint - 视频DNA指纹分析
Analyze video style, rhythm, information density to create unique fingerprint
"""

import json
import hashlib
from typing import Dict, List, Any, Optional
from .ai_client import get_ai_client


class VideoDNA:
    """Generate unique DNA fingerprint for videos"""

    def __init__(self):
        self.ai_client = get_ai_client()

    def generate_fingerprint(self, transcript: str, video_info: Dict = None, language: str = "中文") -> Dict[str, Any]:
        """Generate comprehensive video DNA fingerprint"""
        prompt = f"""分析以下视频内容，生成详细的"视频DNA指纹"报告。

视频内容：
{transcript[:8000]}

请从以下维度分析并生成JSON格式的指纹数据：

1. **内容特征** (content_features):
   - topic_category: 主题分类（如：科技、教育、娱乐等）
   - sub_topics: 子话题列表
   - keywords: 核心关键词（10个）
   - content_type: 内容类型（教程/评测/访谈/讲座/vlog等）

2. **风格特征** (style_features):
   - tone: 语调（专业/轻松/严肃/幽默等）
   - complexity: 复杂度（1-10）
   - formality: 正式程度（1-10）
   - personality: 个性标签

3. **结构特征** (structure_features):
   - pacing: 节奏（快/中/慢）
   - information_density: 信息密度（1-10）
   - organization: 组织方式（线性/模块化/故事性等）
   - segment_pattern: 段落模式

4. **受众特征** (audience_features):
   - target_level: 目标受众水平（初学者/中级/高级/专家）
   - prerequisites: 前置知识要求
   - ideal_viewer: 理想观众画像

5. **独特标识** (unique_markers):
   - catchphrases: 口头禅或特色用语
   - recurring_themes: 反复出现的主题
   - signature_elements: 标志性元素

请用JSON格式返回，语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            # Try to extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                fingerprint = json.loads(response[json_start:json_end])
            else:
                fingerprint = {"raw_analysis": response}
        except json.JSONDecodeError:
            fingerprint = {"raw_analysis": response}

        # Generate unique hash
        content_hash = hashlib.md5(transcript.encode()).hexdigest()[:16]
        fingerprint["dna_hash"] = content_hash

        if video_info:
            fingerprint["video_info"] = {
                "title": video_info.get("title", ""),
                "channel": video_info.get("channel", ""),
                "duration": video_info.get("duration", 0)
            }

        return fingerprint

    def calculate_similarity(self, dna1: Dict, dna2: Dict, language: str = "中文") -> Dict[str, Any]:
        """Calculate similarity between two video DNAs"""
        prompt = f"""比较以下两个视频的DNA指纹，计算它们的相似度。

视频1 DNA:
{json.dumps(dna1, ensure_ascii=False, indent=2)}

视频2 DNA:
{json.dumps(dna2, ensure_ascii=False, indent=2)}

请分析并返回JSON格式的相似度报告：
1. overall_similarity: 总体相似度（0-100%）
2. content_similarity: 内容相似度
3. style_similarity: 风格相似度
4. audience_overlap: 受众重叠度
5. recommendation: 如果喜欢视频1，是否推荐视频2
6. differences: 主要差异点
7. common_ground: 共同点

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"raw_analysis": response}

    def find_similar_profile(self, dna: Dict, language: str = "中文") -> Dict[str, Any]:
        """Generate a profile for finding similar content"""
        prompt = f"""基于以下视频DNA指纹，生成一个用于寻找相似内容的搜索配置文件。

视频DNA:
{json.dumps(dna, ensure_ascii=False, indent=2)}

请返回JSON格式：
1. search_keywords: 推荐搜索关键词列表
2. channel_types: 可能感兴趣的频道类型
3. content_filters: 内容筛选条件
4. avoid_keywords: 应避免的关键词
5. platform_suggestions: 推荐的平台（YouTube/Bilibili/其他）
6. similar_creators: 可能相似的创作者类型描述

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"raw_analysis": response}

    def analyze_evolution(self, dna_list: List[Dict], language: str = "中文") -> Dict[str, Any]:
        """Analyze how a channel's content has evolved over time"""
        prompt = f"""分析以下多个视频DNA指纹，追踪内容的演变趋势。

视频DNA列表（按时间顺序）：
{json.dumps(dna_list, ensure_ascii=False, indent=2)}

请分析并返回JSON格式的演变报告：
1. evolution_summary: 整体演变概述
2. style_changes: 风格变化
3. topic_shifts: 话题转变
4. complexity_trend: 复杂度趋势（上升/下降/稳定）
5. audience_shift: 目标受众变化
6. quality_trend: 质量趋势评估
7. predictions: 未来内容预测
8. recommendations: 给创作者的建议

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"raw_analysis": response}

    def export_fingerprint(self, fingerprint: Dict, format: str = "json") -> str:
        """Export fingerprint in various formats"""
        if format == "json":
            return json.dumps(fingerprint, ensure_ascii=False, indent=2)
        elif format == "markdown":
            md = "# 视频DNA指纹报告\n\n"
            md += f"**DNA Hash:** `{fingerprint.get('dna_hash', 'N/A')}`\n\n"

            if "video_info" in fingerprint:
                info = fingerprint["video_info"]
                md += f"## 视频信息\n"
                md += f"- 标题: {info.get('title', 'N/A')}\n"
                md += f"- 频道: {info.get('channel', 'N/A')}\n\n"

            for key, value in fingerprint.items():
                if key not in ["dna_hash", "video_info", "raw_analysis"]:
                    md += f"## {key.replace('_', ' ').title()}\n"
                    if isinstance(value, dict):
                        for k, v in value.items():
                            md += f"- **{k}:** {v}\n"
                    else:
                        md += f"{value}\n"
                    md += "\n"

            return md
        else:
            return str(fingerprint)
