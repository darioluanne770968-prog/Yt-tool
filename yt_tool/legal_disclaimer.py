"""
Legal Disclaimer - Detect legal disclaimers and warnings in video
法律声明检测 - 检测视频中的免责声明、投资警告、医疗建议等需要注意的内容
"""

from typing import Dict, List, Optional
from .ai_client import get_ai_client


DISCLAIMER_TYPES = {
    "investment": {"name": "投资风险", "keywords": ["投资有风险", "不构成投资建议", "盈亏自负"]},
    "medical": {"name": "医疗健康", "keywords": ["咨询医生", "不能替代医疗", "仅供参考"]},
    "legal": {"name": "法律声明", "keywords": ["不构成法律建议", "咨询律师"]},
    "affiliate": {"name": "推广声明", "keywords": ["affiliate", "推广链接", "合作推广"]},
    "sponsored": {"name": "赞助声明", "keywords": ["sponsored", "赞助", "广告"]},
    "opinion": {"name": "个人观点", "keywords": ["个人观点", "仅代表个人", "不代表"]},
}


class LegalDisclaimer:
    """Legal disclaimer and warning detector"""

    def __init__(self, provider: str = None):
        self.ai = get_ai_client(provider)

    def detect_disclaimers(self, transcript: str, language: str = "中文") -> str:
        """Detect disclaimers in video content"""
        prompt = f"""检测以下视频内容中的声明和警告：

{self._truncate_text(transcript)}

请检测：
## 发现的声明

### 投资相关
- 发现: [是/否]
- 内容: [具体内容]
- 位置: [大概位置]

### 医疗健康相关
- 发现: [是/否]
- 内容:
- 位置:

### 法律相关
### 推广/赞助相关
### 个人观点声明
### 其他声明

## 风险评估
- 合规风险: [高/中/低]
- 建议添加的声明

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是合规审核专家。", temperature=0.3)

    def generate_disclaimers(self, transcript: str, content_type: str = "general", language: str = "中文") -> str:
        """Generate appropriate disclaimers"""
        prompt = f"""为以下内容生成适当的免责声明：

**内容类型**: {content_type}
**内容**: {self._truncate_text(transcript)}

请生成：
## 推荐声明

### 必须添加
[法律上需要的声明]

### 建议添加
[降低风险的声明]

### 口播版本
[适合视频开头/结尾的口播版]

### 文字版本
[适合简介/描述区的文字版]

## 声明位置建议

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是法务合规顾问。", temperature=0.4)

    def check_claims(self, transcript: str, language: str = "中文") -> str:
        """Check for potentially problematic claims"""
        prompt = f"""检查视频中可能有问题的声称：

{self._truncate_text(transcript)}

请检查：
## 潜在问题声称

| 声称内容 | 问题类型 | 风险等级 | 建议修改 |
|----------|----------|----------|----------|

## 夸大宣传
## 未经证实的声称
## 绝对化用语
## 敏感话题
## 修改建议

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是广告法合规专家。", temperature=0.3)

    def analyze_compliance(self, transcript: str, platform: str = "youtube", language: str = "中文") -> str:
        """Analyze platform compliance"""
        prompt = f"""分析内容的平台合规性：

**平台**: {platform}
**内容**: {self._truncate_text(transcript)}

请分析：
## 合规性检查

### 社区准则
- 符合: [是/否]
- 问题点:

### 广告政策
### 版权问题
### 敏感内容

## 风险评估
## 合规建议

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是平台政策专家。", temperature=0.4)

    def _truncate_text(self, text: str, max_chars: int = 20000) -> str:
        if len(text) <= max_chars:
            return text
        return text[:max_chars] + "\n[已截断...]"

    @staticmethod
    def get_disclaimer_types() -> Dict:
        return DISCLAIMER_TYPES
