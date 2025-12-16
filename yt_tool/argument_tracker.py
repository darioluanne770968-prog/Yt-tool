"""
Argument Tracker - 论点追踪器
Track how arguments and viewpoints evolve across different videos/channels
"""

import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from .ai_client import get_ai_client


class ArgumentTracker:
    """Track arguments and viewpoints across videos"""

    def __init__(self, storage_path: str = ".argument_tracker.json"):
        self.ai_client = get_ai_client()
        self.storage_path = storage_path
        self.arguments_db = self._load_database()

    def _load_database(self) -> Dict:
        """Load arguments database from file"""
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"arguments": {}, "videos": [], "topics": {}}

    def _save_database(self):
        """Save arguments database to file"""
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(self.arguments_db, f, ensure_ascii=False, indent=2)

    def extract_arguments(self, transcript: str, video_info: Dict = None, language: str = "中文") -> List[Dict[str, Any]]:
        """Extract main arguments and viewpoints from a video"""
        prompt = f"""分析以下视频内容，提取所有主要论点和观点。

内容：
{transcript[:8000]}

请识别并提取：
1. 主要论点（claims）
2. 支持论据（evidence）
3. 反对意见（counterarguments）
4. 结论（conclusions）

返回JSON数组，每个论点包含：
- id: 唯一标识
- claim: 论点陈述
- type: 类型（main_argument/supporting/counter/conclusion）
- evidence: 支持证据列表
- confidence: 作者的确信程度（1-10）
- topic: 所属话题
- keywords: 关键词
- stance: 立场（positive/negative/neutral）
- quote: 原文引用（如有）

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            if json_start != -1 and json_end > json_start:
                arguments = json.loads(response[json_start:json_end])

                # Add video metadata
                for arg in arguments:
                    arg["source"] = {
                        "title": video_info.get("title", "") if video_info else "",
                        "channel": video_info.get("channel", "") if video_info else "",
                        "url": video_info.get("url", "") if video_info else "",
                        "date": video_info.get("date", "") if video_info else ""
                    }

                return arguments
        except json.JSONDecodeError:
            pass

        return []

    def add_to_database(self, arguments: List[Dict], topic: str = None):
        """Add extracted arguments to the tracking database"""
        for arg in arguments:
            arg_topic = topic or arg.get("topic", "general")

            if arg_topic not in self.arguments_db["topics"]:
                self.arguments_db["topics"][arg_topic] = []

            self.arguments_db["topics"][arg_topic].append(arg)

        self._save_database()

    def track_topic(self, topic: str, transcript: str, video_info: Dict = None, language: str = "中文") -> Dict[str, Any]:
        """Track a specific topic across a new video"""
        # Extract arguments
        arguments = self.extract_arguments(transcript, video_info, language)

        # Filter for topic-relevant arguments
        relevant = [arg for arg in arguments if topic.lower() in arg.get("topic", "").lower()
                   or topic.lower() in " ".join(arg.get("keywords", [])).lower()
                   or topic.lower() in arg.get("claim", "").lower()]

        # Add to database
        self.add_to_database(relevant, topic)

        return {
            "topic": topic,
            "new_arguments": len(relevant),
            "arguments": relevant,
            "total_tracked": len(self.arguments_db["topics"].get(topic, []))
        }

    def compare_stances(self, topic: str, language: str = "中文") -> Dict[str, Any]:
        """Compare different stances on a topic across all tracked videos"""
        topic_args = self.arguments_db["topics"].get(topic, [])

        if not topic_args:
            return {"error": f"No arguments tracked for topic: {topic}"}

        prompt = f"""分析以下关于"{topic}"话题的不同论点，比较各方立场。

论点列表：
{json.dumps(topic_args[:20], ensure_ascii=False, indent=2)}

