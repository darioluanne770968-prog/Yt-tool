"""
Business Tools Suite - 商业/专业工具套件
Including: Competitor Analysis, Trend Prediction, Sponsor Detection, Copyright Check, ROI Calculator
"""

import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from .ai_client import get_ai_client


class BusinessToolsSuite:
    """Comprehensive business analysis tools for video content"""

    def __init__(self):
        self.ai_client = get_ai_client()

    # ============ Competitor Analysis ============

    def analyze_competitor_channel(self, channel_data: Dict, your_channel_data: Dict = None, language: str = "中文") -> Dict[str, Any]:
        """Analyze competitor channel strategy"""
        prompt = f"""分析竞争对手频道策略。

竞争对手数据：
{json.dumps(channel_data, ensure_ascii=False)[:3000]}

{f"我的频道数据：{json.dumps(your_channel_data, ensure_ascii=False)[:2000]}" if your_channel_data else ""}

分析维度：
1. 内容策略
2. 发布频率
3. 受众互动
4. 标题/缩略图策略
5. 主题覆盖

返回JSON格式：
1. content_strategy: 内容策略分析
2. posting_pattern: 发布模式
3. engagement_tactics: 互动策略
4. strengths: 优势
5. weaknesses: 弱点
6. opportunities: 机会
7. recommendations: 建议
8. competitive_gaps: 竞争差距

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

    def compare_video_performance(self, videos: List[Dict], language: str = "中文") -> Dict[str, Any]:
        """Compare performance across multiple videos"""
        prompt = f"""对比分析以下视频的表现。

视频数据：
{json.dumps(videos[:10], ensure_ascii=False)}

分析：
1. 表现最佳的内容特征
2. 标题效果对比
3. 时长与观看的关系
4. 发布时间影响
5. 话题热度

返回JSON格式，语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"raw": response}

    # ============ Trend Prediction ============

    def predict_topic_trends(self, transcript: str, topics: List[str] = None, language: str = "中文") -> Dict[str, Any]:
        """Predict trends based on content analysis"""
        prompt = f"""基于以下内容分析话题趋势。

内容：
{transcript[:6000]}

{f"关注话题：{json.dumps(topics, ensure_ascii=False)}" if topics else ""}

预测：
1. 短期趋势（1-3月）
2. 中期趋势（3-6月）
3. 长期趋势（6-12月）

返回JSON格式：
1. current_state: 当前状态
2. predictions:
   - short_term: 短期预测
   - mid_term: 中期预测
   - long_term: 长期预测
3. confidence_level: 置信度
4. factors: 影响因素
5. opportunities: 内容创作机会
6. risks: 潜在风险
7. recommended_actions: 建议行动

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

    def identify_emerging_topics(self, transcripts: List[str], language: str = "中文") -> Dict[str, Any]:
        """Identify emerging topics from multiple videos"""
        combined = "\n---\n".join(t[:2000] for t in transcripts[:5])

        prompt = f"""从以下多个视频内容中识别新兴话题。

内容：
{combined}

返回JSON格式：
1. emerging_topics: 新兴话题列表
2. growth_indicators: 增长指标
3. early_signals: 早期信号
4. recommendation: 建议关注的话题

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

    # ============ Sponsor Detection ============

    def detect_sponsorships(self, transcript: str, language: str = "中文") -> Dict[str, Any]:
        """Detect sponsored content and brand mentions"""
        prompt = f"""检测以下内容中的赞助/广告植入。

内容：
{transcript[:8000]}

检测：
1. 明确的赞助商声明
2. 品牌提及
3. 产品推广
4. 附属链接暗示
5. 软广植入

返回JSON格式：
1. sponsors: 赞助商列表
   - brand: 品牌名
   - type: 类型（paid/affiliate/free_product）
   - confidence: 置信度
   - mentions: 提及位置

2. brand_mentions: 品牌提及
3. estimated_ad_duration: 广告时长估算（秒）
4. ad_density: 广告密度
5. disclosure_present: 是否有广告声明
6. fTc_compliance: FTC合规性评估

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

    # ============ Copyright Check ============

    def check_copyright_risks(self, transcript: str, language: str = "中文") -> Dict[str, Any]:
        """Check for potential copyright issues"""
        prompt = f"""检查以下内容的潜在版权问题。

