"""
Watch History Analyzer - Analyze YouTube watch history
观看历史分析 - 分析用户的YouTube观看历史，生成兴趣画像和时间分配报告
"""

import json
from typing import Dict, List, Optional
from datetime import datetime
from .ai_client import get_ai_client


class WatchHistoryAnalyzer:
    """Analyze YouTube watch history"""

    def __init__(self, provider: str = None):
        self.ai = get_ai_client(provider)

    def analyze_history(self, history_data: List[Dict], language: str = "中文") -> str:
        """Analyze watch history data"""
        # Format history for analysis
        history_summary = self._summarize_history(history_data)

        prompt = f"""分析以下YouTube观看历史：

{history_summary}

请分析：
## 观看概况
- 总观看数:
- 时间范围:
- 最活跃时段:

## 兴趣画像
### 主要兴趣领域
| 领域 | 视频数 | 占比 |
|------|--------|------|

### 兴趣变化趋势
[时间线上的兴趣变化]

## 观看习惯
- 偏好的视频时长
- 最常观看时间
- 周末vs工作日

## 频道偏好
### Top 10 频道

## 内容建议
[基于历史的内容推荐]

## 时间分配建议
[如何优化观看时间]

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是数据分析专家。", temperature=0.5)

    def generate_interest_profile(self, history_data: List[Dict], language: str = "中文") -> str:
        """Generate user interest profile"""
        history_summary = self._summarize_history(history_data)

        prompt = f"""基于观看历史生成用户画像：

{history_summary}

请生成：
## 用户兴趣画像

### 核心兴趣 (Top 3)
1. [兴趣1] - 置信度: X%
2. [兴趣2] - 置信度: X%
3. [兴趣3] - 置信度: X%

### 次要兴趣
### 潜在兴趣

## 用户特征
- 学习型/娱乐型
- 深度/广度偏好
- 新内容/老内容偏好

## 推荐策略

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是用户研究专家。", temperature=0.5)

    def analyze_time_spent(self, history_data: List[Dict], language: str = "中文") -> str:
        """Analyze time spent watching"""
        history_summary = self._summarize_history(history_data)

        prompt = f"""分析观看时间分布：

{history_summary}

请分析：
## 时间分配报告

### 每日观看时间
| 日期 | 时长 | 主要内容 |
|------|------|----------|

### 时段分布
- 早晨 (6-12):
- 下午 (12-18):
- 晚间 (18-24):
- 深夜 (0-6):

### 周分布
### 月趋势

## 时间质量分析
- 有效学习时间:
- 娱乐时间:
- 可优化时间:

## 改进建议

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是时间管理顾问。", temperature=0.5)

    def detect_patterns(self, history_data: List[Dict], language: str = "中文") -> str:
        """Detect viewing patterns"""
        history_summary = self._summarize_history(history_data)

        prompt = f"""检测观看行为模式：

{history_summary}

请检测：
## 行为模式

### 连续观看模式
[binge watching 检测]

### 主题跳跃模式
### 时间规律
### 推荐依赖度

## 积极模式
[好的观看习惯]

## 需注意模式
[可能需要调整的习惯]

## 建议

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是行为分析师。", temperature=0.5)

    def _summarize_history(self, history_data: List[Dict], max_items: int = 100) -> str:
        """Summarize history data for analysis"""
        if not history_data:
            return "无观看历史数据"

        items = history_data[:max_items]
        summary_parts = []

        for item in items:
            title = item.get('title', '未知')
            channel = item.get('channel', '未知')
            date = item.get('date', '未知')
            duration = item.get('duration', '未知')
            summary_parts.append(f"- {title} | {channel} | {date} | {duration}")

        return "\n".join(summary_parts[:50]) + f"\n... 共{len(history_data)}条记录"

    def export_report(self, analysis: str, format: str = "markdown") -> str:
        """Export analysis report"""
        if format == "html":
            return f"<html><body><pre>{analysis}</pre></body></html>"
        return analysis
