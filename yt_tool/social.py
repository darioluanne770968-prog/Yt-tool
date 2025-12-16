"""
Social media content generation
"""

from typing import Dict, List, Optional
from .ai_client import get_ai_client


class SocialMediaGenerator:
    """Generate social media content from video"""

    def __init__(self):
        self.ai_client = get_ai_client()

    def generate_all(
        self,
        transcript: str,
        title: str = "",
        language: str = "中文",
    ) -> Dict[str, str]:
        """
        Generate content for all platforms

        Args:
            transcript: Video transcript text
            title: Video title
            language: Output language

        Returns:
            Dictionary with content for each platform
        """
        system_prompt = f"""You are a social media expert.
Create engaging, platform-optimized content in {language}.
Understand each platform's unique style and requirements."""

        prompt = f"""Create social media posts for all major platforms based on this video:

Title: {title}
Transcript:
{transcript[:8000]}

Generate optimized content for each platform:

## Twitter/X
[280 characters max, with hashtags]
Post 1: ...
Post 2: ...
Thread (if needed):
1/X: ...
2/X: ...

## LinkedIn
[Professional tone, 1300 characters max]
...

## Instagram
Caption: [2200 characters max, with emojis and hashtags]
...

## 小红书 (Xiaohongshu)
[Chinese style, emojis, engaging]
标题: ...
正文: ...
标签: ...

## 抖音/TikTok
[Hook + value + CTA]
视频脚本: ...
文案: ...

## 微博
[140 characters + extended if needed]
...

## Facebook
[Conversational, shareable]
...

## YouTube Community
[Engage subscribers]
...
"""

        response = self.ai_client.chat(prompt, system_prompt, max_tokens=4096)

        return {"all_platforms": response}

    def generate_twitter(
        self,
        transcript: str,
        language: str = "中文",
    ) -> str:
        """Generate Twitter/X content"""
        system_prompt = f"Create viral Twitter content in {language}."

        prompt = f"""Create Twitter/X posts from this video:

{transcript[:6000]}

Generate:

## 单条推文 (Single Tweets)
[3-5 standalone tweets, each under 280 characters]

1. [Tweet with hook]
2. [Tweet with key insight]
3. [Tweet with question for engagement]
4. [Tweet with quote/stat]
5. [Tweet with CTA]

## 推文串 (Thread)
1/🧵 [Hook - grab attention]
2/ [Context/Problem]
3/ [Key insight 1]
4/ [Key insight 2]
5/ [Key insight 3]
6/ [Actionable takeaway]
7/ [CTA + like/retweet request]

## 话题标签
#tag1 #tag2 #tag3 ...
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=2000)

    def generate_linkedin(
        self,
        transcript: str,
        language: str = "中文",
    ) -> str:
        """Generate LinkedIn content"""
        system_prompt = f"Create professional LinkedIn content in {language}."

        prompt = f"""Create LinkedIn posts from this video:

{transcript[:6000]}

Generate:

## Post 1: Thought Leadership
[Hook line that stops scroll]

[3-4 paragraphs with insights]

[CTA]

#hashtags

---

## Post 2: Story Format
[Personal angle/story]

[Lesson learned]

[Value for readers]

---

## Post 3: List Format
[Topic] - Here's what I learned:

1️⃣ [Point]
2️⃣ [Point]
3️⃣ [Point]
4️⃣ [Point]
5️⃣ [Point]

[Closing thought]
[CTA]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=2000)

    def generate_xiaohongshu(
        self,
        transcript: str,
        language: str = "中文",
    ) -> str:
        """Generate Xiaohongshu (小红书) content"""
        system_prompt = "Create engaging 小红书 content with emojis and Chinese style."

        prompt = f"""Create 小红书 posts from this video:

{transcript[:6000]}

Generate:

## 笔记 1: 干货分享
标题: [吸引眼球的标题，带emoji]

正文:
[开头hook]
📌 要点1...
📌 要点2...
📌 要点3...

💡 总结...

#标签1 #标签2 #标签3

---

## 笔记 2: 经验分享
标题: ...

正文:
🔥 [引人注目的开场]

✨ 亮点1
✨ 亮点2
✨ 亮点3

💬 互动问题...

---

## 笔记 3: 清单体
标题: [XX个必知的XX]

正文:
1️⃣ ...
2️⃣ ...
3️⃣ ...

记得点赞收藏哦～ ❤️

## 推荐封面文案
[3-5个封面标题建议]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=2000)

    def generate_douyin(
        self,
        transcript: str,
        language: str = "中文",
    ) -> str:
        """Generate Douyin/TikTok content"""
        system_prompt = "Create viral 抖音/TikTok scripts in Chinese."

        prompt = f"""Create 抖音 video scripts from this video:

{transcript[:6000]}

Generate:

## 短视频脚本 1 (15-30秒)

**Hook (前3秒):** [必须抓住注意力]

**内容:**
[快节奏要点]

**结尾CTA:** [引导互动]

**文案:** [视频描述文案]
**话题:** #话题1 #话题2

---

## 短视频脚本 2 (30-60秒)

**Hook:** ...

**内容:**
- 段落1
- 段落2
- 段落3

**结尾:** ...

**文案:** ...

---

## 直播话术
[如果做直播讨论这个话题]

开场: ...
互动: ...
结尾: ...

## 评论区互动话术
[回复评论的模板]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=2000)

    def generate_hashtags(
        self,
        transcript: str,
        platform: str = "all",
        language: str = "中文",
    ) -> str:
        """Generate optimized hashtags"""
        system_prompt = f"Generate optimized hashtags in {language}."

        prompt = f"""Generate hashtags for this content:

{transcript[:4000]}

Platform: {platform}

## Hashtag Strategy

### 核心标签 (High relevance)
[5-7 most relevant tags]

### 热门标签 (High volume)
[5-7 popular general tags]

### 长尾标签 (Niche)
[5-7 specific niche tags]

### 平台特定标签
Twitter: ...
Instagram: ...
LinkedIn: ...
小红书: ...
抖音: ...

### 最佳组合
[Recommended combination of 5-10 tags per platform]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=1500)

    def generate_captions(
        self,
        transcript: str,
        language: str = "中文",
    ) -> str:
        """Generate video captions for social media"""
        system_prompt = f"Create engaging video captions in {language}."

        prompt = f"""Create video captions/descriptions for social media:

{transcript[:5000]}

## YouTube 描述
[Full description with timestamps, links, keywords]

## Instagram Caption
[Engaging caption with story, value, CTA]

## TikTok Caption
[Short, punchy, with trending sounds suggestion]

## 通用短描述
[50 characters]
[100 characters]
[150 characters]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=2000)
