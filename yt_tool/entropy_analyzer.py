"""
Information Entropy Analyzer - 信息熵分析
Analyze information density and find the most valuable parts of videos
"""

import json
import re
from typing import Dict, List, Any, Optional, Tuple
from collections import Counter
from .ai_client import get_ai_client


class EntropyAnalyzer:
    """Analyze information entropy and density in video content"""

    def __init__(self):
        self.ai_client = get_ai_client()

    def calculate_lexical_density(self, text: str) -> float:
        """Calculate lexical density (content words / total words)"""
        words = re.findall(r'\b\w+\b', text.lower())
        if not words:
            return 0.0

        # Common function words (simplified)
        function_words = {
            'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'shall', 'can', 'need', 'dare',
            'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from', 'as',
            'and', 'or', 'but', 'if', 'then', 'that', 'which', 'who', 'whom',
            'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it',
            'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your',
            '的', '是', '在', '了', '和', '与', '或', '但', '如果', '那么',
            '这', '那', '我', '你', '他', '她', '它', '我们', '他们', '就',
            '也', '都', '而', '及', '等', '等等', '所以', '因为', '虽然'
        }

        content_words = [w for w in words if w not in function_words and len(w) > 1]
        return len(content_words) / len(words) if words else 0.0

    def calculate_vocabulary_richness(self, text: str) -> Dict[str, float]:
        """Calculate vocabulary richness metrics"""
        words = re.findall(r'\b\w+\b', text.lower())
        if not words:
            return {"ttr": 0.0, "hapax": 0.0, "dis": 0.0}

        unique_words = set(words)
        word_freq = Counter(words)
        hapax_legomena = sum(1 for w, c in word_freq.items() if c == 1)

        return {
            "ttr": len(unique_words) / len(words),  # Type-Token Ratio
            "hapax": hapax_legomena / len(unique_words) if unique_words else 0.0,
            "unique_count": len(unique_words),
            "total_words": len(words)
        }

    def segment_analysis(self, transcript: str, segment_size: int = 500) -> List[Dict[str, Any]]:
        """Analyze information density by segments"""
        words = transcript.split()
        segments = []

        for i in range(0, len(words), segment_size):
            segment_text = ' '.join(words[i:i + segment_size])
            segment_words = words[i:i + segment_size]

            density = self.calculate_lexical_density(segment_text)
            richness = self.calculate_vocabulary_richness(segment_text)

            segments.append({
                "segment_id": len(segments) + 1,
                "start_word": i,
                "end_word": min(i + segment_size, len(words)),
                "word_count": len(segment_words),
                "lexical_density": round(density, 3),
                "vocabulary_richness": richness["ttr"],
                "preview": segment_text[:100] + "..."
            })

        return segments

    def analyze_information_density(self, transcript: str, language: str = "中文") -> Dict[str, Any]:
        """Comprehensive information density analysis using AI"""
        prompt = f"""分析以下视频内容的信息密度。

内容：
{transcript[:8000]}

请从以下维度分析，返回JSON格式：

1. **overall_density** (1-10): 整体信息密度评分
2. **density_distribution**: 信息密度分布描述
3. **high_value_sections**: 高价值片段列表，每个包含：
   - content: 内容摘要
   - reason: 为什么高价值
   - density_score: 密度分（1-10）
4. **low_value_sections**: 低价值/冗余片段
5. **filler_content**: 填充内容（寒暄、重复、跑题）
6. **key_insights**: 核心洞见列表
7. **insight_per_minute**: 每分钟洞见数（估算）
8. **redundancy_rate**: 冗余率（%）
9. **optimal_speed**: 推荐播放倍速
10. **time_save_potential**: 跳过低价值内容可节省时间（%）

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                ai_analysis = json.loads(response[json_start:json_end])
            else:
                ai_analysis = {"raw_analysis": response}
        except json.JSONDecodeError:
            ai_analysis = {"raw_analysis": response}

        # Add computational metrics
        computational = {
            "lexical_density": round(self.calculate_lexical_density(transcript), 3),
            "vocabulary_metrics": self.calculate_vocabulary_richness(transcript)
        }

        return {
            "ai_analysis": ai_analysis,
            "computational_metrics": computational
        }

    def find_golden_nuggets(self, transcript: str, top_n: int = 5, language: str = "中文") -> List[Dict[str, Any]]:
        """Find the most valuable insights ('golden nuggets') in the content"""
        prompt = f"""从以下视频内容中找出最有价值的{top_n}个"金句"或核心洞见。

内容：
{transcript[:8000]}

