"""
Discussion Generator - 讨论问题生成器
Generate thought-provoking discussion questions for group learning
"""

import json
from typing import Dict, List, Any, Optional
from .ai_client import get_ai_client


class DiscussionGenerator:
    """Generate discussion questions and facilitate conversations"""

    def __init__(self):
        self.ai_client = get_ai_client()

    def generate_discussion_questions(self, transcript: str, num_questions: int = 10, discussion_type: str = "general", language: str = "中文") -> List[Dict[str, Any]]:
        """Generate discussion questions from video content"""
        types = {
            "general": "综合讨论问题，涵盖理解、应用、分析",
            "socratic": "苏格拉底式提问，引导深入思考",
            "debate": "辩论性问题，需要立场和论证",
            "reflective": "反思性问题，连接个人经验",
            "critical": "批判性思考问题，质疑和评估",
            "creative": "创造性问题，激发新想法"
        }

        prompt = f"""基于以下视频内容，生成{num_questions}个{types.get(discussion_type, discussion_type)}。

内容：
{transcript[:8000]}

讨论问题要求：
1. 开放性问题，没有唯一正确答案
2. 促进深入思考和讨论
3. 连接现实应用
4. 适合小组讨论

返回JSON数组，每个问题包含：
- question: 讨论问题
- type: 问题类型（understanding/application/analysis/evaluation/synthesis）
- difficulty: 难度（easy/medium/hard）
- time_needed: 建议讨论时间（分钟）
- follow_up_questions: 追问问题列表
- discussion_tips: 讨论建议
- expected_insights: 期望得到的见解
- connection_prompt: 连接个人经验的提示

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

    def generate_socratic_dialogue(self, topic: str, transcript: str = "", language: str = "中文") -> Dict[str, Any]:
        """Generate a Socratic dialogue template for exploring a topic"""
        context = f"\n基于以下内容:\n{transcript[:4000]}" if transcript else ""

        prompt = f"""使用苏格拉底方法设计关于"{topic}"的探究对话。{context}

苏格拉底方法特点：
1. 通过提问引导发现
2. 揭示假设和矛盾
3. 追问"为什么"
4. 不直接给答案

返回JSON格式：
1. opening_question: 开场问题（引入话题）
2. clarifying_questions: 澄清问题数组
3. assumption_probing: 探测假设的问题
4. reason_evidence: 询问理由证据的问题
5. perspective_questions: 探索不同视角的问题
6. implication_questions: 探讨影响/后果的问题
7. meta_questions: 关于问题本身的问题
8. dialogue_example: 对话示例
9. facilitator_notes: 引导者注意事项

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"raw_dialogue": response}

    def generate_think_pair_share(self, transcript: str, num_topics: int = 5, language: str = "中文") -> List[Dict[str, Any]]:
        """Generate Think-Pair-Share activity prompts"""
        prompt = f"""基于以下内容，设计{num_topics}个"思考-配对-分享"活动。

内容：
{transcript[:6000]}

Think-Pair-Share流程：
1. Think: 独立思考（2-3分钟）
2. Pair: 两人讨论（3-5分钟）
3. Share: 全班分享

返回JSON数组，每个活动包含：
- topic: 讨论话题
- think_prompt: 独立思考的问题
- pair_prompts: 配对讨论的问题
- share_format: 分享格式建议
- time_allocation: 时间分配
- expected_outcomes: 预期成果

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

    def generate_fishbowl_discussion(self, transcript: str, language: str = "中文") -> Dict[str, Any]:
        """Generate a fishbowl discussion setup"""
        prompt = f"""为以下内容设计鱼缸式讨论（Fishbowl Discussion）。

内容：
{transcript[:6000]}

鱼缸讨论：
- 内圈：积极讨论者
- 外圈：观察者，可随时加入

返回JSON格式：
1. discussion_topic: 核心话题
2. inner_circle:
   - roles: 内圈角色分配
   - starter_question: 开始问题
   - discussion_points: 讨论要点

3. outer_circle:
   - observation_tasks: 观察任务
   - entry_signals: 加入信号
   - reflection_questions: 反思问题

