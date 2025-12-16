"""
Meme Generator - 表情包/梗图生成器
Automatically identify meme-worthy moments and generate meme content
"""

import json
from typing import Dict, List, Any, Optional
from .ai_client import get_ai_client


class MemeGenerator:
    """Generate memes and shareable content from video"""

    def __init__(self):
        self.ai_client = get_ai_client()

    def find_meme_moments(self, transcript: str, num_moments: int = 10, language: str = "中文") -> List[Dict[str, Any]]:
        """Find meme-worthy moments in the video content"""
        prompt = f"""从以下视频内容中找出{num_moments}个最适合做表情包/梗图的时刻。

内容：
{transcript[:8000]}

找出：
1. 有趣的引用或金句
2. 夸张的表述
3. 可脱离上下文使用的句子
4. 有讽刺意味的内容
5. 可以代入情境的表述

返回JSON数组，每个时刻包含：
- quote: 原话/引用
- context: 原始上下文
- meme_potential: 梗潜力评分（1-10）
- usage_scenarios: 适用场景列表
- emotion: 情感/语气
- meme_type: 梗类型（reaction/quote/situation/relatable）
- viral_potential: 病毒传播潜力（1-10）
- suggested_format: 建议的表情包格式

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return []

    def generate_meme_captions(self, quote: str, template: str = "drake", language: str = "中文") -> Dict[str, Any]:
        """Generate meme captions for popular meme templates"""
        templates = {
            "drake": "Drake格式（上面不要，下面要）",
            "distracted_boyfriend": "男友分心格式（三人图）",
            "two_buttons": "两个按钮选择困难",
            "expanding_brain": "大脑扩展（逐级升华）",
            "is_this": "这是鸽子吗？（指着X问Y）",
            "change_my_mind": "改变我的想法",
            "uno_reverse": "UNO反转卡",
            "stonks": "stonks（股票涨）",
            "panik_kalm": "Panik/Kalm/Panik",
            "this_is_fine": "这很好（着火狗）",
            "always_has_been": "一直都是",
            "modern_problems": "现代问题需要现代方案"
        }

        prompt = f"""基于以下引用，为"{templates.get(template, template)}"表情包模板生成内容。

原引用：{quote}

要求：
1. 保持原意但适应模板格式
2. 有趣且易于理解
3. 可以脱离原视频传播

返回JSON格式：
1. template: 使用的模板
2. panels: 面板内容数组
3. top_text: 顶部文字
4. bottom_text: 底部文字
5. alt_versions: 其他版本创意
6. hashtags: 推荐的标签

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"raw_content": response}

    def generate_reaction_images(self, transcript: str, language: str = "中文") -> List[Dict[str, Any]]:
        """Generate reaction image descriptions for common situations"""
        prompt = f"""基于以下视频内容，生成一系列反应图/表情包创意。

内容：
{transcript[:6000]}

为以下常见情况生成反应：
1. 当你...的时候
2. 那种感觉当...
3. 我：... / 也是我：...
4. 没有人：... / 我：...

返回JSON数组，每个包含：
- situation: 情况描述
- reaction: 反应/表情
- image_description: 图片描述（用于AI图像生成）
- caption: 配图文字
- relatability: 共鸣度（1-10）

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return []

    def generate_quote_graphics(self, transcript: str, num_quotes: int = 5, language: str = "中文") -> List[Dict[str, Any]]:
        """Generate shareable quote graphics from video"""
        prompt = f"""从以下视频内容中提取{num_quotes}句最适合做图文分享的金句。

内容：
{transcript[:8000]}

每句话需要：
1. 能独立存在有意义
2. 有启发性或思考价值
3. 视觉呈现效果好

返回JSON数组，每个包含：
- quote: 金句
- author: 来源/说话人
- design_suggestion:
  - background: 背景建议（颜色/图案）
  - font_style: 字体风格
  - layout: 布局
  - mood: 氛围
- social_platform: 最适合的平台
- image_prompt: AI绘图背景提示词（英文）

