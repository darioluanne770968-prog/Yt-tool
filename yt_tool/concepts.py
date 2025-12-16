"""
Concept explanation and terminology extraction
"""

from typing import List, Dict, Optional
from .ai_client import get_ai_client


class ConceptExplainer:
    """Extract and explain concepts and terminology from video content"""

    def __init__(self):
        self.ai_client = get_ai_client()

    def extract_concepts(
        self,
        transcript: str,
        language: str = "中文",
        detail_level: str = "medium",
    ) -> str:
        """
        Extract and explain key concepts from transcript

        Args:
            transcript: Video transcript text
            language: Output language
            detail_level: brief, medium, detailed

        Returns:
            Formatted concept explanations
        """
        detail_instructions = {
            "brief": "Provide 1-2 sentence explanations",
            "medium": "Provide 3-4 sentence explanations with examples",
            "detailed": "Provide comprehensive explanations with examples, related concepts, and applications",
        }

        system_prompt = f"""You are an expert educator explaining complex concepts simply.
Output in {language}. {detail_instructions.get(detail_level, detail_instructions['medium'])}"""

        prompt = f"""Extract and explain all key concepts and terminology from this video transcript.

For each concept provide:

### [概念名称]

**定义:** [Clear, simple definition]

**解释:** [Detailed explanation]

**例子:** [Real-world example]

**相关概念:** [Related terms]

---

Identify at least 10 key concepts if available.

Transcript:
{transcript[:12000]}
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=4096)

    def create_glossary(
        self,
        transcript: str,
        language: str = "中文",
    ) -> str:
        """Create a glossary of terms"""
        system_prompt = f"Create glossaries in {language}."

        prompt = f"""Create a comprehensive glossary from this video transcript.

Format as an alphabetically sorted list:

## 术语表 (Glossary)

**[Term A]** - [Definition]

**[Term B]** - [Definition]

...

Include:
- Technical terms
- Acronyms (with full form)
- Jargon specific to the topic
- Important names/proper nouns

Transcript:
{transcript[:10000]}
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=2500)

    def explain_for_beginner(
        self,
        concept: str,
        context: str = "",
        language: str = "中文",
    ) -> str:
        """Explain a concept for beginners"""
        system_prompt = f"""Explain concepts in simple terms for complete beginners.
Use analogies and everyday examples. Output in {language}."""

        prompt = f"""Explain this concept for someone with no background knowledge:

Concept: {concept}
{f"Context from video: {context[:2000]}" if context else ""}

Include:
1. Simple definition (ELI5 - Explain Like I'm 5)
2. Everyday analogy
3. Why it matters
4. Common misconceptions
5. How to learn more
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=1500)

    def compare_concepts(
        self,
        transcript: str,
        language: str = "中文",
    ) -> str:
        """Compare and contrast related concepts"""
        system_prompt = f"Compare and contrast concepts clearly in {language}."

        prompt = f"""Identify pairs or groups of related concepts in this transcript and compare them.

For each comparison:

### [Concept A] vs [Concept B]

| 方面 | [Concept A] | [Concept B] |
|------|-------------|-------------|
| 定义 | ... | ... |
| 用途 | ... | ... |
| 优点 | ... | ... |
| 缺点 | ... | ... |
| 适用场景 | ... | ... |

**总结:** When to use each

---

Transcript:
{transcript[:10000]}
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=3000)

    def generate_concept_map(
        self,
        transcript: str,
        language: str = "中文",
    ) -> str:
        """Generate a text-based concept map"""
        system_prompt = f"Create concept maps in {language}."

        prompt = f"""Create a concept map showing relationships between ideas in this transcript.

Format as a hierarchical structure:

```
                    [Main Topic]
                         │
          ┌──────────────┼──────────────┐
          │              │              │
    [Concept 1]    [Concept 2]    [Concept 3]
          │              │              │
     ┌────┴────┐    ┌────┴────┐    ┌────┴────┐
     │         │    │         │    │         │
  [Sub1]   [Sub2] [Sub3]   [Sub4] [Sub5]   [Sub6]
```

Also provide relationship descriptions:
- [Concept A] --[relationship]--> [Concept B]

Transcript:
{transcript[:10000]}
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=2500)

    def create_qa_pairs(
        self,
        transcript: str,
        language: str = "中文",
    ) -> str:
        """Create Q&A pairs for key concepts"""
        system_prompt = f"Create educational Q&A pairs in {language}."

        prompt = f"""Create Q&A pairs that test understanding of key concepts in this transcript.

Format:

**Q1:** [Question about concept]
**A1:** [Clear, complete answer]

**Q2:** [Question]
**A2:** [Answer]

Create at least 15 Q&A pairs covering all major concepts.

Transcript:
{transcript[:10000]}
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=3000)