内容：
{transcript[:6000]}

检查项目：
1. 直接引用
2. 音乐/歌曲提及
3. 电影/电视引用
4. 书籍/文章引用
5. 品牌/商标使用
6. 其他受保护内容

返回JSON格式：
1. risk_level: 风险等级（low/medium/high）
2. identified_content: 识别的受保护内容
   - content: 内容
   - type: 类型
   - risk: 风险
   - recommendation: 建议

3. quotes_analysis: 引用分析
4. fair_use_assessment: 合理使用评估
5. recommendations: 建议
6. disclaimer_needed: 是否需要免责声明

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

    # ============ ROI Calculator ============

    def calculate_content_roi(self, video_data: Dict, costs: Dict = None, language: str = "中文") -> Dict[str, Any]:
        """Calculate ROI for video content"""
        views = video_data.get("views", 0)
        likes = video_data.get("likes", 0)
        comments = video_data.get("comments", 0)
        duration = video_data.get("duration", 0)
        subscribers_gained = video_data.get("subscribers_gained", 0)

        # Estimate revenue (rough estimates)
        cpm = video_data.get("cpm", 2.0)  # $ per 1000 views
        estimated_revenue = (views / 1000) * cpm

        # Calculate costs
        total_costs = 0
        if costs:
            total_costs = sum(costs.values())

        # Engagement metrics
        engagement_rate = ((likes + comments) / views * 100) if views > 0 else 0

        roi = ((estimated_revenue - total_costs) / total_costs * 100) if total_costs > 0 else 0

        result = {
            "metrics": {
                "views": views,
                "likes": likes,
                "comments": comments,
                "engagement_rate": round(engagement_rate, 2),
                "subscribers_gained": subscribers_gained
            },
            "financial": {
                "estimated_revenue": round(estimated_revenue, 2),
                "total_costs": total_costs,
                "net_profit": round(estimated_revenue - total_costs, 2),
                "roi_percent": round(roi, 2)
            },
            "efficiency": {
                "revenue_per_minute": round(estimated_revenue / (duration / 60), 2) if duration > 0 else 0,
                "views_per_dollar": round(views / total_costs, 0) if total_costs > 0 else views
            }
        }

        # AI analysis
        prompt = f"""分析以下视频ROI数据，提供优化建议。

数据：
{json.dumps(result, ensure_ascii=False)}

提供：
1. 表现评估
2. 优化建议
3. 投资建议

返回JSON格式，语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                ai_analysis = json.loads(response[json_start:json_end])
                result["ai_analysis"] = ai_analysis
        except json.JSONDecodeError:
            result["ai_analysis"] = {"raw": response}

        return result

    def estimate_video_value(self, transcript: str, metrics: Dict = None, language: str = "中文") -> Dict[str, Any]:
        """Estimate the potential value of video content"""
        prompt = f"""评估以下视频内容的潜在价值。

内容摘要：
{transcript[:4000]}

{f"已有指标：{json.dumps(metrics, ensure_ascii=False)}" if metrics else ""}

评估：
1. 内容质量分
2. 商业潜力
3. 长期价值
4. 再利用价值

返回JSON格式：
1. quality_score: 内容质量（1-10）
2. commercial_potential: 商业潜力（1-10）
3. longevity: 长期价值（1-10）
4. repurpose_value: 再利用价值（1-10）
5. overall_value_score: 综合评分
6. monetization_suggestions: 变现建议
7. value_drivers: 价值驱动因素

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

    def generate_business_report(self, data: Dict, report_type: str = "comprehensive", language: str = "中文") -> str:
        """Generate business analysis report"""
        if report_type == "comprehensive":
            sections = ["competitor", "trends", "roi", "copyright"]
        elif report_type == "competitive":
            sections = ["competitor"]
        elif report_type == "financial":
            sections = ["roi"]
        else:
            sections = [report_type]

        md = f"# 商业分析报告\n\n"
        md += f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"

        for section in sections:
            if section in data:
                md += f"## {section.upper()}\n\n"
                if isinstance(data[section], dict):
                    for key, value in data[section].items():
                        md += f"### {key}\n{json.dumps(value, ensure_ascii=False, indent=2) if isinstance(value, (dict, list)) else value}\n\n"
                else:
                    md += f"{data[section]}\n\n"

        return md
