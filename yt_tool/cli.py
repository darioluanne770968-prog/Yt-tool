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


# ============================================
# Advanced Feature Commands (Phase 2)
# ============================================

# --- AI Deep Analysis ---

@cli.command("video-dna")
@click.argument("url")
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def video_dna_cmd(url, language, output):
    """Analyze video DNA fingerprint and unique characteristics"""
    from .extractor import TranscriptExtractor
    from .video_dna import VideoDNA
    from .config import Config
    import json

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
            progress.update(task, description="Analyzing video DNA...")
            analyzer = VideoDNA()
            result = analyzer.generate_fingerprint(transcript, language)
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(json.dumps(result, ensure_ascii=False, indent=2))
                console.print(f"[green]Video DNA saved to {output}[/green]")
            else:
                console.print(Panel(Markdown(f"**DNA ID:** {result.get('dna_id', 'N/A')}\n\n**Signature:** {json.dumps(result.get('signature', {}), ensure_ascii=False, indent=2)}"), title="Video DNA", border_style="cyan"))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command("knowledge-graph")
@click.argument("url")
@click.option("--format", "-f", "fmt", default="mermaid", type=click.Choice(["mermaid", "json", "cytoscape", "d3"]))
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def knowledge_graph_cmd(url, fmt, language, output):
    """Generate knowledge graph from video"""
    from .extractor import TranscriptExtractor
    from .knowledge_graph import KnowledgeGraphBuilder
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
            progress.update(task, description="Building knowledge graph...")
            builder = KnowledgeGraphBuilder()
            graph = builder.build_graph(transcript, language)
            if fmt == "mermaid":
                result = builder.export_mermaid(graph)
            elif fmt == "cytoscape":
                result = builder.export_cytoscape(graph)
            elif fmt == "d3":
                result = builder.export_d3(graph)
            else:
                import json
                result = json.dumps(graph, ensure_ascii=False, indent=2)
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(result)
                console.print(f"[green]Knowledge graph saved to {output}[/green]")
            else:
                console.print(Panel(result[:2000] + "..." if len(result) > 2000 else result, title="Knowledge Graph", border_style="green"))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command("argument-tracker")
@click.argument("urls", nargs=-1, required=True)
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def argument_tracker_cmd(urls, language, output):
    """Track arguments across multiple videos"""
    from .argument_tracker import ArgumentTracker
    from .config import Config
    import json

    valid, msg = Config.validate()
    if not valid:
        console.print(f"[red]{msg}[/red]")
        raise SystemExit(1)

    console.print(f"[dim]Analyzing arguments across {len(urls)} videos...[/dim]")
    try:
        tracker = ArgumentTracker()
        for url in urls:
            tracker.add_video_from_url(url, language)
        evolution = tracker.track_evolution(language)
        if output:
            with open(output, "w", encoding="utf-8") as f:
                f.write(json.dumps(evolution, ensure_ascii=False, indent=2))
            console.print(f"[green]Arguments saved to {output}[/green]")
        else:
            console.print(Panel(Markdown(f"**Arguments tracked:** {len(tracker.arguments)}\n\n**Evolution:** {json.dumps(evolution, ensure_ascii=False, indent=2)[:1500]}..."), title="Argument Tracker", border_style="yellow"))
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise SystemExit(1)


@cli.command("entropy")
@click.argument("url")
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def entropy_cmd(url, language, output):
    """Analyze information entropy and density"""
    from .extractor import TranscriptExtractor
    from .entropy_analyzer import EntropyAnalyzer
    from .config import Config
    import json

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
            progress.update(task, description="Analyzing entropy...")
            analyzer = EntropyAnalyzer()
            result = analyzer.analyze_full(transcript, language)
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(json.dumps(result, ensure_ascii=False, indent=2))
                console.print(f"[green]Entropy analysis saved to {output}[/green]")
            else:
                console.print(Panel(Markdown(f"**Lexical Density:** {result.get('lexical_density', {}).get('density', 'N/A')}\n\n**Vocabulary Richness:** {result.get('vocabulary_richness', {})}"), title="Entropy Analysis", border_style="blue"))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command("cognitive-load")
@click.argument("url")
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def cognitive_load_cmd(url, language, output):
    """Analyze cognitive load and learning difficulty"""
    from .extractor import TranscriptExtractor
    from .cognitive_load import CognitiveLoadAnalyzer
    from .config import Config
    import json

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
            progress.update(task, description="Analyzing cognitive load...")
            analyzer = CognitiveLoadAnalyzer()
            result = analyzer.analyze_full(transcript, language)
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(json.dumps(result, ensure_ascii=False, indent=2))
                console.print(f"[green]Cognitive load analysis saved to {output}[/green]")
            else:
                console.print(Panel(Markdown(f"**Overall Load:** {result.get('cognitive_load', {}).get('overall_load', 'N/A')}\n\n**Recommendations:** {json.dumps(result.get('recommendations', []), ensure_ascii=False)}"), title="Cognitive Load Analysis", border_style="magenta"))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


# --- Creative Content Generation ---

@cli.command("voice-clone")
@click.argument("url")
@click.option("--target-language", "-t", default="中文", help="Target language for dubbing")
@click.option("--format", "-f", "fmt", default="script", type=click.Choice(["script", "ssml", "srt"]))
@click.option("--output", "-o", help="Output file path")
def voice_clone_cmd(url, target_language, fmt, output):
    """Generate voice clone dubbing script"""
    from .extractor import TranscriptExtractor
    from .voice_clone import VoiceCloneGenerator
    from .config import Config
    import json

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
            progress.update(task, description="Generating dubbing script...")
            generator = VoiceCloneGenerator()
            if fmt == "ssml":
                result = generator.create_tts_markup(transcript, "ssml", target_language)
            else:
                dubbed = generator.generate_dubbed_script(transcript, target_language)
                result = dubbed.get("dubbed_script", json.dumps(dubbed, ensure_ascii=False, indent=2))
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(result)
                console.print(f"[green]Script saved to {output}[/green]")
            else:
                console.print(Panel(result[:3000] + "..." if len(result) > 3000 else result, title="Voice Clone Script", border_style="cyan"))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command("comic")
@click.argument("url")
@click.option("--style", "-s", default="manga", type=click.Choice(["manga", "western", "webtoon", "storyboard"]))
@click.option("--panels", "-n", default=6, help="Number of panels")
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def comic_cmd(url, style, panels, language, output):
    """Generate comic/storyboard from video"""
    from .extractor import TranscriptExtractor
    from .comic_generator import ComicGenerator
    from .config import Config
    import json

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
            progress.update(task, description="Generating comic...")
            generator = ComicGenerator()
            result = generator.generate_comic(transcript, style, panels, language)
            result_str = json.dumps(result, ensure_ascii=False, indent=2)
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(result_str)
                console.print(f"[green]Comic saved to {output}[/green]")
            else:
                console.print(Panel(result_str[:3000] + "..." if len(result_str) > 3000 else result_str, title=f"Comic ({style})", border_style="yellow"))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command("podcast-dialogue")
