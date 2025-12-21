"""
Virtual Tutor - AI-powered one-on-one tutoring based on video content
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Optional
from .ai_client import get_ai_client


class VirtualTutor:
    """AI virtual tutor for personalized learning"""

    def __init__(self, data_dir: str = ".yt_tool_data"):
        self.client = get_ai_client()
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.sessions_file = self.data_dir / "tutor_sessions.json"
        self.sessions = self._load_sessions()
        self.current_context = ""
        self.conversation_history = []

    def _load_sessions(self) -> dict:
        if self.sessions_file.exists():
            return json.loads(self.sessions_file.read_text(encoding="utf-8"))
        return {"sessions": [], "learner_profile": {}}

    def _save_sessions(self):
        self.sessions_file.write_text(
            json.dumps(self.sessions, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def start_session(self, transcript: str, video_title: str = "", language: str = "中文") -> dict:
        """Start a new tutoring session"""
        self.current_context = transcript
        self.conversation_history = []

        prompt = f"""你是一位专业的AI导师，基于以下视频内容为学生提供一对一辅导。

视频标题：{video_title}
视频内容：
{transcript[:8000]}

请用{language}：
1. 简要介绍这个视频的主题和学习目标
2. 评估这个内容的难度级别
3. 提供3个建议的学习问题帮助学生开始
4. 说明你将如何帮助学生理解这个内容

以友好、鼓励的语气回应。"""

        response = self.client.generate(prompt)

        session = {
            "id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "video_title": video_title,
            "started_at": datetime.now().isoformat(),
            "messages": [],
            "learning_points": []
        }

        self.sessions["sessions"].append(session)
        self._save_sessions()

        return {
            "session_id": session["id"],
            "welcome_message": response,
            "video_title": video_title
        }

    def ask_tutor(self, question: str, language: str = "中文") -> dict:
        """Ask the tutor a question"""
        self.conversation_history.append({"role": "student", "content": question})

        history_text = "\n".join([
            f"{'学生' if m['role'] == 'student' else '导师'}: {m['content']}"
            for m in self.conversation_history[-10:]
        ])

        prompt = f"""你是一位耐心的AI导师，正在辅导学生学习以下内容：

视频内容摘要：
{self.current_context[:6000]}

对话历史：
{history_text}

学生的新问题：{question}

请用{language}回答：
1. 直接回答学生的问题
2. 如果问题涉及视频内容，引用相关部分
3. 使用类比或例子帮助理解
4. 提出一个跟进问题检验理解
5. 给予鼓励和肯定

保持友好、耐心的教学风格。"""

        response = self.client.generate(prompt)

        self.conversation_history.append({"role": "tutor", "content": response})

        # Update session
        if self.sessions["sessions"]:
            self.sessions["sessions"][-1]["messages"].append({
                "question": question,
                "answer": response,
                "timestamp": datetime.now().isoformat()
            })
            self._save_sessions()

        return {
            "answer": response,
            "conversation_length": len(self.conversation_history)
        }

    def explain_concept(self, concept: str, level: str = "beginner", language: str = "中文") -> dict:
        """Explain a specific concept from the video"""
        level_desc = {
            "beginner": "完全的初学者，需要最基础的解释",
            "intermediate": "有一定基础，可以理解中等难度的概念",
            "advanced": "有较深的理解，需要深入的分析"
        }

        prompt = f"""基于以下视频内容，解释概念"{concept}"。

视频内容：
{self.current_context[:6000]}

学生水平：{level_desc.get(level, level_desc["beginner"])}

请用{language}提供：
1. 概念的简单定义（一句话）
2. 详细解释（2-3段）
3. 一个生动的类比或比喻
4. 一个具体的例子
5. 常见的误解和澄清
6. 与视频中其他概念的关联
7. 3个检验理解的问题

