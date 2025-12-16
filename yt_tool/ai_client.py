"""
AI client for interacting with OpenAI, Anthropic and Google Gemini APIs
"""

from typing import Optional
from .config import Config


class AIClient:
    """Unified AI client supporting OpenAI, Anthropic and Google Gemini"""

    def __init__(self, provider: str = None):
        """
        Initialize AI client

        Args:
            provider: 'openai', 'anthropic', or 'gemini'. If None, uses config default.
        """
        self.provider = provider or Config.get_ai_provider()

        if not self.provider:
            raise ValueError(
                "No AI provider configured. Set OPENAI_API_KEY, ANTHROPIC_API_KEY, or GOOGLE_API_KEY in .env"
            )

        if self.provider == "openai":
            self._init_openai()
        elif self.provider == "gemini":
            self._init_gemini()
        else:
            self._init_anthropic()

    def _init_openai(self):
        """Initialize OpenAI client"""
        from openai import OpenAI

        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = Config.OPENAI_MODEL

    def _init_anthropic(self):
        """Initialize Anthropic client"""
        from anthropic import Anthropic

        self.client = Anthropic(api_key=Config.ANTHROPIC_API_KEY)
        self.model = Config.ANTHROPIC_MODEL

    def _init_gemini(self):
        """Initialize Google Gemini client"""
        import google.generativeai as genai

        genai.configure(api_key=Config.GOOGLE_API_KEY)
        self.model = Config.GEMINI_MODEL
        self.client = genai.GenerativeModel(self.model)

    def chat(
        self,
        prompt: str,
        system_prompt: str = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> str:
        """
        Send a chat message to the AI

        Args:
            prompt: User prompt
            system_prompt: System prompt
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature

        Returns:
            AI response text
        """
        if self.provider == "openai":
            return self._chat_openai(prompt, system_prompt, max_tokens, temperature)
        elif self.provider == "gemini":
            return self._chat_gemini(prompt, system_prompt, max_tokens, temperature)
        else:
            return self._chat_anthropic(prompt, system_prompt, max_tokens, temperature)

    def _chat_openai(
        self,
        prompt: str,
        system_prompt: str = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> str:
        """Chat with OpenAI"""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )

        return response.choices[0].message.content

    def _chat_anthropic(
        self,
        prompt: str,
        system_prompt: str = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> str:
        """Chat with Anthropic"""
        kwargs = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [{"role": "user", "content": prompt}],
        }

        if system_prompt:
            kwargs["system"] = system_prompt

        response = self.client.messages.create(**kwargs)

        return response.content[0].text

    def _chat_gemini(
        self,
        prompt: str,
        system_prompt: str = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> str:
        """Chat with Google Gemini"""
        import google.generativeai as genai

        # Combine system prompt with user prompt for Gemini
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"

        # Configure generation settings
        generation_config = genai.GenerationConfig(
            max_output_tokens=max_tokens,
            temperature=temperature,
        )

        response = self.client.generate_content(
            full_prompt,
            generation_config=generation_config,
        )

        return response.text


def get_ai_client(provider: str = None) -> AIClient:
    """Factory function to get AI client"""
    return AIClient(provider)