@click.argument("url")
@click.option("--style", "-s", default="casual", type=click.Choice(["casual", "interview", "debate", "storytelling"]))
@click.option("--hosts", "-n", default=2, help="Number of hosts")
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def podcast_dialogue_cmd(url, style, hosts, language, output):
    """Generate podcast dialogue from video"""
    from .extractor import TranscriptExtractor
    from .podcast_dialogue import PodcastDialogueGenerator
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
            progress.update(task, description="Generating podcast dialogue...")
            generator = PodcastDialogueGenerator()
            if style == "interview":
                dialogue = generator.generate_interview_format(transcript, language=language)
            elif style == "debate":
                dialogue = generator.generate_debate_format(transcript, language)
            elif style == "storytelling":
                dialogue = generator.generate_storytelling_podcast(transcript, language)
            else:
                host_list = generator.create_podcast_hosts("video topic", style, hosts, language)
                dialogue = generator.generate_dialogue(transcript, host_list, style, language)
            result = generator.export_script(dialogue, "script")
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(result)
                console.print(f"[green]Podcast script saved to {output}[/green]")
            else:
                console.print(Panel(Markdown(result[:3000] + "..." if len(result) > 3000 else result), title="Podcast Dialogue", border_style="magenta"))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command("interactive-story")
@click.argument("url")
@click.option("--format", "-f", "fmt", default="twine", type=click.Choice(["twine", "ink", "json"]))
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def interactive_story_cmd(url, fmt, language, output):
    """Generate interactive branching story"""
    from .extractor import TranscriptExtractor
    from .interactive_story import InteractiveStoryGenerator
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
            progress.update(task, description="Generating interactive story...")
            generator = InteractiveStoryGenerator()
            story = generator.generate_story(transcript, language)
            if fmt == "twine":
                result = generator.export_twine(story)
            elif fmt == "ink":
                result = generator.export_ink(story)
            else:
                import json
                result = json.dumps(story, ensure_ascii=False, indent=2)
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(result)
                console.print(f"[green]Story saved to {output}[/green]")
            else:
                console.print(Panel(result[:3000] + "..." if len(result) > 3000 else result, title="Interactive Story", border_style="green"))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command("meme")
@click.argument("url")
@click.option("--num", "-n", default=5, help="Number of memes")
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def meme_cmd(url, num, language, output):
    """Detect meme-worthy moments and generate meme templates"""
    from .extractor import TranscriptExtractor
    from .meme_generator import MemeGenerator
    from .config import Config
    import json

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
            progress.update(task, description="Detecting meme moments...")
            generator = MemeGenerator()
            moments = generator.detect_meme_moments(transcript, num, language)
            result = json.dumps(moments, ensure_ascii=False, indent=2)
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(result)
                console.print(f"[green]Memes saved to {output}[/green]")
            else:
                console.print(Panel(result[:3000] + "..." if len(result) > 3000 else result, title=f"Meme Moments ({len(moments)})", border_style="yellow"))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


# --- Learning & Memory Science ---

@cli.command("spaced-repetition")
@click.argument("url")
@click.option("--format", "-f", "fmt", default="anki", type=click.Choice(["anki", "json", "csv"]))
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def spaced_repetition_cmd(url, fmt, language, output):
    """Generate spaced repetition flashcards with SM-2 algorithm"""
    from .extractor import TranscriptExtractor
    from .spaced_repetition import SpacedRepetitionSystem
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
            progress.update(task, description="Generating spaced repetition cards...")
            srs = SpacedRepetitionSystem()
            cards = srs.generate_cards_from_content(transcript, language)
            result = srs.export_anki(cards)
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(result)
                console.print(f"[green]Cards saved to {output}[/green]")
            else:
                console.print(Panel(result[:3000] + "..." if len(result) > 3000 else result, title=f"Spaced Repetition ({len(cards)} cards)", border_style="cyan"))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command("feynman-notes")
@click.argument("url")
@click.option("--audience", "-a", default="child", type=click.Choice(["child", "teenager", "adult", "expert"]))
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def feynman_notes_cmd(url, audience, language, output):
    """Generate Feynman-style simplified explanations"""
    from .extractor import TranscriptExtractor
    from .feynman_notes import FeynmanNotesGenerator
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
            progress.update(task, description="Generating Feynman notes...")
            generator = FeynmanNotesGenerator()
            notes = generator.generate_eli5(transcript, audience, language)
            result = generator.export_feynman_notes(notes)
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(result)
                console.print(f"[green]Notes saved to {output}[/green]")
            else:
                console.print(Panel(Markdown(result[:3000] + "..." if len(result) > 3000 else result), title="Feynman Notes", border_style="green"))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command("cornell-notes")
@click.argument("url")
@click.option("--format", "-f", "fmt", default="markdown", type=click.Choice(["markdown", "html", "json"]))
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def cornell_notes_cmd(url, fmt, language, output):
    """Generate Cornell-style notes"""
    from .extractor import TranscriptExtractor
    from .cornell_notes import CornellNotesGenerator
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
            progress.update(task, description="Generating Cornell notes...")
            generator = CornellNotesGenerator()
            notes = generator.generate_cornell_notes(transcript, language)
            if fmt == "html":
                result = generator.export_html(notes)
            elif fmt == "json":
                import json
                result = json.dumps(notes, ensure_ascii=False, indent=2)
            else:
                result = generator.export_markdown(notes)
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(result)
                console.print(f"[green]Notes saved to {output}[/green]")
            else:
                console.print(Panel(Markdown(result[:3000] + "..." if len(result) > 3000 else result), title="Cornell Notes", border_style="blue"))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command("memory-palace")
@click.argument("url")
@click.option("--method", "-m", default="loci", type=click.Choice(["loci", "peg", "link", "story"]))
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def memory_palace_cmd(url, method, language, output):
    """Generate memory palace mnemonics"""
    from .extractor import TranscriptExtractor
    from .memory_palace import MemoryPalaceGenerator
    from .config import Config
    import json

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
            progress.update(task, description="Building memory palace...")
            generator = MemoryPalaceGenerator()
            if method == "peg":
                result = generator.create_peg_system(transcript, language)
            elif method == "link":
                result = generator.create_link_method(transcript, language)
            elif method == "story":
                result = generator.create_story_method(transcript, language)
            else:
                result = generator.create_memory_palace(transcript, language)
            result_str = json.dumps(result, ensure_ascii=False, indent=2)
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(result_str)
                console.print(f"[green]Memory palace saved to {output}[/green]")
            else:
                console.print(Panel(result_str[:3000] + "..." if len(result_str) > 3000 else result_str, title=f"Memory Palace ({method})", border_style="magenta"))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command("active-recall")
