"""
Debate Simulator - 观点辩论模拟器
Simulate debates with AI taking different perspectives
"""

import json
from typing import Dict, List, Any, Optional
from .ai_client import get_ai_client


class DebateSimulator:
    """Simulate debates on various topics from video content"""

    def __init__(self):
        self.ai_client = get_ai_client()

    def extract_debate_topics(self, transcript: str, num_topics: int = 5, language: str = "中文") -> List[Dict[str, Any]]:
        """Extract potential debate topics from video content"""
        prompt = f"""从以下视频内容中提取{num_topics}个适合辩论的话题。

内容：
{transcript[:8000]}

辩论话题要求：
1. 有明确的正反两面
2. 没有绝对正确的答案
3. 有足够的论据支持双方
4. 与内容相关但可延伸

返回JSON数组，每个话题包含：
- topic: 辩论话题（陈述句形式）
- proposition: 正方立场
- opposition: 反方立场
- context: 背景信息
- key_arguments_for: 支持论据
- key_arguments_against: 反对论据
- complexity: 复杂度（1-10）
- controversy_level: 争议程度（1-10）

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

    def simulate_debate(self, topic: str, rounds: int = 3, language: str = "中文") -> Dict[str, Any]:
        """Simulate a complete debate between AI debaters"""
        prompt = f"""模拟一场关于"{topic}"的辩论。

辩论设置：
- 共{rounds}轮
- 每轮：正方发言 → 反方发言 → 交叉质询
- 包含开场陈述和结辩

返回JSON格式：
1. debate_topic: 辩论主题
2. proposition:
   - position: 立场
   - debater_persona: 辩手人设

3. opposition:
   - position: 立场
   - debater_persona: 辩手人设

4. opening_statements:
   - proposition: 正方开场
   - opposition: 反方开场

5. rounds: 辩论轮次数组，每轮包含：
   - round_number: 轮次
   - proposition_argument: 正方论述
   - opposition_argument: 反方论述
   - cross_examination: 交叉质询
   - key_clash: 关键冲突点

6. closing_statements:
   - proposition: 正方结辩
   - opposition: 反方结辩

7. judges_notes:
   - key_arguments: 关键论点
   - strongest_points: 最强论点
   - weakest_points: 最弱论点
   - suggested_winner: 建议获胜方及理由

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"raw_debate": response}

    def generate_debate_prep(self, topic: str, side: str = "both", language: str = "中文") -> Dict[str, Any]:
        """Generate debate preparation materials"""
        sides = "正反双方" if side == "both" else ("正方" if side == "pro" else "反方")

        prompt = f"""为辩题"{topic}"准备{sides}的辩论材料。

返回JSON格式：
1. topic_analysis:
   - definition: 关键概念定义
   - scope: 辩论范围
   - burden_of_proof: 举证责任

2. {"pro_case" if side in ["both", "pro"] else ""}:
   - thesis: 核心论点
   - arguments: 论据数组，每个包含：
     - claim: 主张
     - warrant: 理由
     - impact: 影响
     - evidence: 证据
   - preemptive_rebuttals: 预先反驳

3. {"con_case" if side in ["both", "con"] else ""}:
   - thesis: 核心论点
   - arguments: 论据数组
   - preemptive_rebuttals: 预先反驳

4. clash_points: 交锋点
5. questions_to_ask: 质询问题
6. questions_to_prepare: 需要准备回答的问题
7. evidence_needed: 需要搜集的证据

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"raw_prep": response}

    def devil_advocate(self, argument: str, language: str = "中文") -> Dict[str, Any]:
        """Play devil's advocate against an argument"""
        prompt = f"""扮演魔鬼代言人，对以下论点进行挑战。

论点：{argument}

请：
1. 找出论点的漏洞
2. 提出反驳
3. 质疑假设
4. 提供反例

返回JSON格式：
1. original_argument: 原论点
2. weaknesses: 弱点列表
3. counterarguments: 反驳论点数组
4. assumptions_challenged: 被挑战的假设
5. counterexamples: 反例
6. questions_to_ponder: 值得思考的问题
7. steelman_version: 强化版论点（如何改进）

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

    def generate_cross_examination(self, topic: str, position: str, language: str = "中文") -> List[Dict[str, str]]:
        """Generate cross-examination questions"""
        prompt = f"""为辩题"{topic}"中的{position}立场设计交叉质询问题。

问题策略：
1. 暴露矛盾
2. 逼迫承认
3. 引入己方论点
4. 质疑证据

