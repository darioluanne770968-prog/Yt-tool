"""
Presentation/PPT generation from video content
"""

from typing import Dict, List, Optional
from .ai_client import get_ai_client


class PresentationGenerator:
    """Generate presentations from video transcripts"""

    def __init__(self):
        self.ai_client = get_ai_client()

    def generate_slides(
        self,
        transcript: str,
        title: str = "",
        num_slides: int = 10,
        language: str = "中文",
        style: str = "professional",
    ) -> str:
        """
        Generate presentation slides from transcript

        Args:
            transcript: Video transcript text
            title: Presentation title
            num_slides: Target number of slides
            language: Output language
            style: professional, casual, academic, minimal

        Returns:
            Markdown-formatted slides
        """
        style_instructions = {
            "professional": "Use professional business language, clear structure",
            "casual": "Use conversational tone, engaging visuals suggestions",
            "academic": "Use formal language, include citations, detailed content",
            "minimal": "Minimal text, focus on key points only",
        }

        system_prompt = f"""You are a presentation design expert.
Create clear, engaging slides in {language}.
Style: {style_instructions.get(style, style_instructions['professional'])}"""

        prompt = f"""Create a presentation with approximately {num_slides} slides from this video content:

Title: {title}

Transcript:
{transcript[:12000]}

Format each slide as:

---
## Slide 1: [Title]

### [Subtitle if needed]

- Point 1
- Point 2
- Point 3

**Speaker Notes:** [What to say for this slide]

**Visual Suggestion:** [Image/chart/diagram suggestion]

---

Include:
1. Title slide
2. Agenda/Overview slide
3. Content slides
4. Summary slide
5. Q&A slide (optional)

Make slides:
- Visually balanced (not too much text)
- Logically organized
- Easy to present
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=4096)

    def generate_speaker_notes(
        self,
        transcript: str,
        language: str = "中文",
    ) -> str:
        """Generate detailed speaker notes"""
        system_prompt = f"Create presenter notes in {language}."

        prompt = f"""Create detailed speaker notes from this video transcript.

Transcript:
{transcript[:10000]}

Format:

## Speaker Notes

### Slide 1: [Topic]
**Key message:** [Main point]
**Script:**
[What to say - 2-3 paragraphs]

**Transition:** [How to transition to next slide]

### Slide 2: [Topic]
...

Include:
- What to emphasize
- Stories/examples to share
- Potential questions to anticipate
- Timing suggestions
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=4096)

    def generate_marp_slides(
        self,
        transcript: str,
        title: str = "",
        language: str = "中文",
    ) -> str:
        """Generate Marp-compatible markdown slides"""
        system_prompt = f"Create Marp markdown slides in {language}."

        prompt = f"""Create Marp-format presentation from this video:

Title: {title}

Transcript:
{transcript[:10000]}

Use Marp markdown format:

---
marp: true
theme: default
paginate: true
---

# {title or 'Presentation Title'}

---

## Slide Title

- Point 1
- Point 2
- Point 3

![bg right:40%](image-suggestion.jpg)

---

## Another Slide

Content here

---

Create 8-12 slides with proper Marp syntax.
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=3500)

    def generate_reveal_js(
        self,
        transcript: str,
        title: str = "",
        language: str = "中文",
    ) -> str:
        """Generate Reveal.js HTML slides"""
        system_prompt = f"Create Reveal.js slides in {language}."

        prompt = f"""Create Reveal.js presentation from this video:

Title: {title}

Transcript:
{transcript[:10000]}

Generate HTML in Reveal.js format:

```html
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4/dist/reveal.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4/dist/theme/white.css">
</head>
<body>
    <div class="reveal">
        <div class="slides">
            <section>
                <h1>{title or 'Title'}</h1>
            </section>
            <section>
                <h2>Slide 2</h2>
                <ul>
                    <li>Point 1</li>
                    <li>Point 2</li>
                </ul>
            </section>
            <!-- More slides -->
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@4/dist/reveal.js"></script>
    <script>Reveal.initialize();</script>
</body>
</html>
```

Create a complete presentation with 8-12 slides.
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=4096)

    def extract_visual_suggestions(
        self,
        transcript: str,
        language: str = "中文",
    ) -> str:
        """Extract suggestions for visuals and diagrams"""
        system_prompt = f"Suggest visuals for presentations in {language}."

        prompt = f"""Based on this transcript, suggest visuals for a presentation:

{transcript[:10000]}

## Visual Suggestions

### Charts and Graphs
[Suggest specific charts based on data mentioned]
1. [Type]: [Description] - [Data to show]

### Diagrams
[Suggest diagrams to explain concepts]
1. [Type]: [Description] - [What it illustrates]

### Images
[Suggest images/photos]
1. [Description] - [Where to find or what to search]

### Icons
[Suggest icons for key concepts]
1. [Concept]: [Icon suggestion]

### Animations/Transitions
[Suggest where animations would help]

### Stock Photo Keywords
[Search terms for finding relevant images]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=2000)

    def generate_handout(
        self,
        transcript: str,
        language: str = "中文",
    ) -> str:
        """Generate audience handout"""
        system_prompt = f"Create presentation handouts in {language}."

        prompt = f"""Create a presentation handout from this video content:

{transcript[:10000]}

## 演示文稿讲义

### 主题概述
[Brief overview]

### 关键要点
1. [Key point with explanation]
2. [Key point with explanation]
...

### 重要概念
| 概念 | 定义 | 示例 |
|------|------|------|
| ... | ... | ... |

### 笔记区域
[Space for notes]
_______________________
_______________________
_______________________

### 问题与讨论
[Questions to consider]

### 延伸阅读
[Further reading suggestions]

### 联系方式
[Space for contact info]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=2500)
