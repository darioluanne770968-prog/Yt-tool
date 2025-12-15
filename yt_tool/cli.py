"""
Command Line Interface for YouTube AI Tool
"""

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.markdown import Markdown

console = Console()


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """YouTube AI Tool - AI-powered YouTube video analysis toolkit"""
    pass


@cli.command()
@click.argument("url")
@click.option("--timestamps/--no-timestamps", default=True, help="Include timestamps")
@click.option("--output", "-o", help="Output file path")
def transcript(url, timestamps, output):
    """Extract transcript/subtitles from a YouTube video"""
    from .extractor import TranscriptExtractor

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        progress.add_task("Extracting transcript...", total=None)

        try:
            extractor = TranscriptExtractor(url)
            extractor.extract()

            result = extractor.get_formatted(include_timestamps=timestamps)

            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(result)
                console.print(f"[green]Transcript saved to {output}[/green]")
            else:
                console.print(Panel(result, title="Transcript", border_style="blue"))

            console.print(f"\n[dim]Language: {extractor.language}[/dim]")

        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command()
@click.argument("url")
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--style", "-s", default="default",
              type=click.Choice(["default", "brief", "detailed", "bullets", "academic", "casual", "twitter"]),
              help="Summary style")
@click.option("--output", "-o", help="Output file path")
def summary(url, language, style, output):
    """Generate AI summary of a YouTube video"""
    from .extractor import TranscriptExtractor
    from .summarizer import Summarizer
    from .config import Config

    valid, msg = Config.validate()
    if not valid:
        console.print(f"[red]{msg}[/red]")
        raise SystemExit(1)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Extracting transcript...", total=None)

        try:
            extractor = TranscriptExtractor(url)
            extractor.extract()
            transcript_text = extractor.get_plain_text()

            progress.update(task, description=f"Generating {style} summary...")

            summarizer = Summarizer()
            result = summarizer.summarize(transcript_text, language, style)

            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(result)
                console.print(f"[green]Summary saved to {output}[/green]")
            else:
                console.print(Panel(Markdown(result), title=f"Video Summary ({style})", border_style="green"))

        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command()
@click.argument("url")
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def keypoints(url, language, output):
    """Extract key points from a YouTube video"""
    from .extractor import TranscriptExtractor
    from .summarizer import Summarizer
    from .config import Config

    valid, msg = Config.validate()
    if not valid:
        console.print(f"[red]{msg}[/red]")
        raise SystemExit(1)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Extracting transcript...", total=None)

        try:
            extractor = TranscriptExtractor(url)
            extractor.extract()
            transcript_text = extractor.get_plain_text()

            progress.update(task, description="Extracting key points...")

            summarizer = Summarizer()
            result = summarizer.extract_key_points(transcript_text, language)

            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(result)
                console.print(f"[green]Key points saved to {output}[/green]")
            else:
                console.print(Panel(Markdown(result), title="Key Points", border_style="yellow"))

        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command()
@click.argument("url")
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def chapters(url, language, output):
    """Generate chapter timestamps for a YouTube video"""
    from .extractor import TranscriptExtractor
    from .timestamp import TimestampGenerator
    from .config import Config

    valid, msg = Config.validate()
    if not valid:
        console.print(f"[red]{msg}[/red]")
        raise SystemExit(1)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Extracting transcript...", total=None)

        try:
            extractor = TranscriptExtractor(url)
            extractor.extract()
            transcript_formatted = extractor.get_formatted(include_timestamps=True)

            progress.update(task, description="Generating chapters...")

            generator = TimestampGenerator()
            chapters_list = generator.generate(transcript_formatted, language)

            result = generator.format_chapters(chapters_list)

            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(result)
                console.print(f"[green]Chapters saved to {output}[/green]")
            else:
                # Display as table
                table = Table(title="Video Chapters")
                table.add_column("Time", style="cyan")
                table.add_column("Chapter", style="white")

                for chapter in chapters_list:
                    table.add_row(chapter["time"], chapter["title"])

                console.print(table)

                # Also print copy-paste format
                console.print("\n[dim]Copy-paste format:[/dim]")
                console.print(result)

        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command()
