"""
Quiz generation from video content
"""

from typing import List, Dict, Optional
from .ai_client import get_ai_client


class QuizGenerator:
    """Generate quizzes from video transcripts"""

    def __init__(self):
        self.ai_client = get_ai_client()

    def generate_quiz(
        self,
        transcript: str,
        num_questions: int = 10,
        question_types: List[str] = None,
        difficulty: str = "medium",
        language: str = "中文",
    ) -> Dict:
        """
        Generate a quiz from video transcript

        Args:
            transcript: Video transcript text
            num_questions: Number of questions to generate
            question_types: Types of questions (multiple_choice, true_false, fill_blank, short_answer)
            difficulty: easy, medium, hard
            language: Output language

        Returns:
            Quiz data with questions and answers
        """
        if question_types is None:
            question_types = ["multiple_choice", "true_false", "fill_blank"]

        types_str = ", ".join(question_types)

        system_prompt = f"""You are an expert quiz creator. Generate educational quizzes that test understanding of video content.
Output in {language}. Create questions at {difficulty} difficulty level."""

        prompt = f"""Based on the following video transcript, create a quiz with {num_questions} questions.

Question types to include: {types_str}

For each question, provide:
1. Question text
2. Question type
3. Options (for multiple choice)
4. Correct answer
5. Explanation of why this is correct

Format the output as follows:

## Quiz

### Question 1
**Type:** [question_type]
**Question:** [question text]
**Options:** (if multiple choice)
A) [option]
B) [option]
C) [option]
D) [option]
**Answer:** [correct answer]
**Explanation:** [why this is correct]

---

Transcript:
{transcript[:12000]}
"""

        response = self.ai_client.chat(prompt, system_prompt, max_tokens=4096)

        return {
            "quiz": response,
            "num_questions": num_questions,
            "difficulty": difficulty,
            "question_types": question_types,
        }

    def generate_multiple_choice(
        self,
        transcript: str,
        num_questions: int = 5,
        language: str = "中文",
    ) -> str:
        """Generate multiple choice questions only"""
        return self.generate_quiz(
            transcript,
            num_questions,
            question_types=["multiple_choice"],
            language=language,
        )["quiz"]

    def generate_true_false(
        self,
        transcript: str,
        num_questions: int = 5,
        language: str = "中文",
    ) -> str:
        """Generate true/false questions only"""
        return self.generate_quiz(
            transcript,
            num_questions,
            question_types=["true_false"],
            language=language,
        )["quiz"]

    def generate_fill_blank(
        self,
        transcript: str,
        num_questions: int = 5,
        language: str = "中文",
    ) -> str:
        """Generate fill-in-the-blank questions only"""
        return self.generate_quiz(
            transcript,
            num_questions,
            question_types=["fill_blank"],
            language=language,
        )["quiz"]

    def export_anki(self, quiz_data: Dict) -> str:
        """Export quiz to Anki-compatible format"""
        system_prompt = "Convert the quiz to Anki flashcard format with question on front and answer on back."

        prompt = f"""Convert this quiz to Anki format (tab-separated: front<tab>back):

{quiz_data['quiz']}

Output only the tab-separated lines, one card per line."""

        return self.ai_client.chat(prompt, system_prompt, max_tokens=2048)
