"""
Reference and citation extraction from video content
"""

from typing import List, Dict, Optional
from .ai_client import get_ai_client


class ReferenceExtractor:
    """Extract references, citations, and resources from video transcripts"""

    def __init__(self):
        self.ai_client = get_ai_client()

    def extract_references(
        self,
        transcript: str,
        language: str = "中文",
    ) -> Dict:
        """
        Extract all references and citations from transcript

        Args:
            transcript: Video transcript text
            language: Output language

        Returns:
            Dictionary with categorized references
        """
        system_prompt = f"""You are a research assistant extracting references and citations.
Output in {language}. Be thorough and accurate."""

        prompt = f"""Extract all references, citations, and resources mentioned in this video transcript.

Categorize them as follows:

## 📚 书籍 (Books)
- [Book title] by [Author] - [Brief description if mentioned]

## 📄 论文/研究 (Papers/Research)
- [Paper title] - [Authors/Institution] - [Year if mentioned]

## 🌐 网站/工具 (Websites/Tools)
- [Name] - [URL if mentioned] - [Description]

## 👤 人物引用 (People Cited)
- [Name] - [Title/Role] - [What was cited]

## 📺 其他视频/课程 (Other Videos/Courses)
- [Title] - [Platform/Creator]

## 💡 概念/理论 (Concepts/Theories)
- [Concept name] - [Brief explanation]

If a category has no items, omit it.

Transcript:
{transcript[:12000]}
"""

        response = self.ai_client.chat(prompt, system_prompt, max_tokens=3000)

        return {
            "references": response,
            "raw_transcript_length": len(transcript),
        }

    def extract_books(
        self,
        transcript: str,
        language: str = "中文",
    ) -> str:
        """Extract only book references"""
        system_prompt = f"Extract book references in {language}."

        prompt = f"""Extract all books mentioned in this transcript.

For each book provide:
- Title
- Author (if mentioned)
- Why it was recommended
- Key topics covered

Transcript:
{transcript[:10000]}
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=1500)

    def extract_tools(
        self,
        transcript: str,
        language: str = "中文",
    ) -> str:
        """Extract tools and software mentioned"""
        system_prompt = f"Extract tools and software references in {language}."

        prompt = f"""Extract all tools, software, and services mentioned in this transcript.

For each tool provide:
- Name
- Category (e.g., IDE, framework, service)
- URL (if mentioned)
- What it's used for
- Alternatives mentioned (if any)

Transcript:
{transcript[:10000]}
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=1500)

    def extract_people(
        self,
        transcript: str,
        language: str = "中文",
    ) -> str:
        """Extract people and experts mentioned"""
        system_prompt = f"Extract people references in {language}."

        prompt = f"""Extract all people, experts, and thought leaders mentioned in this transcript.

For each person provide:
- Name
- Title/Role (if mentioned)
- Why they were mentioned
- Their contribution/quote

Transcript:
{transcript[:10000]}
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=1500)

    def generate_bibliography(
        self,
        transcript: str,
        style: str = "apa",
        language: str = "中文",
    ) -> str:
        """Generate formatted bibliography"""
        system_prompt = f"Generate {style.upper()} style bibliography in {language}."

        prompt = f"""Generate a formatted bibliography from all sources mentioned in this transcript.

Use {style.upper()} citation style.

Format properly with:
- Proper indentation
- Alphabetical order
- Complete citation information where available

For missing information, use [Unknown] placeholders.

Transcript:
{transcript[:10000]}
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=2000)

    def export_to_bibtex(
        self,
        transcript: str,
    ) -> str:
        """Export references to BibTeX format"""
        system_prompt = "Generate BibTeX entries for academic references."

        prompt = f"""Extract academic references from this transcript and convert to BibTeX format.

Example format:
@book{{key,
  author = {{Author Name}},
  title = {{Book Title}},
  year = {{2023}},
  publisher = {{Publisher}}
}}

@article{{key,
  author = {{Author Name}},
  title = {{Article Title}},
  journal = {{Journal Name}},
  year = {{2023}}
}}

Transcript:
{transcript[:10000]}
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=2000)