@click.argument("url")
@click.option("--target", "-t", default="中文", help="Target language")
@click.option("--output", "-o", help="Output file path")
def translate(url, target, output):
    """Translate video subtitles to another language"""
    from .extractor import TranscriptExtractor
    from .translator import Translator
    from .config import Config

    valid, msg = Config.validate()
    if not valid:
        console.print(f"[red]{msg}[/red]")
        raise SystemExit(1)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Extracting transcript...", total=None)

        try:
            extractor = TranscriptExtractor(url)
            extractor.extract()
            transcript_formatted = extractor.get_formatted(include_timestamps=True)

            progress.update(task, description=f"Translating to {target}...")

            translator = Translator()
            result = translator.translate(transcript_formatted, target)

            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(result)
                console.print(f"[green]Translation saved to {output}[/green]")
            else:
                console.print(Panel(result, title=f"Translation ({target})", border_style="magenta"))

        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command()
@click.argument("url")
@click.option("--language", "-l", default="中文", help="Response language")
def qa(url, language):
    """Interactive Q&A about video content"""
    from .extractor import TranscriptExtractor
    from .qa import VideoQA
    from .config import Config

    valid, msg = Config.validate()
    if not valid:
        console.print(f"[red]{msg}[/red]")
        raise SystemExit(1)

    console.print("[dim]Loading video transcript...[/dim]")

    try:
        extractor = TranscriptExtractor(url)
        extractor.extract()
        transcript_text = extractor.get_plain_text()

        qa_system = VideoQA(transcript_text)

        # Suggest initial questions
        console.print("\n[green]Video loaded! Here are some suggested questions:[/green]\n")
        suggestions = qa_system.suggest_questions(language)
        for i, q in enumerate(suggestions, 1):
            console.print(f"  {i}. {q}")

        console.print("\n[dim]Type your question (or 'quit' to exit):[/dim]\n")

        while True:
            question = console.input("[bold cyan]You:[/bold cyan] ").strip()

            if question.lower() in ("quit", "exit", "q"):
                console.print("[dim]Goodbye![/dim]")
                break

            if not question:
                continue

            with console.status("Thinking..."):
                answer = qa_system.ask(question, language)

            console.print(f"\n[bold green]AI:[/bold green] {answer}\n")

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise SystemExit(1)


@cli.command()
@click.argument("url")
@click.argument("keyword")
@click.option("--format", "-f", "fmt", default="text", type=click.Choice(["text", "markdown", "json"]))
def search(url, keyword, fmt):
    """Search for keywords in video transcript"""
    from .extractor import TranscriptExtractor
    from .search import TranscriptSearch

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        progress.add_task("Searching...", total=None)

        try:
            extractor = TranscriptExtractor(url)
            extractor.extract()

            searcher = TranscriptSearch(extractor.get_segments(), extractor.video_id)
            matches = searcher.search(keyword)

            if not matches:
                console.print(f"[yellow]No matches found for '{keyword}'[/yellow]")
                return

            result = searcher.format_results(matches, fmt)

            if fmt == "markdown":
                console.print(Panel(Markdown(result), title=f"Search: {keyword}"))
            else:
                console.print(result)

        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command()
@click.argument("url")
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--format", "-f", "fmt", default="markdown",
              type=click.Choice(["markdown", "json", "notion", "obsidian"]))
