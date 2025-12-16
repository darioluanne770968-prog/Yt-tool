"""
Complete video analysis report generation
"""

import os
from datetime import datetime
from typing import Optional

from .extractor import TranscriptExtractor
from .video_info import VideoInfo
from .summarizer import Summarizer
from .timestamp import TimestampGenerator
from .mindmap import MindmapGenerator
from .generator import ContentGenerator
from .exporter import Exporter


class ReportGenerator:
    """Generate comprehensive video analysis reports"""

    def __init__(self, provider: str = None, output_dir: str = "output"):
        """
        Initialize report generator

        Args:
            provider: AI provider
            output_dir: Output directory
        """
        self.provider = provider
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_full_report(
        self,
        url_or_id: str,
        language: str = "中文",
        include_transcript: bool = True,
        include_flashcards: bool = True,
        include_mindmap: bool = True,
        include_vocabulary: bool = True,
        progress_callback=None,
    ) -> dict:
        """
        Generate a comprehensive analysis report

        Args:
            url_or_id: YouTube URL or video ID
            language: Output language
            include_transcript: Include full transcript
            include_flashcards: Generate flashcards
            include_mindmap: Generate mind map
            include_vocabulary: Extract vocabulary
            progress_callback: Progress callback function(step, total, description)

        Returns:
            Dictionary with all generated content and file paths
        """
        result = {
            "success": True,
            "video_id": None,
            "files": [],
        }

        total_steps = 7 + sum([include_flashcards, include_mindmap, include_vocabulary])
        current_step = 0

        def update_progress(description):
            nonlocal current_step
            current_step += 1
            if progress_callback:
                progress_callback(current_step, total_steps, description)

        try:
            # Step 1: Get video info
            update_progress("Fetching video info...")
            video_info = VideoInfo(url_or_id)
            video_info.fetch()
            result["video_id"] = video_info.video_id
            result["video_info"] = video_info.info

            # Step 2: Extract transcript
            update_progress("Extracting transcript...")
            extractor = TranscriptExtractor(url_or_id)
            extractor.extract()
            transcript_text = extractor.get_plain_text()
            transcript_formatted = extractor.get_formatted(include_timestamps=True)
            result["transcript"] = transcript_formatted
            result["transcript_language"] = extractor.language

            # Step 3: Generate summary
            update_progress("Generating summary...")
            summarizer = Summarizer(self.provider)
            result["summary"] = summarizer.summarize(transcript_text, language)

            # Step 4: Extract key points
            update_progress("Extracting key points...")
            result["key_points"] = summarizer.extract_key_points(transcript_text, language)

            # Step 5: Generate chapters
            update_progress("Generating chapters...")
            timestamp_gen = TimestampGenerator(self.provider)
            result["chapters"] = timestamp_gen.generate(transcript_formatted, language)

            # Step 6: Generate mind map (optional)
            if include_mindmap:
                update_progress("Generating mind map...")
                mindmap_gen = MindmapGenerator(self.provider)
                mindmap_data = mindmap_gen.generate(transcript_text, language)
                result["mindmap"] = mindmap_gen.to_markdown(mindmap_data)
                result["mindmap_mermaid"] = mindmap_gen.to_mermaid(mindmap_data)

            # Step 7: Generate flashcards (optional)
            if include_flashcards:
                update_progress("Generating flashcards...")
                content_gen = ContentGenerator(self.provider)
                result["flashcards"] = content_gen.generate_flashcards(transcript_text, language)

            # Step 8: Extract vocabulary (optional)
            if include_vocabulary:
                update_progress("Extracting vocabulary...")
                content_gen = ContentGenerator(self.provider)
                result["vocabulary"] = content_gen.extract_vocabulary(transcript_text, language)

            # Step 9: Generate report file
            update_progress("Generating report file...")
            report_path = self._create_report_file(result, language, include_transcript)
            result["files"].append(report_path)
            result["report_path"] = report_path

            # Export individual files
            update_progress("Exporting files...")
            exporter = Exporter(self.output_dir)

            # Export JSON
            json_path = exporter.export_json(
                video_id=result["video_id"],
                title=result["video_info"].get("title"),
                transcript=transcript_formatted if include_transcript else None,
                summary=result["summary"],
                key_points=result["key_points"],
                chapters=result["chapters"],
            )
            result["files"].append(json_path)

            # Export flashcards to Anki format if generated
            if include_flashcards and result.get("flashcards"):
                content_gen = ContentGenerator(self.provider)
                anki_content = content_gen.export_flashcards_anki(result["flashcards"])
                anki_path = os.path.join(
                    self.output_dir,
                    f"{result['video_id']}_flashcards.txt"
                )
                with open(anki_path, "w", encoding="utf-8") as f:
                    f.write(anki_content)
                result["files"].append(anki_path)

        except Exception as e:
            result["success"] = False
            result["error"] = str(e)

        return result

    def _create_report_file(
        self,
        data: dict,
        language: str,
        include_transcript: bool,
    ) -> str:
        """Create the main report file"""
        lines = []
        video_info = data.get("video_info", {})
        video_id = data.get("video_id", "unknown")

        # Header
        lines.append(f"# {video_info.get('title', 'Video Analysis Report')}")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Video info
        lines.append("## 视频信息")
        lines.append("")
        lines.append(f"- **标题**: {video_info.get('title', 'N/A')}")
        lines.append(f"- **频道**: {video_info.get('channel', 'N/A')}")
        lines.append(f"- **时长**: {video_info.get('duration_formatted', 'N/A')}")
        lines.append(f"- **观看数**: {video_info.get('view_count', 0):,}")
        lines.append(f"- **上传日期**: {video_info.get('upload_date', 'N/A')}")
        lines.append(f"- **链接**: https://youtube.com/watch?v={video_id}")
        lines.append(f"- **报告生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")

        # Table of contents
        lines.append("## 目录")
        lines.append("")
        lines.append("1. [视频摘要](#视频摘要)")
        lines.append("2. [关键要点](#关键要点)")
        lines.append("3. [章节时间戳](#章节时间戳)")
        if data.get("mindmap"):
            lines.append("4. [思维导图](#思维导图)")
        if data.get("vocabulary"):
            lines.append("5. [词汇术语](#词汇术语)")
        if data.get("flashcards"):
            lines.append("6. [学习卡片](#学习卡片)")
        if include_transcript:
            lines.append("7. [完整字幕](#完整字幕)")
        lines.append("")

        # Summary
        lines.append("---")
        lines.append("")
        lines.append("## 视频摘要")
        lines.append("")
        lines.append(data.get("summary", ""))
        lines.append("")

        # Key points
        lines.append("---")
        lines.append("")
        lines.append("## 关键要点")
        lines.append("")
        lines.append(data.get("key_points", ""))
        lines.append("")

        # Chapters
        lines.append("---")
        lines.append("")
        lines.append("## 章节时间戳")
        lines.append("")
        chapters = data.get("chapters", [])
        for chapter in chapters:
            time_str = chapter.get("time", "00:00")
            title = chapter.get("title", "")
            # Convert time to seconds for link
            parts = time_str.split(":")
            if len(parts) == 2:
                seconds = int(parts[0]) * 60 + int(parts[1])
            elif len(parts) == 3:
                seconds = int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
            else:
                seconds = 0
            lines.append(f"- [{time_str}](https://youtube.com/watch?v={video_id}&t={seconds}) {title}")
        lines.append("")

        # Mind map
        if data.get("mindmap"):
            lines.append("---")
            lines.append("")
            lines.append("## 思维导图")
            lines.append("")
            lines.append(data["mindmap"])
            lines.append("")
            if data.get("mindmap_mermaid"):
                lines.append("### Mermaid 格式")
                lines.append("")
                lines.append(data["mindmap_mermaid"])
                lines.append("")

        # Vocabulary
        if data.get("vocabulary"):
            lines.append("---")
            lines.append("")
            lines.append("## 词汇术语")
            lines.append("")
            lines.append(data["vocabulary"])
            lines.append("")

        # Flashcards
        if data.get("flashcards"):
            lines.append("---")
            lines.append("")
            lines.append("## 学习卡片")
            lines.append("")
            for i, card in enumerate(data["flashcards"], 1):
                lines.append(f"### 卡片 {i}")
                lines.append("")
                lines.append(f"**问题**: {card['question']}")
                lines.append("")
                lines.append("<details>")
                lines.append("<summary>点击查看答案</summary>")
                lines.append("")
                lines.append(f"{card['answer']}")
                lines.append("")
                lines.append("</details>")
                lines.append("")

        # Transcript
        if include_transcript and data.get("transcript"):
            lines.append("---")
            lines.append("")
            lines.append("## 完整字幕")
            lines.append("")
            lines.append(f"*语言: {data.get('transcript_language', 'unknown')}*")
            lines.append("")
            lines.append("```")
            lines.append(data["transcript"])
            lines.append("```")
            lines.append("")

        # Footer
        lines.append("---")
        lines.append("")
        lines.append("*由 YouTube AI Tool 生成*")

        # Write file
        content = "\n".join(lines)
        filename = f"{video_id}_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        return filepath
