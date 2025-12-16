"""
Fact checking for video content
"""

from typing import Dict, List, Optional
from .ai_client import get_ai_client


class FactChecker:
    """AI-powered fact checking for video content"""

    def __init__(self):
        self.ai_client = get_ai_client()

    def check_facts(
        self,
        transcript: str,
        language: str = "中文",
    ) -> Dict:
        """
        Check factual claims in video transcript

        Args:
            transcript: Video transcript text
            language: Output language

        Returns:
            Fact check results
        """
        system_prompt = f"""You are a fact-checking expert. Analyze claims critically.
Be objective and note when you cannot verify claims.
Output in {language}."""

        prompt = f"""Analyze the factual claims in this video transcript:

{transcript[:10000]}

Provide fact-check analysis:

## 事实核查报告

### 可验证声明
[List specific factual claims made]

| 声明 | 准确性 | 说明 |
|------|--------|------|
| [Claim 1] | ✅/⚠️/❌ | [Explanation] |
| [Claim 2] | ✅/⚠️/❌ | [Explanation] |
| ... | ... | ... |

Legend:
- ✅ 准确 (Accurate)
- ⚠️ 部分准确/需要更多背景 (Partially accurate/needs context)
- ❌ 不准确 (Inaccurate)
- ❓ 无法验证 (Cannot verify)

### 统计数据核查
[Check any statistics or numbers mentioned]

### 引用核查
[Check any quotes or attributed statements]

### 潜在误导信息
[Identify potentially misleading statements]

### 信息来源评估
[Assess credibility of sources cited]

### 整体可信度评分
[1-10 score with explanation]

### 建议
[Recommendations for viewers]
"""

        response = self.ai_client.chat(prompt, system_prompt, max_tokens=3500)

        return {
            "report": response,
            "disclaimer": "This fact-check is AI-generated and should be verified with authoritative sources.",
        }

    def extract_claims(
        self,
        transcript: str,
        language: str = "中文",
    ) -> str:
        """Extract all factual claims from transcript"""
        system_prompt = f"Extract factual claims in {language}."

        prompt = f"""Extract all factual claims from this transcript:

{transcript[:10000]}

List each claim as:
1. [Claim] - [Type: Statistic/Quote/Fact/Opinion]

Focus on:
- Numerical claims
- Historical facts
- Scientific statements
- Attributed quotes
- Cause-and-effect claims
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=2500)

    def verify_statistics(
        self,
        transcript: str,
        language: str = "中文",
    ) -> str:
        """Verify statistical claims"""
        system_prompt = f"Analyze statistical claims critically in {language}."

        prompt = f"""Analyze statistical claims in this transcript:

{transcript[:10000]}

For each statistic:

## 统计数据分析

### 数据点 1
- 声明: [The statistic]
- 来源: [Source if mentioned]
- 可验证性: [Can this be verified?]
- 潜在问题: [Missing context, outdated, etc.]
- 准确性评估: [Assessment]

### 数据点 2
...

## 统计方法评估
[Are statistics used correctly?]

## 数据可视化问题
[Any misleading presentations?]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=2500)

    def check_sources(
        self,
        transcript: str,
        language: str = "中文",
    ) -> str:
        """Evaluate sources cited in video"""
        system_prompt = f"Evaluate source credibility in {language}."

        prompt = f"""Evaluate sources mentioned in this transcript:

{transcript[:10000]}

## 信息来源评估

### 引用的来源
| 来源 | 类型 | 可信度 | 说明 |
|------|------|--------|------|
| [Source] | [Type] | [1-5] | [Notes] |

### 来源质量分析
- 学术来源: [Count and quality]
- 新闻来源: [Count and quality]
- 个人观点: [Count]
- 未注明来源: [Count]

### 来源多样性
[How diverse are the sources?]

### 建议验证的来源
[Which claims need independent verification]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=2000)

    def identify_opinions_vs_facts(
        self,
        transcript: str,
        language: str = "中文",
    ) -> str:
        """Distinguish between opinions and facts"""
        system_prompt = f"Distinguish facts from opinions in {language}."

        prompt = f"""Analyze this transcript to distinguish facts from opinions:

{transcript[:10000]}

## 事实与观点区分

### 客观事实
[Statements that can be verified]
1. [Fact]
2. [Fact]
...

### 主观观点
[Statements of opinion/belief]
1. [Opinion]
2. [Opinion]
...

### 混合陈述
[Statements mixing fact and opinion]
1. [Statement] → 事实部分: X / 观点部分: Y
...

### 呈现为事实的观点
[Opinions presented as facts - most problematic]
1. [Statement]
...

### 分析总结
- 事实比例: X%
- 观点比例: X%
- 内容客观性评分: [1-10]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=2500)

    def generate_verification_guide(
        self,
        transcript: str,
        language: str = "中文",
    ) -> str:
        """Generate guide for viewers to verify claims themselves"""
        system_prompt = f"Create verification guides in {language}."

        prompt = f"""Create a verification guide for claims in this transcript:

{transcript[:8000]}

## 自我验证指南

### 关键声明清单
[List claims to verify]

### 验证资源
| 声明类型 | 推荐验证来源 |
|----------|--------------|
| 统计数据 | [Sources] |
| 科学声明 | [Sources] |
| 历史事实 | [Sources] |
| 新闻事件 | [Sources] |

### 验证步骤
1. [Step]
2. [Step]
...

### 红旗警告
[Warning signs of misinformation]

### 批判性思考问题
[Questions to ask yourself]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=2000)