@click.option("--output-dir", "-d", default="output", help="Output directory")
@click.option("--all", "all_features", is_flag=True, help="Run all analysis features")
def analyze(url, language, fmt, output_dir, all_features):
    """Run full analysis on a YouTube video"""
    from .extractor import TranscriptExtractor
    from .summarizer import Summarizer
    from .timestamp import TimestampGenerator
    from .exporter import Exporter
    from .config import Config

    valid, msg = Config.validate()
    if not valid:
        console.print(f"[red]{msg}[/red]")
        raise SystemExit(1)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Extracting transcript...", total=None)

        try:
            # Extract transcript
            extractor = TranscriptExtractor(url)
            extractor.extract()
            transcript_text = extractor.get_plain_text()
            transcript_formatted = extractor.get_formatted(include_timestamps=True)

            # Summary
            progress.update(task, description="Generating summary...")
            summarizer = Summarizer()
            summary = summarizer.summarize(transcript_text, language)

            # Key points
            progress.update(task, description="Extracting key points...")
            key_points = summarizer.extract_key_points(transcript_text, language)

            # Chapters
            progress.update(task, description="Generating chapters...")
            generator = TimestampGenerator()
            chapters_list = generator.generate(transcript_formatted, language)

            # Export
            progress.update(task, description="Exporting results...")
            exporter = Exporter(output_dir)

            if fmt == "json":
                filepath = exporter.export_json(
                    video_id=extractor.video_id,
                    transcript=transcript_formatted if all_features else None,
                    summary=summary,
                    key_points=key_points,
                    chapters=chapters_list,
                )
            elif fmt == "notion":
                filepath = exporter.export_notion(
                    video_id=extractor.video_id,
                    summary=summary,
                    key_points=key_points,
                    chapters=chapters_list,
                )
            elif fmt == "obsidian":
                filepath = exporter.export_obsidian(
                    video_id=extractor.video_id,
                    summary=summary,
                    key_points=key_points,
                    chapters=chapters_list,
                )
            else:  # markdown
                filepath = exporter.export_markdown(
                    video_id=extractor.video_id,
                    transcript=transcript_formatted if all_features else None,
                    summary=summary,
                    key_points=key_points,
                    chapters=chapters_list,
                )

            console.print(f"\n[green]Analysis complete! Saved to: {filepath}[/green]")

            # Display summary
            console.print(Panel(Markdown(summary), title="Summary Preview", border_style="green"))

        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command("batch")
@click.argument("urls", nargs=-1)
@click.option("--file", "-f", "file_path", help="File containing URLs (one per line)")
@click.option("--playlist", "-p", help="YouTube playlist URL")
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output-dir", "-d", default="output", help="Output directory")
def batch_process(urls, file_path, playlist, language, output_dir):
    """Process multiple videos in batch"""
    from .batch import BatchProcessor, get_playlist_videos, extract_playlist_id
    from .config import Config

    valid, msg = Config.validate()
    if not valid:
        console.print(f"[red]{msg}[/red]")
        raise SystemExit(1)

    video_urls = list(urls)

    # Load URLs from file
    if file_path:
        try:
            with open(file_path, "r") as f:
                video_urls.extend(line.strip() for line in f if line.strip())
        except Exception as e:
            console.print(f"[red]Error reading file: {e}[/red]")
            raise SystemExit(1)

    # Load from playlist
    if playlist:
        console.print("[dim]Loading playlist...[/dim]")
        try:
            playlist_id = extract_playlist_id(playlist)
            if playlist_id:
                video_urls.extend(get_playlist_videos(playlist_id))
        except Exception as e:
            console.print(f"[red]Error loading playlist: {e}[/red]")
            raise SystemExit(1)

    if not video_urls:
        console.print("[red]No videos to process[/red]")
        raise SystemExit(1)

    console.print(f"[green]Processing {len(video_urls)} videos...[/green]\n")

    processor = BatchProcessor(output_dir=output_dir)

    def progress_callback(video_id, current, total):
        console.print(f"[{current}/{total}] Processing {video_id}...")

    results = processor.process_videos(
        video_urls,
        operations=["summary", "chapters", "transcript"],
        language=language,
        progress_callback=progress_callback,
    )

    # Summary
    success = sum(1 for r in results if r.get("success"))
    failed = len(results) - success

    console.print(f"\n[green]Completed: {success} successful, {failed} failed[/green]")

    if failed > 0:
        console.print("\n[red]Failed videos:[/red]")
        for r in results:
            if not r.get("success"):
                console.print(f"  - {r.get('url', r.get('video_id'))}: {r.get('error')}")


