"""
AI Tutor - Adaptive AI personal tutor based on video content
AI私人教师 - 根据用户的学习水平自适应讲解视频内容
"""

from typing import Dict, List, Optional
from .ai_client import get_ai_client


# Learning levels configuration
LEARNING_LEVELS = {
    "beginner": {
        "name": "初学者",
        "description": "刚接触这个领域，需要从基础概念讲起",
        "style": "使用简单易懂的语言，多用类比和生活化的例子，避免专业术语或详细解释每个术语"
    },
    "intermediate": {
        "name": "中级",
        "description": "有一定基础，可以理解专业概念",
        "style": "可以使用专业术语，提供更深入的解释，关注概念之间的联系"
    },
    "advanced": {
        "name": "高级",
        "description": "有较好的基础，追求深度理解",
        "style": "深入探讨原理和细节，讨论边界情况和最佳实践，可以涉及高级话题"
    },
    "expert": {
        "name": "专家",
        "description": "该领域的专业人士，寻求精准和全面的信息",
        "style": "使用精确的专业语言，讨论前沿话题，关注细微差别和优化"
    }
}


class AITutor:
    """Adaptive AI personal tutor for video-based learning"""

    def __init__(self, provider: str = None):
        """
        Initialize AI tutor

        Args:
            provider: AI provider ('openai', 'anthropic', or 'gemini')
        """
        self.ai = get_ai_client(provider)
        self.video_context = ""
        self.video_title = ""
        self.learning_level = "intermediate"
        self.knowledge_gaps: List[str] = []
        self.mastered_concepts: List[str] = []
        self.learning_progress: List[Dict] = []

    def set_video_context(self, transcript: str, title: str = ""):
        """Set video context for tutoring"""
        self.video_context = transcript
        self.video_title = title

    def set_learning_level(self, level: str):
        """
        Set user's learning level

        Args:
            level: 'beginner', 'intermediate', 'advanced', or 'expert'
        """
        if level in LEARNING_LEVELS:
            self.learning_level = level

    def assess_level(self, language: str = "中文") -> Dict:
        """
        Assess user's current knowledge level through questions

        Args:
            language: Output language

        Returns:
            Assessment questions and rubric
        """
        prompt = f"""基于以下视频内容，生成3-5个评估问题来判断学习者的知识水平。

视频内容：
{self._truncate_context(self.video_context)}

请生成：
1. 一个基础问题（测试是否了解基本概念）
2. 一个中级问题（测试是否理解概念应用）
3. 一个高级问题（测试是否能深入分析）
4. 一个专家问题（测试是否了解高级技巧或边界情况）

每个问题请提供：
- 问题内容
- 期望答案要点
- 对应的知识水平

请用{language}输出，使用JSON格式。"""

        system_prompt = """你是一个专业的教育评估专家。你的任务是设计问题来准确评估学习者的知识水平。
问题应该逐级递增难度，能够区分不同水平的学习者。"""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.5
        )
        return response

    def explain_concept(
        self,
        concept: str,
        language: str = "中文",
        include_examples: bool = True,
        include_quiz: bool = False
    ) -> str:
        """
        Explain a concept based on user's level

        Args:
            concept: Concept to explain
            language: Output language
            include_examples: Include practical examples
            include_quiz: Include a quick quiz

        Returns:
            Personalized explanation
        """
        level_config = LEARNING_LEVELS[self.learning_level]

        prompt = f"""请解释视频中提到的概念：「{concept}」

视频内容参考：
{self._truncate_context(self.video_context)}

学习者水平：{level_config['name']} - {level_config['description']}
解释风格：{level_config['style']}

请提供：
1. **概念解释**：适合该水平的解释
2. **核心要点**：列出关键点
{"3. **实际例子**：提供1-2个具体例子" if include_examples else ""}
{"4. **小测验**：1-2个简单问题检验理解" if include_quiz else ""}
5. **延伸学习**：建议进一步学习的方向

请用{language}输出。"""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt=self._get_tutor_system_prompt(language),
            temperature=0.6
        )

        # Track learning progress
        self.learning_progress.append({
            "type": "concept_explained",
            "concept": concept,
            "level": self.learning_level
        })

        return response

    def answer_question(self, question: str, language: str = "中文") -> str:
        """
        Answer a question with adaptive explanation

        Args:
            question: Student's question
            language: Output language

        Returns:
            Adaptive answer
        """
        level_config = LEARNING_LEVELS[self.learning_level]

        prompt = f"""学生问题：{question}

视频内容参考：
{self._truncate_context(self.video_context)}

学习者水平：{level_config['name']}
解释风格：{level_config['style']}

请：
1. 直接回答问题
2. 解释相关概念（适合学习者水平）
3. 如果问题暴露了知识盲点，指出需要补充的知识
4. 提供一个引导性问题帮助学生深入思考

请用{language}输出。"""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt=self._get_tutor_system_prompt(language),
            temperature=0.6
        )

        return response

    def identify_knowledge_gaps(self, language: str = "中文") -> str:
        """
        Identify potential knowledge gaps based on video content

        Args:
            language: Output language

        Returns:
            Analysis of potential knowledge gaps
        """
        level_config = LEARNING_LEVELS[self.learning_level]

        prompt = f"""分析以下视频内容，识别{level_config['name']}水平的学习者可能存在的知识盲点。

视频内容：
{self._truncate_context(self.video_context)}

请提供：
1. **前置知识**：理解这个视频需要的背景知识
2. **潜在难点**：对该水平学习者可能困难的概念
3. **常见误区**：该话题常见的理解错误
4. **建议补充**：推荐先学习的内容

请用{language}输出。"""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt=self._get_tutor_system_prompt(language),
            temperature=0.5
        )

        return response

    def create_learning_path(self, language: str = "中文") -> str:
        """
        Create a personalized learning path based on video content

        Args:
            language: Output language

        Returns:
            Structured learning path
        """
        level_config = LEARNING_LEVELS[self.learning_level]

        prompt = f"""基于以下视频内容，为{level_config['name']}水平的学习者创建学习路径。

视频内容：
{self._truncate_context(self.video_context)}

请创建：
1. **学习目标**：完成学习后应该掌握什么
2. **学习步骤**：分步骤的学习计划
3. **每步要点**：每个步骤的关键学习点
4. **练习任务**：每个步骤对应的练习
5. **检查清单**：自我检查是否掌握的清单
6. **进阶方向**：学完后的进一步学习建议

请用{language}输出。"""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt=self._get_tutor_system_prompt(language),
            temperature=0.5
        )

        return response

    def generate_practice(
        self,
        topic: str = None,
        difficulty: str = None,
        count: int = 5,
        language: str = "中文"
    ) -> str:
        """
        Generate practice questions

        Args:
            topic: Specific topic (optional)
            difficulty: Override difficulty level
            count: Number of questions
            language: Output language

        Returns:
            Practice questions with answers
        """
        level = difficulty or self.learning_level
        level_config = LEARNING_LEVELS.get(level, LEARNING_LEVELS["intermediate"])

        topic_text = f"关于「{topic}」的" if topic else ""

        prompt = f"""基于视频内容，生成{count}个{topic_text}练习题。

视频内容：
{self._truncate_context(self.video_context)}

难度水平：{level_config['name']}

请生成：
1. 各种题型（选择题、填空题、简答题等）
2. 每题附带答案和解析
3. 标注每题考察的知识点

格式：
## 练习题

### 题目1：[题型]
[题目内容]

**答案**：
[答案内容]

**解析**：
[解析内容]

请用{language}输出。"""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt=self._get_tutor_system_prompt(language),
            temperature=0.7
        )

        return response

    def socratic_dialogue(self, topic: str, language: str = "中文") -> str:
        """
        Start a Socratic dialogue to guide understanding

        Args:
            topic: Topic for dialogue
            language: Output language

        Returns:
            Socratic questions to guide thinking
        """
        prompt = f"""使用苏格拉底式提问法，引导学习者深入理解「{topic}」。

视频内容参考：
{self._truncate_context(self.video_context)}

学习者水平：{LEARNING_LEVELS[self.learning_level]['name']}

请提供一系列递进的问题：
1. 起始问题：引导学习者思考基本概念
2. 追问：深入探究
3. 反例：提出挑战性的反例或边界情况
4. 应用：引导思考实际应用
5. 总结问题：帮助学习者总结理解

每个问题后提供思考提示，但不直接给出答案。

请用{language}输出。"""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt=self._get_tutor_system_prompt(language),
            temperature=0.7
        )

        return response

    def simplify_explanation(self, content: str, language: str = "中文") -> str:
        """
        Simplify complex content (ELI5 style)

        Args:
            content: Content to simplify
            language: Output language

        Returns:
            Simplified explanation
        """
        prompt = f"""请将以下内容简化解释，就像向一个10岁的孩子解释一样：

内容：
{content}

要求：
1. 使用简单的词汇
2. 用生活中的例子类比
3. 避免专业术语
4. 生动有趣

请用{language}输出。"""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt="你是一个擅长将复杂概念简单化的教育专家。",
            temperature=0.7
        )

        return response

    def get_learning_summary(self, language: str = "中文") -> str:
        """
        Get summary of learning progress

        Args:
            language: Output language

        Returns:
            Learning progress summary
        """
        if not self.learning_progress:
            return "尚无学习记录。"

        concepts = [p["concept"] for p in self.learning_progress if p["type"] == "concept_explained"]

        prompt = f"""总结学习进度：

已学习的概念：{', '.join(concepts) if concepts else '无'}
当前水平：{LEARNING_LEVELS[self.learning_level]['name']}
已掌握：{', '.join(self.mastered_concepts) if self.mastered_concepts else '待评估'}
知识盲点：{', '.join(self.knowledge_gaps) if self.knowledge_gaps else '待识别'}

请提供：
1. 学习进度概述
2. 建议的下一步
3. 需要复习的内容

请用{language}输出。"""

        response = self.ai.chat(
            prompt=prompt,
            system_prompt=self._get_tutor_system_prompt(language),
            temperature=0.5
        )

        return response

    def _get_tutor_system_prompt(self, language: str) -> str:
        """Get tutor system prompt"""
        level_config = LEARNING_LEVELS[self.learning_level]
        return f"""你是一个经验丰富的AI私人教师。你的任务是根据学生的水平，以最合适的方式教授视频中的知识。

当前学生水平：{level_config['name']}
教学风格：{level_config['style']}

教学原则：
1. 因材施教，根据学生水平调整讲解深度
2. 使用恰当的例子和类比
3. 鼓励学生思考，而不是直接给出答案
4. 及时发现并纠正误解
5. 保持耐心和友好
6. 使用{language}进行教学"""

    def _truncate_context(self, text: str, max_chars: int = 20000) -> str:
        """Truncate context if too long"""
        if len(text) <= max_chars:
            return text
        return text[:max_chars] + "\n\n[内容过长，已截断...]"

    @staticmethod
    def get_available_levels() -> Dict:
        """Get available learning levels"""
        return {
            key: {"name": val["name"], "description": val["description"]}
            for key, val in LEARNING_LEVELS.items()
        }


def create_tutor(
    transcript: str,
    title: str = "",
    level: str = "intermediate",
    provider: str = None
) -> AITutor:
    """
    Factory function to create an AI tutor instance

    Args:
        transcript: Video transcript
        title: Video title
        level: Learning level
        provider: AI provider

    Returns:
        Configured AITutor instance
    """
    tutor = AITutor(provider)
    tutor.set_video_context(transcript, title)
    tutor.set_learning_level(level)
    return tutor
