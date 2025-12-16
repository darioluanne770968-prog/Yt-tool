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


@cli.command()
@click.argument("url")
@click.option("--quality", "-q", default="720", type=click.Choice(["360", "480", "720", "1080", "best"]))
@click.option("--output-dir", "-d", default="output", help="Output directory")
def video(url, quality, output_dir):
    """Download video from YouTube"""
    from .downloader import Downloader
    from .extractor import extract_video_id

    video_id = extract_video_id(url)
    if not video_id:
        console.print("[red]Invalid YouTube URL[/red]")
        raise SystemExit(1)

    console.print(f"[dim]Downloading video ({quality}p)...[/dim]")

    try:
        downloader = Downloader(output_dir)
        filepath = downloader.download_video(video_id, quality)
        console.print(f"[green]Video saved to: {filepath}[/green]")

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise SystemExit(1)


@cli.command()
@click.argument("url")
@click.option("--output-dir", "-d", default="output", help="Output directory")
def thumbnail(url, output_dir):
    """Download video thumbnail"""
    from .downloader import Downloader
    from .extractor import extract_video_id

    video_id = extract_video_id(url)
    if not video_id:
        console.print("[red]Invalid YouTube URL[/red]")
        raise SystemExit(1)

    try:
        downloader = Downloader(output_dir)
        filepath = downloader.download_thumbnail(video_id)
        console.print(f"[green]Thumbnail saved to: {filepath}[/green]")

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise SystemExit(1)


@cli.command()
@click.argument("url")
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--format", "-f", "fmt", default="markdown", type=click.Choice(["markdown", "anki"]))
@click.option("--output", "-o", help="Output file path")
def flashcards(url, language, fmt, output):
    """Generate flashcards from video content"""
    from .extractor import TranscriptExtractor
    from .generator import ContentGenerator
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

            progress.update(task, description="Generating flashcards...")

            generator = ContentGenerator()
            cards = generator.generate_flashcards(transcript_text, language)

            if fmt == "anki":
                result = generator.export_flashcards_anki(cards)
            else:
                result = generator.export_flashcards_markdown(cards)

            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(result)
                console.print(f"[green]Flashcards saved to {output}[/green]")
            else:
                console.print(Panel(Markdown(result), title=f"Flashcards ({len(cards)} cards)", border_style="yellow"))

            console.print(f"\n[dim]Generated {len(cards)} flashcards[/dim]")

        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command()
@click.argument("url")
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def blog(url, language, output):
    """Generate blog post from video content"""
    from .extractor import TranscriptExtractor
    from .generator import ContentGenerator
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

            progress.update(task, description="Generating blog post...")

            generator = ContentGenerator()
            result = generator.generate_blog_post(transcript_text, language)

            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(result)
                console.print(f"[green]Blog post saved to {output}[/green]")
            else:
                console.print(Panel(Markdown(result), title="Blog Post", border_style="blue"))

        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command()
@click.argument("url")
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def vocabulary(url, language, output):
    """Extract vocabulary and terminology from video"""
    from .extractor import TranscriptExtractor
    from .generator import ContentGenerator
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

            progress.update(task, description="Extracting vocabulary...")

            generator = ContentGenerator()
            result = generator.extract_vocabulary(transcript_text, language)

            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(result)
                console.print(f"[green]Vocabulary saved to {output}[/green]")
            else:
                console.print(Panel(Markdown(result), title="Vocabulary & Terminology", border_style="green"))

        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command()
@click.argument("url")
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def podcast(url, language, output):
    """Generate podcast script from video content"""
    from .extractor import TranscriptExtractor
    from .generator import ContentGenerator
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

            progress.update(task, description="Generating podcast script...")

            generator = ContentGenerator()
            result = generator.generate_podcast_script(transcript_text, language)

            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(result)
                console.print(f"[green]Podcast script saved to {output}[/green]")
            else:
                console.print(Panel(result, title="Podcast Script", border_style="magenta"))

        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command()
