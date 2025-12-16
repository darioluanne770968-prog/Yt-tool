"""
Configuration management for Yt-tool
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration class for the application"""

    # AI Provider settings
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    AI_PROVIDER = os.getenv("AI_PROVIDER", "openai")  # openai, anthropic, or gemini

    # Default settings
    DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "zh-CN")

    # Model settings
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-haiku-20240307")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

    @classmethod
    def get_ai_provider(cls):
        """Get the configured AI provider"""
        if cls.AI_PROVIDER == "anthropic" and cls.ANTHROPIC_API_KEY:
            return "anthropic"
        elif cls.AI_PROVIDER == "gemini" and cls.GOOGLE_API_KEY:
            return "gemini"
        elif cls.OPENAI_API_KEY:
            return "openai"
        elif cls.ANTHROPIC_API_KEY:
            return "anthropic"
        elif cls.GOOGLE_API_KEY:
            return "gemini"
        return None

    @classmethod
    def validate(cls):
        """Validate that required configuration is present"""
        if not cls.OPENAI_API_KEY and not cls.ANTHROPIC_API_KEY and not cls.GOOGLE_API_KEY:
            return False, "No AI API key configured. Please set OPENAI_API_KEY, ANTHROPIC_API_KEY, or GOOGLE_API_KEY in .env file"
        return True, "Configuration valid"