对于每个金句，返回JSON数组：
- nugget: 金句内容
- context: 上下文背景
- value_type: 价值类型（实用技巧/深刻洞见/独特观点/数据事实/人生智慧）
- actionable: 是否可执行
- memorability: 记忆价值（1-10）
- share_worthy: 是否值得分享
- application: 如何应用

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

    def generate_condensed_version(self, transcript: str, target_ratio: float = 0.3, language: str = "中文") -> str:
        """Generate a condensed version keeping only high-value content"""
        prompt = f"""将以下视频内容压缩到原来的{int(target_ratio * 100)}%，只保留最有价值的信息。

原内容：
{transcript[:10000]}

要求：
1. 删除所有寒暄、重复、跑题内容
2. 保留所有关键信息和洞见
3. 保持逻辑连贯
4. 使用精炼的语言
5. 标注【重要】在关键点前

生成压缩版本，语言使用{language}。"""

        return self.ai_client.chat(prompt)

    def create_density_heatmap_data(self, transcript: str, segments: int = 20) -> List[Dict[str, Any]]:
        """Create data for information density heatmap visualization"""
        segment_results = self.segment_analysis(transcript, len(transcript.split()) // segments)

        # Normalize scores for heatmap
        densities = [s["lexical_density"] for s in segment_results]
        if densities:
            max_d = max(densities)
            min_d = min(densities)
            range_d = max_d - min_d if max_d != min_d else 1

            for seg in segment_results:
                normalized = (seg["lexical_density"] - min_d) / range_d
                seg["heatmap_value"] = round(normalized, 2)
                seg["color_intensity"] = int(normalized * 255)

        return segment_results

    def compare_density(self, transcripts: List[str], labels: List[str] = None, language: str = "中文") -> Dict[str, Any]:
        """Compare information density across multiple videos"""
        results = []

        for i, transcript in enumerate(transcripts):
            label = labels[i] if labels and i < len(labels) else f"Video {i+1}"
            density = self.calculate_lexical_density(transcript)
            richness = self.calculate_vocabulary_richness(transcript)

            results.append({
                "label": label,
                "lexical_density": round(density, 3),
                "vocabulary_richness": richness,
                "word_count": len(transcript.split())
            })

        # Sort by density
        results.sort(key=lambda x: x["lexical_density"], reverse=True)

        return {
            "comparison": results,
            "highest_density": results[0]["label"] if results else None,
            "lowest_density": results[-1]["label"] if results else None,
            "average_density": sum(r["lexical_density"] for r in results) / len(results) if results else 0
        }

    def suggest_skip_sections(self, transcript: str, language: str = "中文") -> Dict[str, Any]:
        """Suggest sections to skip for time-efficient viewing"""
        prompt = f"""分析以下视频内容，建议哪些部分可以跳过以节省时间。

内容：
{transcript[:8000]}

返回JSON格式：
1. skip_sections: 可跳过的部分列表，每个包含：
   - description: 内容描述
   - reason: 跳过原因（重复/寒暄/广告/跑题/基础回顾）
   - time_save: 预估节省时间（相对比例）
2. must_watch: 必看部分
3. total_save_estimate: 总共可节省的时间比例
4. efficient_path: 高效观看路径建议

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

    def export_report(self, analysis: Dict, format: str = "markdown") -> str:
        """Export entropy analysis report"""
        if format == "markdown":
            md = "# 信息熵分析报告\n\n"

            if "computational_metrics" in analysis:
                cm = analysis["computational_metrics"]
                md += "## 计算指标\n\n"
                md += f"- **词汇密度:** {cm.get('lexical_density', 'N/A')}\n"
                vm = cm.get("vocabulary_metrics", {})
                md += f"- **词汇丰富度 (TTR):** {vm.get('ttr', 'N/A'):.3f}\n"
                md += f"- **独特词汇数:** {vm.get('unique_count', 'N/A')}\n"
                md += f"- **总词数:** {vm.get('total_words', 'N/A')}\n\n"

            if "ai_analysis" in analysis:
                ai = analysis["ai_analysis"]
                md += "## AI 分析\n\n"
                md += f"- **整体密度评分:** {ai.get('overall_density', 'N/A')}/10\n"
                md += f"- **冗余率:** {ai.get('redundancy_rate', 'N/A')}%\n"
                md += f"- **推荐倍速:** {ai.get('optimal_speed', 'N/A')}x\n"
                md += f"- **可节省时间:** {ai.get('time_save_potential', 'N/A')}%\n\n"

                if "high_value_sections" in ai:
                    md += "### 高价值片段\n\n"
                    for section in ai["high_value_sections"][:5]:
                        md += f"- {section.get('content', 'N/A')} (密度: {section.get('density_score', 'N/A')}/10)\n"
                    md += "\n"

                if "key_insights" in ai:
                    md += "### 核心洞见\n\n"
                    for insight in ai["key_insights"][:5]:
                        md += f"- {insight}\n"

            return md

        elif format == "json":
            return json.dumps(analysis, ensure_ascii=False, indent=2)

        return str(analysis)
