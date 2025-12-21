"""
Monetization Advisor - Video monetization strategy suggestions
变现建议 - 分析视频内容，提供变现建议（广告、赞助、产品植入）
"""

from typing import Dict, List, Optional
from .ai_client import get_ai_client


MONETIZATION_TYPES = {
    "ads": {"name": "广告收入", "description": "平台广告分成"},
    "sponsorship": {"name": "品牌赞助", "description": "品牌合作推广"},
    "affiliate": {"name": "联盟营销", "description": "推广链接佣金"},
    "membership": {"name": "会员订阅", "description": "付费会员内容"},
    "merchandise": {"name": "周边商品", "description": "自有品牌产品"},
    "courses": {"name": "付费课程", "description": "知识付费"},
    "consulting": {"name": "咨询服务", "description": "一对一服务"},
    "donations": {"name": "打赏/捐赠", "description": "粉丝支持"},
}


class MonetizationAdvisor:
    """Video monetization strategy advisor"""

    def __init__(self, provider: str = None):
        self.ai = get_ai_client(provider)

    def analyze_monetization_potential(self, transcript: str, channel_info: Dict = None, language: str = "中文") -> str:
        """Analyze monetization potential"""
        channel_text = str(channel_info) if channel_info else "未提供"

        prompt = f"""分析视频的变现潜力：

**频道信息**: {channel_text}
**视频内容**: {self._truncate_text(transcript)}

请分析：
## 变现潜力评估
- 广告价值: /10
- 赞助价值: /10
- 产品化潜力: /10

## 目标受众分析
- 人群画像
- 消费能力
- 购买意愿

## 适合的变现方式
[按推荐度排序]

## 潜在赞助商类型
## 产品植入机会
## 收入预估

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是内容变现专家。", temperature=0.6)

    def suggest_sponsors(self, transcript: str, niche: str = "general", language: str = "中文") -> str:
        """Suggest potential sponsors"""
        prompt = f"""基于视频内容推荐潜在赞助商：

**领域**: {niche}
**内容**: {self._truncate_text(transcript)}

请推荐：
## 高匹配度品牌
| 品牌类型 | 匹配原因 | 合作形式 | 预估报价 |
|----------|----------|----------|----------|

## 潜在品牌
## 接洽建议
## 合作提案要点
## 定价建议

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是品牌合作顾问。", temperature=0.6)

    def identify_product_placements(self, transcript: str, language: str = "中文") -> str:
        """Identify product placement opportunities"""
        prompt = f"""识别视频中的产品植入机会：

{self._truncate_text(transcript)}

请识别：
## 自然植入点
| 时间点 | 场景 | 适合品类 | 植入方式 |
|--------|------|----------|----------|

## 软性推荐机会
## 硬广位置
## 植入技巧
## 避免事项

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是广告植入专家。", temperature=0.6)

    def create_media_kit(self, channel_info: Dict, transcript_samples: List[str], language: str = "中文") -> str:
        """Create media kit content"""
        samples = "\n".join([f"示例{i+1}: {self._truncate_text(t, 1000)}" for i, t in enumerate(transcript_samples[:3])])

        prompt = f"""生成媒体合作资料：

**频道信息**: {channel_info}
**内容示例**: {samples}

请生成：
## 频道介绍
## 受众分析
## 内容特色
## 合作形式
## 成功案例（模板）
## 报价参考
## 联系方式模板

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是商务合作专家。", temperature=0.5)

    def calculate_roi(self, investment: float, metrics: Dict, language: str = "中文") -> str:
        """Calculate potential ROI"""
        prompt = f"""计算内容变现ROI：

**投入**: {investment}
**数据**: {metrics}

请分析：
## 收入预估
## ROI计算
## 优化建议
## 增长路径

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是商业分析师。", temperature=0.5)

    def _truncate_text(self, text: str, max_chars: int = 15000) -> str:
        if len(text) <= max_chars:
            return text
        return text[:max_chars] + "..."

    @staticmethod
    def get_monetization_types() -> Dict:
        return MONETIZATION_TYPES
