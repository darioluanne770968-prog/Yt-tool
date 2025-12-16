"""
Active Recall System - 主动回忆测试系统
Generate active recall exercises and tests for better retention
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Any, Optional
from .ai_client import get_ai_client


class ActiveRecallSystem:
    """Generate active recall tests and exercises"""

    def __init__(self, storage_path: str = ".active_recall.json"):
        self.ai_client = get_ai_client()
        self.storage_path = storage_path
        self.data = self._load_data()

    def _load_data(self) -> Dict:
        """Load recall data from file"""
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "questions": [],
                "sessions": [],
                "performance": {}
            }

    def _save_data(self):
        """Save recall data to file"""
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2, default=str)

    def generate_recall_questions(self, transcript: str, num_questions: int = 10, difficulty_mix: str = "balanced", language: str = "中文") -> List[Dict[str, Any]]:
        """Generate active recall questions from content"""
        difficulty_instruction = {
            "easy": "全部简单题（直接回忆）",
            "balanced": "混合难度（40%简单，40%中等，20%困难）",
            "hard": "全部困难题（分析应用）",
            "progressive": "由易到难递进"
        }.get(difficulty_mix, "混合难度")

        prompt = f"""从以下视频内容生成{num_questions}道主动回忆问题。

难度要求：{difficulty_instruction}

内容：
{transcript[:8000]}

问题类型要求：
1. 填空题 - 关键信息填空
2. 简答题 - 用自己的话解释
3. 列举题 - 列出要点
4. 比较题 - 对比分析
5. 应用题 - 实际应用场景

返回JSON数组，每题包含：
- id: 问题ID
- type: 题型（fill_blank/short_answer/list/compare/apply）
- question: 问题
- hint: 提示（可选显示）
- answer: 参考答案
- key_points: 答案要点
- difficulty: 难度（easy/medium/hard）
- cognitive_level: 认知层次（remember/understand/apply/analyze）
- topic: 相关话题
- time_limit: 建议回答时间（秒）

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            if json_start != -1 and json_end > json_start:
                questions = json.loads(response[json_start:json_end])
                # Add metadata
                for q in questions:
                    q["created_at"] = datetime.now().isoformat()
                    q["attempts"] = 0
                    q["success_rate"] = 0

                self.data["questions"].extend(questions)
                self._save_data()
                return questions
        except json.JSONDecodeError:
            pass

        return []

    def generate_blank_filling(self, transcript: str, num_blanks: int = 5, language: str = "中文") -> List[Dict[str, Any]]:
        """Generate fill-in-the-blank exercises"""
        prompt = f"""从以下内容生成{num_blanks}道填空题。

内容：
{transcript[:6000]}

要求：
1. 空格应该是关键概念或重要信息
2. 上下文足够推断答案
3. 每题只有1-2个空

返回JSON数组，每题包含：
- sentence: 带空格的句子（用 ___ 表示空格）
- blanks: 空格答案数组
- context: 帮助理解的上下文
- difficulty: 难度

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

    def generate_retrieval_practice(self, transcript: str, language: str = "中文") -> Dict[str, Any]:
        """Generate a complete retrieval practice session"""
        prompt = f"""创建一个完整的检索练习（Retrieval Practice）会话。

内容：
{transcript[:8000]}

检索练习包含：
1. 自由回忆 - 不看材料写出所有记得的内容
2. 提示回忆 - 根据提示回忆
3. 识别测试 - 判断陈述正确与否
4. 重组测试 - 将打乱的要点排序

返回JSON格式：
1. free_recall:
   - instruction: 指导语
   - prompt: 提示问题
   - expected_points: 期望回忆出的要点

2. cued_recall: 提示回忆数组
   - cue: 提示
   - expected_response: 期望回答

3. recognition: 识别判断数组
   - statement: 陈述
   - is_correct: 是否正确
   - explanation: 解释

4. sequencing:
   - items: 需要排序的项目（打乱）
   - correct_order: 正确顺序
   - ordering_principle: 排序依据

5. elaboration: 深化问题
   - questions: 需要展开回答的问题

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"raw_practice": response}

    def generate_brain_dump_exercise(self, topic: str, time_limit: int = 5, language: str = "中文") -> Dict[str, Any]:
        """Generate a brain dump exercise"""
        return {
            "exercise_type": "brain_dump",
            "topic": topic,
            "time_limit_minutes": time_limit,
            "instructions": f"""
# 大脑倾泻练习

**话题:** {topic}
**时间限制:** {time_limit}分钟

## 指导

1. 设置一个{time_limit}分钟的计时器
2. 不看任何笔记或材料
3. 写下所有你能回忆起的关于"{topic}"的内容
4. 不要担心组织或格式，只管写
5. 时间到后停止

## 完成后

1. 回顾你的笔记
2. 标记你不确定的内容
3. 与原材料对比
4. 识别遗漏的关键点
5. 重新学习遗漏的内容

**开始计时后开始书写！**
""",
            "reflection_questions": [
                "你能回忆起多少百分比的内容？",
                "哪些部分最容易回忆？",
                "哪些部分完全遗忘了？",
                "下次复习应该重点关注什么？"
            ]
        }

    def generate_interleaved_practice(self, topics: List[Dict], language: str = "中文") -> List[Dict[str, Any]]:
        """Generate interleaved practice mixing multiple topics"""
        prompt = f"""为以下多个话题创建交替练习（Interleaved Practice）。

话题：
{json.dumps(topics, ensure_ascii=False)}

交替练习原则：
1. 不同话题的问题混合出现
2. 强制大脑在不同概念间切换
3. 增加"可取难度"提升长期记忆

为每个话题生成2-3个问题，然后随机混合排列。

返回JSON数组，每题包含：
- topic: 所属话题
- question: 问题
- answer: 答案
- switch_difficulty: 切换难度（与前一题话题相关性）

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            if json_start != -1 and json_end > json_start:
                questions = json.loads(response[json_start:json_end])
                random.shuffle(questions)  # Additional shuffle
                return questions
        except json.JSONDecodeError:
            pass

        return []

    def generate_elaborative_interrogation(self, transcript: str, language: str = "中文") -> List[Dict[str, Any]]:
        """Generate elaborative interrogation questions (Why? How?)"""
        prompt = f"""使用精细化追问法（Elaborative Interrogation）生成深度问题。

