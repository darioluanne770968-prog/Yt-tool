"""
Learning path generation from playlists
"""

import subprocess
import json
from typing import Dict, List, Optional
from .ai_client import get_ai_client
from .extractor import TranscriptExtractor


class LearningPathGenerator:
    """Generate optimized learning paths from video playlists"""

    def __init__(self):
        self.ai_client = get_ai_client()

    def get_playlist_videos(self, playlist_url: str) -> List[Dict]:
        """Get videos from a playlist"""
        cmd = [
            "yt-dlp",
            "--dump-json",
            "--flat-playlist",
            playlist_url,
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120,
            )

            videos = []
            for line in result.stdout.strip().split("\n"):
                if line:
                    try:
                        videos.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue

            return videos
        except Exception as e:
            return []

    def generate_learning_path(
        self,
        playlist_url: str,
        language: str = "中文",
        skill_level: str = "beginner",
    ) -> str:
        """
        Generate optimized learning path from playlist

        Args:
            playlist_url: YouTube playlist URL
            language: Output language
            skill_level: beginner, intermediate, advanced

        Returns:
            Learning path guide
        """
        videos = self.get_playlist_videos(playlist_url)

        if not videos:
            return "无法获取播放列表信息"

        video_list = "\n".join([
            f"{i}. {v.get('title', 'Unknown')} (duration: {v.get('duration', 'N/A')}s)"
            for i, v in enumerate(videos, 1)
        ])

        system_prompt = f"""You are an expert learning designer.
Create optimized learning paths in {language}. Consider {skill_level} level learners."""

        prompt = f"""Create an optimized learning path from this playlist:

Videos in playlist:
{video_list}

Generate:

## 学习路径规划

### 课程概览
- 总视频数: {len(videos)}
- 预计总时长: [Calculate]
- 难度级别: {skill_level}
- 适合人群: [Description]

### 推荐学习顺序
[Reorder videos for optimal learning, may differ from playlist order]

#### 第一阶段: 基础入门
| 顺序 | 视频 | 预计时长 | 学习目标 |
|------|------|----------|----------|
| 1 | [Video] | Xmin | [Objective] |
| 2 | [Video] | Xmin | [Objective] |

#### 第二阶段: 核心概念
...

#### 第三阶段: 进阶应用
...

#### 第四阶段: 实战练习
...

### 每日学习计划
[Suggested daily schedule]

| 天数 | 视频 | 学习时间 | 复习/练习 |
|------|------|----------|-----------|
| Day 1 | [Videos] | Xhr | [Tasks] |
| Day 2 | [Videos] | Xhr | [Tasks] |
...

### 里程碑检查点
[Checkpoints to verify understanding]

### 补充资源建议
[Additional resources for each stage]

### 学习技巧
[Tips for maximizing learning from these videos]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=4096)

    def analyze_prerequisites(
        self,
        video_titles: List[str],
        language: str = "中文",
    ) -> str:
        """Analyze prerequisites for videos"""
        system_prompt = f"Analyze learning prerequisites in {language}."

        titles = "\n".join([f"- {t}" for t in video_titles])

        prompt = f"""Analyze prerequisites for these videos:

{titles}

## 前置知识分析

### 基础要求
[What learners should know before starting]

### 依赖关系图
[Which videos depend on others]

```
Video A
  └── Video B (requires A)
      └── Video C (requires B)
Video D (independent)
```

### 可跳过内容
[Videos that can be skipped based on experience]

### 建议复习
[Topics to review before starting]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=2000)

    def estimate_completion_time(
        self,
        playlist_url: str,
        hours_per_day: float = 2,
        language: str = "中文",
    ) -> str:
        """Estimate time to complete playlist"""
        videos = self.get_playlist_videos(playlist_url)

        if not videos:
            return "无法获取播放列表信息"

        total_seconds = sum(v.get("duration", 0) or 0 for v in videos)
        total_hours = total_seconds / 3600

        # Account for practice time (1.5x video time)
        learning_hours = total_hours * 1.5
        days_needed = learning_hours / hours_per_day

        return f"""## 完成时间估算

### 视频总时长
- 视频数量: {len(videos)}
- 纯视频时长: {total_hours:.1f} 小时

### 学习时间估算
- 包含练习: {learning_hours:.1f} 小时
- 每天学习 {hours_per_day} 小时
- 预计完成天数: {days_needed:.0f} 天

### 时间分配建议
- 观看视频: {total_hours:.1f} 小时 (40%)
- 笔记整理: {total_hours * 0.3:.1f} 小时 (20%)
- 练习实践: {total_hours * 0.5:.1f} 小时 (30%)
- 复习巩固: {total_hours * 0.2:.1f} 小时 (10%)
"""

    def create_study_schedule(
        self,
        playlist_url: str,
        start_date: str = None,
        hours_per_day: float = 2,
        language: str = "中文",
    ) -> str:
        """Create detailed study schedule"""
        videos = self.get_playlist_videos(playlist_url)

        if not videos:
            return "无法获取播放列表信息"

        video_list = "\n".join([
            f"- {v.get('title', 'Unknown')} ({(v.get('duration', 0) or 0) // 60}min)"
            for v in videos
        ])

        system_prompt = f"Create study schedules in {language}."

        prompt = f"""Create a detailed study schedule for this playlist:

Videos:
{video_list}

Parameters:
- Study time per day: {hours_per_day} hours
- Starting: {start_date or 'Tomorrow'}

Generate:

## 学习日程表

### Week 1
| 日期 | 学习内容 | 时长 | 任务 | 完成 |
|------|----------|------|------|------|
| Day 1 | [Video(s)] | Xhr | [Tasks] | [ ] |
| Day 2 | [Video(s)] | Xhr | [Tasks] | [ ] |
...

### Week 2
...

### 休息日建议
[Recommended rest days]

### 复习日
[Scheduled review sessions]

### 弹性时间
[Buffer time for catching up]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=3000)

    def identify_key_videos(
        self,
        playlist_url: str,
        language: str = "中文",
    ) -> str:
        """Identify the most important videos in playlist"""
        videos = self.get_playlist_videos(playlist_url)

        if not videos:
            return "无法获取播放列表信息"

        video_list = "\n".join([
            f"- {v.get('title', 'Unknown')}"
            for v in videos
        ])

        system_prompt = f"Identify key learning content in {language}."

        prompt = f"""Identify the most important videos in this playlist:

{video_list}

## 核心视频分析

### 必看视频 (Core)
[Videos that are absolutely essential]
1. [Video] - Reason: [Why essential]
...

### 重要视频 (Important)
[Videos that are highly recommended]
1. [Video] - Reason
...

### 可选视频 (Optional)
[Videos that can be skipped if time is limited]
1. [Video] - When to watch
...

### 速成路径
[Minimum videos for quick learning - if time is very limited]

### 完整路径
[All videos in recommended order]
"""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=2500)
