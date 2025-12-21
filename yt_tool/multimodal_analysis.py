"""
Multimodal Analysis - Combine video frames, audio, and subtitles for comprehensive analysis
多模态分析 - 结合视频画面（截图）+ 音频 + 字幕进行综合分析
"""

import os
import json
import subprocess
from typing import Dict, List, Optional, Tuple
from .ai_client import get_ai_client


class MultimodalAnalyzer:
    """Multimodal analyzer combining visual, audio, and text analysis"""

    def __init__(self, provider: str = None):
        """
        Initialize multimodal analyzer

        Args:
            provider: AI provider ('openai', 'anthropic', or 'gemini')
        """
        self.ai = get_ai_client(provider)
        self.frames: List[Dict] = []
        self.transcript = ""
        self.audio_analysis = {}

    def extract_frames(
        self,
        video_path: str,
        interval: int = 30,
        output_dir: str = None,
        max_frames: int = 20
    ) -> List[str]:
        """
        Extract key frames from video

        Args:
            video_path: Path to video file
            interval: Seconds between frames
            output_dir: Output directory for frames
            max_frames: Maximum number of frames to extract

        Returns:
            List of frame file paths
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video not found: {video_path}")

        output_dir = output_dir or os.path.dirname(video_path)
        os.makedirs(output_dir, exist_ok=True)

        # Get video duration
        duration = self._get_video_duration(video_path)
        if duration <= 0:
            return []

        # Calculate actual interval to get max_frames
        actual_interval = max(interval, duration // max_frames)

        # Extract frames using ffmpeg
        frame_paths = []
        base_name = os.path.splitext(os.path.basename(video_path))[0]

        for i, timestamp in enumerate(range(0, int(duration), actual_interval)):
            if len(frame_paths) >= max_frames:
                break

            output_path = os.path.join(output_dir, f"{base_name}_frame_{i:04d}.jpg")

            cmd = [
                "ffmpeg", "-y",
                "-ss", str(timestamp),
                "-i", video_path,
                "-frames:v", "1",
                "-q:v", "2",
                output_path
            ]

            try:
                subprocess.run(cmd, capture_output=True, check=True)
                if os.path.exists(output_path):
                    frame_paths.append(output_path)
                    self.frames.append({
                        "path": output_path,
                        "timestamp": timestamp,
                        "index": i
                    })
            except subprocess.CalledProcessError:
                continue

        return frame_paths

    def _get_video_duration(self, video_path: str) -> float:
        """Get video duration in seconds"""
        cmd = [
            "ffprobe",
            "-v", "quiet",
            "-show_entries", "format=duration",
            "-of", "csv=p=0",
            video_path
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return float(result.stdout.strip())
        except (subprocess.CalledProcessError, ValueError):
            return 0

    def set_transcript(self, transcript: str):
        """Set video transcript for analysis"""
        self.transcript = transcript

    def analyze_frame(
        self,
        frame_path: str,
        timestamp: float = None,
        language: str = "中文"
    ) -> str:
        """
        Analyze a single video frame

        Args:
            frame_path: Path to frame image
            timestamp: Timestamp of the frame
            language: Output language

        Returns:
            Frame analysis
        """
        # Note: Actual image analysis would require vision-capable models
        # This is a placeholder for the prompt structure

        timestamp_text = f"（时间戳: {self._format_timestamp(timestamp)}）" if timestamp else ""

        prompt = f"""分析以下视频截图{timestamp_text}：

请描述：
1. 画面中的主要内容
2. 文字信息（如有）
3. 图表、代码或公式（如有）
4. 与字幕内容的关联

使用{language}输出。"""

        # In real implementation, would send image to vision model
        return f"[需要视觉模型支持] 帧分析: {frame_path}"

    def detect_visual_elements(
        self,
        frame_paths: List[str] = None,
        language: str = "中文"
    ) -> Dict:
        """
        Detect visual elements in video frames

        Args:
            frame_paths: List of frame paths to analyze
            language: Output language

        Returns:
            Detected visual elements by category
        """
        frame_paths = frame_paths or [f["path"] for f in self.frames]

        # Structure for detected elements
        elements = {
            "code_blocks": [],
            "charts_graphs": [],
            "formulas": [],
            "text_overlays": [],
            "diagrams": [],
            "screenshots": [],
            "faces": [],
            "products": []
        }

        # Note: Actual detection would require vision models
        # This provides the structure for integration

        return elements

    def analyze_with_context(
        self,
        transcript: str = None,
        frames: List[str] = None,
        language: str = "中文"
    ) -> str:
        """
        Comprehensive multimodal analysis

        Args:
            transcript: Video transcript
            frames: Frame paths for analysis
            language: Output language

        Returns:
            Comprehensive analysis
        """
        transcript = transcript or self.transcript

        prompt = f"""进行多模态综合分析：

## 字幕内容
{self._truncate_text(transcript)}

## 视频帧信息
已提取 {len(self.frames)} 个关键帧

请提供：

### 1. 内容概述
基于字幕和视觉内容的综合摘要

### 2. 视觉内容分析
- 主要的视觉元素
- 图表、代码、公式等专业内容
- 演示或演讲风格

### 3. 信息密度分析
- 高信息密度的时间段
- 需要重点关注的部分