@click.argument("url")
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output-dir", "-d", default="output", help="Output directory")
@click.option("--no-transcript", is_flag=True, help="Exclude transcript from report")
@click.option("--no-flashcards", is_flag=True, help="Exclude flashcards")
@click.option("--no-mindmap", is_flag=True, help="Exclude mind map")
@click.option("--no-vocabulary", is_flag=True, help="Exclude vocabulary")
def report(url, language, output_dir, no_transcript, no_flashcards, no_mindmap, no_vocabulary):
    """Generate comprehensive analysis report"""
    from .report import ReportGenerator
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
        task = progress.add_task("Starting...", total=None)

        def progress_callback(step, total, description):
            progress.update(task, description=f"[{step}/{total}] {description}")

        try:
            generator = ReportGenerator(output_dir=output_dir)
            result = generator.generate_full_report(
                url,
                language=language,
                include_transcript=not no_transcript,
                include_flashcards=not no_flashcards,
                include_mindmap=not no_mindmap,
                include_vocabulary=not no_vocabulary,
                progress_callback=progress_callback,
            )

            if result["success"]:
                console.print(f"\n[green]Report generated successfully![/green]")
                console.print(f"\n[bold]Generated files:[/bold]")
                for f in result["files"]:
                    console.print(f"  - {f}")

                # Show summary preview
                if result.get("summary"):
                    preview = result["summary"][:500] + "..." if len(result["summary"]) > 500 else result["summary"]
                    console.print(Panel(Markdown(preview), title="Summary Preview", border_style="green"))
            else:
                console.print(f"[red]Error: {result.get('error')}[/red]")
                raise SystemExit(1)

        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


# ============================================
# New Feature Commands
# ============================================

@cli.command()
@click.argument("url")
@click.option("--num", "-n", default=10, help="Number of questions")
@click.option("--difficulty", "-d", default="medium", type=click.Choice(["easy", "medium", "hard"]))
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def quiz(url, num, difficulty, language, output):
    """Generate quiz from video content"""
    from .extractor import TranscriptExtractor
    from .quiz import QuizGenerator
    from .config import Config

    valid, msg = Config.validate()
    if not valid:
        console.print(f"[red]{msg}[/red]")
        raise SystemExit(1)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
        task = progress.add_task("Extracting transcript...", total=None)
        try:
            extractor = TranscriptExtractor(url)
            extractor.extract()
            transcript = extractor.get_plain_text()
            progress.update(task, description="Generating quiz...")
            generator = QuizGenerator()
            result = generator.generate_quiz(transcript, num, difficulty=difficulty, language=language)
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(result["quiz"])
                console.print(f"[green]Quiz saved to {output}[/green]")
            else:
                console.print(Panel(Markdown(result["quiz"]), title=f"Quiz ({num} questions)", border_style="yellow"))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command("study-guide")
@click.argument("url")
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def study_guide(url, language, output):
    """Generate study guide from video"""
    from .extractor import TranscriptExtractor
    from .study_guide import StudyGuideGenerator
    from .config import Config

    valid, msg = Config.validate()
    if not valid:
        console.print(f"[red]{msg}[/red]")
        raise SystemExit(1)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
        task = progress.add_task("Extracting transcript...", total=None)
        try:
            extractor = TranscriptExtractor(url)
            extractor.extract()
            transcript = extractor.get_plain_text()
            progress.update(task, description="Generating study guide...")
            generator = StudyGuideGenerator()
            result = generator.generate_study_guide(transcript, language=language)
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(result)
                console.print(f"[green]Study guide saved to {output}[/green]")
            else:
                console.print(Panel(Markdown(result), title="Study Guide", border_style="green"))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command("extract-code")