内容：
{transcript[:6000]}

精细化追问特点：
1. 问"为什么"和"如何"
2. 连接新知识与已有知识
3. 要求解释机制和原因
4. 促进深度理解

返回JSON数组，每个包含：
- fact: 原始事实/陈述
- why_question: 为什么问题
- how_question: 如何问题
- connection_question: 与已知知识的连接问题
- example_answer: 示例答案
- depth_level: 深度层次（1-5）

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

    def create_recall_session(self, num_questions: int = 10) -> Dict[str, Any]:
        """Create a recall session from stored questions"""
        if not self.data["questions"]:
            return {"error": "No questions available. Generate questions first."}

        # Select questions prioritizing those with lower success rates
        available = self.data["questions"].copy()
        available.sort(key=lambda q: q.get("success_rate", 0))

        selected = available[:num_questions]
        random.shuffle(selected)

        session = {
            "session_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "created_at": datetime.now().isoformat(),
            "questions": selected,
            "total_questions": len(selected),
            "completed": False,
            "results": []
        }

        self.data["sessions"].append(session)
        self._save_data()

        return session

    def record_answer(self, session_id: str, question_id: str, user_answer: str, is_correct: bool):
        """Record user's answer and update statistics"""
        # Find session
        session = None
        for s in self.data["sessions"]:
            if s["session_id"] == session_id:
                session = s
                break

        if not session:
            return {"error": "Session not found"}

        # Record result
        session["results"].append({
            "question_id": question_id,
            "user_answer": user_answer,
            "is_correct": is_correct,
            "timestamp": datetime.now().isoformat()
        })

        # Update question statistics
        for q in self.data["questions"]:
            if q.get("id") == question_id:
                q["attempts"] = q.get("attempts", 0) + 1
                correct_count = q.get("correct_count", 0) + (1 if is_correct else 0)
                q["correct_count"] = correct_count
                q["success_rate"] = correct_count / q["attempts"]
                break

        self._save_data()

        return {"recorded": True}

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get overall performance statistics"""
        total_questions = len(self.data["questions"])
        total_sessions = len(self.data["sessions"])

        if not self.data["sessions"]:
            return {
                "total_questions": total_questions,
                "total_sessions": 0,
                "average_accuracy": 0,
                "topics_mastered": [],
                "topics_to_review": []
            }

        # Calculate accuracy across all sessions
        total_answers = 0
        correct_answers = 0
        topic_performance = {}

        for session in self.data["sessions"]:
            for result in session.get("results", []):
                total_answers += 1
                if result.get("is_correct"):
                    correct_answers += 1

        # Topic-level analysis
        for q in self.data["questions"]:
            topic = q.get("topic", "general")
            if topic not in topic_performance:
                topic_performance[topic] = {"attempts": 0, "correct": 0}
            topic_performance[topic]["attempts"] += q.get("attempts", 0)
            topic_performance[topic]["correct"] += q.get("correct_count", 0)

        mastered = []
        to_review = []
        for topic, perf in topic_performance.items():
            if perf["attempts"] > 0:
                rate = perf["correct"] / perf["attempts"]
                if rate >= 0.8:
                    mastered.append(topic)
                elif rate < 0.6:
                    to_review.append(topic)

        return {
            "total_questions": total_questions,
            "total_sessions": total_sessions,
            "total_answers": total_answers,
            "average_accuracy": correct_answers / total_answers if total_answers > 0 else 0,
            "topics_mastered": mastered,
            "topics_to_review": to_review,
            "topic_breakdown": topic_performance
        }

    def export_questions(self, format: str = "markdown") -> str:
        """Export all questions"""
        if format == "markdown":
            md = "# 主动回忆问题库\n\n"

            for i, q in enumerate(self.data["questions"], 1):
                md += f"## 问题 {i}\n\n"
                md += f"**类型:** {q.get('type', 'N/A')}\n"
                md += f"**难度:** {q.get('difficulty', 'N/A')}\n"
                md += f"**话题:** {q.get('topic', 'N/A')}\n\n"
                md += f"**问题:** {q.get('question', '')}\n\n"
                md += f"<details><summary>查看答案</summary>\n\n"
                md += f"{q.get('answer', '')}\n\n"
                md += "</details>\n\n"
                md += "---\n\n"

            return md

        elif format == "json":
            return json.dumps(self.data["questions"], ensure_ascii=False, indent=2)

        return str(self.data["questions"])