请分析并返回JSON格式：
1. stance_summary: 各种立场的概述
2. pro_arguments: 支持方论点汇总
3. con_arguments: 反对方论点汇总
4. neutral_observations: 中立观察
5. consensus_points: 各方共识点
6. controversy_points: 争议焦点
7. evolution: 观点如何随时间演变
8. strongest_argument: 最有力的论点
9. recommendation: 综合建议

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

    def find_contradictions(self, topic: str = None, language: str = "中文") -> List[Dict[str, Any]]:
        """Find contradictions in arguments across videos"""
        if topic:
            args = self.arguments_db["topics"].get(topic, [])
        else:
            args = []
            for topic_args in self.arguments_db["topics"].values():
                args.extend(topic_args)

        if len(args) < 2:
            return []

        prompt = f"""分析以下论点，找出相互矛盾或冲突的观点。

论点列表：
{json.dumps(args[:30], ensure_ascii=False, indent=2)}

请识别矛盾对，返回JSON数组：
每个矛盾包含：
- argument1: 第一个论点
- argument2: 与之矛盾的论点
- contradiction_type: 矛盾类型（直接矛盾/部分矛盾/隐含矛盾）
- explanation: 矛盾解释
- resolution: 可能的调和方式
- which_stronger: 哪个论点更有力

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

    def trace_argument_origin(self, claim: str, language: str = "中文") -> Dict[str, Any]:
        """Trace the origin and spread of a specific argument"""
        all_args = []
        for topic_args in self.arguments_db["topics"].values():
            all_args.extend(topic_args)

        prompt = f"""追踪以下论点的来源和传播。

目标论点："{claim}"

数据库中的所有论点：
{json.dumps(all_args[:30], ensure_ascii=False, indent=2)}

请分析并返回JSON格式：
1. original_source: 最可能的原始来源
2. similar_claims: 类似的论点列表
3. timeline: 论点出现的时间线
4. variations: 论点的变体形式
5. adoption_pattern: 被谁引用或采纳
6. strength_over_time: 论点力度随时间的变化

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

    def generate_debate_brief(self, topic: str, language: str = "中文") -> str:
        """Generate a debate briefing document on a topic"""
        topic_args = self.arguments_db["topics"].get(topic, [])

        prompt = f"""基于以下关于"{topic}"的论点数据，生成一份辩论简报。

论点数据：
{json.dumps(topic_args[:25], ensure_ascii=False, indent=2)}

请生成包含以下部分的完整简报：

# {topic} 辩论简报

## 1. 话题概述
## 2. 主要立场
### 2.1 支持方观点
### 2.2 反对方观点
## 3. 关键论据分析
## 4. 常见反驳及回应
## 5. 数据与事实
## 6. 辩论策略建议
## 7. 参考来源

语言使用{language}，格式使用Markdown。"""

        return self.ai_client.chat(prompt)

    def get_topic_timeline(self, topic: str) -> List[Dict]:
        """Get timeline of arguments on a topic"""
        topic_args = self.arguments_db["topics"].get(topic, [])

        # Sort by date if available
        timeline = sorted(
            topic_args,
            key=lambda x: x.get("source", {}).get("date", ""),
            reverse=False
        )

        return timeline

    def export_report(self, topic: str = None, format: str = "markdown") -> str:
        """Export tracking report"""
        if topic:
            topics = {topic: self.arguments_db["topics"].get(topic, [])}
        else:
            topics = self.arguments_db["topics"]

        if format == "markdown":
            md = "# 论点追踪报告\n\n"

            for topic_name, args in topics.items():
                md += f"## {topic_name}\n\n"
                md += f"共追踪 {len(args)} 个论点\n\n"

                for i, arg in enumerate(args[:10], 1):
                    md += f"### {i}. {arg.get('claim', 'N/A')}\n"
                    md += f"- **类型:** {arg.get('type', 'N/A')}\n"
                    md += f"- **立场:** {arg.get('stance', 'N/A')}\n"
                    md += f"- **来源:** {arg.get('source', {}).get('channel', 'N/A')}\n"
                    md += f"- **证据:** {', '.join(arg.get('evidence', []))}\n\n"

            return md

        elif format == "json":
            return json.dumps(topics, ensure_ascii=False, indent=2)

        return str(topics)