@cli.command()
@click.argument("url")
@click.option("--output", "-o", help="Output file path")
def info(url, output):
    """Get video information and metadata"""
    from .video_info import VideoInfo

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        progress.add_task("Fetching video info...", total=None)

        try:
            video = VideoInfo(url)
            video.fetch()

            if output:
                content = video.format_markdown()
                with open(output, "w", encoding="utf-8") as f:
                    f.write(content)
                console.print(f"[green]Video info saved to {output}[/green]")
            else:
                # Display as table
                info = video.info
                table = Table(title=info["title"], show_header=False)
                table.add_column("Field", style="cyan")
                table.add_column("Value", style="white")

                table.add_row("Channel", info["channel"])
                table.add_row("Duration", info["duration_formatted"])
                table.add_row("Views", f"{info['view_count']:,}")
                table.add_row("Likes", f"{info.get('like_count', 0):,}")
                table.add_row("Upload Date", info["upload_date"])
                table.add_row("URL", info["url"])

                if info.get("tags"):
                    table.add_row("Tags", ", ".join(info["tags"][:5]))

                console.print(table)

        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command()
@click.argument("url")
@click.option("--format", "-f", "fmt", default="srt", type=click.Choice(["srt", "vtt", "txt"]))
@click.option("--output-dir", "-d", default="output", help="Output directory")
def subtitle(url, fmt, output_dir):
    """Download subtitles in SRT/VTT/TXT format"""
    from .extractor import TranscriptExtractor
    from .subtitle import SubtitleExporter

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        progress.add_task("Extracting subtitles...", total=None)

        try:
            extractor = TranscriptExtractor(url)
            extractor.extract()

            exporter = SubtitleExporter(
                extractor.get_segments(),
                extractor.video_id,
            )

            filepath = exporter.save(output_dir, fmt)
            console.print(f"[green]Subtitle saved to: {filepath}[/green]")

        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command()
@click.argument("url")
@click.option("--format", "-f", "fmt", default="mp3", type=click.Choice(["mp3", "m4a", "wav"]))
@click.option("--quality", "-q", default="192", type=click.Choice(["128", "192", "256", "320"]))
@click.option("--output-dir", "-d", default="output", help="Output directory")
def audio(url, fmt, quality, output_dir):
    """Download audio from a YouTube video"""
    from .downloader import Downloader
    from .extractor import extract_video_id

    video_id = extract_video_id(url)
    if not video_id:
        console.print("[red]Invalid YouTube URL[/red]")
        raise SystemExit(1)

    console.print(f"[dim]Downloading audio as {fmt} ({quality}kbps)...[/dim]")

    try:
        downloader = Downloader(output_dir)
        filepath = downloader.download_audio(video_id, fmt, quality)
        console.print(f"[green]Audio saved to: {filepath}[/green]")

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise SystemExit(1)


@cli.command()
@click.argument("url")
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--format", "-f", "fmt", default="markdown",
              type=click.Choice(["markdown", "mermaid", "json"]))
@click.option("--output", "-o", help="Output file path")
def mindmap(url, language, fmt, output):
    """Generate mind map from video content"""
    from .extractor import TranscriptExtractor
    from .mindmap import MindmapGenerator
    from .config import Config

    valid, msg = Config.validate()
    if not valid:
        console.print(f"[red]{msg}[/red]")
        raise SystemExit(1)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Extracting transcript...", total=None)

        try:
            extractor = TranscriptExtractor(url)
            extractor.extract()
            transcript_text = extractor.get_plain_text()

            progress.update(task, description="Generating mind map...")

            generator = MindmapGenerator()
            mindmap_data = generator.generate(transcript_text, language)

            if fmt == "mermaid":
                result = generator.to_mermaid(mindmap_data)
            elif fmt == "json":
                result = generator.to_json(mindmap_data)
            else:
                result = generator.to_markdown(mindmap_data)

            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(result)
                console.print(f"[green]Mind map saved to {output}[/green]")
            else:
                console.print(Panel(Markdown(result), title="Mind Map", border_style="cyan"))

        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command("styles")