使用清晰、易懂的语言。"""

        response = self.client.generate(prompt)

        return {
            "concept": concept,
            "level": level,
            "explanation": response
        }

    def generate_practice(self, topic: str, num_questions: int = 5, language: str = "中文") -> dict:
        """Generate practice questions for a topic"""
        prompt = f"""基于以下视频内容，为主题"{topic}"生成练习题。

视频内容：
{self.current_context[:6000]}

请用{language}生成{num_questions}道练习题，包括：
1. 基础概念题（选择题或填空题）
2. 理解应用题（简答题）
3. 分析思考题（开放性问题）

每道题包含：
- 题目
- 选项（如适用）
- 参考答案
- 解答说明
- 相关知识点

格式清晰，难度递进。"""

        response = self.client.generate(prompt)

        return {
            "topic": topic,
            "num_questions": num_questions,
            "practice": response
        }

    def diagnose_understanding(self, student_answer: str, topic: str, language: str = "中文") -> dict:
        """Diagnose student's understanding based on their answer"""
        prompt = f"""作为AI导师，分析学生对"{topic}"的理解程度。

视频内容：
{self.current_context[:4000]}

学生的回答：
{student_answer}

请用{language}提供：
1. 理解程度评分（1-10分）
2. 正确理解的部分
3. 需要改进的部分
4. 具体的知识漏洞
5. 个性化的学习建议
6. 推荐复习的内容
7. 鼓励和激励的话语

保持建设性和鼓励性的语气。"""

        response = self.client.generate(prompt)

        return {
            "topic": topic,
            "diagnosis": response,
            "timestamp": datetime.now().isoformat()
        }

    def create_study_plan(self, goals: list, duration_days: int = 7, language: str = "中文") -> dict:
        """Create a personalized study plan"""
        goals_text = "\n".join([f"- {g}" for g in goals])

        prompt = f"""基于视频内容和学习目标，创建个性化学习计划。

视频内容：
{self.current_context[:4000]}

学习目标：
{goals_text}

计划时长：{duration_days}天

请用{language}创建详细的学习计划：
1. 每日学习任务
2. 重点复习内容
3. 练习题安排
4. 里程碑和检查点
5. 预期成果
6. 调整建议

格式清晰，任务具体可执行。"""

        response = self.client.generate(prompt)

        plan = {
            "goals": goals,
            "duration_days": duration_days,
            "plan": response,
            "created_at": datetime.now().isoformat()
        }

        return plan

    def get_encouragement(self, progress: float, language: str = "中文") -> str:
        """Get personalized encouragement based on progress"""
        prompt = f"""作为AI导师，为学习进度为{progress*100:.0f}%的学生提供鼓励。

请用{language}：
1. 肯定已取得的进步
2. 提供继续前进的动力
3. 分享一个励志的学习名言
4. 给出下一步的具体建议

语气温暖、真诚、鼓励。"""

        return self.client.generate(prompt)

    def summarize_session(self, language: str = "中文") -> dict:
        """Summarize the current tutoring session"""
        if not self.conversation_history:
            return {"summary": "暂无对话记录"}

        history_text = "\n".join([
            f"{'学生' if m['role'] == 'student' else '导师'}: {m['content'][:200]}"
            for m in self.conversation_history
        ])

        prompt = f"""总结这次辅导课程：

对话记录：
{history_text}

请用{language}提供：
1. 课程主要内容
2. 学生提出的问题
3. 关键学习点
4. 学生的理解程度
5. 建议的后续学习
6. 课程亮点

格式简洁明了。"""

        response = self.client.generate(prompt)

        return {
            "summary": response,
            "messages_count": len(self.conversation_history),
            "session_duration": "N/A"
        }

    def get_learner_profile(self) -> dict:
        """Get the learner's profile based on session history"""
        return self.sessions.get("learner_profile", {})

    def update_learner_profile(self, updates: dict):
        """Update learner profile"""
        if "learner_profile" not in self.sessions:
            self.sessions["learner_profile"] = {}
        self.sessions["learner_profile"].update(updates)
        self._save_sessions()