4. rotation_rules: 轮换规则
5. debrief_questions: 总结问题
6. time_structure: 时间结构

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"raw_setup": response}

    def generate_world_cafe(self, transcript: str, num_tables: int = 4, language: str = "中文") -> Dict[str, Any]:
        """Generate World Café discussion setup"""
        prompt = f"""为以下内容设计世界咖啡馆（World Café）讨论活动。

内容：
{transcript[:6000]}

世界咖啡馆：
- 多个讨论桌
- 参与者轮换
- 每桌一个话题
- 建立在前人讨论基础上

设计{num_tables}个讨论桌，返回JSON格式：
1. theme: 整体主题
2. tables: 桌子数组，每桌包含：
   - table_number: 桌号
   - topic: 话题
   - guiding_question: 引导问题
   - table_host_notes: 桌长提示
   - materials_needed: 所需材料

3. rounds: 轮次设计
4. harvest: 收获环节设计
5. facilitator_script: 主持人脚本

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"raw_setup": response}

    def generate_icebreakers(self, topic: str, group_size: int = 8, language: str = "中文") -> List[Dict[str, Any]]:
        """Generate icebreaker activities related to topic"""
        prompt = f"""为关于"{topic}"的学习小组（{group_size}人）设计破冰活动。

要求：
1. 与学习主题相关
2. 促进互相了解
3. 建立学习氛围
4. 时间适中（5-15分钟）

返回JSON数组，每个活动包含：
- name: 活动名称
- duration: 时长
- instructions: 说明
- materials: 所需材料
- connection_to_topic: 与主题的联系
- energy_level: 能量级别（low/medium/high）

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

    def generate_reflection_prompts(self, transcript: str, language: str = "中文") -> List[Dict[str, str]]:
        """Generate reflection prompts for individual or group reflection"""
        prompt = f"""基于以下内容，生成反思提示。

内容：
{transcript[:6000]}

反思类型：
1. 内容反思 - 学到了什么
2. 过程反思 - 如何学习的
3. 连接反思 - 与已知的联系
4. 应用反思 - 如何应用
5. 情感反思 - 感受如何

返回JSON数组，每个提示包含：
- type: 反思类型
- prompt: 反思提示
- journaling_prompt: 日记写作提示
- discussion_version: 小组讨论版本

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

    def generate_discussion_protocol(self, transcript: str, discussion_time: int = 30, language: str = "中文") -> Dict[str, Any]:
        """Generate a complete discussion protocol/agenda"""
        prompt = f"""基于以下内容，设计一个{discussion_time}分钟的完整讨论议程。

内容：
{transcript[:6000]}

返回JSON格式：
1. objectives: 讨论目标
2. agenda: 议程数组，每项包含：
   - time: 时间段
   - activity: 活动
   - description: 描述
   - facilitator_actions: 主持人行动
   - participant_actions: 参与者行动

3. materials: 所需材料
4. room_setup: 场地布置
5. ground_rules: 基本规则
6. contingency_plans: 应急方案
7. success_indicators: 成功指标

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"raw_protocol": response}

    def export_discussion_guide(self, questions: List[Dict], format: str = "markdown") -> str:
        """Export discussion questions in various formats"""
        if format == "markdown":
            md = "# 讨论问题指南\n\n"

            for i, q in enumerate(questions, 1):
                md += f"## 问题 {i}\n\n"
                md += f"**{q.get('question', '')}**\n\n"
                md += f"- 类型: {q.get('type', 'N/A')}\n"
                md += f"- 难度: {q.get('difficulty', 'N/A')}\n"
                md += f"- 建议时间: {q.get('time_needed', 'N/A')}分钟\n\n"

                if q.get('follow_up_questions'):
                    md += "**追问:**\n"
                    for fq in q['follow_up_questions']:
                        md += f"- {fq}\n"
                    md += "\n"

                if q.get('discussion_tips'):
                    md += f"**讨论提示:** {q['discussion_tips']}\n\n"

                md += "---\n\n"

            return md

        elif format == "json":
            return json.dumps(questions, ensure_ascii=False, indent=2)

        return str(questions)
