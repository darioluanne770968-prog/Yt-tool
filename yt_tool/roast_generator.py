"""
Roast Generator - Generate humorous roasts of video content
吐槽生成器 - 生成视频内容的幽默吐槽/脱口秀版本
"""

from typing import Dict, List, Optional
from .ai_client import get_ai_client


ROAST_STYLES = {
    "gentle": {"name": "温和吐槽", "description": "友好的调侃，不伤害感情"},
    "sarcastic": {"name": "讽刺风", "description": "带有讽刺意味的幽默"},
    "standup": {"name": "脱口秀风", "description": "像单口喜剧演员一样"},
    "internet": {"name": "网络梗风", "description": "充满网络流行语和梗"},
    "intellectual": {"name": "知识分子风", "description": "高级黑，需要一定知识才能理解"},
}


class RoastGenerator:
    """Humorous roast content generator"""

    def __init__(self, provider: str = None):
        self.ai = get_ai_client(provider)

    def generate_roast(self, transcript: str, style: str = "gentle", language: str = "中文") -> str:
        """Generate roast of video content"""
        style_info = ROAST_STYLES.get(style, ROAST_STYLES["gentle"])

        prompt = f"""用{style_info['name']}风格吐槽以下视频内容：

{self._truncate_text(transcript)}

风格说明: {style_info['description']}

请生成：
## 吐槽开场
[幽默的开场白]

## 内容吐槽
[针对视频内容的吐槽，每个要点一段]

### 第一弹
[吐槽点 + 笑点]

### 第二弹
[吐槽点 + 笑点]

### 第三弹
...

## 总结金句
[一句话总结吐槽]

## 免责声明
[友好的免责说明]

用{language}输出。注意保持幽默但不恶意。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是一个幽默的脱口秀演员，擅长友好的吐槽。", temperature=0.8)

    def generate_standup(self, transcript: str, duration: int = 5, language: str = "中文") -> str:
        """Generate standup comedy script"""
        prompt = f"""将视频内容改编成{duration}分钟的脱口秀段子：

{self._truncate_text(transcript)}

请生成：
## 脱口秀剧本

### 开场 (30秒)
[吸引观众的开场]

### 主体段子
**段子1**
[铺垫] → [包袱] → [抖包袱]

**段子2**
[铺垫] → [包袱] → [抖包袱]

**段子3**
...

### 收尾 (30秒)
[有力的结尾]

## 表演提示
- 语气变化
- 停顿位置
- 动作建议

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是专业的喜剧编剧。", temperature=0.8)

    def generate_meme_script(self, transcript: str, language: str = "中文") -> str:
        """Generate meme-style commentary"""
        prompt = f"""用网络段子风格评论这个视频：

{self._truncate_text(transcript)}

请生成：
## 网友锐评

### 高赞评论区
1. 🔥 [热评1]
2. 😂 [热评2]
3. 💀 [热评3]
...

### 弹幕风暴
[模拟弹幕效果的评论]

### 梗图文案
[适合做成表情包的文案]

### 社死名场面
[视频中的尴尬/搞笑时刻]

用{language}输出，多用网络流行语。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是网络文化专家，精通各种梗。", temperature=0.9)

    def generate_parody(self, transcript: str, parody_style: str = "news", language: str = "中文") -> str:
        """Generate parody version"""
        prompt = f"""将视频内容改编成{parody_style}风格的恶搞版：

{self._truncate_text(transcript)}

请生成：
## 恶搞版本

[用{parody_style}风格重新演绎内容]

## 对比原版
[搞笑的对比]

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是恶搞视频创作者。", temperature=0.8)

    def _truncate_text(self, text: str, max_chars: int = 15000) -> str:
        if len(text) <= max_chars:
            return text
        return text[:max_chars] + "..."

    @staticmethod
    def get_styles() -> Dict:
        return ROAST_STYLES
