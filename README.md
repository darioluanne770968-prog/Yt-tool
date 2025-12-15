# YouTube AI Tool

AI-powered YouTube video analysis toolkit - 智能 YouTube 视频分析工具

## Features

| Feature | Description |
|---------|-------------|
| **Transcript Extraction** | Extract subtitles/transcripts from YouTube videos |
| **AI Summary** | Generate comprehensive video summaries |
| **Key Points** | Extract highlights and important information |
| **Chapter Generation** | Auto-generate chapter timestamps |
| **Translation** | Translate subtitles to multiple languages |
| **Q&A** | Interactive question-answering based on video content |
| **Search** | Search keywords within video content |
| **Batch Processing** | Process multiple videos or playlists |
| **Export** | Export to Markdown, JSON, Notion, Obsidian formats |

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/Yt-tool.git
cd Yt-tool
```

### 2. Create virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
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

Copy the example environment file and add your API keys:

```bash
cp .env.example .env
```

Edit `.env` and add your API key:

```env
# Choose one or both
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Default provider
AI_PROVIDER=openai
```

## Usage

### Extract Transcript

```bash
# Basic usage
yt-tool transcript "https://www.youtube.com/watch?v=VIDEO_ID"

# Without timestamps
yt-tool transcript "VIDEO_ID" --no-timestamps

# Save to file
yt-tool transcript "VIDEO_ID" -o transcript.txt
```

### Generate Summary

```bash
# Generate summary in Chinese (default)
yt-tool summary "VIDEO_ID"

# Generate summary in English
yt-tool summary "VIDEO_ID" -l English

# Save to file
yt-tool summary "VIDEO_ID" -o summary.md
```

### Extract Key Points

```bash
yt-tool keypoints "VIDEO_ID"
yt-tool keypoints "VIDEO_ID" -l English -o keypoints.md
```

### Generate Chapters

```bash
yt-tool chapters "VIDEO_ID"
yt-tool chapters "VIDEO_ID" -o chapters.txt
```

### Translate Subtitles

```bash
# Translate to Chinese
yt-tool translate "VIDEO_ID" -t 中文

# Translate to Japanese
yt-tool translate "VIDEO_ID" -t 日本語

# Translate to English
yt-tool translate "VIDEO_ID" -t English
```

### Interactive Q&A

```bash
yt-tool qa "VIDEO_ID"

# The tool will suggest questions and allow interactive dialogue
```

### Search Keywords

```bash
# Search for a keyword
yt-tool search "VIDEO_ID" "machine learning"

# Output as markdown
yt-tool search "VIDEO_ID" "AI" -f markdown
```

### Full Analysis

```bash
# Run complete analysis (summary + keypoints + chapters)
yt-tool analyze "VIDEO_ID"

# Include full transcript
yt-tool analyze "VIDEO_ID" --all

# Export to different formats
yt-tool analyze "VIDEO_ID" -f notion
yt-tool analyze "VIDEO_ID" -f obsidian
yt-tool analyze "VIDEO_ID" -f json
```

### Batch Processing

```bash
# Process multiple videos
yt-tool batch "VIDEO_ID_1" "VIDEO_ID_2" "VIDEO_ID_3"

# Process from file (one URL per line)
yt-tool batch -f videos.txt

# Process entire playlist
yt-tool batch -p "PLAYLIST_URL"
```

## Python API

You can also use this as a Python library:

```python
from yt_tool.extractor import TranscriptExtractor
from yt_tool.summarizer import Summarizer
from yt_tool.timestamp import TimestampGenerator
from yt_tool.translator import Translator
from yt_tool.qa import VideoQA
from yt_tool.search import TranscriptSearch
from yt_tool.exporter import Exporter

# Extract transcript
extractor = TranscriptExtractor("VIDEO_ID")
extractor.extract()
transcript = extractor.get_plain_text()

# Generate summary
summarizer = Summarizer()
summary = summarizer.summarize(transcript, language="中文")

# Extract key points
key_points = summarizer.extract_key_points(transcript)

# Generate chapters
generator = TimestampGenerator()
chapters = generator.generate(extractor.get_formatted())

# Translate
translator = Translator()
translated = translator.translate(transcript, target_language="English")

# Q&A
qa = VideoQA(transcript)
answer = qa.ask("What is this video about?")

# Search
searcher = TranscriptSearch(extractor.get_segments(), "VIDEO_ID")
results = searcher.search("keyword")

# Export
exporter = Exporter("output")
exporter.export_markdown(
    video_id="VIDEO_ID",
    summary=summary,
    key_points=key_points,
    chapters=chapters
)
```

## Supported Languages

The tool supports multiple languages for output:

- Chinese (中文) - default
- English
- Japanese (日本語)
- Korean (한국어)
- Spanish (Español)
- French (Français)
- German (Deutsch)
- Russian (Русский)
- And more...

## Requirements

- Python 3.9+
- OpenAI API key or Anthropic API key

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
