"""
Story Mode - Convert educational content to engaging stories
故事化改编 - 将枯燥的教程内容改编成有趣的故事版本
"""

from typing import Dict, List, Optional
from .ai_client import get_ai_client


STORY_STYLES = {
    "adventure": {"name": "冒险故事", "description": "主角踏上学习冒险之旅"},
    "mystery": {"name": "悬疑故事", "description": "通过解谜学习知识"},
    "comedy": {"name": "喜剧故事", "description": "轻松幽默的学习故事"},
    "scifi": {"name": "科幻故事", "description": "未来科技背景"},
    "fantasy": {"name": "奇幻故事", "description": "魔法世界设定"},
    "slice_of_life": {"name": "日常故事", "description": "贴近生活的场景"},
    "historical": {"name": "历史故事", "description": "历史背景设定"},
}


class StoryMode:
    """Convert educational content to stories"""

    def __init__(self, provider: str = None):
        self.ai = get_ai_client(provider)

    def convert_to_story(self, transcript: str, style: str = "adventure", language: str = "中文") -> str:
        """Convert content to story format"""
        style_info = STORY_STYLES.get(style, STORY_STYLES["adventure"])

        prompt = f"""将以下教程内容改编成{style_info['name']}：

{self._truncate_text(transcript)}

故事风格: {style_info['description']}

请创作：
## {style_info['name']}

### 角色介绍
- 主角:
- 配角:
- 导师:

### 第一章: 起点
[故事开始，引入问题]

### 第二章: 挑战
[遇到困难，开始学习]

### 第三章: 成长
[掌握知识，克服困难]

### 第四章: 胜利
[应用所学，解决问题]

### 结语
[总结收获]

## 知识点对照表
| 故事情节 | 对应知识点 |
|----------|------------|

用{language}创作。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是擅长寓教于乐的故事作家。", temperature=0.8)

    def generate_dialogue_version(self, transcript: str, characters: List[str] = None, language: str = "中文") -> str:
        """Generate dialogue-based version"""
        characters = characters or ["小明", "老师"]

        prompt = f"""将内容改编成对话形式：

{self._truncate_text(transcript)}

角色: {', '.join(characters)}

请生成：
## 对话剧本

**场景: [描述]**

**{characters[0]}**: [台词]

**{characters[1]}**: [台词]

...

[继续对话，涵盖所有知识点]

## 角色设定
## 场景设计

用{language}创作。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是剧本作家。", temperature=0.7)

    def generate_analogy_story(self, transcript: str, analogy_domain: str = "cooking", language: str = "中文") -> str:
        """Generate story using analogies"""
        prompt = f"""用{analogy_domain}作为类比，讲解以下内容：

{self._truncate_text(transcript)}

请创作：
## 类比故事

[用{analogy_domain}的概念类比解释技术概念]

## 对照表
| 原概念 | {analogy_domain}类比 |
|--------|---------------------|

## 为什么这个类比有效

用{language}创作。"""

        return self.ai.chat(prompt=prompt, system_prompt="你擅长用类比解释复杂概念。", temperature=0.7)

    def generate_bedtime_story(self, transcript: str, age_group: str = "8-12", language: str = "中文") -> str:
        """Generate bedtime story version"""
        prompt = f"""将内容改编成适合{age_group}岁儿童的睡前故事：

{self._truncate_text(transcript)}

请创作：
## 睡前故事

### 故事开始
"从前，在一个..."

[完整故事，融入知识点]

### 故事结束
[温馨的结尾]

## 家长指南
- 可以讨论的问题
- 延伸活动建议

用{language}创作。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是儿童故事作家。", temperature=0.8)

    def generate_comic_script(self, transcript: str, panels: int = 12, language: str = "中文") -> str:
        """Generate comic/manga script"""
        prompt = f"""将内容改编成{panels}格漫画脚本：

{self._truncate_text(transcript)}

请生成：
## 漫画脚本

### 第1格
**画面**: [描述]
**对话**: [台词]
**旁白**: [旁白]

### 第2格
...

[继续到第{panels}格]

## 角色设计建议
## 画风建议

用{language}创作。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是漫画编剧。", temperature=0.7)

    def _truncate_text(self, text: str, max_chars: int = 15000) -> str:
        if len(text) <= max_chars:
            return text
        return text[:max_chars] + "..."

    @staticmethod
    def get_styles() -> Dict:
        return STORY_STYLES
