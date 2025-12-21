"""
Trend Detector - Detect content trends and predict topics
趋势预测 - 基于频道/领域的视频数据，预测下一个热门话题
"""

from typing import Dict, List, Optional
from .ai_client import get_ai_client


class TrendDetector:
    """Content trend detection and prediction"""

    def __init__(self, provider: str = None):
        self.ai = get_ai_client(provider)

    def analyze_trends(self, videos: List[Dict], language: str = "中文") -> str:
        """Analyze content trends"""
        videos_text = "\n".join([
            f"- 《{v.get('title', '未知')}》| 发布: {v.get('date', '未知')} | 播放: {v.get('views', '未知')}"
            for v in videos[:30]
        ])

        prompt = f"""分析以下视频的趋势：

{videos_text}

请分析：
## 趋势分析

### 上升趋势
| 话题 | 增长率 | 代表视频 |
|------|--------|----------|

### 下降趋势
### 稳定话题
### 新兴话题

## 趋势图
[用文字描述趋势曲线]

## 原因分析
## 预测未来3个月趋势

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是内容趋势分析师。", temperature=0.6)

    def predict_topics(self, historical_data: List[Dict], niche: str = "general", language: str = "中文") -> str:
        """Predict upcoming hot topics"""
        data_text = "\n".join([
            f"- {d.get('topic', '未知')}: {d.get('trend', '未知')}"
            for d in historical_data[:20]
        ])

        prompt = f"""预测{niche}领域的下一个热门话题：

历史数据：
{data_text}

请预测：
## 热门话题预测

### 近期热门 (1-2周)
1. [话题] - 概率: X% - 原因:
2.
3.

### 中期热门 (1个月)
### 长期趋势 (3个月)

## 内容建议
| 话题 | 建议切入角度 | 最佳发布时机 |
|------|--------------|--------------|

## 风险提示
[可能的风险和规避方法]

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是趋势预测专家。", temperature=0.7)

    def analyze_seasonality(self, videos: List[Dict], language: str = "中文") -> str:
        """Analyze seasonal trends"""
        videos_text = "\n".join([
            f"- 《{v.get('title', '未知')}》| {v.get('date', '未知')} | {v.get('views', '未知')}"
            for v in videos[:30]
        ])

        prompt = f"""分析内容的季节性规律：

{videos_text}

请分析：
## 季节性分析

### 月度规律
| 月份 | 热门话题 | 观看趋势 |
|------|----------|----------|

### 节假日影响
### 事件驱动
### 周期性话题

## 内容日历建议
[全年内容规划]

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是内容策划专家。", temperature=0.6)

    def detect_viral_signals(self, transcript: str, title: str, language: str = "中文") -> str:
        """Detect viral potential signals"""
        prompt = f"""检测内容的病毒传播信号：

标题: {title}
内容: {self._truncate_text(transcript)}

请检测：
## 病毒传播信号

### 积极信号
- [信号1] ✓
- [信号2] ✓

### 缺失信号
- [信号] ✗

### 病毒传播评分
X/100

### 优化建议
## 传播路径预测

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是病毒营销专家。", temperature=0.6)

    def _truncate_text(self, text: str, max_chars: int = 10000) -> str:
        if len(text) <= max_chars:
            return text
        return text[:max_chars] + "..."
