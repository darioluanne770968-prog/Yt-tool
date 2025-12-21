"""
Citation Generator - Generate academic citations for videos
学术引用生成 - 生成视频的学术引用格式（APA、MLA、Chicago等）
"""

from typing import Dict, List, Optional
from datetime import datetime
from .ai_client import get_ai_client


CITATION_STYLES = {
    "apa": {"name": "APA (7th Edition)", "description": "美国心理学会格式"},
    "mla": {"name": "MLA (9th Edition)", "description": "现代语言协会格式"},
    "chicago": {"name": "Chicago (17th Edition)", "description": "芝加哥格式"},
    "harvard": {"name": "Harvard", "description": "哈佛引用格式"},
    "ieee": {"name": "IEEE", "description": "电气电子工程师协会格式"},
    "vancouver": {"name": "Vancouver", "description": "温哥华格式（医学）"},
    "gb": {"name": "GB/T 7714", "description": "中国国家标准"},
}


class CitationGenerator:
    """Generate academic citations for video content"""

    def __init__(self, provider: str = None):
        self.ai = get_ai_client(provider)

    def generate_citation(self, video_info: Dict, style: str = "apa", language: str = "中文") -> str:
        """Generate citation in specified style"""
        style_info = CITATION_STYLES.get(style, CITATION_STYLES["apa"])

        prompt = f"""为以下视频生成{style_info['name']}格式的学术引用：

视频信息：
- 标题: {video_info.get('title', '未知')}
- 作者/频道: {video_info.get('channel', '未知')}
- 发布日期: {video_info.get('date', '未知')}
- URL: {video_info.get('url', '未知')}
- 时长: {video_info.get('duration', '未知')}

请生成：
## {style_info['name']} 引用格式

### 参考文献格式
[完整的参考文献条目]

### 文内引用格式
[括号引用格式]

### 注释格式
[脚注/尾注格式]

## 引用说明
- 格式要求
- 注意事项

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是学术写作专家。", temperature=0.3)

    def generate_all_formats(self, video_info: Dict, language: str = "中文") -> str:
        """Generate citations in all major formats"""
        prompt = f"""为以下视频生成所有主要格式的学术引用：

视频信息：
- 标题: {video_info.get('title', '未知')}
- 作者/频道: {video_info.get('channel', '未知')}
- 发布日期: {video_info.get('date', '未知')}
- URL: {video_info.get('url', '未知')}

请生成：
## 学术引用格式汇总

### APA (7th Edition)
[引用]

### MLA (9th Edition)
[引用]

### Chicago (17th Edition)
[引用]

### Harvard
[引用]

### IEEE
[引用]

### GB/T 7714
[引用]

## 复制模板
[便于复制的纯文本版本]

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是引用格式专家。", temperature=0.3)

    def extract_citable_content(self, transcript: str, video_info: Dict, language: str = "中文") -> str:
        """Extract citable quotes and content"""
        prompt = f"""从视频中提取可引用的内容：

视频: {video_info.get('title', '未知')}
内容: {self._truncate_text(transcript)}

请提取：
## 可引用内容

### 直接引用
| 引用内容 | 时间点 | 引用格式 |
|----------|--------|----------|
| "[原话]" | XX:XX | (作者, 年份, XX:XX) |

### 间接引用/转述
[可以转述的观点]

### 关键概念
[可以引用的定义或概念]

## 引用建议
- 何时使用直接引用
- 何时使用间接引用

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是学术写作导师。", temperature=0.4)

    def create_bibliography(self, videos: List[Dict], style: str = "apa", language: str = "中文") -> str:
        """Create bibliography from multiple videos"""
        videos_text = "\n".join([
            f"- {v.get('title', '未知')} | {v.get('channel', '未知')} | {v.get('date', '未知')} | {v.get('url', '')}"
            for v in videos
        ])

        style_info = CITATION_STYLES.get(style, CITATION_STYLES["apa"])

        prompt = f"""生成{style_info['name']}格式的参考文献列表：

视频列表：
{videos_text}

请生成：
## 参考文献

[按格式要求排列的完整参考文献列表]

## 格式说明
## 排序规则

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是文献管理专家。", temperature=0.3)

    def _truncate_text(self, text: str, max_chars: int = 10000) -> str:
        if len(text) <= max_chars:
            return text
        return text[:max_chars] + "..."

    @staticmethod
    def get_styles() -> Dict:
        return CITATION_STYLES
