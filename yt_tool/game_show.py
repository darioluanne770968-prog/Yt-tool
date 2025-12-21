"""
Game Show - Generate quiz game show content from video
知识问答游戏 - 基于视频内容生成《开心辞典》《一站到底》风格的问答游戏
"""

from typing import Dict, List, Optional
from .ai_client import get_ai_client


GAME_FORMATS = {
    "millionaire": {"name": "百万富翁", "description": "15题递增难度，4选项"},
    "jeopardy": {"name": "Jeopardy", "description": "分类+金额，答案形式是问题"},
    "rapid_fire": {"name": "快问快答", "description": "30秒内尽量多答"},
    "true_false": {"name": "是非题挑战", "description": "快速判断对错"},
    "elimination": {"name": "一站到底", "description": "答错淘汰"},
    "pyramid": {"name": "金字塔", "description": "用描述猜词"},
}


class GameShow:
    """Quiz game show content generator"""

    def __init__(self, provider: str = None):
        self.ai = get_ai_client(provider)

    def generate_game(self, transcript: str, format: str = "millionaire", language: str = "中文") -> str:
        """Generate quiz game"""
        format_info = GAME_FORMATS.get(format, GAME_FORMATS["millionaire"])

        prompt = f"""基于视频内容创建{format_info['name']}风格的问答游戏：

{self._truncate_text(transcript)}

游戏格式: {format_info['description']}

请生成：
## {format_info['name']} 游戏

### 游戏规则
[简述规则]

### 题目

#### 第1题 (简单)
**问题**:
A.
B.
C.
D.
**正确答案**:
**解析**:

#### 第2题
...

[按难度递增生成15题]

### 生命线/道具
[可用的帮助选项]

### 主持人台词
[串场词建议]

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是知识问答节目编剧。", temperature=0.6)

    def generate_rapid_fire(self, transcript: str, count: int = 30, language: str = "中文") -> str:
        """Generate rapid fire questions"""
        prompt = f"""生成{count}道快问快答题目：

{self._truncate_text(transcript)}

请生成：
## 快问快答 ({count}题)

1. Q: [问题] → A: [简短答案]
2. Q: [问题] → A: [简短答案]
...

## 计分规则
## 挑战模式
- 30秒限时
- 每题2秒

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是速答游戏设计师。", temperature=0.6)

    def generate_jeopardy_board(self, transcript: str, categories: int = 6, language: str = "中文") -> str:
        """Generate Jeopardy-style game board"""
        prompt = f"""创建Jeopardy风格的游戏板：

{self._truncate_text(transcript)}

请生成{categories}个类别，每类5道题（100-500分）：

## Jeopardy 游戏板

| 类别1 | 类别2 | 类别3 | 类别4 | 类别5 | 类别6 |
|-------|-------|-------|-------|-------|-------|
| $100  | $100  | $100  | $100  | $100  | $100  |
| $200  | $200  | $200  | $200  | $200  | $200  |
| $300  | $300  | $300  | $300  | $300  | $300  |
| $400  | $400  | $400  | $400  | $400  | $400  |
| $500  | $500  | $500  | $500  | $500  | $500  |

### 类别1: [类别名]
$100 - 答案: [答案] | 问题: [什么是...]
$200 - ...
...

### 类别2: [类别名]
...

## Daily Double
## Final Jeopardy

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是Jeopardy游戏设计师。", temperature=0.6)

    def generate_elimination_game(self, transcript: str, rounds: int = 5, language: str = "中文") -> str:
        """Generate elimination-style game"""
        prompt = f"""创建一站到底风格的淘汰赛：

{self._truncate_text(transcript)}

请生成{rounds}轮对战：

## 一站到底

### 比赛规则
[淘汰规则说明]

### 第1轮
**选手A vs 选手B**
1. [问题] → [答案]
2. [问题] → [答案]
3. [问题] → [答案]

### 第2轮
...

### 终极对决

## 主持人串词
## 气氛调节问题

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是竞技问答节目策划。", temperature=0.6)

    def generate_party_game(self, transcript: str, players: int = 4, language: str = "中文") -> str:
        """Generate party game version"""
        prompt = f"""创建适合{players}人玩的派对问答游戏：

{self._truncate_text(transcript)}

请生成：
## 派对问答游戏

### 游戏准备
- 所需道具
- 分组方式

### 游戏环节
**环节1: 热身赛**
[简单题目]

**环节2: 团队赛**
[需要合作的题目]

**环节3: 抢答赛**
[快速抢答]

**环节4: 终极挑战**
[高难度题目]

### 惩罚/奖励
## 气氛道具

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是派对游戏策划师。", temperature=0.7)

    def _truncate_text(self, text: str, max_chars: int = 15000) -> str:
        if len(text) <= max_chars:
            return text
        return text[:max_chars] + "..."

    @staticmethod
    def get_formats() -> Dict:
        return GAME_FORMATS
