"""
Email newsletter generation from video content
"""

from typing import Dict, Optional
from .ai_client import get_ai_client


class NewsletterGenerator:
    """Generate email newsletters from video content"""

    def __init__(self):
        self.ai_client = get_ai_client()

    def generate_newsletter(
        self,
        transcript: str,
        title: str = "",
        author: str = "",
        language: str = "中文",
        style: str = "professional",
    ) -> str:
        """
        Generate email newsletter from transcript

        Args:
            transcript: Video transcript text
            title: Newsletter title
            author: Author name
            language: Output language
            style: professional, casual, educational

        Returns:
            Formatted newsletter content
        """
        style_guide = {
            "professional": "Formal, business-appropriate tone",
            "casual": "Conversational, friendly tone with personality",
            "educational": "Teaching-focused, clear explanations",
        }

        system_prompt = f"""You are a newsletter writer.
Create engaging email content in {language}.
Style: {style_guide.get(style, style_guide['professional'])}"""

        prompt = f"""Create an email newsletter from this video content:

Video Title: {title}
Author: {author}

Transcript:
{transcript[:10000]}

Generate:

## 📧 Newsletter

### Subject Line Options
1. [Compelling subject line 1]
2. [Compelling subject line 2]
3. [Compelling subject line 3]

### Preview Text
[First line that shows in email preview - 50-100 chars]

---

### Email Content

**Header Image Alt Text:** [Description for header image]

---

# [Newsletter Title]

*{author or "[Author]"} · [Date]*

---

## 本期精华 (TLDR)
[2-3 sentence summary]

---

## 深度内容

[Main content - 3-4 paragraphs with insights]

### 要点 1: [Title]
[Content]

### 要点 2: [Title]
[Content]

### 要点 3: [Title]
[Content]

---

## 💡 行动建议
[What readers should do with this information]

---

## 📚 延伸阅读
- [Resource 1]
- [Resource 2]
- [Resource 3]

---

## 📝 本期总结
[Key takeaways in bullet points]

---

**[CTA Button Text]**

---

*喜欢这期内容吗？转发给朋友或回复告诉我你的想法！*

---

[Footer with unsubscribe, etc.]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=3500)

    def generate_digest(
        self,
        transcripts: list,
        language: str = "中文",
    ) -> str:
        """Generate a digest from multiple videos"""
        system_prompt = f"Create newsletter digests in {language}."

        videos_content = ""
        for i, t in enumerate(transcripts, 1):
            title = t.get("title", f"Video {i}")
            content = t.get("transcript", "")[:2000]
            videos_content += f"\n### Video {i}: {title}\n{content}\n"

        prompt = f"""Create a newsletter digest from these videos:

{videos_content}

## 📧 Weekly Digest

### 本周精选
[Overview of what's covered]

### Video 1: [Title]
**核心观点:** [Key insight]
**一句话总结:** [One-line summary]
**阅读原文:** [Link placeholder]

### Video 2: [Title]
...

### 本周热点
[Trending topics across videos]

### 编辑推荐
[Editor's pick with reason]

### 下期预告
[Teaser for next week]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=3000)

    def generate_html_email(
        self,
        transcript: str,
        title: str = "",
        language: str = "中文",
    ) -> str:
        """Generate HTML-formatted email"""
        system_prompt = f"Create HTML email templates in {language}."

        prompt = f"""Create an HTML email newsletter from this video:

Title: {title}
Transcript:
{transcript[:8000]}

Generate clean HTML email:

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title or 'Newsletter'}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: #4A90A4; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
        .content {{ background: #fff; padding: 20px; border: 1px solid #ddd; }}
        .highlight {{ background: #f8f9fa; padding: 15px; border-left: 4px solid #4A90A4; margin: 15px 0; }}
        .cta {{ background: #4A90A4; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block; margin: 20px 0; }}
        .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>[Newsletter Title]</h1>
    </div>
    <div class="content">
        <!-- Content here -->
    </div>
    <div class="footer">
        <!-- Footer -->
    </div>
</body>
</html>
```

Fill in with actual content from the video.
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=4096)

    def generate_substack(
        self,
        transcript: str,
        title: str = "",
        language: str = "中文",
    ) -> str:
        """Generate Substack-style newsletter"""
        system_prompt = f"Create Substack-style content in {language}."

        prompt = f"""Create a Substack-style newsletter from this video:

Title: {title}
Transcript:
{transcript[:10000]}

## {title or 'Newsletter Title'}

*[Tagline/subtitle]*

---

[Opening hook - personal story or observation]

---

### The Big Idea

[Main thesis of the newsletter]

---

### What I Learned

[Detailed insights organized into sections]

#### Section 1
[Content]

#### Section 2
[Content]

---

### Why This Matters

[Relevance and implications]

---

### My Take

[Personal opinion/analysis]

---

### The Bottom Line

[Concise summary]

---

**📣 If you found this valuable:**
- Share with a friend
- Leave a comment below
- Subscribe if you haven't

---

*Until next time,*
*[Author]*

---

**🔗 Links & Resources**
- [Resource 1]
- [Resource 2]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=3500)

    def generate_subject_lines(
        self,
        transcript: str,
        language: str = "中文",
    ) -> str:
        """Generate email subject line options"""
        system_prompt = f"Create compelling email subject lines in {language}."

        prompt = f"""Generate email subject lines for this content:

{transcript[:5000]}

## Subject Line Options

### Curiosity Gap
1. [Subject that creates curiosity]
2. [Subject that creates curiosity]

### How-To
1. [Subject with practical promise]
2. [Subject with practical promise]

### List Format
1. [X ways to...]
2. [X things about...]

### Question
1. [Engaging question?]
2. [Engaging question?]

### Urgency/FOMO
1. [Time-sensitive subject]
2. [Scarcity subject]

### Personal/Story
1. [Story-based subject]
2. [Personal angle]

### Emoji Enhanced
1. 🔥 [With emoji]
2. 💡 [With emoji]

### A/B Test Pairs
Option A: [Version A]
Option B: [Version B]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=1500)
