"""
QA Bot - 24/7 AI-powered question answering bot based on video content
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from .ai_client import get_ai_client


class QABot:
    """Intelligent Q&A bot for video content"""

    def __init__(self, data_dir: str = ".yt_tool_data"):
        self.client = get_ai_client()
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.qa_file = self.data_dir / "qa_bot_data.json"
        self.data = self._load_data()
        self.knowledge_base = {}
        self.faq_cache = {}

    def _load_data(self) -> dict:
        if self.qa_file.exists():
            return json.loads(self.qa_file.read_text(encoding="utf-8"))
        return {
            "conversations": [],
            "knowledge_base": {},
            "faq": [],
            "unanswered": []
        }

    def _save_data(self):
        self.qa_file.write_text(
            json.dumps(self.data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def load_video_content(self, video_id: str, transcript: str, title: str = ""):
        """Load video content into the bot's knowledge base"""
        self.knowledge_base[video_id] = {
            "transcript": transcript,
            "title": title,
            "loaded_at": datetime.now().isoformat()
        }

        self.data["knowledge_base"][video_id] = {
            "title": title,
            "content_length": len(transcript),
            "loaded_at": datetime.now().isoformat()
        }
        self._save_data()

    def ask(self, question: str, video_id: Optional[str] = None, language: str = "中文") -> dict:
        """Ask a question and get an answer"""
        # Get relevant context
        context = ""
        if video_id and video_id in self.knowledge_base:
            context = self.knowledge_base[video_id]["transcript"][:6000]
            video_title = self.knowledge_base[video_id].get("title", "")
        elif self.knowledge_base:
            # Use all available knowledge
            all_content = []
            for vid, data in self.knowledge_base.items():
                all_content.append(f"[{data.get('title', vid)}]: {data['transcript'][:2000]}")
            context = "\n\n".join(all_content[:3])
            video_title = "多个视频"
        else:
            context = "暂无加载的视频内容"
            video_title = ""

        prompt = f"""你是一个智能问答机器人，基于视频内容回答问题。

视频内容：
{context}

用户问题：{question}

请用{language}回答：

1. 直接回答问题
2. 如果答案在视频内容中，引用相关部分
3. 如果问题超出视频范围，诚实说明并提供一般性指导
4. 提供相关的延伸信息
5. 如有必要，建议用户的后续问题

回答要准确、有帮助、友好。"""

        response = self.client.generate(prompt)

        # Log the conversation
        conversation = {
            "question": question,
            "answer": response,
            "video_id": video_id,
            "timestamp": datetime.now().isoformat()
        }
        self.data["conversations"].append(conversation)
        self._save_data()

        return {
            "question": question,
            "answer": response,
            "source": video_title,
            "confidence": "high" if context else "low"
        }

    def ask_followup(self, question: str, conversation_history: List[Dict], language: str = "中文") -> dict:
        """Ask a follow-up question with conversation context"""
        history_text = "\n".join([
            f"Q: {c['question']}\nA: {c['answer'][:200]}..."
            for c in conversation_history[-5:]
        ])

        context = ""
        if self.knowledge_base:
            vid = list(self.knowledge_base.keys())[0]
            context = self.knowledge_base[vid]["transcript"][:4000]

        prompt = f"""继续回答用户的追问。

视频内容：
{context}

对话历史：
{history_text}

新问题：{question}

请用{language}：
1. 理解问题与之前对话的关联
2. 提供连贯的回答
3. 必要时引用之前的讨论
4. 深入解答"""

        response = self.client.generate(prompt)

        return {
            "question": question,
            "answer": response,
            "is_followup": True
        }

    def generate_faq(self, transcript: str, num_questions: int = 10, language: str = "中文") -> List[Dict]:
        """Generate FAQ based on video content"""
        prompt = f"""基于以下视频内容生成常见问题解答（FAQ）：

视频内容：
{transcript[:6000]}

请用{language}生成{num_questions}个常见问题及其答案：

格式：
Q1: [问题]
A1: [答案]

Q2: [问题]
A2: [答案]

问题应该：
1. 覆盖视频的主要内容
2. 从简单到复杂排列
3. 包含概念解释、应用场景、常见误解等
4. 答案简洁但完整"""

        response = self.client.generate(prompt)

        # Parse FAQ
        faqs = []
        lines = response.split("\n")
        current_q = ""
        current_a = ""

        for line in lines:
            line = line.strip()
            if line.startswith("Q") and ":" in line:
                if current_q and current_a:
                    faqs.append({"question": current_q, "answer": current_a})
                current_q = line.split(":", 1)[1].strip() if ":" in line else line
                current_a = ""
            elif line.startswith("A") and ":" in line:
                current_a = line.split(":", 1)[1].strip() if ":" in line else line

        if current_q and current_a:
            faqs.append({"question": current_q, "answer": current_a})

        self.data["faq"] = faqs
        self._save_data()

        return faqs

    def search_similar_questions(self, question: str, language: str = "中文") -> List[Dict]:
        """Search for similar questions in history"""
        if not self.data.get("conversations"):
            return []

        # Get recent conversations
        recent = self.data["conversations"][-50:]
        questions = [c["question"] for c in recent]

        prompt = f"""从以下问题列表中找出与新问题最相似的3个：

新问题：{question}

历史问题：
{json.dumps(questions, ensure_ascii=False)}

请返回最相似的问题索引（0开始）和相似度（0-1），格式：
索引1,相似度1
索引2,相似度2
索引3,相似度3"""

        response = self.client.generate(prompt)

        similar = []
        try:
            for line in response.strip().split("\n"):
                if "," in line:
                    parts = line.split(",")
                    idx = int(parts[0].strip())
                    similarity = float(parts[1].strip())
                    if 0 <= idx < len(recent):
                        similar.append({
                            "question": recent[idx]["question"],
                            "answer": recent[idx]["answer"],
                            "similarity": similarity
                        })
        except:
            pass

        return similar[:3]

    def rate_answer(self, question: str, answer: str, rating: int, feedback: str = ""):
        """Rate an answer for quality improvement"""
        self.data.setdefault("ratings", []).append({
            "question": question,
            "answer": answer[:200],
            "rating": rating,
            "feedback": feedback,
            "timestamp": datetime.now().isoformat()
        })
        self._save_data()

    def get_unanswered_questions(self) -> List[str]:
        """Get questions that couldn't be answered well"""
        return self.data.get("unanswered", [])

    def explain_term(self, term: str, context: str = "", language: str = "中文") -> dict:
        """Explain a specific term or concept"""
        video_context = ""
        if self.knowledge_base:
            vid = list(self.knowledge_base.keys())[0]
            video_context = self.knowledge_base[vid]["transcript"][:3000]

        prompt = f"""解释术语"{term}"的含义。

视频上下文：
{video_context}

用户提供的上下文：{context}

请用{language}解释：
1. 术语定义
2. 在视频中的含义
3. 简单例子
4. 相关术语"""

        response = self.client.generate(prompt)

        return {
            "term": term,
            "explanation": response
        }

    def get_conversation_summary(self, language: str = "中文") -> dict:
        """Get a summary of all conversations"""
        conversations = self.data.get("conversations", [])

        if not conversations:
            return {"summary": "暂无对话记录", "total": 0}

        questions = [c["question"] for c in conversations[-20:]]

        prompt = f"""总结以下问答对话的主题和趋势：

问题列表：
{json.dumps(questions, ensure_ascii=False)}

请用{language}分析：
1. 主要讨论主题
2. 常见问题类型
3. 用户关注点
4. 建议改进"""

        response = self.client.generate(prompt)

        return {
            "summary": response,
            "total_conversations": len(conversations),
            "recent_count": len(questions)
        }

    def export_knowledge(self) -> dict:
        """Export the bot's knowledge base"""
        return {
            "videos_loaded": len(self.knowledge_base),
            "total_conversations": len(self.data.get("conversations", [])),
            "faq_count": len(self.data.get("faq", [])),
            "knowledge_base": self.data.get("knowledge_base", {})
        }