@click.argument("url")
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output-dir", "-d", default="output", help="Output directory")
def extract_code(url, language, output_dir):
    """Extract code snippets from programming tutorial"""
    from .extractor import TranscriptExtractor
    from .code_extractor import CodeExtractor
    from .config import Config

    valid, msg = Config.validate()
    if not valid:
        console.print(f"[red]{msg}[/red]")
        raise SystemExit(1)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
        task = progress.add_task("Extracting transcript...", total=None)
        try:
            extractor = TranscriptExtractor(url)
            extractor.extract()
            transcript = extractor.get_plain_text()
            progress.update(task, description="Extracting code...")
            code_extractor = CodeExtractor()
            result = code_extractor.extract_code(transcript, output_language=language)
            console.print(Panel(Markdown(result["full_response"]), title="Extracted Code", border_style="cyan"))
            console.print(f"\n[dim]Found {len(result['code_blocks'])} code blocks[/dim]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command()
@click.argument("url")
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def references(url, language, output):
    """Extract references and citations from video"""
    from .extractor import TranscriptExtractor
    from .references import ReferenceExtractor
    from .config import Config

    valid, msg = Config.validate()
    if not valid:
        console.print(f"[red]{msg}[/red]")
        raise SystemExit(1)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
        task = progress.add_task("Extracting transcript...", total=None)
        try:
            extractor = TranscriptExtractor(url)
            extractor.extract()
            transcript = extractor.get_plain_text()
            progress.update(task, description="Extracting references...")
            ref_extractor = ReferenceExtractor()
            result = ref_extractor.extract_references(transcript, language)
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(result["references"])
                console.print(f"[green]References saved to {output}[/green]")
            else:
                console.print(Panel(Markdown(result["references"]), title="References", border_style="blue"))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command()
@click.argument("url")
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def concepts(url, language, output):
    """Extract and explain key concepts"""
    from .extractor import TranscriptExtractor
    from .concepts import ConceptExplainer
    from .config import Config

    valid, msg = Config.validate()
    if not valid:
        console.print(f"[red]{msg}[/red]")
        raise SystemExit(1)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
        task = progress.add_task("Extracting transcript...", total=None)
        try:
            extractor = TranscriptExtractor(url)
            extractor.extract()
            transcript = extractor.get_plain_text()
            progress.update(task, description="Extracting concepts...")
            explainer = ConceptExplainer()
            result = explainer.extract_concepts(transcript, language)
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(result)
                console.print(f"[green]Concepts saved to {output}[/green]")
            else:
                console.print(Panel(Markdown(result), title="Key Concepts", border_style="magenta"))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command()
@click.argument("urls", nargs=-1, required=True)
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def compare(urls, language, output):
    """Compare multiple videos"""
    from .compare import VideoComparator
    from .config import Config

    valid, msg = Config.validate()
    if not valid:
        console.print(f"[red]{msg}[/red]")
        raise SystemExit(1)

    console.print(f"[dim]Comparing {len(urls)} videos...[/dim]")
    try:
        comparator = VideoComparator()
        result = comparator.compare_by_urls(list(urls), language)
        if output:
            with open(output, "w", encoding="utf-8") as f:
                f.write(result)
            console.print(f"[green]Comparison saved to {output}[/green]")
        else:
            console.print(Panel(Markdown(result), title="Video Comparison", border_style="cyan"))
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise SystemExit(1)


@cli.command("channel")
@click.argument("channel_url")
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def analyze_channel(channel_url, language, output):
    """Analyze YouTube channel"""
    from .channel import ChannelAnalyzer
    from .config import Config

    valid, msg = Config.validate()
    if not valid:
        console.print(f"[red]{msg}[/red]")
        raise SystemExit(1)

    console.print("[dim]Analyzing channel...[/dim]")
    try:
        analyzer = ChannelAnalyzer()
        result = analyzer.analyze_channel(channel_url, language)
        if output:
            with open(output, "w", encoding="utf-8") as f:
                f.write(result)
            console.print(f"[green]Analysis saved to {output}[/green]")
        else:
            console.print(Panel(Markdown(result), title="Channel Analysis", border_style="blue"))
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise SystemExit(1)


@cli.command()
@click.argument("url")
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def sentiment(url, language, output):
    """Analyze video sentiment and tone"""
    from .extractor import TranscriptExtractor
    from .sentiment import SentimentAnalyzer
    from .config import Config

    valid, msg = Config.validate()
    if not valid:
        console.print(f"[red]{msg}[/red]")
        raise SystemExit(1)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
        task = progress.add_task("Extracting transcript...", total=None)
        try:
            extractor = TranscriptExtractor(url)
            extractor.extract()
            transcript = extractor.get_plain_text()
            progress.update(task, description="Analyzing sentiment...")
            analyzer = SentimentAnalyzer()
            result = analyzer.analyze_sentiment(transcript, language)
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(result["analysis"])
                console.print(f"[green]Analysis saved to {output}[/green]")
            else:
                console.print(Panel(Markdown(result["analysis"]), title="Sentiment Analysis", border_style="yellow"))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command()
@click.argument("url")
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def factcheck(url, language, output):
    """Fact-check video claims"""
    from .extractor import TranscriptExtractor
    from .factcheck import FactChecker
    from .config import Config

    valid, msg = Config.validate()
    if not valid:
        console.print(f"[red]{msg}[/red]")
        raise SystemExit(1)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
        task = progress.add_task("Extracting transcript...", total=None)
        try:
            extractor = TranscriptExtractor(url)
            extractor.extract()
            transcript = extractor.get_plain_text()
            progress.update(task, description="Fact-checking...")
            checker = FactChecker()
            result = checker.check_facts(transcript, language)
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(result["report"])
                console.print(f"[green]Report saved to {output}[/green]")
            else:
                console.print(Panel(Markdown(result["report"]), title="Fact Check Report", border_style="red"))
                console.print(f"\n[dim]{result['disclaimer']}[/dim]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command("learning-path")
@click.argument("playlist_url")
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--level", default="beginner", type=click.Choice(["beginner", "intermediate", "advanced"]))
@click.option("--output", "-o", help="Output file path")
def learning_path(playlist_url, language, level, output):
    """Generate learning path from playlist"""
    from .learning_path import LearningPathGenerator
    from .config import Config

    valid, msg = Config.validate()
    if not valid:
        console.print(f"[red]{msg}[/red]")
        raise SystemExit(1)

    console.print("[dim]Analyzing playlist...[/dim]")
    try:
        generator = LearningPathGenerator()
        result = generator.generate_learning_path(playlist_url, language, level)
        if output:
            with open(output, "w", encoding="utf-8") as f:
                f.write(result)
            console.print(f"[green]Learning path saved to {output}[/green]")
        else:
            console.print(Panel(Markdown(result), title="Learning Path", border_style="green"))
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise SystemExit(1)


@cli.command()
@click.argument("url")
@click.option("--slides", "-n", default=10, help="Number of slides")
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--format", "-f", "fmt", default="markdown", type=click.Choice(["markdown", "marp", "reveal"]))
@click.option("--output", "-o", help="Output file path")
def presentation(url, slides, language, fmt, output):
    """Generate presentation slides from video"""
    from .extractor import TranscriptExtractor
    from .presentation import PresentationGenerator
    from .config import Config

    valid, msg = Config.validate()
    if not valid:
        console.print(f"[red]{msg}[/red]")
        raise SystemExit(1)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
        task = progress.add_task("Extracting transcript...", total=None)
        try:
            extractor = TranscriptExtractor(url)
            extractor.extract()
            transcript = extractor.get_plain_text()
            progress.update(task, description="Generating presentation...")
            generator = PresentationGenerator()
            if fmt == "marp":
                result = generator.generate_marp_slides(transcript, language=language)
            elif fmt == "reveal":
                result = generator.generate_reveal_js(transcript, language=language)
            else:
                result = generator.generate_slides(transcript, num_slides=slides, language=language)
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(result)
                console.print(f"[green]Presentation saved to {output}[/green]")
            else:
                console.print(Panel(Markdown(result), title=f"Presentation ({slides} slides)", border_style="cyan"))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command()
@click.argument("url")
@click.option("--platform", "-p", default="all", type=click.Choice(["all", "twitter", "linkedin", "xiaohongshu", "douyin"]))
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def social(url, platform, language, output):
    """Generate social media content"""
    from .extractor import TranscriptExtractor
    from .social import SocialMediaGenerator
    from .config import Config

    valid, msg = Config.validate()
    if not valid:
        console.print(f"[red]{msg}[/red]")
        raise SystemExit(1)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
        task = progress.add_task("Extracting transcript...", total=None)
        try:
            extractor = TranscriptExtractor(url)
            extractor.extract()
            transcript = extractor.get_plain_text()
            progress.update(task, description="Generating content...")
            generator = SocialMediaGenerator()
            if platform == "twitter":
                result = generator.generate_twitter(transcript, language)
            elif platform == "linkedin":
                result = generator.generate_linkedin(transcript, language)
            elif platform == "xiaohongshu":
                result = generator.generate_xiaohongshu(transcript, language)
            elif platform == "douyin":
                result = generator.generate_douyin(transcript, language)
            else:
                result = generator.generate_all(transcript, language=language)["all_platforms"]
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(result)
                console.print(f"[green]Content saved to {output}[/green]")
            else:
                console.print(Panel(Markdown(result), title=f"Social Media ({platform})", border_style="magenta"))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command()
@click.argument("url")
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def newsletter(url, language, output):
    """Generate email newsletter from video"""
    from .extractor import TranscriptExtractor
    from .newsletter import NewsletterGenerator
    from .config import Config

    valid, msg = Config.validate()
    if not valid:
        console.print(f"[red]{msg}[/red]")
        raise SystemExit(1)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
        task = progress.add_task("Extracting transcript...", total=None)
        try:
            extractor = TranscriptExtractor(url)
            extractor.extract()
            transcript = extractor.get_plain_text()
            progress.update(task, description="Generating newsletter...")
            generator = NewsletterGenerator()
            result = generator.generate_newsletter(transcript, language=language)
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(result)
                console.print(f"[green]Newsletter saved to {output}[/green]")
            else:
                console.print(Panel(Markdown(result), title="Newsletter", border_style="blue"))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command()
@click.argument("url")
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def seo(url, language, output):
    """Analyze and optimize video SEO"""
    from .video_info import VideoInfo
    from .extractor import TranscriptExtractor
    from .seo import SEOAnalyzer
    from .config import Config

    valid, msg = Config.validate()
    if not valid:
        console.print(f"[red]{msg}[/red]")
        raise SystemExit(1)

    console.print("[dim]Analyzing SEO...[/dim]")
    try:
        video = VideoInfo(url)
        video.fetch()
        extractor = TranscriptExtractor(url)
        extractor.extract()
        transcript = extractor.get_plain_text()
        analyzer = SEOAnalyzer()
        result = analyzer.analyze_seo(
            video.title, video.description or "", video.tags or [], transcript, language
        )
        if output:
            with open(output, "w", encoding="utf-8") as f:
                f.write(result["report"])
            console.print(f"[green]SEO analysis saved to {output}[/green]")
        else:
            console.print(Panel(Markdown(result["report"]), title="SEO Analysis", border_style="yellow"))
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise SystemExit(1)


@cli.command()
@click.argument("url")
@click.option("--model", "-m", default="base", type=click.Choice(["tiny", "base", "small", "medium", "large"]))
@click.option("--output-dir", "-d", default="output", help="Output directory")
def whisper(url, model, output_dir):
    """Transcribe video using Whisper AI"""
    from .whisper_transcribe import WhisperTranscriber

    console.print(f"[dim]Transcribing with Whisper ({model} model)...[/dim]")
    console.print("[yellow]This may take several minutes...[/yellow]")
    try:
        transcriber = WhisperTranscriber(model)
        result = transcriber.transcribe(url, output_dir=output_dir)
        if result.get("success"):
            console.print(f"[green]Transcription complete![/green]")
            for fmt, path in result.get("files", {}).items():
                console.print(f"  - {fmt}: {path}")
        else:
            console.print(f"[red]Error: {result.get('error')}[/red]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise SystemExit(1)


@cli.command()
@click.argument("url")
@click.argument("start_time")
@click.argument("end_time")
@click.option("--output-dir", "-d", default="output", help="Output directory")
@click.option("--name", "-n", help="Output filename")
def clip(url, start_time, end_time, output_dir, name):
    """Extract video clip between timestamps"""
    from .clip import ClipExtractor

    console.print(f"[dim]Extracting clip {start_time} - {end_time}...[/dim]")
    try:
        extractor = ClipExtractor(output_dir)
        result = extractor.extract_clip(url, start_time, end_time, name)
        if result.get("success"):
            console.print(f"[green]Clip saved to: {result['output_path']}[/green]")
        else:
            console.print(f"[red]Error: {result.get('error')}[/red]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise SystemExit(1)


@cli.command()
@click.argument("url")
@click.argument("start_time")
@click.option("--duration", "-t", default=5.0, help="GIF duration in seconds")
@click.option("--width", "-w", default=480, help="GIF width")
@click.option("--output-dir", "-d", default="output", help="Output directory")
def gif(url, start_time, duration, width, output_dir):
    """Create GIF from video"""
    from .gif import GifGenerator

    console.print(f"[dim]Creating GIF from {start_time} ({duration}s)...[/dim]")
    try:
        generator = GifGenerator(output_dir)
        result = generator.create_gif(url, start_time, duration, width=width)
        if result.get("success"):
            console.print(f"[green]GIF saved to: {result['output_path']}[/green]")
            console.print(f"[dim]Size: {result['size_kb']} KB[/dim]")
        else:
            console.print(f"[red]Error: {result.get('error')}[/red]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise SystemExit(1)


@cli.command("api")
@click.option("--host", default="0.0.0.0", help="Host address")
@click.option("--port", "-p", default=5000, help="Port number")
@click.option("--debug", is_flag=True, help="Debug mode")
def api_server(host, port, debug):
    """Start REST API server"""
    from .api_server import run_server

    console.print(f"[green]Starting API server on {host}:{port}[/green]")
    run_server(host, port, debug)


@cli.command("tts")
@click.argument("url")
@click.option("--provider", "-p", default="edge", type=click.Choice(["openai", "edge", "gtts"]))
@click.option("--output-dir", "-d", default="output", help="Output directory")
def text_to_speech(url, provider, output_dir):
    """Generate audio summary using TTS"""
    from .extractor import TranscriptExtractor
    from .tts import TTSGenerator
    from .config import Config

    valid, msg = Config.validate()
    if not valid:
        console.print(f"[red]{msg}[/red]")
        raise SystemExit(1)

    console.print(f"[dim]Generating audio summary ({provider})...[/dim]")
    try:
        extractor = TranscriptExtractor(url)
        extractor.extract()
        transcript = extractor.get_plain_text()
        generator = TTSGenerator(output_dir)
        result = generator.generate_summary_audio(transcript, provider=provider)
        if result.get("success"):
            console.print(f"[green]Audio saved to: {result['output_path']}[/green]")
        else:
            console.print(f"[red]Error: {result.get('error')}[/red]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise SystemExit(1)


@cli.command("multi-summary")
@click.argument("urls", nargs=-1, required=True)
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def multi_summary(urls, language, output):
    """Summarize multiple videos together"""
    from .multi_summary import MultiVideoSummarizer
    from .config import Config

    valid, msg = Config.validate()
    if not valid:
        console.print(f"[red]{msg}[/red]")
        raise SystemExit(1)

    console.print(f"[dim]Summarizing {len(urls)} videos...[/dim]")
    try:
        summarizer = MultiVideoSummarizer()
        result = summarizer.summarize_multiple(list(urls), language)
        if output:
            with open(output, "w", encoding="utf-8") as f:
                f.write(result)
            console.print(f"[green]Summary saved to {output}[/green]")
        else:
            console.print(Panel(Markdown(result), title="Multi-Video Summary", border_style="green"))
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise SystemExit(1)


@cli.command("progress")
@click.option("--add", "-a", help="Add video to tracking")
@click.option("--complete", "-c", help="Mark video as completed")
@click.option("--stats", is_flag=True, help="Show statistics")
@click.option("--export", "-e", help="Export to file")
def progress_cmd(add, complete, stats, export):
    """Track learning progress"""
    from .progress import ProgressTracker

    tracker = ProgressTracker()

    if add:
        result = tracker.add_video(add, status="to_watch")
        console.print(f"[green]Added: {add}[/green]")
    elif complete:
        result = tracker.add_video(complete, status="completed")
        console.print(f"[green]Marked complete: {complete}[/green]")
    elif stats:
        stats_data = tracker.get_stats()
        table = Table(title="Learning Progress")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="white")
        for key, value in stats_data.items():
            table.add_row(key.replace("_", " ").title(), str(value))
        console.print(table)
    elif export:
        data = tracker.export_data("markdown")
        with open(export, "w", encoding="utf-8") as f:
            f.write(data)
        console.print(f"[green]Progress exported to {export}[/green]")
    else:
        videos = tracker.get_all_videos()
        if not videos:
            console.print("[dim]No videos tracked yet[/dim]")
        else:
            table = Table(title="Tracked Videos")
            table.add_column("ID", style="cyan")
            table.add_column("Title", style="white")
            table.add_column("Status", style="green")
            for v in videos[:20]:
                table.add_row(v["id"][:11], v.get("title", "-")[:30], v["status"])
            console.print(table)


@cli.command()
@click.argument("url")
@click.option("--language", "-l", default="中文", help="Output language")
def recommend(url, language):
    """Get learning recommendations"""
    from .extractor import TranscriptExtractor
    from .recommend import VideoRecommender
    from .config import Config

    valid, msg = Config.validate()
    if not valid:
        console.print(f"[red]{msg}[/red]")
        raise SystemExit(1)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
        task = progress.add_task("Analyzing...", total=None)
        try:
            extractor = TranscriptExtractor(url)
            extractor.extract()
            transcript = extractor.get_plain_text()
            progress.update(task, description="Generating recommendations...")
            recommender = VideoRecommender()
            result = recommender.recommend_next(transcript, language)
            console.print(Panel(Markdown(result), title="Learning Recommendations", border_style="green"))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command()
@click.option("--add", "-a", help="Add channel to monitor")
@click.option("--remove", "-r", help="Remove channel")
@click.option("--check", is_flag=True, help="Check for new videos")
@click.option("--list", "list_channels", is_flag=True, help="List monitored channels")
def monitor(add, remove, check, list_channels):
    """Monitor YouTube channels"""
    from .monitor import ChannelMonitor

    mon = ChannelMonitor()

    if add:
        result = mon.add_channel(add)
        if "error" in result:
            console.print(f"[red]{result['error']}[/red]")
        else:
            console.print(f"[green]Added channel: {result['name']}[/green]")
    elif remove:
        if mon.remove_channel(remove):
            console.print(f"[green]Removed channel[/green]")
        else:
            console.print("[red]Channel not found[/red]")
    elif check:
        console.print("[dim]Checking for new videos...[/dim]")
        new_videos = mon.check_new_videos()
        if new_videos:
            console.print(f"[green]Found {len(new_videos)} new videos:[/green]")
            for v in new_videos:
                console.print(f"  - {v['title']} ({v['channel']})")
        else:
            console.print("[dim]No new videos[/dim]")
    elif list_channels:
        channels = mon.get_channels()
        if not channels:
            console.print("[dim]No channels monitored[/dim]")
        else:
            table = Table(title="Monitored Channels")
            table.add_column("Name", style="cyan")
            table.add_column("URL", style="white")
            for c in channels:
                table.add_row(c["name"], c["url"])
            console.print(table)
    else:
        status = mon.get_status()
        console.print(f"Monitoring {status['channels_count']} channels")
        console.print(f"Last check: {status['last_check'] or 'Never'}")


def main():
    """Main entry point"""
    cli()


if __name__ == "__main__":
    main()