@click.argument("url")
@click.option("--method", "-m", default="retrieval", type=click.Choice(["retrieval", "elaborative", "interleaved"]))
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def active_recall_cmd(url, method, language, output):
    """Generate active recall practice materials"""
    from .extractor import TranscriptExtractor
    from .active_recall import ActiveRecallGenerator
    from .config import Config
    import json

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
            progress.update(task, description="Generating active recall materials...")
            generator = ActiveRecallGenerator()
            if method == "elaborative":
                result = generator.elaborative_interrogation(transcript, language)
            elif method == "interleaved":
                result = generator.interleaved_practice([transcript], language)
            else:
                result = generator.generate_retrieval_practice(transcript, language)
            result_str = json.dumps(result, ensure_ascii=False, indent=2)
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(result_str)
                console.print(f"[green]Materials saved to {output}[/green]")
            else:
                console.print(Panel(result_str[:3000] + "..." if len(result_str) > 3000 else result_str, title=f"Active Recall ({method})", border_style="yellow"))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


# --- Collaboration & Social ---

@cli.command("collaborative-notes")
@click.argument("url")
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def collaborative_notes_cmd(url, language, output):
    """Generate collaborative annotation template"""
    from .extractor import TranscriptExtractor
    from .collaborative_notes import CollaborativeNotes
    from .config import Config
    import json

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
            progress.update(task, description="Generating collaborative notes...")
            notes = CollaborativeNotes()
            annotations = notes.generate_annotations(transcript, language)
            result = json.dumps(annotations, ensure_ascii=False, indent=2)
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(result)
                console.print(f"[green]Annotations saved to {output}[/green]")
            else:
                console.print(Panel(result[:3000] + "..." if len(result) > 3000 else result, title="Collaborative Notes", border_style="cyan"))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command("study-group")
@click.argument("url")
@click.option("--size", "-s", default=4, help="Group size")
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def study_group_cmd(url, size, language, output):
    """Generate study group discussion guide"""
    from .extractor import TranscriptExtractor
    from .study_group import StudyGroupGenerator
    from .config import Config
    import json

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
            progress.update(task, description="Generating study group guide...")
            generator = StudyGroupGenerator()
            guide = generator.generate_discussion_guide(transcript, language)
            result = json.dumps(guide, ensure_ascii=False, indent=2)
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(result)
                console.print(f"[green]Guide saved to {output}[/green]")
            else:
                console.print(Panel(result[:3000] + "..." if len(result) > 3000 else result, title="Study Group Guide", border_style="green"))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command("discussion")
@click.argument("url")
@click.option("--format", "-f", "fmt", default="socratic", type=click.Choice(["socratic", "think-pair-share", "world-cafe", "fishbowl"]))
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def discussion_cmd(url, fmt, language, output):
    """Generate discussion guide in various formats"""
    from .extractor import TranscriptExtractor
    from .discussion_generator import DiscussionGenerator
    from .config import Config
    import json

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
            progress.update(task, description="Generating discussion guide...")
            generator = DiscussionGenerator()
            if fmt == "think-pair-share":
                result = generator.think_pair_share(transcript, language)
            elif fmt == "world-cafe":
                result = generator.world_cafe(transcript, language)
            elif fmt == "fishbowl":
                result = generator.fishbowl_discussion(transcript, language)
            else:
                result = generator.socratic_dialogue(transcript, language)
            result_str = json.dumps(result, ensure_ascii=False, indent=2)
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(result_str)
                console.print(f"[green]Discussion guide saved to {output}[/green]")
            else:
                console.print(Panel(result_str[:3000] + "..." if len(result_str) > 3000 else result_str, title=f"Discussion ({fmt})", border_style="blue"))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command("debate")
@click.argument("url")
@click.option("--rounds", "-r", default=3, help="Number of debate rounds")
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def debate_cmd(url, rounds, language, output):
    """Simulate debate on video topics"""
    from .extractor import TranscriptExtractor
    from .debate_simulator import DebateSimulator
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
            progress.update(task, description="Extracting debate topics...")
            simulator = DebateSimulator()
            topics = simulator.extract_debate_topics(transcript, 1, language)
            if topics:
                progress.update(task, description="Simulating debate...")
                debate = simulator.simulate_debate(topics[0]["topic"], rounds, language)
                result = simulator.export_debate(debate, "markdown")
            else:
                result = "No debate topics found in the video."
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(result)
                console.print(f"[green]Debate saved to {output}[/green]")
            else:
                console.print(Panel(Markdown(result[:3000] + "..." if len(result) > 3000 else result), title="Debate Simulation", border_style="red"))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


# --- Automation Workflow ---

@cli.command("workflow")
@click.option("--create", "-c", help="Create new workflow from template")
@click.option("--run", "-r", help="Run workflow by name")
@click.option("--list", "list_workflows", is_flag=True, help="List available workflows")
def workflow_cmd(create, run, list_workflows):
    """Manage automation workflows"""
    from .workflow_automation import WorkflowAutomation
    import json

    automation = WorkflowAutomation()

    if create:
        # Create from predefined template
        templates = automation.get_workflow_templates()
        if create in templates:
            workflow = automation.create_workflow(templates[create])
            console.print(f"[green]Workflow created: {workflow['name']}[/green]")
        else:
            console.print(f"[yellow]Available templates: {', '.join(templates.keys())}[/yellow]")
    elif run:
        console.print(f"[dim]Running workflow: {run}...[/dim]")
        result = automation.run_workflow(run)
        console.print(Panel(json.dumps(result, ensure_ascii=False, indent=2)[:2000], title="Workflow Result", border_style="green"))
    elif list_workflows:
        workflows = automation.list_workflows()
        if workflows:
            table = Table(title="Available Workflows")
            table.add_column("Name", style="cyan")
            table.add_column("Triggers", style="white")
            table.add_column("Actions", style="green")
            for w in workflows:
                table.add_row(w["name"], str(len(w.get("triggers", []))), str(len(w.get("actions", []))))
            console.print(table)
        else:
            console.print("[dim]No workflows defined[/dim]")
    else:
        console.print("[dim]Use --create, --run, or --list[/dim]")


@cli.command("scheduled-report")
@click.option("--type", "-t", "report_type", default="daily", type=click.Choice(["daily", "weekly", "monthly"]))
@click.option("--output", "-o", help="Output file path")
def scheduled_report_cmd(report_type, output):
    """Generate scheduled learning report"""
    from .scheduled_reports import ScheduledReportGenerator

    console.print(f"[dim]Generating {report_type} report...[/dim]")
    try:
        generator = ScheduledReportGenerator()
        if report_type == "weekly":
            result = generator.generate_weekly_report()
        elif report_type == "monthly":
            result = generator.generate_monthly_report()
        else:
            result = generator.generate_daily_report()
        if output:
            with open(output, "w", encoding="utf-8") as f:
                f.write(result)
            console.print(f"[green]Report saved to {output}[/green]")
        else:
            console.print(Panel(Markdown(result), title=f"{report_type.title()} Report", border_style="blue"))
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise SystemExit(1)