语言使用{language}（image_prompt除外）。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return []

    def generate_twitter_memes(self, transcript: str, language: str = "中文") -> List[Dict[str, str]]:
        """Generate Twitter/X style meme tweets"""
        prompt = f"""基于以下内容，生成Twitter风格的梗推文。

内容：
{transcript[:6000]}

风格要求：
1. 简短有力（280字符内）
2. 有梗/有趣
3. 易于转发
4. 包含热点模式（如：POV、红旗🚩、这是测试等）

生成10条推文，返回JSON数组：
- tweet: 推文内容
- format: 使用的格式/模式
- engagement_potential: 互动潜力（1-10）

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return []

    def generate_emoji_story(self, transcript: str, language: str = "中文") -> Dict[str, Any]:
        """Generate emoji summary/story of the content"""
        prompt = f"""用emoji讲述以下视频内容的故事。

内容：
{transcript[:4000]}

要求：
1. 用15-30个emoji概括内容
2. 有叙事感
3. 可以猜出大意

返回JSON格式：
1. emoji_story: emoji序列
2. explanation: 解释每个emoji的含义
3. guessing_game: 可以用来猜内容的提示

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"raw_content": response}

    def generate_gif_suggestions(self, transcript: str, language: str = "中文") -> List[Dict[str, Any]]:
        """Suggest timestamps for GIF extraction"""
        prompt = f"""分析以下视频内容，建议适合制作GIF的时刻。

内容：
{transcript[:6000]}

找出适合做循环GIF的时刻：
1. 表情变化
2. 戏剧性时刻
3. 可循环的动作
4. 反应镜头

返回JSON数组，每个包含：
- description: 时刻描述
- loop_type: 循环类型（perfect_loop/reaction/emphasis）
- duration_suggestion: 建议时长（秒）
- usage: 使用场景
- text_overlay: 建议的文字叠加

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return []

    def create_meme_pack(self, transcript: str, pack_name: str = "video_memes", language: str = "中文") -> Dict[str, Any]:
        """Create a complete meme pack from video content"""
        moments = self.find_meme_moments(transcript, num_moments=5, language=language)
        quotes = self.generate_quote_graphics(transcript, num_quotes=3, language=language)
        reactions = self.generate_reaction_images(transcript, language=language)[:5]
        tweets = self.generate_twitter_memes(transcript, language=language)[:5]
        emoji = self.generate_emoji_story(transcript, language=language)

        return {
            "pack_name": pack_name,
            "meme_moments": moments,
            "quote_graphics": quotes,
            "reaction_images": reactions,
            "meme_tweets": tweets,
            "emoji_story": emoji,
            "total_items": len(moments) + len(quotes) + len(reactions) + len(tweets) + 1
        }

    def export_meme_pack(self, pack: Dict, format: str = "markdown") -> str:
        """Export meme pack in various formats"""
        if format == "markdown":
            md = f"# 表情包合集: {pack.get('pack_name', '')}\n\n"
            md += f"共 {pack.get('total_items', 0)} 个素材\n\n"

            md += "## 梗图时刻\n\n"
            for i, moment in enumerate(pack.get("meme_moments", []), 1):
                md += f"### {i}. {moment.get('quote', '')}\n"
                md += f"- 梗潜力: {moment.get('meme_potential', 'N/A')}/10\n"
                md += f"- 适用场景: {', '.join(moment.get('usage_scenarios', []))}\n\n"

            md += "## 金句图\n\n"
            for quote in pack.get("quote_graphics", []):
                md += f"> {quote.get('quote', '')}\n\n"

            md += "## 反应图\n\n"
            for reaction in pack.get("reaction_images", []):
                md += f"- **{reaction.get('situation', '')}**: {reaction.get('reaction', '')}\n"

            md += "\n## 梗推文\n\n"
            for tweet in pack.get("meme_tweets", []):
                md += f"```\n{tweet.get('tweet', '')}\n```\n\n"

            md += "## Emoji故事\n\n"
            emoji_story = pack.get("emoji_story", {})
            md += f"{emoji_story.get('emoji_story', '')}\n\n"

            return md

        elif format == "json":
            return json.dumps(pack, ensure_ascii=False, indent=2)

        return str(pack)
