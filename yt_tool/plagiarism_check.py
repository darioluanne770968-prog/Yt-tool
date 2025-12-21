"""
Plagiarism Check - Check content similarity and originality
内容查重 - 检测视频内容是否与其他视频/文章相似
"""

from typing import Dict, List, Optional
from .ai_client import get_ai_client


class PlagiarismCheck:
    """Content similarity and originality checker"""

    def __init__(self, provider: str = None):
        self.ai = get_ai_client(provider)

    def check_originality(self, transcript: str, language: str = "中文") -> str:
        """Check content originality"""
        prompt = f"""分析以下内容的原创性：

{self._truncate_text(transcript)}

请分析：
## 原创性评估

### 内容类型
- 原创内容: X%
- 常见知识: X%
- 疑似引用: X%

### 独特观点
[列出内容中的独特见解]

### 常见表述
[可能在其他地方见过的表述]

### 潜在引用来源
[可能的参考来源类型]

## 建议
- 如何提高原创性
- 需要标注引用的部分

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是内容审核专家。", temperature=0.4)

    def compare_content(self, content1: str, content2: str, language: str = "中文") -> str:
        """Compare two pieces of content"""
        prompt = f"""对比以下两段内容的相似度：

**内容1**: {self._truncate_text(content1, 8000)}

**内容2**: {self._truncate_text(content2, 8000)}

请分析：
## 相似度分析

### 整体相似度: X%

### 结构相似度
### 观点相似度
### 表述相似度

### 相似段落
| 内容1位置 | 内容2位置 | 相似度 |
|-----------|-----------|--------|

### 差异分析
## 判断结论

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是内容对比专家。", temperature=0.3)

    def identify_sources(self, transcript: str, language: str = "中文") -> str:
        """Identify potential source materials"""
        prompt = f"""识别内容可能的来源：

{self._truncate_text(transcript)}

请识别：
## 可能的来源

### 学术/书籍
### 新闻报道
### 其他视频
### 网络文章
### 官方资料

## 引用建议
[哪些内容需要标注来源]

## 版权提醒

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是信息溯源专家。", temperature=0.5)

    def suggest_citations(self, transcript: str, language: str = "中文") -> str:
        """Suggest proper citations"""
        prompt = f"""为以下内容建议引用格式：

{self._truncate_text(transcript)}

请建议：
## 需要引用的内容

| 内容 | 来源类型 | 建议引用格式 |
|------|----------|--------------|

## 引用示例
## 视频描述引用模板

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是学术引用专家。", temperature=0.5)

    def _truncate_text(self, text: str, max_chars: int = 15000) -> str:
        if len(text) <= max_chars:
            return text
        return text[:max_chars] + "..."