@cli.command("smart-playlist")
@click.argument("goal")
@click.option("--duration", "-d", default=60, help="Target duration in minutes")
@click.option("--level", "-l", default="beginner", type=click.Choice(["beginner", "intermediate", "advanced"]))
@click.option("--language", "-lang", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def smart_playlist_cmd(goal, duration, level, language, output):
    """Generate AI-curated learning playlist"""
    from .smart_playlist import SmartPlaylistGenerator
    from .config import Config
    import json

    valid, msg = Config.validate()
    if not valid:
        console.print(f"[red]{msg}[/red]")
        raise SystemExit(1)

    console.print(f"[dim]Creating playlist for: {goal}...[/dim]")
    try:
        generator = SmartPlaylistGenerator()
        playlist = generator.generate_learning_playlist(goal, duration, level, language)
        result = json.dumps(playlist, ensure_ascii=False, indent=2)
        if output:
            with open(output, "w", encoding="utf-8") as f:
                f.write(result)
            console.print(f"[green]Playlist saved to {output}[/green]")
        else:
            console.print(Panel(result[:3000] + "..." if len(result) > 3000 else result, title="Smart Playlist", border_style="green"))
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise SystemExit(1)


@cli.command("cross-platform")
@click.argument("url")
@click.option("--platform", "-p", required=True, type=click.Choice(["bilibili", "douyin", "tiktok", "xiaohongshu"]))
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def cross_platform_cmd(url, platform, language, output):
    """Analyze content from other platforms"""
    from .cross_platform import CrossPlatformAnalyzer
    from .config import Config
    import json

    valid, msg = Config.validate()
    if not valid:
        console.print(f"[red]{msg}[/red]")
        raise SystemExit(1)

    console.print(f"[dim]Analyzing {platform} content...[/dim]")
    try:
        analyzer = CrossPlatformAnalyzer()
        if platform == "bilibili":
            result = analyzer.analyze_bilibili(url, language)
        elif platform == "douyin":
            result = analyzer.analyze_douyin(url, language)
        else:
            result = {"error": f"Platform {platform} support coming soon"}
        result_str = json.dumps(result, ensure_ascii=False, indent=2)
        if output:
            with open(output, "w", encoding="utf-8") as f:
                f.write(result_str)
            console.print(f"[green]Analysis saved to {output}[/green]")
        else:
            console.print(Panel(result_str[:3000] + "..." if len(result_str) > 3000 else result_str, title=f"{platform.title()} Analysis", border_style="magenta"))
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise SystemExit(1)


@cli.command("rss")
@click.option("--add", "-a", help="Add video URL to feed")
@click.option("--export", "-e", "export_format", type=click.Choice(["rss", "atom", "json"]), help="Export feed")
@click.option("--output", "-o", help="Output file path")
def rss_cmd(add, export_format, output):
    """Generate RSS feed from videos"""
    from .rss_generator import RSSFeedGenerator

    generator = RSSFeedGenerator()

    if add:
        generator.add_video_to_feed(add)
        console.print(f"[green]Added to feed: {add}[/green]")
    elif export_format:
        if export_format == "atom":
            result = generator.generate_atom()
        elif export_format == "json":
            result = generator.generate_json_feed()
        else:
            result = generator.generate_rss()
        if output:
            with open(output, "w", encoding="utf-8") as f:
                f.write(result)
            console.print(f"[green]Feed saved to {output}[/green]")
        else:
            console.print(Panel(result[:2000] + "..." if len(result) > 2000 else result, title=f"{export_format.upper()} Feed", border_style="yellow"))
    else:
        console.print("[dim]Use --add to add video or --export to generate feed[/dim]")


# --- Visualization & Data ---

@cli.command("knowledge-3d")
@click.argument("url")
@click.option("--format", "-f", "fmt", default="html", type=click.Choice(["html", "json"]))
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def knowledge_3d_cmd(url, fmt, language, output):
    """Generate 3D knowledge map visualization"""
    from .extractor import TranscriptExtractor
    from .knowledge_map_3d import KnowledgeMap3D
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
            progress.update(task, description="Building 3D knowledge map...")
            mapper = KnowledgeMap3D()
            map_data = mapper.build_map(transcript, language)
            if fmt == "html":
                result = mapper.export_threejs(map_data)
            else:
                import json
                result = json.dumps(map_data, ensure_ascii=False, indent=2)
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(result)
                console.print(f"[green]3D map saved to {output}[/green]")
            else:
                console.print(f"[green]Generated 3D map with {len(map_data.get('nodes', []))} nodes[/green]")
                console.print("[dim]Use --output to save HTML file[/dim]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command("learning-heatmap")
@click.option("--output", "-o", help="Output file path")
def learning_heatmap_cmd(output):
    """Generate learning activity heatmap"""
    from .learning_heatmap import LearningHeatmap

    console.print("[dim]Generating learning heatmap...[/dim]")
    try:
        heatmap = LearningHeatmap()
        result = heatmap.export_html_calendar()
        if output:
            with open(output, "w", encoding="utf-8") as f:
                f.write(result)
            console.print(f"[green]Heatmap saved to {output}[/green]")
        else:
            stats = heatmap.get_statistics()
            console.print(Panel(f"Total videos: {stats['total_videos']}\nTotal time: {stats['total_time_hours']:.1f} hours\nStreak: {stats['current_streak']} days", title="Learning Stats", border_style="green"))
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise SystemExit(1)


@cli.command("concept-network")
@click.argument("url")
@click.option("--format", "-f", "fmt", default="html", type=click.Choice(["html", "json", "cytoscape"]))
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def concept_network_cmd(url, fmt, language, output):
    """Generate interactive concept network"""
    from .extractor import TranscriptExtractor
    from .concept_network import ConceptNetworkBuilder
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
            progress.update(task, description="Building concept network...")
            builder = ConceptNetworkBuilder()
            network = builder.build_network(transcript, language)
            if fmt == "html":
                result = builder.export_visjs(network)
            elif fmt == "cytoscape":
                import json
                result = json.dumps(builder.export_cytoscape(network), ensure_ascii=False, indent=2)
            else:
                import json
                result = json.dumps(network, ensure_ascii=False, indent=2)
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(result)
                console.print(f"[green]Network saved to {output}[/green]")
            else:
                console.print(f"[green]Generated network with {len(network.get('nodes', []))} concepts[/green]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command("timeline")
@click.argument("url")
@click.option("--format", "-f", "fmt", default="youtube", type=click.Choice(["youtube", "vtt", "edl", "html"]))
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def timeline_cmd(url, fmt, language, output):
    """Generate video timeline with chapters"""
    from .extractor import TranscriptExtractor
    from .timeline_editor import TimelineEditor
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
            progress.update(task, description="Generating timeline...")
            editor = TimelineEditor()
            timeline = editor.generate_timeline(transcript, language=language)
            if fmt == "vtt":
                result = editor.export_vtt_chapters(timeline)
            elif fmt == "edl":
                result = editor.export_edl(timeline)
            elif fmt == "html":
                result = editor.generate_visual_timeline_html(timeline)
            else:
                result = editor.export_youtube_chapters(timeline)
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(result)
                console.print(f"[green]Timeline saved to {output}[/green]")
            else:
                console.print(Panel(result[:2000] + "..." if len(result) > 2000 else result, title="Video Timeline", border_style="cyan"))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


# --- Accessibility ---

@cli.command("accessibility")
@click.argument("url")
@click.option("--feature", "-f", required=True, type=click.Choice(["sign-language", "audio-description", "simplified", "multisensory"]))
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def accessibility_cmd(url, feature, language, output):
    """Generate accessible content versions"""
    from .extractor import TranscriptExtractor
    from .accessibility import AccessibilitySuite
    from .config import Config
    import json

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
            progress.update(task, description=f"Generating {feature}...")
            suite = AccessibilitySuite()
            if feature == "sign-language":
                result = suite.generate_sign_language_script(transcript, language)
            elif feature == "audio-description":
                result = suite.generate_audio_description(transcript, language)
            elif feature == "simplified":
                result = suite.simplify_content(transcript, "simple", language)
            else:
                result = suite.create_multisensory_notes(transcript, language)
            result_str = json.dumps(result, ensure_ascii=False, indent=2) if isinstance(result, dict) else result
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(result_str)
                console.print(f"[green]Accessible content saved to {output}[/green]")
            else:
                console.print(Panel(result_str[:3000] + "..." if len(result_str) > 3000 else result_str, title=f"Accessibility ({feature})", border_style="blue"))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


# --- Business Tools ---

@cli.command("business")
@click.argument("url")
@click.option("--feature", "-f", required=True, type=click.Choice(["competitor", "trends", "sponsors", "copyright", "roi"]))
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def business_cmd(url, feature, language, output):
    """Business analysis tools"""
    from .extractor import TranscriptExtractor
    from .business_tools import BusinessToolsSuite
    from .config import Config
    import json

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
            progress.update(task, description=f"Running {feature} analysis...")
            suite = BusinessToolsSuite()
            if feature == "trends":
                result = suite.predict_topic_trends(transcript, language=language)
            elif feature == "sponsors":
                result = suite.detect_sponsorships(transcript, language)
            elif feature == "copyright":
                result = suite.check_copyright_risks(transcript, language)
            elif feature == "roi":
                result = suite.estimate_video_value(transcript, language=language)
            else:
                result = {"message": "Use channel command for competitor analysis"}
            result_str = json.dumps(result, ensure_ascii=False, indent=2)
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(result_str)
                console.print(f"[green]Analysis saved to {output}[/green]")
            else:
                console.print(Panel(result_str[:3000] + "..." if len(result_str) > 3000 else result_str, title=f"Business ({feature})", border_style="yellow"))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


# ============================================
# Phase 3 Advanced Feature Commands
# ============================================

# --- AI Teaching Assistant ---

@cli.command("tutor")
@click.argument("url")
@click.option("--question", "-q", help="Ask tutor a question")
@click.option("--language", "-l", default="中文", help="Output language")
def tutor_cmd(url, question, language):
    """Start AI tutoring session"""
    from .extractor import TranscriptExtractor
    from .virtual_tutor import VirtualTutor
    from .config import Config

    valid, msg = Config.validate()
    if not valid:
        console.print(f"[red]{msg}[/red]")
        raise SystemExit(1)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
        task = progress.add_task("Starting tutor session...", total=None)
        try:
            extractor = TranscriptExtractor(url)
            extractor.extract()
            transcript = extractor.get_plain_text()
            tutor = VirtualTutor()
            if question:
                tutor.current_context = transcript
                result = tutor.ask_tutor(question, language)
                console.print(Panel(Markdown(result["answer"]), title="AI Tutor", border_style="cyan"))
            else:
                result = tutor.start_session(transcript, language=language)
                console.print(Panel(Markdown(result["welcome_message"]), title="AI Tutor Session", border_style="cyan"))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command("diagnose")
@click.argument("url")
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def diagnose_cmd(url, language, output):
    """Diagnose learning challenges for content"""
    from .extractor import TranscriptExtractor
    from .learning_diagnosis import LearningDiagnostics
    from .config import Config
    import json

    valid, msg = Config.validate()
    if not valid:
        console.print(f"[red]{msg}[/red]")
        raise SystemExit(1)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
        task = progress.add_task("Diagnosing content...", total=None)
        try:
            extractor = TranscriptExtractor(url)
            extractor.extract()
            transcript = extractor.get_plain_text()
            diagnostics = LearningDiagnostics()
            result = diagnostics.diagnose_from_transcript(transcript, "video content", language)
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(json.dumps(result, ensure_ascii=False, indent=2))
                console.print(f"[green]Diagnosis saved to {output}[/green]")
            else:
                console.print(Panel(Markdown(result["diagnosis"]), title="Learning Diagnosis", border_style="blue"))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command("predict-time")
@click.argument("url")
@click.option("--level", "-l", default="intermediate", type=click.Choice(["beginner", "intermediate", "advanced"]))
@click.option("--language", "-lang", default="中文", help="Output language")
def predict_time_cmd(url, level, language):
    """Predict learning time for content"""
    from .extractor import TranscriptExtractor
    from .knowledge_predictor import KnowledgePredictor
    from .config import Config

    valid, msg = Config.validate()
    if not valid:
        console.print(f"[red]{msg}[/red]")
        raise SystemExit(1)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
        task = progress.add_task("Predicting learning time...", total=None)
        try:
            extractor = TranscriptExtractor(url)
            extractor.extract()
            transcript = extractor.get_plain_text()
            predictor = KnowledgePredictor()
            result = predictor.predict_learning_time(transcript, level, language)
            console.print(Panel(Markdown(result["prediction"]), title="Learning Time Prediction", border_style="green"))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command("qa-bot")
@click.argument("url")
@click.option("--question", "-q", required=True, help="Question to ask")
@click.option("--language", "-l", default="中文", help="Output language")
def qa_bot_cmd(url, question, language):
    """Ask the QA bot a question about video"""
    from .extractor import TranscriptExtractor
    from .qa_bot import QABot
    from .config import Config

    valid, msg = Config.validate()
    if not valid:
        console.print(f"[red]{msg}[/red]")
        raise SystemExit(1)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
        task = progress.add_task("Processing question...", total=None)
        try:
            extractor = TranscriptExtractor(url)
            extractor.extract()
            transcript = extractor.get_plain_text()
            bot = QABot()
            bot.load_video_content(url, transcript)
            result = bot.ask(question, url, language)
            console.print(Panel(Markdown(result["answer"]), title="QA Bot Answer", border_style="cyan"))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


# --- Logic Analysis ---

@cli.command("logic")
@click.argument("url")
@click.option("--type", "-t", "analysis_type", default="structure", type=click.Choice(["structure", "fallacies", "assumptions", "causal", "full"]))
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def logic_cmd(url, analysis_type, language, output):
    """Analyze logical structure and reasoning"""
    from .extractor import TranscriptExtractor
    from .logic_analyzer import LogicAnalyzer
    from .config import Config

    valid, msg = Config.validate()
    if not valid:
        console.print(f"[red]{msg}[/red]")
        raise SystemExit(1)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
        task = progress.add_task("Analyzing logic...", total=None)
        try:
            extractor = TranscriptExtractor(url)
            extractor.extract()
            transcript = extractor.get_plain_text()
            analyzer = LogicAnalyzer()
            if analysis_type == "fallacies":
                result = analyzer.detect_fallacies(transcript, language)
                content = result["fallacies"]
            elif analysis_type == "assumptions":
                result = analyzer.extract_hidden_assumptions(transcript, language)
                content = result["hidden_assumptions"]
            elif analysis_type == "causal":
                result = analyzer.build_causal_graph(transcript, language)
                content = result["causal_graph"]
            elif analysis_type == "full":
                result = analyzer.generate_logic_report(transcript, language)
                content = result["report"]
            else:
                result = analyzer.analyze_argument_structure(transcript, language)
                content = result["analysis"]
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(content)
                console.print(f"[green]Analysis saved to {output}[/green]")
            else:
                console.print(Panel(Markdown(content[:3000] + "..." if len(content) > 3000 else content), title=f"Logic Analysis ({analysis_type})", border_style="yellow"))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


# --- Multimedia Tools ---

@cli.command("thumbnail-design")
@click.argument("url")
@click.option("--style", "-s", default="modern", help="Design style")
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def thumbnail_design_cmd(url, style, language, output):
    """Generate thumbnail design prompts"""
    from .extractor import TranscriptExtractor
    from .multimedia_creator import MultimediaCreator
    from .config import Config

    valid, msg = Config.validate()
    if not valid:
        console.print(f"[red]{msg}[/red]")
        raise SystemExit(1)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
        task = progress.add_task("Designing thumbnail...", total=None)
        try:
            extractor = TranscriptExtractor(url)
            extractor.extract()
            transcript = extractor.get_plain_text()
            creator = MultimediaCreator()
            result = creator.generate_thumbnail_prompt(transcript, style=style, language=language)
            content = result["thumbnail_designs"]
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(content)
                console.print(f"[green]Design saved to {output}[/green]")
            else:
                console.print(Panel(Markdown(content[:3000] + "..." if len(content) > 3000 else content), title="Thumbnail Design", border_style="magenta"))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command("music-recommend")
@click.argument("url")
@click.option("--language", "-l", default="中文", help="Output language")
def music_recommend_cmd(url, language):
    """Recommend background music"""
    from .extractor import TranscriptExtractor
    from .multimedia_creator import MultimediaCreator
    from .config import Config

    valid, msg = Config.validate()
    if not valid:
        console.print(f"[red]{msg}[/red]")
        raise SystemExit(1)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
        task = progress.add_task("Analyzing for music...", total=None)
        try:
            extractor = TranscriptExtractor(url)
            extractor.extract()
            transcript = extractor.get_plain_text()
            creator = MultimediaCreator()
            result = creator.recommend_background_music(transcript, language)
            console.print(Panel(Markdown(result["music_recommendations"][:3000]), title="Music Recommendations", border_style="green"))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command("highlights")
@click.argument("url")
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def highlights_cmd(url, language, output):
    """Detect video highlight moments"""
    from .extractor import TranscriptExtractor
    from .multimedia_creator import MultimediaCreator
    from .config import Config

    valid, msg = Config.validate()
    if not valid:
        console.print(f"[red]{msg}[/red]")
        raise SystemExit(1)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
        task = progress.add_task("Detecting highlights...", total=None)
        try:
            extractor = TranscriptExtractor(url)
            extractor.extract()
            transcript = extractor.get_plain_text()
            creator = MultimediaCreator()
            result = creator.detect_highlight_moments(transcript, language)
            content = result["highlights"]
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(content)
                console.print(f"[green]Highlights saved to {output}[/green]")
            else:
                console.print(Panel(Markdown(content[:3000] + "..." if len(content) > 3000 else content), title="Video Highlights", border_style="yellow"))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


# --- Gamification ---

@cli.command("game-stats")
def game_stats_cmd():
    """Show gamification stats"""
    from .gamification import GamificationSystem

    game = GamificationSystem()
    stats = game.get_stats()

    table = Table(title="Learning Game Stats")
    table.add_column("Stat", style="cyan")
    table.add_column("Value", style="green")
    table.add_row("Level", str(stats["level"]))
    table.add_row("XP", f"{stats['xp']} / {stats['xp'] + stats['xp_to_next_level']}")
    table.add_row("Total XP", str(stats["total_xp"]))
    table.add_row("Streak", f"{stats['streak']} days")
    table.add_row("Longest Streak", f"{stats['longest_streak']} days")
    table.add_row("Coins", str(stats["coins"]))
    table.add_row("Achievements", f"{stats['achievements_unlocked']}/{stats['total_achievements']}")
    console.print(table)


@cli.command("achievements")
def achievements_cmd():
    """Show available achievements"""
    from .gamification import GamificationSystem

    game = GamificationSystem()
    achievements = game.get_available_achievements()

    table = Table(title="Achievements")
    table.add_column("", width=3)
    table.add_column("Name", style="cyan")
    table.add_column("Description")
    table.add_column("XP", style="yellow")
    table.add_column("Status")

    for ach in achievements:
        status = "[green]✓ Unlocked[/green]" if ach["unlocked"] else "[dim]Locked[/dim]"
        table.add_row(ach["icon"], ach["name"], ach["description"], str(ach["xp"]), status)

    console.print(table)


@cli.command("daily-challenges")
def daily_challenges_cmd():
    """Show daily challenges"""
    from .gamification import GamificationSystem

    game = GamificationSystem()
    challenges = game.generate_daily_challenges()

    table = Table(title="Daily Challenges")
    table.add_column("Challenge", style="cyan")
    table.add_column("Progress")
    table.add_column("XP", style="yellow")
    table.add_column("Coins", style="green")

    for ch in challenges:
        progress = f"{ch['progress']}/{ch['target']}"
        table.add_row(ch["title"], progress, str(ch["xp_reward"]), str(ch["coin_reward"]))

    console.print(table)


# --- AI Writer ---

@cli.command("paper-outline")
@click.argument("url")
@click.option("--topic", "-t", default="", help="Paper topic")
@click.option("--type", "paper_type", default="research", type=click.Choice(["research", "review", "essay"]))
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def paper_outline_cmd(url, topic, paper_type, language, output):
    """Generate academic paper outline"""
    from .extractor import TranscriptExtractor
    from .ai_writer import AIWriter
    from .config import Config

    valid, msg = Config.validate()
    if not valid:
        console.print(f"[red]{msg}[/red]")
        raise SystemExit(1)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
        task = progress.add_task("Generating outline...", total=None)
        try:
            extractor = TranscriptExtractor(url)
            extractor.extract()
            transcript = extractor.get_plain_text()
            writer = AIWriter()
            result = writer.generate_paper_outline(transcript, topic, paper_type, language)
            content = result["outline"]
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(content)
                console.print(f"[green]Outline saved to {output}[/green]")
            else:
                console.print(Panel(Markdown(content[:3000] + "..." if len(content) > 3000 else content), title="Paper Outline", border_style="blue"))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command("lesson-plan")
@click.argument("url")
@click.option("--grade", "-g", default="high_school", help="Grade level")
@click.option("--duration", "-d", default=45, help="Duration in minutes")
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def lesson_plan_cmd(url, grade, duration, language, output):
    """Generate teaching lesson plan"""
    from .extractor import TranscriptExtractor
    from .ai_writer import AIWriter
    from .config import Config

    valid, msg = Config.validate()
    if not valid:
        console.print(f"[red]{msg}[/red]")
        raise SystemExit(1)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
        task = progress.add_task("Generating lesson plan...", total=None)
        try:
            extractor = TranscriptExtractor(url)
            extractor.extract()
            transcript = extractor.get_plain_text()
            writer = AIWriter()
            result = writer.generate_lesson_plan(transcript, grade, duration, language)
            content = result["lesson_plan"]
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(content)
                console.print(f"[green]Lesson plan saved to {output}[/green]")
            else:
                console.print(Panel(Markdown(content[:3000] + "..." if len(content) > 3000 else content), title="Lesson Plan", border_style="green"))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command("review-article")
@click.argument("url")
@click.option("--style", "-s", default="professional", type=click.Choice(["academic", "casual", "professional", "blog"]))
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def review_article_cmd(url, style, language, output):
    """Generate review article"""
    from .extractor import TranscriptExtractor
    from .ai_writer import AIWriter
    from .config import Config

    valid, msg = Config.validate()
    if not valid:
        console.print(f"[red]{msg}[/red]")
        raise SystemExit(1)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
        task = progress.add_task("Writing review...", total=None)
        try:
            extractor = TranscriptExtractor(url)
            extractor.extract()
            transcript = extractor.get_plain_text()
            writer = AIWriter()
            result = writer.generate_book_review(transcript, style, language)
            content = result["review"]
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(content)
                console.print(f"[green]Review saved to {output}[/green]")
            else:
                console.print(Panel(Markdown(content[:3000] + "..." if len(content) > 3000 else content), title="Review Article", border_style="magenta"))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


# --- Learning Analytics ---

@cli.command("analytics")
@click.option("--report", "-r", is_flag=True, help="Generate full report")
@click.option("--trends", "-t", is_flag=True, help="Show learning trends")
@click.option("--best-time", "-b", is_flag=True, help="Find best learning time")
@click.option("--language", "-l", default="中文", help="Output language")
def analytics_cmd(report, trends, best_time, language):
    """View learning analytics"""
    from .learning_analytics import LearningAnalytics

    analytics = LearningAnalytics()

    if report:
        result = analytics.generate_analytics_report(language)
        console.print(Panel(Markdown(result["report"]), title="Analytics Report", border_style="blue"))
    elif trends:
        result = analytics.get_learning_trends(30)
        console.print(f"[cyan]Learning Trends (Last 30 days)[/cyan]")
        console.print(f"Trend: {result['trend']}")
        console.print(f"Active days: {result['active_days']}")
        console.print(f"Total time: {result['total_time']} minutes")
    elif best_time:
        result = analytics.get_best_learning_time()
        console.print(f"[cyan]Best Learning Time[/cyan]")
        console.print(result["recommendation"])
    else:
        console.print("[dim]Use --report, --trends, or --best-time[/dim]")


# --- Smart Reminders ---

@cli.command("reminders")
@click.option("--today", "-t", is_flag=True, help="Show today's agenda")
@click.option("--schedule", "-s", help="Schedule review for topic")
@click.option("--goal", "-g", help="Set a learning goal")
@click.option("--deadline", "-d", help="Goal deadline (YYYY-MM-DD)")
def reminders_cmd(today, schedule, goal, deadline):
    """Manage smart reminders"""
    from .smart_reminder import SmartReminder
    import json

    reminder = SmartReminder()

    if today:
        agenda = reminder.get_today_agenda()
        console.print(f"[cyan]{agenda['daily_message']}[/cyan]")
        if agenda["reviews_due"]:
            console.print(f"\n[yellow]Reviews due: {len(agenda['reviews_due'])}[/yellow]")
        if agenda["goal_reminders"]:
            for g in agenda["goal_reminders"]:
                console.print(f"  • {g['message']}")
    elif schedule:
        result = reminder.schedule_ebbinghaus_review(schedule)
        console.print(f"[green]Scheduled {len(result['review_schedule'])} reviews for '{schedule}'[/green]")
    elif goal and deadline:
        result = reminder.set_goal(goal, deadline)
        console.print(f"[green]Goal set: {goal} (due {deadline})[/green]")
    else:
        console.print("[dim]Use --today, --schedule, or --goal with --deadline[/dim]")


# --- Content Quality ---

@cli.command("quality")
@click.argument("url")
@click.option("--type", "-t", "assess_type", default="full", type=click.Choice(["teaching", "reliability", "depth", "originality", "audience", "full"]))
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def quality_cmd(url, assess_type, language, output):
    """Assess content quality"""
    from .extractor import TranscriptExtractor
    from .content_quality import ContentQualityAssessor
    from .config import Config

    valid, msg = Config.validate()
    if not valid:
        console.print(f"[red]{msg}[/red]")
        raise SystemExit(1)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
        task = progress.add_task("Assessing quality...", total=None)
        try:
            extractor = TranscriptExtractor(url)
            extractor.extract()
            transcript = extractor.get_plain_text()
            assessor = ContentQualityAssessor()
            if assess_type == "teaching":
                result = assessor.assess_teaching_effectiveness(transcript, language)
                content = result["assessment"]
            elif assess_type == "reliability":
                result = assessor.evaluate_information_reliability(transcript, language)
                content = result["reliability_assessment"]
            elif assess_type == "depth":
                result = assessor.assess_content_depth(transcript, language=language)
                content = result["depth_assessment"]
            elif assess_type == "originality":
                result = assessor.detect_originality(transcript, language)
                content = result["originality_assessment"]
            elif assess_type == "audience":
                result = assessor.evaluate_audience_match(transcript, language=language)
                content = result["audience_match"]
            else:
                result = assessor.generate_quality_report(transcript, language)
                content = result["quality_report"]
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(content)
                console.print(f"[green]Assessment saved to {output}[/green]")
            else:
                console.print(Panel(Markdown(content[:3000] + "..." if len(content) > 3000 else content), title=f"Quality Assessment ({assess_type})", border_style="yellow"))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


# --- Collaboration ---

@cli.command("watch-party")
@click.argument("url")
@click.option("--create", "-c", is_flag=True, help="Create watch party")
@click.option("--host", "-h", default="Host", help="Host name")
def watch_party_cmd(url, create, host):
    """Create a watch party"""
    from .collaboration_hub import CollaborationHub

    hub = CollaborationHub()

    if create:
        party = hub.create_watch_party(url, "Video Watch Party", host)
        console.print(f"[green]Watch party created![/green]")
        console.print(f"Room ID: [cyan]{party['room_id']}[/cyan]")
        console.print(f"Share this ID with others to join")
    else:
        console.print("[dim]Use --create to start a watch party[/dim]")


@cli.command("annotate")
@click.argument("url")
@click.option("--add", "-a", help="Add annotation")
@click.option("--timestamp", "-t", default=0.0, help="Video timestamp")
@click.option("--user", "-u", default="User", help="Your name")
@click.option("--list", "list_all", is_flag=True, help="List annotations")
def annotate_cmd(url, add, timestamp, user, list_all):
    """Manage video annotations"""
    from .collaboration_hub import CollaborationHub
    import json

    hub = CollaborationHub()

    if add:
        result = hub.create_shared_annotation(url, user, timestamp, add)
        console.print(f"[green]Annotation added at {timestamp}s[/green]")
    elif list_all:
        annotations = hub.get_video_annotations(url)
        if annotations:
            for ann in annotations:
                console.print(f"[{ann['timestamp']}s] {ann['user']}: {ann['text']}")
        else:
            console.print("[dim]No annotations yet[/dim]")
    else:
        console.print("[dim]Use --add to annotate or --list to view[/dim]")


# --- Cross-modal ---

@cli.command("to-podcast")
@click.argument("url")
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def to_podcast_cmd(url, language, output):
    """Convert video to podcast script"""
    from .extractor import TranscriptExtractor
    from .cross_modal import CrossModalConverter
    from .config import Config

    valid, msg = Config.validate()
    if not valid:
        console.print(f"[red]{msg}[/red]")
        raise SystemExit(1)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
        task = progress.add_task("Converting to podcast...", total=None)
        try:
            extractor = TranscriptExtractor(url)
            extractor.extract()
            transcript = extractor.get_plain_text()
            converter = CrossModalConverter()
            result = converter.video_to_podcast_audio(transcript, language=language)
            content = result["podcast_script"]
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(content)
                console.print(f"[green]Podcast script saved to {output}[/green]")
            else:
                console.print(Panel(Markdown(content[:3000] + "..." if len(content) > 3000 else content), title="Podcast Script", border_style="cyan"))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command("to-ebook")
@click.argument("url")
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def to_ebook_cmd(url, language, output):
    """Convert video to ebook chapter"""
    from .extractor import TranscriptExtractor
    from .cross_modal import CrossModalConverter
    from .config import Config

    valid, msg = Config.validate()
    if not valid:
        console.print(f"[red]{msg}[/red]")
        raise SystemExit(1)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
        task = progress.add_task("Converting to ebook...", total=None)
        try:
            extractor = TranscriptExtractor(url)
            extractor.extract()
            transcript = extractor.get_plain_text()
            converter = CrossModalConverter()
            result = converter.video_to_ebook(transcript, language=language)
            content = result["ebook_content"]
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(content)
                console.print(f"[green]Ebook chapter saved to {output}[/green]")
            else:
                console.print(Panel(Markdown(content[:3000] + "..." if len(content) > 3000 else content), title="Ebook Chapter", border_style="green"))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command("infographic")
@click.argument("url")
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def infographic_cmd(url, language, output):
    """Generate infographic design"""
    from .extractor import TranscriptExtractor
    from .cross_modal import CrossModalConverter
    from .config import Config

    valid, msg = Config.validate()
    if not valid:
        console.print(f"[red]{msg}[/red]")
        raise SystemExit(1)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
        task = progress.add_task("Designing infographic...", total=None)
        try:
            extractor = TranscriptExtractor(url)
            extractor.extract()
            transcript = extractor.get_plain_text()
            converter = CrossModalConverter()
            result = converter.content_to_infographic(transcript, language)
            content = result["infographic_design"]
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(content)
                console.print(f"[green]Infographic design saved to {output}[/green]")
            else:
                console.print(Panel(Markdown(content[:3000] + "..." if len(content) > 3000 else content), title="Infographic Design", border_style="magenta"))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


@cli.command("storyboard")
@click.argument("url")
@click.option("--duration", "-d", default=5, help="Target duration in minutes")
@click.option("--language", "-l", default="中文", help="Output language")
@click.option("--output", "-o", help="Output file path")
def storyboard_cmd(url, duration, language, output):
    """Generate video storyboard"""
    from .extractor import TranscriptExtractor
    from .cross_modal import CrossModalConverter
    from .config import Config

    valid, msg = Config.validate()
    if not valid:
        console.print(f"[red]{msg}[/red]")
        raise SystemExit(1)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
        task = progress.add_task("Creating storyboard...", total=None)
        try:
            extractor = TranscriptExtractor(url)
            extractor.extract()
            transcript = extractor.get_plain_text()
            converter = CrossModalConverter()
            result = converter.text_to_video_storyboard(transcript, duration, language)
            content = result["storyboard"]
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(content)
                console.print(f"[green]Storyboard saved to {output}[/green]")
            else:
                console.print(Panel(Markdown(content[:3000] + "..." if len(content) > 3000 else content), title="Video Storyboard", border_style="yellow"))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise SystemExit(1)


def main():
    """Main entry point"""
    cli()


if __name__ == "__main__":
    main()
