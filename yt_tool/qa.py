"""
AI-powered Q&A based on video content
"""

from typing import Optional
from .ai_client import get_ai_client


QA_SYSTEM_PROMPT = """你是一个基于视频内容的智能问答助手。你只能根据提供的视频字幕内容来回答问题。

规则：
1. 只回答与视频内容相关的问题
2. 如果问题的答案不在视频内容中，明确告知用户
3. 引用视频中的具体内容来支持你的回答
4. 如果可能，提供相关的时间戳
5. 使用清晰、简洁的语言回答"""


QA_PROMPT_TEMPLATE = """以下是YouTube视频的字幕内容：

{transcript}

---

用户问题：{question}

请根据视频内容回答这个问题。如果视频中没有相关信息，请说明。
请用{language}回答。"""


class VideoQA:
    """Question & Answer system based on video content"""

    def __init__(self, transcript: str, provider: str = None):
        """
        Initialize Q&A system

        Args:
            transcript: Video transcript text
            provider: AI provider ('openai' or 'anthropic')
        """
        self.transcript = transcript
        self.ai = get_ai_client(provider)
        self.conversation_history = []

    def ask(self, question: str, language: str = "中文") -> str:
        """
        Ask a question about the video

        Args:
            question: User's question
            language: Response language

        Returns:
            Answer based on video content
        """
        prompt = QA_PROMPT_TEMPLATE.format(
            transcript=self._get_relevant_context(question),
            question=question,
            language=language,
        )

        answer = self.ai.chat(
            prompt=prompt,
            system_prompt=QA_SYSTEM_PROMPT,
            temperature=0.5,
        )

        # Store in conversation history
        self.conversation_history.append({"question": question, "answer": answer})

        return answer

    def ask_followup(self, question: str, language: str = "中文") -> str:
        """
        Ask a follow-up question with conversation context

        Args:
            question: Follow-up question
            language: Response language

        Returns:
            Answer considering previous conversation
        """
        # Build conversation context
        context = ""
        if self.conversation_history:
            context = "\n\n之前的对话：\n"
            for qa in self.conversation_history[-3:]:  # Last 3 Q&As
                context += f"问：{qa['question']}\n答：{qa['answer'][:200]}...\n\n"

        prompt = f"""以下是YouTube视频的字幕内容：

{self._get_relevant_context(question)}

{context}
---

用户的后续问题：{question}

请根据视频内容和之前的对话回答这个问题。
请用{language}回答。"""

        answer = self.ai.chat(
            prompt=prompt,
            system_prompt=QA_SYSTEM_PROMPT,
            temperature=0.5,
        )

        self.conversation_history.append({"question": question, "answer": answer})

        return answer

    def _get_relevant_context(self, question: str, max_chars: int = 20000) -> str:
        """
        Get relevant portion of transcript for the question

        For now, returns truncated transcript. Could be enhanced with
        semantic search in the future.
        """
        if len(self.transcript) <= max_chars:
            return self.transcript

        # Simple truncation for now
        return self.transcript[:max_chars] + "\n\n[内容过长，已截断...]"

    def get_history(self) -> list[dict]:
        """Get conversation history"""
        return self.conversation_history.copy()

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []

    def suggest_questions(self, language: str = "中文") -> list[str]:
        """
        Suggest questions based on video content

        Args:
            language: Language for suggestions

        Returns:
            List of suggested questions
        """
        prompt = f"""基于以下视频内容，建议5个用户可能想问的问题：

{self._get_relevant_context("", max_chars=10000)}

请用{language}输出5个问题，每行一个问题，不要编号。"""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt="你是一个帮助用户理解视频内容的助手。",
            temperature=0.7,
        )

        # Parse questions from response
        questions = [
            q.strip().lstrip("0123456789.、-) ")
            for q in response.strip().split("\n")
            if q.strip()
        ]

        return questions[:5]