def list_styles():
    """List available summary styles"""
    from .summarizer import Summarizer

    styles = Summarizer.get_available_styles()

    table = Table(title="Available Summary Styles")
    table.add_column("Style", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Description", style="white")

    for key, info in styles.items():
        table.add_row(key, info["name"], info["description"])

    console.print(table)
    console.print("\n[dim]Use: yt-tool summary URL --style STYLE[/dim]")


@cli.command()
@click.argument("url")
@click.option("--max-comments", "-n", default=50, help="Maximum comments to analyze")
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def comments(url, max_comments, language, output):
    """Analyze video comments"""
    from .comments import CommentsAnalyzer
    from .config import Config

    valid, msg = Config.validate()
    if not valid:
        console.print(f"[red]{msg}[/red]")
        raise SystemExit(1)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Fetching comments...", total=None)

        try:
            from .extractor import extract_video_id
            video_id = extract_video_id(url)

            analyzer = CommentsAnalyzer()

            progress.update(task, description="Analyzing comments...")
            result = analyzer.analyze_video(video_id, max_comments, language)

            if result["comments_count"] == 0:
                console.print("[yellow]No comments found for this video[/yellow]")
                return

            # Show statistics
            sentiment = analyzer.get_sentiment_summary(result["comments"])
            table = Table(title=f"Comments Analysis ({result['comments_count']} comments)")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="white")
            table.add_row("Positive", f"{sentiment['positive']} ({sentiment['positive_ratio']}%)")
            table.add_row("Negative", f"{sentiment['negative']} ({sentiment['negative_ratio']}%)")
            table.add_row("Neutral", str(sentiment['neutral']))
            console.print(table)

            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(result["analysis"])
                console.print(f"\n[green]Analysis saved to {output}[/green]")
            else:
                console.print(Panel(Markdown(result["analysis"]), title="AI Analysis", border_style="magenta"))

        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command("cache")
@click.option("--clear", is_flag=True, help="Clear all cache")
@click.option("--clear-expired", is_flag=True, help="Clear only expired cache")
@click.option("--stats", is_flag=True, help="Show cache statistics")
def cache_cmd(clear, clear_expired, stats):
    """Manage cache"""
    from .cache import get_transcript_cache, get_analysis_cache

    transcript_cache = get_transcript_cache()
    analysis_cache = get_analysis_cache()

    if clear:
        t_count = transcript_cache.clear()
        a_count = analysis_cache.clear()
        console.print(f"[green]Cleared {t_count + a_count} cache files[/green]")

    elif clear_expired:
        t_count = transcript_cache.clear_expired()
        a_count = analysis_cache.clear_expired()
        console.print(f"[green]Cleared {t_count + a_count} expired cache files[/green]")

    elif stats:
        t_stats = transcript_cache.get_stats()
        a_stats = analysis_cache.get_stats()

        table = Table(title="Cache Statistics")
        table.add_column("Cache", style="cyan")
        table.add_column("Files", style="white")
        table.add_column("Size", style="green")
        table.add_column("Location", style="dim")

        table.add_row(
            "Transcripts",
            f"{t_stats['valid_files']} ({t_stats['expired_files']} expired)",
            f"{t_stats['total_size_mb']} MB",
            t_stats['cache_dir'],
        )
        table.add_row(
            "Analysis",
            f"{a_stats['valid_files']} ({a_stats['expired_files']} expired)",
            f"{a_stats['total_size_mb']} MB",
            a_stats['cache_dir'],
        )

        console.print(table)

    else:
        console.print("[dim]Use --stats, --clear, or --clear-expired[/dim]")


def main():
    """Main entry point"""
    cli()


if __name__ == "__main__":
    main()
