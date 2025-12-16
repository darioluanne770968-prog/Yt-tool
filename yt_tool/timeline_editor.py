"""
Timeline Editor - 时间线编辑器
Visual timeline editing and video segmentation tools
"""

import json
from typing import Dict, List, Any, Optional
from .ai_client import get_ai_client


class TimelineEditor:
    """Edit and visualize video timelines"""

    def __init__(self):
        self.ai_client = get_ai_client()

    def generate_timeline(self, transcript: str, duration: int = 0, language: str = "中文") -> Dict[str, Any]:
        """Generate timeline segments from transcript"""
        prompt = f"""分析以下视频内容，生成时间线分段。

内容：
{transcript[:8000]}

视频时长：{duration}秒（如果为0请估算）

返回JSON格式：
1. total_duration: 总时长（秒）
2. segments: 分段数组，每个包含：
   - id: 段落ID
   - start: 开始时间（秒）
   - end: 结束时间（秒）
   - title: 段落标题
   - summary: 简要内容
   - type: 类型（intro/main/example/conclusion/transition）
   - importance: 重要度（1-10）
   - tags: 标签

3. highlights: 高光时刻
4. skip_suggestions: 可跳过的部分

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"raw": response}

    def format_timestamp(self, seconds: int) -> str:
        """Convert seconds to HH:MM:SS format"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        return f"{minutes:02d}:{secs:02d}"

    def parse_timestamp(self, timestamp: str) -> int:
        """Convert HH:MM:SS or MM:SS to seconds"""
        parts = timestamp.split(":")
        if len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
        elif len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        return 0

    def export_youtube_chapters(self, timeline: Dict) -> str:
        """Export as YouTube chapter format"""
        chapters = []
        for seg in timeline.get("segments", []):
            start = self.format_timestamp(seg.get("start", 0))
            title = seg.get("title", "")
            chapters.append(f"{start} {title}")

        return "\n".join(chapters)

    def export_vtt_chapters(self, timeline: Dict) -> str:
        """Export as WebVTT chapter format"""
        vtt = "WEBVTT\n\n"
        for i, seg in enumerate(timeline.get("segments", []), 1):
            start = self.format_timestamp(seg.get("start", 0))
            end = self.format_timestamp(seg.get("end", 0))
            title = seg.get("title", "")
            vtt += f"{i}\n{start}.000 --> {end}.000\n{title}\n\n"
        return vtt

    def export_edl(self, timeline: Dict, fps: float = 30.0) -> str:
        """Export as Edit Decision List (EDL) format"""
        edl = "TITLE: Video Timeline\nFCM: NON-DROP FRAME\n\n"
        for i, seg in enumerate(timeline.get("segments", []), 1):
            start_tc = self._seconds_to_timecode(seg.get("start", 0), fps)
            end_tc = self._seconds_to_timecode(seg.get("end", 0), fps)
            edl += f"{i:03d}  001      V     C        {start_tc} {end_tc} {start_tc} {end_tc}\n"
            edl += f"* FROM CLIP NAME: {seg.get('title', 'Segment')}\n\n"
        return edl

    def _seconds_to_timecode(self, seconds: int, fps: float) -> str:
        """Convert seconds to SMPTE timecode"""
        frames = int((seconds % 1) * fps)
        total_seconds = int(seconds)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        secs = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:02d}:{frames:02d}"

    def generate_visual_timeline_html(self, timeline: Dict, title: str = "视频时间线") -> str:
        """Generate visual HTML timeline"""
        total = timeline.get("total_duration", 100)
        segments_html = ""

        colors = {
            "intro": "#3498db",
            "main": "#2ecc71",
            "example": "#f39c12",
            "conclusion": "#9b59b6",
            "transition": "#95a5a6"
        }

        for seg in timeline.get("segments", []):
            start_pct = (seg.get("start", 0) / total) * 100
            width_pct = ((seg.get("end", 0) - seg.get("start", 0)) / total) * 100
            color = colors.get(seg.get("type", "main"), "#3498db")
            segments_html += f"""
            <div class="segment" style="left:{start_pct}%;width:{width_pct}%;background:{color};"
                 title="{seg.get('title', '')}">
                <span>{seg.get('title', '')[:20]}</span>
            </div>"""

        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        .timeline {{ position:relative; height:60px; background:#ecf0f1; margin:20px 0; border-radius:5px; }}
        .segment {{ position:absolute; height:100%; display:flex; align-items:center; justify-content:center;
                   color:white; font-size:12px; overflow:hidden; cursor:pointer; border-radius:3px; }}
        .segment:hover {{ opacity:0.8; }}
        body {{ font-family:sans-serif; padding:20px; }}
        .legend {{ display:flex; gap:20px; margin:10px 0; }}
        .legend-item {{ display:flex; align-items:center; gap:5px; }}
        .legend-color {{ width:20px; height:20px; border-radius:3px; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <div class="legend">
        <div class="legend-item"><div class="legend-color" style="background:#3498db"></div>开场</div>
        <div class="legend-item"><div class="legend-color" style="background:#2ecc71"></div>主要内容</div>
        <div class="legend-item"><div class="legend-color" style="background:#f39c12"></div>示例</div>
        <div class="legend-item"><div class="legend-color" style="background:#9b59b6"></div>结论</div>
    </div>
    <div class="timeline">{segments_html}</div>
    <h2>段落详情</h2>
    <ul>
"""
        for seg in timeline.get("segments", []):
            html += f"""<li><strong>{self.format_timestamp(seg.get('start', 0))}</strong> - {seg.get('title', '')}: {seg.get('summary', '')}</li>"""

        html += """</ul></body></html>"""
        return html

    def merge_segments(self, timeline: Dict, segment_ids: List[str]) -> Dict[str, Any]:
        """Merge multiple segments into one"""
        segments = timeline.get("segments", [])
        to_merge = [s for s in segments if s.get("id") in segment_ids]
        others = [s for s in segments if s.get("id") not in segment_ids]

        if len(to_merge) < 2:
            return timeline

        merged = {
            "id": f"merged_{to_merge[0]['id']}",
            "start": min(s.get("start", 0) for s in to_merge),
            "end": max(s.get("end", 0) for s in to_merge),
            "title": " + ".join(s.get("title", "") for s in to_merge),
            "summary": " ".join(s.get("summary", "") for s in to_merge),
            "type": "main",
            "importance": max(s.get("importance", 5) for s in to_merge)
        }

        others.append(merged)
        others.sort(key=lambda x: x.get("start", 0))

        timeline["segments"] = others
        return timeline

    def split_segment(self, timeline: Dict, segment_id: str, split_point: int) -> Dict[str, Any]:
        """Split a segment at a specific point"""
        segments = timeline.get("segments", [])
        new_segments = []

        for seg in segments:
            if seg.get("id") == segment_id:
                if seg.get("start", 0) < split_point < seg.get("end", 0):
                    new_segments.append({
                        **seg,
                        "id": f"{seg['id']}_a",
                        "end": split_point
                    })
                    new_segments.append({
                        **seg,
                        "id": f"{seg['id']}_b",
                        "start": split_point,
                        "title": f"{seg.get('title', '')} (续)"
                    })
                else:
                    new_segments.append(seg)
            else:
                new_segments.append(seg)

        timeline["segments"] = new_segments
        return timeline
