"""
Thumbnail Idea - Generate thumbnail design ideas
封面创意生成 - 基于视频内容生成封面设计建议和文案
"""

from typing import Dict, List, Optional
from .ai_client import get_ai_client


THUMBNAIL_STYLES = {
    "minimalist": {"name": "极简风", "description": "简洁清爽，重点突出"},
    "bold": {"name": "大胆醒目", "description": "强对比，大文字"},
    "professional": {"name": "专业风", "description": "商务、权威感"},
    "playful": {"name": "活泼风", "description": "有趣、年轻化"},
    "dramatic": {"name": "戏剧化", "description": "夸张表情、强情绪"},
    "educational": {"name": "教育风", "description": "清晰、信息化"},
}


class ThumbnailIdea:
    """Thumbnail design idea generator"""

    def __init__(self, provider: str = None):
        self.ai = get_ai_client(provider)

    def generate_ideas(self, transcript: str, title: str = "", style: str = "bold", count: int = 5, language: str = "中文") -> str:
        """Generate thumbnail ideas"""
        style_info = THUMBNAIL_STYLES.get(style, THUMBNAIL_STYLES["bold"])

        prompt = f"""为以下视频生成{count}个封面创意：

**标题**: {title}
**风格**: {style_info['name']} - {style_info['description']}
**内容**: {self._truncate_text(transcript)}

请生成{count}个封面创意：

### 创意1
- **视觉描述**: [详细画面描述]
- **文字内容**: [封面文字]
- **配色方案**: [主色+辅色]
- **情绪表达**: [传达的情感]
- **预期效果**: [点击吸引力分析]

[继续其他创意...]

## 设计建议
- 尺寸规格
- 字体推荐
- 避免事项

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是视觉设计专家和点击率优化师。", temperature=0.8)

    def generate_text_overlays(self, title: str, transcript: str, count: int = 10, language: str = "中文") -> str:
        """Generate text overlay options"""
        prompt = f"""为视频封面生成{count}个文字叠加方案：

**标题**: {title}
**内容**: {self._truncate_text(transcript, 5000)}

请生成：
## 主标题方案（3-6字）
1.
2.
...

## 副标题方案（可选）
1.
2.
...

## 数字亮点（如有）

## 疑问句式（引发好奇）

## 排版建议

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是封面文案专家。", temperature=0.8)

    def analyze_thumbnail(self, description: str, language: str = "中文") -> str:
        """Analyze existing thumbnail"""
        prompt = f"""分析以下封面描述并提供优化建议：

**封面描述**: {description}

请分析：
## 当前分析
- 视觉吸引力: /10
- 信息传达: /10
- 点击欲望: /10

## 优点

## 改进建议

## 优化版本描述

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是封面优化专家。", temperature=0.6)

    def suggest_ab_test(self, idea1: str, idea2: str, language: str = "中文") -> str:
        """Suggest A/B test approach"""
        prompt = f"""为以下两个封面方案设计A/B测试：

**方案A**: {idea1}
**方案B**: {idea2}

请提供：
## 差异分析
## 测试假设
## 成功指标
## 测试建议
## 预期结果

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是增长实验专家。", temperature=0.6)

    def _truncate_text(self, text: str, max_chars: int = 10000) -> str:
        if len(text) <= max_chars:
            return text
        return text[:max_chars] + "..."

    @staticmethod
    def get_styles() -> Dict:
        return THUMBNAIL_STYLES
