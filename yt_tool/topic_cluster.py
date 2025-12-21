"""
Topic Cluster - Cluster videos by topic
主题聚类 - 将多个视频按主题自动分类聚类
"""

from typing import Dict, List, Optional
from .ai_client import get_ai_client


class TopicCluster:
    """Cluster videos by topic"""

    def __init__(self, provider: str = None):
        self.ai = get_ai_client(provider)

    def cluster_videos(self, videos: List[Dict], language: str = "中文") -> str:
        """Cluster videos by topic"""
        videos_text = "\n".join([
            f"- 《{v.get('title', '未知')}》: {self._truncate_text(v.get('transcript', ''), 500)}"
            for v in videos[:20]
        ])

        prompt = f"""将以下视频按主题聚类：

{videos_text}

请分析：
## 主题聚类

### 主题1: [主题名称]
- 视频列表:
- 共同特征:
- 子主题:

### 主题2: [主题名称]
...

## 聚类可视化
```
主题1
├── 子主题A
│   ├── 视频1
│   └── 视频2
└── 子主题B
    └── 视频3
```

## 关联分析
[主题之间的关联]

## 学习路径建议

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是内容分类专家。", temperature=0.5)

    def suggest_categories(self, video_titles: List[str], language: str = "中文") -> str:
        """Suggest category structure"""
        prompt = f"""为以下视频标题建议分类结构：

{chr(10).join(video_titles[:30])}

请建议：
## 分类体系

### 一级分类
1. [分类名]
   - 二级分类A
   - 二级分类B

### 分类映射
| 视频 | 建议分类 |
|------|----------|

## 标签建议
## 分类原则

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是信息架构师。", temperature=0.5)

    def find_related_videos(self, target_video: Dict, all_videos: List[Dict], top_n: int = 5, language: str = "中文") -> str:
        """Find related videos"""
        target_text = f"目标: 《{target_video.get('title', '未知')}》\n{self._truncate_text(target_video.get('transcript', ''), 2000)}"
        videos_text = "\n".join([
            f"- 《{v.get('title', '未知')}》: {self._truncate_text(v.get('transcript', ''), 300)}"
            for v in all_videos[:20]
        ])

        prompt = f"""找出与目标视频最相关的{top_n}个视频：

{target_text}

候选视频：
{videos_text}

请分析：
## 相关视频 Top {top_n}

### 1. 《视频名》
- 相关度: X%
- 相关原因:
- 关系类型: [补充/深入/对比/...]

### 2. ...

## 观看顺序建议
## 关联图谱

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是内容推荐专家。", temperature=0.5)

    def generate_topic_map(self, videos: List[Dict], language: str = "中文") -> str:
        """Generate topic map"""
        videos_text = "\n".join([
            f"- 《{v.get('title', '未知')}》"
            for v in videos[:30]
        ])

        prompt = f"""为以下视频生成主题地图：

{videos_text}

请生成：
## 主题地图

### Mermaid图
```mermaid
graph TD
    A[核心主题] --> B[子主题1]
    A --> C[子主题2]
    B --> D[视频1]
    ...
```

### 主题说明
### 知识结构
### 学习建议

用{language}输出。"""

        return self.ai.chat(prompt=prompt, system_prompt="你是知识图谱专家。", temperature=0.5)

    def _truncate_text(self, text: str, max_chars: int = 500) -> str:
        if len(text) <= max_chars:
            return text
        return text[:max_chars] + "..."
