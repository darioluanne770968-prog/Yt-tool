"""
Video Chat - Multi-turn conversation assistant based on video content
视频多轮对话助手 - 基于视频内容进行持续的多轮对话，保持上下文记忆
"""

from typing import List, Dict, Optional
from .ai_client import get_ai_client


class VideoChat:
    """Video-based multi-turn conversation assistant"""

    def __init__(self, provider: str = None):
        """
        Initialize video chat assistant

        Args:
            provider: AI provider ('openai', 'anthropic', or 'gemini')
        """
        self.ai = get_ai_client(provider)
        self.conversation_history: List[Dict[str, str]] = []
        self.video_context: str = ""
        self.video_title: str = ""

    def set_video_context(self, transcript: str, title: str = "", metadata: dict = None):
        """
        Set video context for the conversation

        Args:
            transcript: Video transcript text
            title: Video title
            metadata: Additional video metadata (duration, channel, etc.)
        """
        self.video_context = transcript
        self.video_title = title
        self.metadata = metadata or {}
        self.conversation_history = []

    def chat(
        self,
        message: str,
        language: str = "中文",
        max_history: int = 10,
    ) -> str:
        """
        Send a message and get AI response based on video content

        Args:
            message: User message
            language: Response language
            max_history: Maximum conversation history to keep

        Returns:
            AI response
        """
        if not self.video_context:
            return "请先设置视频内容。Please set video context first using set_video_context()."

        # Build conversation context
        system_prompt = self._build_system_prompt(language)

        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": message
        })

        # Build full prompt with history
        full_prompt = self._build_conversation_prompt(max_history)

        # Get AI response
        response = self.ai.chat(
            prompt=full_prompt,
            system_prompt=system_prompt,
            temperature=0.7,
        )

        # Add assistant response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": response
        })

        # Trim history if too long
        if len(self.conversation_history) > max_history * 2:
            self.conversation_history = self.conversation_history[-(max_history * 2):]

        return response

    def _build_system_prompt(self, language: str) -> str:
        """Build system prompt for conversation"""
        return f"""你是一个专业的视频内容助手。你的任务是基于用户提供的视频内容，回答用户的问题并进行深入讨论。

视频信息：
- 标题：{self.video_title or '未知'}
- 时长：{self.metadata.get('duration', '未知')}
- 频道：{self.metadata.get('channel', '未知')}

视频内容（字幕）：
{self._truncate_context(self.video_context)}

要求：
1. 基于视频内容回答问题，如果问题超出视频范围，请明确说明
2. 如果用户提到时间戳（如 3:25），尝试定位到相应内容
3. 保持友好、专业的对话风格
4. 记住之前的对话内容，保持上下文连贯
5. 使用{language}回复

你可以：
- 解释视频中的概念
- 总结特定部分的内容
- 回答关于视频的任何问题
- 提供基于视频内容的扩展信息"""

    def _build_conversation_prompt(self, max_history: int) -> str:
        """Build conversation prompt with history"""
        # Get recent history
        recent_history = self.conversation_history[-(max_history * 2):]

        # Format conversation
        conversation_parts = []
        for msg in recent_history[:-1]:  # Exclude the last user message
            role = "用户" if msg["role"] == "user" else "助手"
            conversation_parts.append(f"{role}：{msg['content']}")

        # Build prompt
        if conversation_parts:
            history_text = "\n".join(conversation_parts)
            current_message = self.conversation_history[-1]["content"]
            return f"""之前的对话：
{history_text}

当前问题：
用户：{current_message}

请基于视频内容和对话上下文回答："""
        else:
            return self.conversation_history[-1]["content"]

    def _truncate_context(self, text: str, max_chars: int = 25000) -> str:
        """Truncate context if too long"""
        if len(text) <= max_chars:
            return text
        return text[:max_chars] + "\n\n[内容过长，已截断...]"

    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get conversation history"""
        return self.conversation_history.copy()

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []

    def ask_about_timestamp(self, timestamp: str, language: str = "中文") -> str:
        """
        Ask about content at a specific timestamp

        Args:
            timestamp: Time in format "MM:SS" or "HH:MM:SS"
            language: Response language

        Returns:
            AI response about that part of the video
        """
        message = f"请解释视频中 {timestamp} 时间点附近讲述的内容"
        return self.chat(message, language)

    def summarize_section(
        self,
        start_time: str,
        end_time: str,
        language: str = "中文"
    ) -> str:
        """
        Summarize a specific section of the video

        Args:
            start_time: Start time (MM:SS or HH:MM:SS)
            end_time: End time (MM:SS or HH:MM:SS)
            language: Response language

        Returns:
            Summary of the section
        """
        message = f"请总结视频从 {start_time} 到 {end_time} 这段时间的内容"
        return self.chat(message, language)

    def explain_concept(self, concept: str, language: str = "中文") -> str:
        """
        Explain a concept mentioned in the video

        Args:
            concept: Concept to explain
            language: Response language

        Returns:
            Explanation of the concept
        """
        message = f"请详细解释视频中提到的「{concept}」这个概念"
        return self.chat(message, language)

    def get_examples(self, topic: str, language: str = "中文") -> str:
        """
        Get examples related to a topic in the video

        Args:
            topic: Topic to find examples for
            language: Response language

        Returns:
            Examples from the video
        """
        message = f"视频中有哪些关于「{topic}」的例子或案例？"
        return self.chat(message, language)

    def compare_points(self, point1: str, point2: str, language: str = "中文") -> str:
        """
        Compare two points or concepts from the video

        Args:
            point1: First point
            point2: Second point
            language: Response language

        Returns:
            Comparison analysis
        """
        message = f"请对比视频中提到的「{point1}」和「{point2}」"
        return self.chat(message, language)

    def export_conversation(self, format: str = "markdown") -> str:
        """
        Export conversation history

        Args:
            format: Export format ('markdown', 'text', 'json')

        Returns:
            Formatted conversation
        """
        if format == "json":
            import json
            return json.dumps({
                "video_title": self.video_title,
                "conversation": self.conversation_history
            }, ensure_ascii=False, indent=2)

        lines = []
        if format == "markdown":
            lines.append(f"# 视频对话记录")
            lines.append(f"\n**视频标题**: {self.video_title or '未知'}\n")
            lines.append("---\n")

            for msg in self.conversation_history:
                if msg["role"] == "user":
                    lines.append(f"**🙋 用户**: {msg['content']}\n")
                else:
                    lines.append(f"**🤖 助手**: {msg['content']}\n")
                lines.append("")
        else:
            lines.append(f"视频对话记录 - {self.video_title or '未知'}")
            lines.append("=" * 50)

            for msg in self.conversation_history:
                role = "用户" if msg["role"] == "user" else "助手"
                lines.append(f"\n{role}：\n{msg['content']}")

        return "\n".join(lines)


def create_video_chat(
    transcript: str,
    title: str = "",
    metadata: dict = None,
    provider: str = None
) -> VideoChat:
    """
    Factory function to create a video chat instance

    Args:
        transcript: Video transcript
        title: Video title
        metadata: Video metadata
        provider: AI provider

    Returns:
        Configured VideoChat instance
    """
    chat = VideoChat(provider)
    chat.set_video_context(transcript, title, metadata)
    return chat
