"""
REST API server for yt-tool
"""

from typing import Optional
import json


def create_app():
    """Create Flask application"""
    try:
        from flask import Flask, request, jsonify
        from flask_cors import CORS
    except ImportError:
        raise ImportError("Flask not installed. Run: pip install flask flask-cors")

    app = Flask(__name__)
    CORS(app)

    # Import modules
    from .extractor import TranscriptExtractor
    from .summarizer import Summarizer
    from .timestamp import TimestampGenerator
    from .translator import Translator
    from .qa import VideoQA
    from .video_info import VideoInfo
    from .generator import ContentGenerator
    from .quiz import QuizGenerator
    from .study_guide import StudyGuideGenerator
    from .mindmap import MindmapGenerator
    from .concepts import ConceptExplainer
    from .sentiment import SentimentAnalyzer
    from .social import SocialMediaGenerator
    from .presentation import PresentationGenerator
    from .cornell_notes import CornellNotesGenerator
    from .feynman_notes import FeynmanNotesGenerator

    @app.route("/")
    def index():
        """API info endpoint"""
        return jsonify({
            "name": "YouTube AI Tool API",
            "version": "1.0.0",
            "endpoints": [
                "/api/transcript",
                "/api/summary",
                "/api/keypoints",
                "/api/chapters",
                "/api/translate",
                "/api/qa",
                "/api/info",
                "/api/quiz",
                "/api/flashcards",
                "/api/study-guide",
            ]
        })

    @app.route("/api/transcript", methods=["POST"])
    def get_transcript():
        """Get video transcript"""
        data = request.json
        video_id = data.get("video_id") or data.get("url")
        language = data.get("language", "zh-CN")

        if not video_id:
            return jsonify({"error": "video_id is required"}), 400

        try:
            extractor = TranscriptExtractor(video_id)
            extractor.extract(languages=[language])

            return jsonify({
                "success": True,
                "transcript": extractor.get_formatted(include_timestamps=False),
                "language": extractor.language,
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/summary", methods=["POST"])
    def get_summary():
        """Generate video summary"""
        data = request.json
        video_id = data.get("video_id") or data.get("url")
        style = data.get("style", "default")
        language = data.get("language", "中文")

        if not video_id:
            return jsonify({"error": "video_id is required"}), 400

        try:
            extractor = TranscriptExtractor(video_id)
            extractor.extract()
            transcript = extractor.get_plain_text()

            summarizer = Summarizer()
            summary = summarizer.summarize(transcript, language, style)

            return jsonify({
                "success": True,
                "summary": summary,
                "style": style,
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/keypoints", methods=["POST"])
    def get_keypoints():
        """Extract key points"""
        data = request.json
        video_id = data.get("video_id") or data.get("url")
        language = data.get("language", "中文")

        if not video_id:
            return jsonify({"error": "video_id is required"}), 400

        try:
            extractor = TranscriptExtractor(video_id)
            extractor.extract()
            transcript = extractor.get_plain_text()

            summarizer = Summarizer()
            keypoints = summarizer.extract_key_points(transcript, language)

            return jsonify({
                "success": True,
                "keypoints": keypoints,
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/chapters", methods=["POST"])
    def get_chapters():
        """Generate chapters"""
        data = request.json
        video_id = data.get("video_id") or data.get("url")
        language = data.get("language", "中文")

        if not video_id:
            return jsonify({"error": "video_id is required"}), 400

        try:
            extractor = TranscriptExtractor(video_id)
            extractor.extract()
            transcript = extractor.get_formatted()

            generator = TimestampGenerator()
            chapters = generator.generate(transcript, language)

            return jsonify({
                "success": True,
                "chapters": chapters,
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/translate", methods=["POST"])
    def translate():
        """Translate transcript"""
        data = request.json
        video_id = data.get("video_id") or data.get("url")
        target_language = data.get("target_language", "English")

        if not video_id:
            return jsonify({"error": "video_id is required"}), 400

        try:
            extractor = TranscriptExtractor(video_id)
            extractor.extract()
            transcript = extractor.get_plain_text()

            translator = Translator()
            translated = translator.translate(transcript, target_language)

            return jsonify({
                "success": True,
                "translation": translated,
                "target_language": target_language,
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/qa", methods=["POST"])
    def ask_question():
        """Answer question about video"""
        data = request.json
        video_id = data.get("video_id") or data.get("url")
        question = data.get("question")
        language = data.get("language", "中文")

        if not video_id or not question:
            return jsonify({"error": "video_id and question are required"}), 400

        try:
            extractor = TranscriptExtractor(video_id)
            extractor.extract()
            transcript = extractor.get_plain_text()

            qa = VideoQA(transcript)
            answer = qa.ask(question, language)

            return jsonify({
                "success": True,
                "question": question,
                "answer": answer,
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/info", methods=["POST"])
    def get_info():
        """Get video info"""
        data = request.json
        video_id = data.get("video_id") or data.get("url")

        if not video_id:
            return jsonify({"error": "video_id is required"}), 400

        try:
            info = VideoInfo(video_id)
            info.fetch()

            return jsonify({
                "success": True,
                "title": info.title,
                "channel": info.channel,
                "duration": info.duration_formatted,
                "views": info.view_count,
                "likes": info.like_count,
                "upload_date": info.upload_date,
                "description": info.description[:500] if info.description else None,
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/quiz", methods=["POST"])
    def generate_quiz():
        """Generate quiz from video"""
        data = request.json
        video_id = data.get("video_id") or data.get("url")
        num_questions = data.get("num_questions", 10)
        language = data.get("language", "中文")

        if not video_id:
            return jsonify({"error": "video_id is required"}), 400

        try:
            extractor = TranscriptExtractor(video_id)
            extractor.extract()
            transcript = extractor.get_plain_text()

            quiz_gen = QuizGenerator()
            quiz = quiz_gen.generate_quiz(transcript, num_questions, language=language)

            return jsonify({
                "success": True,
                "quiz": quiz["quiz"],
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/flashcards", methods=["POST"])
    def generate_flashcards():
        """Generate flashcards from video"""
        data = request.json
        video_id = data.get("video_id") or data.get("url")
        language = data.get("language", "中文")

        if not video_id:
            return jsonify({"error": "video_id is required"}), 400

        try:
            extractor = TranscriptExtractor(video_id)
            extractor.extract()
            transcript = extractor.get_plain_text()

            generator = ContentGenerator()
            flashcards = generator.generate_flashcards(transcript, language)

            return jsonify({
                "success": True,
                "flashcards": flashcards,
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/study-guide", methods=["POST"])
    def generate_study_guide():
        """Generate study guide from video"""
        data = request.json
        video_id = data.get("video_id") or data.get("url")
        language = data.get("language", "中文")

        if not video_id:
            return jsonify({"error": "video_id is required"}), 400

        try:
            extractor = TranscriptExtractor(video_id)
            extractor.extract()
            transcript = extractor.get_plain_text()

            generator = StudyGuideGenerator()
            guide = generator.generate_study_guide(transcript, language=language)

            return jsonify({
                "success": True,
                "study_guide": guide,
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/blog", methods=["POST"])
    def generate_blog():
        """Generate blog post from video"""
        data = request.json
        video_id = data.get("video_id") or data.get("url")
        language = data.get("language", "中文")

        if not video_id:
            return jsonify({"error": "video_id is required"}), 400

        try:
            extractor = TranscriptExtractor(video_id)
            extractor.extract()
            transcript = extractor.get_plain_text()

            generator = ContentGenerator()
            blog = generator.generate_blog_post(transcript, language)

            return jsonify({
                "success": True,
                "blog": blog,
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/mindmap", methods=["POST"])
    def generate_mindmap():
        """Generate mindmap from video"""
        data = request.json
        video_id = data.get("video_id") or data.get("url")
        language = data.get("language", "中文")
        format_type = data.get("format", "markdown")

        if not video_id:
            return jsonify({"error": "video_id is required"}), 400

        try:
            extractor = TranscriptExtractor(video_id)
            extractor.extract()
            transcript = extractor.get_plain_text()

            generator = MindmapGenerator()
            if format_type == "mermaid":
                mindmap = generator.generate_mermaid(transcript, language)
            else:
                mindmap = generator.generate(transcript, language)

            return jsonify({
                "success": True,
                "mindmap": mindmap,
                "format": format_type,
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/podcast", methods=["POST"])
    def generate_podcast():
        """Generate podcast script from video"""
        data = request.json
        video_id = data.get("video_id") or data.get("url")
        language = data.get("language", "中文")

        if not video_id:
            return jsonify({"error": "video_id is required"}), 400

        try:
            extractor = TranscriptExtractor(video_id)
            extractor.extract()
            transcript = extractor.get_plain_text()

            generator = ContentGenerator()
            podcast = generator.generate_podcast_script(transcript, language)

            return jsonify({
                "success": True,
                "podcast": podcast,
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/vocabulary", methods=["POST"])
    def extract_vocabulary():
        """Extract vocabulary from video"""
        data = request.json
        video_id = data.get("video_id") or data.get("url")
        language = data.get("language", "中文")

        if not video_id:
            return jsonify({"error": "video_id is required"}), 400

        try:
            extractor = TranscriptExtractor(video_id)
            extractor.extract()
            transcript = extractor.get_plain_text()

            generator = ContentGenerator()
            vocabulary = generator.extract_vocabulary(transcript, language)

            return jsonify({
                "success": True,
                "vocabulary": vocabulary,
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/concepts", methods=["POST"])
    def extract_concepts():
        """Extract and explain concepts from video"""
        data = request.json
        video_id = data.get("video_id") or data.get("url")
        language = data.get("language", "中文")

        if not video_id:
            return jsonify({"error": "video_id is required"}), 400

        try:
            extractor = TranscriptExtractor(video_id)
            extractor.extract()
            transcript = extractor.get_plain_text()

            concept_exp = ConceptExplainer()
            concepts = concept_exp.extract_concepts(transcript, language)

            return jsonify({
                "success": True,
                "concepts": concepts,
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/sentiment", methods=["POST"])
    def analyze_sentiment():
        """Analyze video sentiment"""
        data = request.json
        video_id = data.get("video_id") or data.get("url")
        language = data.get("language", "中文")

        if not video_id:
            return jsonify({"error": "video_id is required"}), 400

        try:
            extractor = TranscriptExtractor(video_id)
            extractor.extract()
            transcript = extractor.get_plain_text()

            analyzer = SentimentAnalyzer()
            sentiment = analyzer.analyze(transcript, language)

            return jsonify({
                "success": True,
                "sentiment": sentiment,
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/social", methods=["POST"])
    def generate_social():
        """Generate social media content"""
        data = request.json
        video_id = data.get("video_id") or data.get("url")
        platform = data.get("platform", "twitter")
        language = data.get("language", "中文")

        if not video_id:
            return jsonify({"error": "video_id is required"}), 400

        try:
            extractor = TranscriptExtractor(video_id)
            extractor.extract()
            transcript = extractor.get_plain_text()

            generator = SocialMediaGenerator()
            if platform == "twitter":
                content = generator.generate_twitter_thread(transcript, language)
            elif platform == "linkedin":
                content = generator.generate_linkedin_post(transcript, language)
            elif platform == "xiaohongshu":
                content = generator.generate_xiaohongshu(transcript, language)
            else:
                content = generator.generate_twitter_thread(transcript, language)

            return jsonify({
                "success": True,
                "content": content,
                "platform": platform,
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/presentation", methods=["POST"])
    def generate_presentation():
        """Generate presentation slides"""
        data = request.json
        video_id = data.get("video_id") or data.get("url")
        language = data.get("language", "中文")

        if not video_id:
            return jsonify({"error": "video_id is required"}), 400

        try:
            extractor = TranscriptExtractor(video_id)
            extractor.extract()
            transcript = extractor.get_plain_text()

            generator = PresentationGenerator()
            slides = generator.generate_marp_slides(transcript, language)

            return jsonify({
                "success": True,
                "presentation": slides,
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/cornell-notes", methods=["POST"])
    def generate_cornell_notes():
        """Generate Cornell notes"""
        data = request.json
        video_id = data.get("video_id") or data.get("url")
        language = data.get("language", "中文")

        if not video_id:
            return jsonify({"error": "video_id is required"}), 400

        try:
            extractor = TranscriptExtractor(video_id)
            extractor.extract()
            transcript = extractor.get_plain_text()

            generator = CornellNotesGenerator()
            notes = generator.generate(transcript, language)

            return jsonify({
                "success": True,
                "cornell_notes": notes,
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/feynman-notes", methods=["POST"])
    def generate_feynman_notes():
        """Generate Feynman-style notes"""
        data = request.json
        video_id = data.get("video_id") or data.get("url")
        language = data.get("language", "中文")

        if not video_id:
            return jsonify({"error": "video_id is required"}), 400

        try:
            extractor = TranscriptExtractor(video_id)
            extractor.extract()
            transcript = extractor.get_plain_text()

            generator = FeynmanNotesGenerator()
            notes = generator.generate(transcript, language)

            return jsonify({
                "success": True,
                "feynman_notes": notes,
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app


def run_server(host: str = "0.0.0.0", port: int = 5000, debug: bool = False):
    """Run the API server"""
    app = create_app()
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    run_server(debug=True)
