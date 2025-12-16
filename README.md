# YouTube AI Tool

AI-powered YouTube video analysis toolkit - 智能 YouTube 视频分析工具

## Features

### Core Features

| Feature | Description | Command |
|---------|-------------|---------|
| **Transcript Extraction** | Extract subtitles/transcripts | `yt-tool transcript` |
| **AI Summary** | Generate video summaries (7 styles) | `yt-tool summary` |
| **Key Points** | Extract highlights and key info | `yt-tool keypoints` |
| **Chapter Generation** | Auto-generate timestamps | `yt-tool chapters` |
| **Translation** | Multi-language translation | `yt-tool translate` |
| **Q&A** | Interactive video Q&A | `yt-tool qa` |
| **Search** | Search keywords in content | `yt-tool search` |

### Extended Features

| Feature | Description | Command |
|---------|-------------|---------|
| **Video Info** | Get video metadata | `yt-tool info` |
| **Mind Map** | Generate mind maps | `yt-tool mindmap` |
| **Subtitles Download** | Export SRT/VTT/TXT | `yt-tool subtitle` |
| **Audio Download** | Download MP3/M4A/WAV | `yt-tool audio` |
| **Video Download** | Download MP4 video | `yt-tool video` |
| **Thumbnail** | Download video thumbnail | `yt-tool thumbnail` |
| **Comments Analysis** | AI analyze comments | `yt-tool comments` |
| **Batch Processing** | Process multiple videos | `yt-tool batch` |
| **Cache Management** | Manage local cache | `yt-tool cache` |
| **Export** | Markdown/JSON/Notion/Obsidian | `yt-tool analyze` |

### Content Generation

| Feature | Description | Command |
|---------|-------------|---------|
| **Flashcards** | Generate Anki-style flashcards | `yt-tool flashcards` |
| **Blog Post** | Convert video to blog article | `yt-tool blog` |
| **Vocabulary** | Extract terminology | `yt-tool vocabulary` |
| **Podcast Script** | Generate podcast script | `yt-tool podcast` |
| **Full Report** | Comprehensive analysis report | `yt-tool report` |

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/Yt-tool.git
cd Yt-tool
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install the package

```bash
pip install -e .
```

### 5. Configure API keys

```bash
cp .env.example .env
```

Edit `.env`:

```env
OPENAI_API_KEY=your_openai_api_key_here
# or
ANTHROPIC_API_KEY=your_anthropic_api_key_here

AI_PROVIDER=openai
```

## Usage

### Basic Commands

```bash
# Get video info
yt-tool info "VIDEO_URL"

# Extract transcript
yt-tool transcript "VIDEO_URL"
yt-tool transcript "VIDEO_URL" --no-timestamps -o transcript.txt

# Generate summary (with style options)
yt-tool summary "VIDEO_URL"
yt-tool summary "VIDEO_URL" --style brief      # Short summary
yt-tool summary "VIDEO_URL" --style detailed   # In-depth notes
yt-tool summary "VIDEO_URL" --style bullets    # Bullet points
yt-tool summary "VIDEO_URL" --style academic   # Academic style
yt-tool summary "VIDEO_URL" --style casual     # Casual style
yt-tool summary "VIDEO_URL" --style twitter    # Social media

# List available summary styles
yt-tool styles

# Extract key points
yt-tool keypoints "VIDEO_URL"

# Generate chapters
yt-tool chapters "VIDEO_URL"

# Translate subtitles
yt-tool translate "VIDEO_URL" -t English
yt-tool translate "VIDEO_URL" -t 日本語

# Interactive Q&A
yt-tool qa "VIDEO_URL"

# Search keywords
yt-tool search "VIDEO_URL" "keyword"
```

### Download Commands

```bash
# Download video
yt-tool video "VIDEO_URL" -q 1080
yt-tool video "VIDEO_URL" -q 720

# Download audio
yt-tool audio "VIDEO_URL" -f mp3 -q 320
yt-tool audio "VIDEO_URL" -f m4a -q 256

# Download thumbnail
yt-tool thumbnail "VIDEO_URL"

# Download subtitles
yt-tool subtitle "VIDEO_URL" -f srt
yt-tool subtitle "VIDEO_URL" -f vtt
```

### Content Generation

```bash
# Generate flashcards
yt-tool flashcards "VIDEO_URL"
yt-tool flashcards "VIDEO_URL" -f anki -o cards.txt

# Generate blog post
yt-tool blog "VIDEO_URL" -o article.md

# Extract vocabulary
yt-tool vocabulary "VIDEO_URL"

# Generate podcast script
yt-tool podcast "VIDEO_URL"

# Generate comprehensive report (includes everything!)
yt-tool report "VIDEO_URL"
yt-tool report "VIDEO_URL" --no-flashcards --no-vocabulary
```