### 4. 多模态关联
- 字幕与画面的配合程度
- 视觉辅助对理解的帮助

### 5. 学习建议
- 需要反复观看的部分
- 建议的学习方式

请用{language}输出。"""

        system_prompt = """你是一个多模态内容分析专家，擅长综合分析视频的视觉和音频内容。
你的分析应该全面、深入、有见地。"""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.5
        )

        return response

    def extract_visual_knowledge(
        self,
        transcript: str = None,
        language: str = "中文"
    ) -> str:
        """
        Extract knowledge that's primarily conveyed visually

        Args:
            transcript: Video transcript
            language: Output language

        Returns:
            Visual knowledge extraction
        """
        transcript = transcript or self.transcript

        prompt = f"""基于视频内容，识别主要通过视觉传达的知识：

字幕内容：
{self._truncate_text(transcript)}

请识别并描述：

1. **代码示例**
   - 视频中展示的代码片段
   - 代码的功能和用法

2. **图表和数据**
   - 展示的图表类型
   - 关键数据点和趋势

3. **公式和方程**
   - 数学公式
   - 科学方程

4. **流程和架构图**
   - 流程图
   - 系统架构图
   - 关系图

5. **操作演示**
   - 软件操作步骤
   - 工具使用方法

请用{language}输出，尽可能还原视觉内容。"""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt="你是一个视觉知识提取专家，擅长从视频内容中识别和描述视觉传达的信息。",
            temperature=0.5
        )

        return response

    def generate_scene_summary(
        self,
        transcript: str = None,
        language: str = "中文"
    ) -> str:
        """
        Generate scene-by-scene summary

        Args:
            transcript: Video transcript
            language: Output language

        Returns:
            Scene summary
        """
        transcript = transcript or self.transcript

        prompt = f"""将视频分解为场景并总结每个场景：

字幕内容：
{self._truncate_text(transcript)}

请提供：

## 场景分解

### 场景 1: [场景标题]
- **时间范围**: [开始] - [结束]
- **内容摘要**: [场景主要内容]
- **关键要点**: [重要信息]
- **视觉特征**: [场景的视觉特点]

### 场景 2: [场景标题]
...

## 场景关联分析
- 场景之间的逻辑关系
- 内容的递进结构

请用{language}输出。"""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt="你是一个视频内容分析专家，擅长识别和总结视频场景。",
            temperature=0.5
        )

        return response

    def analyze_presentation_style(
        self,
        transcript: str = None,
        language: str = "中文"
    ) -> str:
        """
        Analyze video presentation style

        Args:
            transcript: Video transcript
            language: Output language

        Returns:
            Presentation style analysis
        """
        transcript = transcript or self.transcript

        prompt = f"""分析视频的呈现风格：

字幕内容：
{self._truncate_text(transcript)}

请分析：

### 1. 演讲风格
- 正式程度
- 语速和节奏
- 表达方式

### 2. 视觉设计
- 整体视觉风格
- 配色和布局
- 信息呈现方式

### 3. 内容组织
- 结构安排
- 过渡方式
- 重点突出方法

### 4. 互动元素
- 观众互动方式
- 问题引导
- 行动号召

### 5. 专业评价
- 优点
- 可改进之处
- 适合的受众

请用{language}输出。"""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt="你是一个演示技巧和内容呈现专家。",
            temperature=0.6
        )

        return response

    def create_visual_notes(
        self,
        transcript: str = None,
        language: str = "中文"
    ) -> str:
        """
        Create visual-enhanced notes

        Args:
            transcript: Video transcript
            language: Output language

        Returns:
            Visual notes in markdown format
        """
        transcript = transcript or self.transcript

        prompt = f"""创建视觉增强的学习笔记：

字幕内容：
{self._truncate_text(transcript)}

请创建包含以下元素的笔记：

1. **结构化笔记**
   - 使用标题、列表、表格组织内容
   - 突出关键信息

2. **Mermaid图表**
   - 为概念关系创建流程图或思维导图
   - 使用mermaid语法

3. **代码块**
   - 整理提到的代码示例

4. **数学公式**
   - 使用LaTeX格式

5. **时间戳索引**
   - 重要内容的时间戳

请用{language}输出，使用Markdown格式。"""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt="你是一个笔记整理专家，擅长创建视觉化的学习笔记。",
            temperature=0.5
        )

        return response

    def _format_timestamp(self, seconds: float) -> str:
        """Format seconds to MM:SS or HH:MM:SS"""
        if seconds is None:
            return ""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        return f"{minutes:02d}:{secs:02d}"

    def _truncate_text(self, text: str, max_chars: int = 25000) -> str:
        """Truncate text if too long"""
        if len(text) <= max_chars:
            return text
        return text[:max_chars] + "\n\n[内容过长，已截断...]"


def analyze_video_multimodal(
    transcript: str,
    video_path: str = None,
    language: str = "中文",
    provider: str = None
) -> str:
    """
    Convenience function for multimodal analysis

    Args:
        transcript: Video transcript
        video_path: Optional path to video file
        language: Output language
        provider: AI provider

    Returns:
        Multimodal analysis
    """
    analyzer = MultimodalAnalyzer(provider)
    analyzer.set_transcript(transcript)

    if video_path and os.path.exists(video_path):
        analyzer.extract_frames(video_path)

    return analyzer.analyze_with_context(language=language)
