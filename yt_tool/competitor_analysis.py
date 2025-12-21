"""
Competitor Analysis - Analyze competitor video strategies
竞品分析 - 分析竞争对手的视频策略（发布频率、选题规律、热门内容）
"""

from typing import Dict, List, Optional
from .ai_client import get_ai_client


class CompetitorAnalysis:
    """Competitor video strategy analyzer"""

    def __init__(self, provider: str = None):
        self.ai = get_ai_client(provider)

    def analyze_video_strategy(self, transcripts: List[Dict], language: str = "中文") -> str:
        """Analyze video strategy from multiple videos"""
        videos_text = "\n\n".join([
            f"### 视频{i+1}: {v.get('title', '未知')}\n{self._truncate_text(v.get('transcript', ''), 3000)}"
            for i, v in enumerate(transcripts[:10])
        ])

        prompt = f"""分析以下竞争对手的视频策略：

{videos_text}

请分析：
## 内容策略
- 主要话题领域
- 内容类型分布
- 选题规律

## 风格特点
- 表达风格
- 呈现方式
- 独特卖点

## 成功元素
- 高互动内容特征
- 爆款要素

## 可借鉴之处
## 差异化机会

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是内容策略分析专家。", temperature=0.6)

    def analyze_title_patterns(self, titles: List[str], language: str = "中文") -> str:
        """Analyze title patterns"""
        prompt = f"""分析以下视频标题的规律：

{chr(10).join([f'{i+1}. {t}' for i, t in enumerate(titles)])}

请分析：
## 标题模式
- 常用句式
- 数字使用
- 关键词频率

## 情感触发词
## 点击诱因
## 标题长度分布
## 可借鉴模板

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是标题优化专家。", temperature=0.6)

    def analyze_content_gaps(self, competitor_topics: List[str], your_topics: List[str], language: str = "中文") -> str:
        """Identify content gaps"""
        prompt = f"""对比分析内容差距：

**竞品话题**: {', '.join(competitor_topics)}
**我的话题**: {', '.join(your_topics)}

请分析：
## 内容重叠度
## 竞品独有话题
## 我的独特话题
## 市场机会（未被覆盖的话题）
## 内容建议

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是市场分析师。", temperature=0.6)

    def generate_competitive_report(self, competitor_data: Dict, language: str = "中文") -> str:
        """Generate comprehensive competitive report"""
        prompt = f"""生成竞品分析报告：

**竞品数据**: {competitor_data}

请生成：
## 执行摘要
## 竞品概况
## SWOT分析
## 内容策略对比
## 增长趋势
## 机会与威胁
## 行动建议

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是商业分析顾问。", temperature=0.5)

    def _truncate_text(self, text: str, max_chars: int = 5000) -> str:
        if len(text) <= max_chars:
            return text
        return text[:max_chars] + "..."
