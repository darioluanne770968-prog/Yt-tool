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
            extractor.extract(language_preferences=[language])

            return jsonify({
                "success": True,
                "transcript": extractor.get_plain_text(),
                "segments": extractor.get_segments(),
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
                "info": {
                    "title": info.title,
                    "channel": info.channel,
                    "duration": info.duration_formatted,
                    "views": info.view_count,
                    "likes": info.like_count,
                    "upload_date": info.upload_date,
                    "description": info.description[:500] if info.description else None,
                }
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

    return app


def run_server(host: str = "0.0.0.0", port: int = 5000, debug: bool = False):
    """Run the API server"""
    app = create_app()
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    run_server(debug=True)
