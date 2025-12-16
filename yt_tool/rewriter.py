"""
Video script rewriting and adaptation
"""

from typing import Dict, Optional
from .ai_client import get_ai_client


class ScriptRewriter:
    """Rewrite and adapt video scripts"""

    def __init__(self):
        self.ai_client = get_ai_client()

    def rewrite_script(
        self,
        transcript: str,
        target_style: str = "conversational",
        target_length: str = "similar",
        language: str = "中文",
    ) -> str:
        """
        Rewrite script in different style

        Args:
            transcript: Original transcript
            target_style: conversational, formal, educational, entertaining
            target_length: shorter, similar, longer
            language: Output language

        Returns:
            Rewritten script
        """
        style_instructions = {
            "conversational": "Make it sound natural, like talking to a friend",
            "formal": "Use professional, polished language",
            "educational": "Focus on clear explanations and learning",
            "entertaining": "Make it engaging, fun, with personality",
        }

        length_instructions = {
            "shorter": "Condense to 50% of original length",
            "similar": "Keep similar length",
            "longer": "Expand with more details and examples",
        }

        system_prompt = f"""You are a professional script writer.
Rewrite content in {language}.
Style: {style_instructions.get(target_style, target_style)}
Length: {length_instructions.get(target_length, target_length)}"""

        prompt = f"""Rewrite this video script:

Original:
{transcript[:10000]}

Create a new version that:
1. Maintains the core message
2. Uses the specified style
3. Improves flow and engagement
4. Fixes any awkward phrasing

## Rewritten Script

[New script here with clear sections/timestamps]

## Changes Made
[Summary of key changes]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=4096)

    def adapt_for_platform(
        self,
        transcript: str,
        platform: str = "youtube",
        language: str = "中文",
    ) -> str:
        """Adapt script for different platforms"""
        platform_specs = {
            "youtube": "10-15 minute video, hook in first 30 seconds, clear structure",
            "tiktok": "15-60 second video, immediate hook, fast pace",
            "podcast": "30-60 minute audio, conversational, no visual references",
            "presentation": "5-10 minute talk, clear points, audience engagement",
            "course": "Educational module, structured learning, exercises",
        }

        system_prompt = f"Adapt content for {platform} in {language}."

        prompt = f"""Adapt this video script for {platform}:

Platform requirements: {platform_specs.get(platform, platform)}

Original:
{transcript[:10000]}

## {platform.upper()} Adapted Script

### Opening Hook
[Platform-specific hook]

### Main Content
[Adapted content with platform-specific formatting]

### Closing
[Platform-appropriate ending]

### Platform-Specific Notes
[Tips for recording/producing on this platform]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=4096)

    def create_voiceover(
        self,
        transcript: str,
        tone: str = "professional",
        language: str = "中文",
    ) -> str:
        """Create voiceover script"""
        system_prompt = f"Create voiceover scripts in {language}."

        prompt = f"""Create a voiceover script from this content:

Original:
{transcript[:8000]}

Tone: {tone}

## Voiceover Script

### Scene 1
[VISUAL: Description]
[VO: Voiceover text - written for speech]

### Scene 2
[VISUAL: Description]
[VO: Text]

...

Include:
- Natural pauses (marked with ...)
- Emphasis markers (*word*)
- Pronunciation guides [word: pronunciation]
- Timing suggestions [X seconds]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=3500)

    def translate_and_localize(
        self,
        transcript: str,
        target_language: str = "English",
        source_language: str = "中文",
    ) -> str:
        """Translate and culturally localize script"""
        system_prompt = f"Translate and localize content from {source_language} to {target_language}."

        prompt = f"""Translate and localize this script:

Original ({source_language}):
{transcript[:10000]}

Provide:

## Translated Script ({target_language})

[Full translation]

## Localization Notes

### Cultural Adaptations
[Changes made for cultural relevance]

### Idiom Translations
| Original | Translation | Explanation |
|----------|-------------|-------------|
| ... | ... | ... |

### References Adapted
[Local references substituted]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=4096)

    def expand_outline(
        self,
        outline: str,
        language: str = "中文",
    ) -> str:
        """Expand outline into full script"""
        system_prompt = f"Expand outlines into full scripts in {language}."

        prompt = f"""Expand this outline into a full video script:

Outline:
{outline}

## Full Script

[For each outline point, create:]
- Opening line/hook
- Main content (2-3 paragraphs)
- Transition to next point

Include:
- Natural conversational flow
- Examples and stories
- Engagement points
- Clear timestamps
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=4096)

    def create_ab_versions(
        self,
        transcript: str,
        language: str = "中文",
    ) -> str:
        """Create A/B test versions of script"""
        system_prompt = f"Create A/B test script versions in {language}."

        prompt = f"""Create two distinct versions of this script for A/B testing:

Original:
{transcript[:6000]}

## Version A: [Style Description]
[Rewritten script - Version A approach]

## Version B: [Style Description]
[Rewritten script - Version B approach]

## Key Differences
| Aspect | Version A | Version B |
|--------|-----------|-----------|
| Opening | ... | ... |
| Tone | ... | ... |
| CTA | ... | ... |

## Test Hypothesis
[What we're testing and expected outcomes]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=4096)

    def simplify_for_beginners(
        self,
        transcript: str,
        language: str = "中文",
    ) -> str:
        """Simplify script for beginner audience"""
        system_prompt = f"Simplify content for beginners in {language}."

        prompt = f"""Simplify this script for beginners with no prior knowledge:

Original:
{transcript[:10000]}

## Beginner-Friendly Version

[Rewrite with:]
- Simple vocabulary
- More explanations
- Analogies for complex concepts
- Removed jargon (or explained when necessary)

## Glossary
[Terms that needed simplification]
| Original Term | Simple Explanation |
|---------------|-------------------|
| ... | ... |

## Added Explanations
[Concepts that needed more context]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=4096)