### Analysis Commands

```bash
# Generate mind map
yt-tool mindmap "VIDEO_URL"
yt-tool mindmap "VIDEO_URL" -f mermaid

# Analyze comments
yt-tool comments "VIDEO_URL" -n 100

# Full analysis (summary + keypoints + chapters)
yt-tool analyze "VIDEO_URL"
yt-tool analyze "VIDEO_URL" --all -f notion

# Batch processing
yt-tool batch "URL1" "URL2" "URL3"
yt-tool batch -f urls.txt
yt-tool batch -p "PLAYLIST_URL"

# Cache management
yt-tool cache --stats
yt-tool cache --clear
```

## Summary Styles

| Style | Name | Description |
|-------|------|-------------|
| `default` | 标准摘要 | Balanced summary for general use |
| `brief` | 简短摘要 | One paragraph, quick overview |
| `detailed` | 详细摘要 | In-depth learning notes |
| `bullets` | 要点列表 | Bullet point format |
| `academic` | 学术风格 | Academic/research style |
| `casual` | 口语化 | Casual conversational |
| `twitter` | 推文风格 | Social media ready |

## All Commands

| Command | Description |
|---------|-------------|
| `transcript` | Extract video transcript |
| `summary` | Generate AI summary |
| `keypoints` | Extract key points |
| `chapters` | Generate chapter timestamps |
| `translate` | Translate subtitles |
| `qa` | Interactive Q&A |
| `search` | Search in transcript |
| `info` | Get video info |
| `mindmap` | Generate mind map |
| `subtitle` | Download subtitles (SRT/VTT) |
| `audio` | Download audio (MP3/M4A) |
| `video` | Download video (MP4) |
| `thumbnail` | Download thumbnail |
| `comments` | Analyze comments |
| `flashcards` | Generate flashcards |
| `blog` | Generate blog post |
| `vocabulary` | Extract vocabulary |
| `podcast` | Generate podcast script |
| `report` | Generate full report |
| `analyze` | Full video analysis |
| `batch` | Batch process videos |
| `cache` | Manage cache |
| `styles` | List summary styles |

## Python API

```python
from yt_tool.extractor import TranscriptExtractor
from yt_tool.summarizer import Summarizer
from yt_tool.timestamp import TimestampGenerator
from yt_tool.translator import Translator
from yt_tool.qa import VideoQA
from yt_tool.search import TranscriptSearch
from yt_tool.mindmap import MindmapGenerator
from yt_tool.video_info import VideoInfo
from yt_tool.comments import CommentsAnalyzer
from yt_tool.subtitle import SubtitleExporter
from yt_tool.downloader import Downloader
from yt_tool.generator import ContentGenerator
from yt_tool.report import ReportGenerator
from yt_tool.exporter import Exporter

# Get video info
video = VideoInfo("VIDEO_ID")
video.fetch()
print(video.title, video.duration_formatted)

# Extract transcript
extractor = TranscriptExtractor("VIDEO_ID")
extractor.extract()
transcript = extractor.get_plain_text()

# Generate summary with style
summarizer = Summarizer()
summary = summarizer.summarize(transcript, language="中文", style="detailed")

# Generate flashcards
content_gen = ContentGenerator()
cards = content_gen.generate_flashcards(transcript, language="中文")
anki_format = content_gen.export_flashcards_anki(cards)

# Generate blog post
blog_post = content_gen.generate_blog_post(transcript, language="中文")

# Extract vocabulary
vocabulary = content_gen.extract_vocabulary(transcript, language="中文")

# Generate comprehensive report
report_gen = ReportGenerator(output_dir="output")
result = report_gen.generate_full_report(
    "VIDEO_ID",
    language="中文",
    include_flashcards=True,
    include_mindmap=True,
)
print(result["report_path"])

# Download video/audio
downloader = Downloader("output")
downloader.download_video("VIDEO_ID", quality="1080")
downloader.download_audio("VIDEO_ID", format="mp3", quality="320")
downloader.download_thumbnail("VIDEO_ID")
```

## Supported Languages

- Chinese (中文) - default
- English
- Japanese (日本語)
- Korean (한국어)
- Spanish (Español)
- French (Français)
- German (Deutsch)
- Russian (Русский)
- Portuguese (Português)
- Italian (Italiano)
- And more...

## Export Formats

- **Markdown** - Standard markdown
- **JSON** - Structured data
- **Notion** - Notion-compatible format
- **Obsidian** - Obsidian-compatible format
- **SRT** - SubRip subtitle format
- **VTT** - WebVTT subtitle format
- **Mermaid** - Mind map diagram
- **Anki** - Flashcard import format

## Requirements

- Python 3.9+
- OpenAI API key or Anthropic API key
- FFmpeg (for audio/video download)

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
