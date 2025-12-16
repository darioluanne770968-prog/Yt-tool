"""
SEO analysis and optimization for video content
"""

from typing import Dict, List, Optional
from .ai_client import get_ai_client


class SEOAnalyzer:
    """Analyze and optimize video SEO"""

    def __init__(self):
        self.ai_client = get_ai_client()

    def analyze_seo(
        self,
        title: str,
        description: str,
        tags: List[str] = None,
        transcript: str = "",
        language: str = "中文",
    ) -> Dict:
        """
        Analyze video SEO

        Args:
            title: Video title
            description: Video description
            tags: Video tags
            transcript: Video transcript
            language: Output language

        Returns:
            SEO analysis report
        """
        tags_str = ", ".join(tags) if tags else "No tags provided"

        system_prompt = f"Analyze YouTube SEO in {language}."

        prompt = f"""Analyze the SEO of this video:

Title: {title}
Description: {description}
Tags: {tags_str}
Transcript excerpt: {transcript[:3000]}

## SEO Analysis Report

### Title Analysis
- Length: [X characters] (Optimal: 60-70)
- Keywords present: [Yes/No]
- Clickability: [Score 1-10]
- Improvements: [Suggestions]

### Description Analysis
- Length: [X characters] (Optimal: 200-350 for above fold)
- Keywords: [Found keywords]
- Links: [Present/Missing]
- CTA: [Present/Missing]
- Improvements: [Suggestions]

### Tags Analysis
- Count: [X] (Optimal: 5-15)
- Relevance: [Score 1-10]
- Mix of broad/specific: [Analysis]
- Missing tags: [Suggestions]

### Content SEO
- Topic relevance: [Analysis]
- Keyword density: [Analysis]
- Search intent match: [Analysis]

### Overall SEO Score: [X/100]

### Priority Improvements
1. [Most important fix]
2. [Second priority]
3. [Third priority]
"""

        response = self.ai_client.chat(prompt, system_prompt, max_tokens=2500)

        return {"report": response}

    def generate_optimized_title(
        self,
        transcript: str,
        current_title: str = "",
        language: str = "中文",
    ) -> str:
        """Generate SEO-optimized titles"""
        system_prompt = f"Create SEO-optimized YouTube titles in {language}."

        prompt = f"""Generate optimized title options:

Current title: {current_title}
Content: {transcript[:5000]}

## Title Options

### High CTR (Click-Through Rate)
1. [Curiosity-driven title]
2. [Number-based title]
3. [How-to title]
4. [Question title]
5. [Controversial/bold title]

### SEO-Optimized
1. [Keyword-rich title]
2. [Search-intent matching title]
3. [Long-tail keyword title]

### Balanced (CTR + SEO)
1. [Best overall option]
2. [Second best option]
3. [Third option]

### Title Templates
- [Template 1 explanation]
- [Template 2 explanation]

### Recommended Title
[Best choice with explanation]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=1500)

    def generate_description(
        self,
        transcript: str,
        title: str = "",
        language: str = "中文",
    ) -> str:
        """Generate SEO-optimized description"""
        system_prompt = f"Create YouTube descriptions in {language}."

        prompt = f"""Create an optimized YouTube description:

Title: {title}
Content: {transcript[:8000]}

## Optimized Description

### Above the Fold (First 200 characters)
[Hook + main keyword + value proposition]

### Full Description

[Paragraph 1: What the video covers]

📌 Key Points:
• [Point 1]
• [Point 2]
• [Point 3]

⏱️ Timestamps:
00:00 - Introduction
[Add more timestamps]

🔗 Resources Mentioned:
• [Resource 1]
• [Resource 2]

📱 Connect with me:
• [Social link placeholder]

🔔 Subscribe for more: [Channel link]

#hashtag1 #hashtag2 #hashtag3

### Keywords Included
[List of SEO keywords used]

### Character Count: [X]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=2000)

    def generate_tags(
        self,
        transcript: str,
        title: str = "",
        language: str = "中文",
    ) -> str:
        """Generate optimized tags"""
        system_prompt = f"Create YouTube tags in {language}."

        prompt = f"""Generate optimized YouTube tags:

Title: {title}
Content: {transcript[:5000]}

## Tag Strategy

### Primary Tags (High Priority)
[5 most important, directly relevant tags]
1.
2.
3.
4.
5.

### Secondary Tags (Medium Priority)
[5 broader topic tags]
1.
2.
3.
4.
5.

### Long-tail Tags
[5 specific, less competitive tags]
1.
2.
3.
4.
5.

### Related Topic Tags
[5 tags for related searches]
1.
2.
3.
4.
5.

### Recommended Tag String
[Copy-paste ready, comma-separated]

### Character Count: [X/500]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=1500)

    def keyword_research(
        self,
        topic: str,
        language: str = "中文",
    ) -> str:
        """Research keywords for topic"""
        system_prompt = f"Research YouTube keywords in {language}."

        prompt = f"""Research keywords for: {topic}

## Keyword Research

### Primary Keywords
[Main target keywords]
| Keyword | Est. Volume | Competition | Priority |
|---------|-------------|-------------|----------|
| ... | High/Med/Low | High/Med/Low | 1-5 |

### Long-tail Keywords
[Specific phrases with lower competition]
| Keyword | Est. Volume | Competition |
|---------|-------------|-------------|
| ... | ... | ... |

### Question Keywords
[Questions people search]
• How to...?
• What is...?
• Why...?

### Related Searches
[Related topics to cover]

### Trending Keywords
[Currently trending related terms]

### Content Strategy
[How to target these keywords]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=2000)

    def analyze_competition(
        self,
        topic: str,
        language: str = "中文",
    ) -> str:
        """Analyze competition for topic"""
        system_prompt = f"Analyze YouTube competition in {language}."

        prompt = f"""Analyze competition for: {topic}

## Competition Analysis

### Market Overview
[General assessment of the topic's competitiveness]

### Content Gaps
[What existing videos are missing]
1.
2.
3.

### Differentiation Opportunities
[How to stand out]
1.
2.
3.

### Recommended Angles
[Unique perspectives to take]
1.
2.
3.

### Optimal Video Length
[Recommended based on topic]

### Best Publishing Time
[Suggested upload times]

### Thumbnail Strategy
[What works for this niche]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=2000)

    def generate_timestamps(
        self,
        transcript: str,
        language: str = "中文",
    ) -> str:
        """Generate SEO-friendly timestamps"""
        system_prompt = f"Create video timestamps in {language}."

        prompt = f"""Create timestamps for this video:

{transcript[:10000]}

## Video Chapters

### Timestamps
00:00 - Introduction
[Create timestamps for each major section]

### Enhanced Timestamps (with keywords)
[Same timestamps but with SEO keywords included]

### Chapter Titles
[Alternative titles for chapters that might rank for different searches]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=1500)