返回JSON数组，每个问题包含：
- question: 问题
- purpose: 目的
- expected_answer: 预期回答
- follow_up: 追问（如果对方如何回答）
- trap_potential: 陷阱潜力说明

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

    def evaluate_argument(self, argument: str, language: str = "中文") -> Dict[str, Any]:
        """Evaluate the strength of an argument"""
        prompt = f"""评估以下论证的强度。

论证：{argument}

评估维度：
1. 逻辑性
2. 证据支持
3. 说服力
4. 反驳难度

返回JSON格式：
1. argument_structure:
   - claim: 主张
   - reasoning: 推理
   - evidence: 证据

2. scores:
   - logic: 逻辑分（1-10）
   - evidence: 证据分（1-10）
   - persuasion: 说服力分（1-10）
   - originality: 原创性分（1-10）
   - overall: 总分

3. strengths: 优点
4. weaknesses: 缺点
5. logical_fallacies: 逻辑谬误（如有）
6. improvement_suggestions: 改进建议
7. rebuttal_vulnerability: 被反驳的脆弱点

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"raw_evaluation": response}

    def generate_rebuttals(self, argument: str, language: str = "中文") -> List[Dict[str, Any]]:
        """Generate possible rebuttals to an argument"""
        prompt = f"""为以下论点生成多种反驳方式。

论点：{argument}

反驳类型：
1. 直接反驳
2. 削弱前提
3. 质疑因果
4. 提供反例
5. 转化框架

返回JSON数组，每个反驳包含：
- type: 反驳类型
- rebuttal: 反驳内容
- strength: 强度（1-10）
- follow_up: 对方可能的回应
- counter_counter: 对回应的再反驳

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

    def simulate_socratic_debate(self, topic: str, language: str = "中文") -> Dict[str, Any]:
        """Simulate a Socratic-style debate/dialogue"""
        prompt = f"""模拟关于"{topic}"的苏格拉底式对话。

角色：
- 苏格拉底：通过提问引导
- 对话者：持有观点，被引导思考

对话特点：
1. 从对话者的观点开始
2. 通过提问揭示矛盾
3. 逐步深入核心问题
4. 达到新的理解

返回JSON格式：
1. initial_position: 对话者初始立场
2. dialogue: 对话数组，每条包含：
   - speaker: 说话人
   - text: 内容
   - purpose: 对话目的（如适用）

3. key_moments: 关键转折点
4. final_insight: 最终洞见
5. lessons_learned: 学到的教训
6. unresolved_questions: 未解决的问题

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

    def generate_perspective_switch(self, topic: str, num_perspectives: int = 4, language: str = "中文") -> List[Dict[str, Any]]:
        """Generate multiple perspectives on a topic"""
        prompt = f"""为话题"{topic}"提供{num_perspectives}种不同视角的观点。

视角类型示例：
- 乐观主义者 vs 悲观主义者
- 实用主义者 vs 理想主义者
- 专家 vs 普通人
- 短期 vs 长期
- 个人 vs 社会

返回JSON数组，每个视角包含：
- perspective_name: 视角名称
- persona: 持有者人设
- core_belief: 核心信念
- key_arguments: 关键论点
- values_prioritized: 优先的价值观
- blind_spots: 盲点
- synthesis_point: 可以综合的点

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

    def export_debate(self, debate: Dict, format: str = "markdown") -> str:
        """Export debate in various formats"""
        if format == "markdown":
            md = f"# 辩论记录: {debate.get('debate_topic', '未知话题')}\n\n"

            if "proposition" in debate:
                md += f"## 正方: {debate['proposition'].get('position', '')}\n\n"
            if "opposition" in debate:
                md += f"## 反方: {debate['opposition'].get('position', '')}\n\n"

            md += "---\n\n"

            if "opening_statements" in debate:
                md += "## 开场陈述\n\n"
                md += f"**正方:** {debate['opening_statements'].get('proposition', '')}\n\n"
                md += f"**反方:** {debate['opening_statements'].get('opposition', '')}\n\n"

            if "rounds" in debate:
                for r in debate["rounds"]:
                    md += f"## 第{r.get('round_number', '?')}轮\n\n"
                    md += f"**正方论述:** {r.get('proposition_argument', '')}\n\n"
                    md += f"**反方论述:** {r.get('opposition_argument', '')}\n\n"
                    if r.get('key_clash'):
                        md += f"**关键冲突:** {r['key_clash']}\n\n"
                    md += "---\n\n"

            if "closing_statements" in debate:
                md += "## 结辩\n\n"
                md += f"**正方:** {debate['closing_statements'].get('proposition', '')}\n\n"
                md += f"**反方:** {debate['closing_statements'].get('opposition', '')}\n\n"

            if "judges_notes" in debate:
                md += "## 评委点评\n\n"
                jn = debate["judges_notes"]
                md += f"**建议获胜方:** {jn.get('suggested_winner', 'N/A')}\n\n"

            return md

        elif format == "json":
            return json.dumps(debate, ensure_ascii=False, indent=2)

        return str(debate)
