"""
Sentiment analysis for video content
"""

from typing import Dict, List, Optional
from .ai_client import get_ai_client


class SentimentAnalyzer:
    """Analyze sentiment and emotional tone of video content"""

    def __init__(self):
        self.ai_client = get_ai_client()

    def analyze_sentiment(
        self,
        transcript: str,
        language: str = "中文",
    ) -> Dict:
        """
        Analyze overall sentiment of video content

        Args:
            transcript: Video transcript text
            language: Output language

        Returns:
            Sentiment analysis results
        """
        system_prompt = f"""You are a sentiment analysis expert.
Analyze emotional tone and sentiment in {language}. Be objective and thorough."""

        prompt = f"""Analyze the sentiment and emotional tone of this video transcript:

Transcript:
{transcript[:10000]}

Provide analysis:

## 整体情感分析

### 情感评分
- 积极度: [1-10]
- 消极度: [1-10]
- 中性度: [1-10]
- 情感强度: [1-10]

### 主导情绪
[Primary emotions: happiness, sadness, anger, fear, surprise, etc.]

## 情感变化曲线
[Describe how sentiment changes throughout the video]
- 开场: [sentiment]
- 中段: [sentiment]
- 结尾: [sentiment]

## 语气分析
- 正式程度: [1-10]
- 热情程度: [1-10]
- 专业程度: [1-10]
- 亲和力: [1-10]

## 关键情感时刻
[Identify moments with strong emotional content]

## 观众可能的情感反应
[How viewers might feel watching this]
"""

        response = self.ai_client.chat(prompt, system_prompt, max_tokens=2500)

        return {
            "analysis": response,
            "transcript_length": len(transcript),
        }

    def detect_bias(
        self,
        transcript: str,
        language: str = "中文",
    ) -> str:
        """Detect potential bias in content"""
        system_prompt = f"Detect bias objectively in {language}."

        prompt = f"""Analyze this transcript for potential bias:

{transcript[:10000]}

Identify:

## 偏见分析

### 潜在偏见类型
- 确认偏见: [Yes/No - Evidence]
- 选择性报道: [Yes/No - Evidence]
- 情感操纵: [Yes/No - Evidence]
- 片面观点: [Yes/No - Evidence]

### 语言偏见指标
- 加载性词汇: [Examples]
- 绝对化表述: [Examples]
- 情感化语言: [Examples]

### 信息平衡度
[How balanced is the information presented]

### 建议
[How to consume this content critically]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=2000)

    def analyze_persuasion(
        self,
        transcript: str,
        language: str = "中文",
    ) -> str:
        """Analyze persuasion techniques used"""
        system_prompt = f"Analyze persuasion techniques in {language}."

        prompt = f"""Analyze persuasion techniques in this transcript:

{transcript[:10000]}

Identify:

## 说服技巧分析

### 使用的修辞手法
- 情感诉求 (Pathos): [Examples]
- 逻辑论证 (Logos): [Examples]
- 权威引用 (Ethos): [Examples]

### 说服策略
- 社会认同: [Yes/No - How used]
- 稀缺性: [Yes/No - How used]
- 互惠原则: [Yes/No - How used]
- 权威效应: [Yes/No - How used]

### 语言技巧
- 重复强调: [Key phrases repeated]
- 问答引导: [Questions used]
- 故事叙述: [Stories told]

### 有效性评估
[How effective are these techniques]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=2500)

    def analyze_tone_by_section(
        self,
        transcript: str,
        language: str = "中文",
    ) -> str:
        """Analyze tone changes throughout the video"""
        system_prompt = f"Analyze tone progression in {language}."

        prompt = f"""Analyze how the tone changes throughout this video:

{transcript[:10000]}

Divide into sections and analyze:

## 语气变化分析

### 第一部分 (开场)
- 时间范围: 0:00 - X:XX
- 语气: [描述]
- 情感: [描述]
- 目的: [吸引注意/介绍主题/etc]

### 第二部分 (发展)
- 时间范围: X:XX - X:XX
- 语气: [描述]
- 情感: [描述]
- 目的: [描述]

### 第三部分 (高潮/重点)
...

### 第四部分 (结尾)
...

## 语气变化图
```
积极 ████████░░ → ██████████ → ████░░░░░░ → ████████░░
中性 ░░████████ → ░░░░░░░░░░ → ░░██████░░ → ░░████████
消极 ░░░░░░░░░░ → ░░░░░░░░░░ → ██████░░░░ → ░░░░░░░░░░
     开场         发展         高潮         结尾
```

## 关键转折点
[Moments where tone significantly shifts]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=2500)

    def analyze_audience_reaction(
        self,
        transcript: str,
        comments: List[str] = None,
        language: str = "中文",
    ) -> str:
        """Predict or analyze audience reaction"""
        system_prompt = f"Analyze audience reaction in {language}."

        comments_section = ""
        if comments:
            comments_text = "\n".join([f"- {c[:200]}" for c in comments[:20]])
            comments_section = f"\n\nSample comments:\n{comments_text}"

        prompt = f"""Analyze/predict audience reaction to this video:

Transcript:
{transcript[:8000]}
{comments_section}

Provide:

## 观众反应分析

### 预期情感反应
- 正面反应: [What viewers might like]
- 负面反应: [What might upset viewers]
- 中性反应: [Neutral takeaways]

### 目标观众匹配度
[How well content matches target audience]

### 争议性评估
- 争议可能性: [Low/Medium/High]
- 潜在争议点: [List]

### 参与度预测
- 点赞可能性: [High/Medium/Low]
- 评论可能性: [High/Medium/Low]
- 分享可能性: [High/Medium/Low]

### 改进建议
[How to improve audience reception]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=2500)
