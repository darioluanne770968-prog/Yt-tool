"""
Feynman Notes Generator - 费曼笔记生成器
Generate notes using the Feynman Technique for deeper understanding
"""

import json
from typing import Dict, List, Any, Optional
from .ai_client import get_ai_client


class FeynmanNotesGenerator:
    """Generate Feynman-style notes that explain concepts simply"""

    def __init__(self):
        self.ai_client = get_ai_client()

    def generate_feynman_notes(self, transcript: str, language: str = "中文") -> Dict[str, Any]:
        """Generate complete Feynman-style notes"""
        prompt = f"""使用费曼学习法，将以下内容转换为简单易懂的笔记。

费曼学习法四步骤：
1. 选择概念
2. 用简单语言解释（像教小学生一样）
3. 识别知识缺口
4. 简化和类比

原内容：
{transcript[:8000]}

请为每个重要概念生成费曼笔记，返回JSON格式：

1. concepts: 概念数组，每个包含：
   - name: 概念名称
   - original_explanation: 原始解释
   - simple_explanation: 简单解释（用5岁小孩能懂的话）
   - analogy: 生活类比
   - key_insight: 核心洞察
   - common_misconceptions: 常见误解
   - knowledge_gaps: 可能的知识缺口
   - follow_up_questions: 深入问题

2. overall_summary: 整体简化总结
3. eli5_version: "像我5岁一样解释"版本
4. story_version: 故事化版本
5. one_sentence_each: 每个概念一句话总结

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"raw_notes": response}

    def explain_like_im_five(self, concept: str, context: str = "", language: str = "中文") -> str:
        """Explain a concept as if to a 5-year-old"""
        prompt = f"""用费曼技巧，像解释给5岁小孩一样解释以下概念。

概念：{concept}
{f"上下文：{context}" if context else ""}

要求：
1. 使用简单的日常词汇
2. 用具体的比喻和例子
3. 避免任何专业术语
4. 用短句子
5. 可以用故事形式

语言使用{language}。"""

        return self.ai_client.chat(prompt)

    def generate_analogies(self, transcript: str, num_analogies: int = 5, language: str = "中文") -> List[Dict[str, Any]]:
        """Generate everyday analogies for concepts in the content"""
        prompt = f"""为以下内容中的概念生成{num_analogies}个日常生活类比。

内容：
{transcript[:6000]}

要求：
1. 类比要贴近日常生活
2. 准确反映概念本质
3. 易于记忆

返回JSON数组，每个类比包含：
- concept: 原概念
- analogy: 类比
- explanation: 为什么这个类比有效
- limitations: 类比的局限性（类比在哪些方面不完全准确）
- visual_suggestion: 可视化建议

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return []

    def identify_jargon(self, transcript: str, language: str = "中文") -> Dict[str, Any]:
        """Identify jargon and provide simple alternatives"""
        prompt = f"""识别以下内容中的专业术语/行话，并提供简单替代。

内容：
{transcript[:6000]}

返回JSON格式：
1. jargon_list: 术语列表，每个包含：
   - term: 专业术语
   - simple_alternative: 简单替代表达
   - definition: 简单定义
   - example: 使用例子
   - necessity: 是否必须使用这个术语（yes/no/optional）

2. jargon_density: 术语密度评估（low/medium/high）
3. accessibility_score: 内容可及性评分（1-10）
4. simplified_version: 去除术语后的简化版本

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"raw_analysis": response}

    def generate_teaching_script(self, transcript: str, audience: str = "beginner", language: str = "中文") -> str:
        """Generate a script for teaching this content to others"""
        prompt = f"""将以下内容转换为适合教给{audience}的教学脚本。

原内容：
{transcript[:8000]}

费曼技巧教学脚本要求：
1. 从最基础的概念开始
2. 循序渐进建立知识
3. 使用大量类比和例子
4. 预设学生可能的疑问并解答
5. 包含互动检查点

脚本格式：
- 开场引入（吸引注意力）
- 核心概念讲解（分段）
- 类比解释
- 常见问题
- 总结回顾

语言使用{language}。"""

        return self.ai_client.chat(prompt)

    def create_knowledge_gaps_quiz(self, transcript: str, language: str = "中文") -> List[Dict[str, Any]]:
        """Create a quiz to identify knowledge gaps"""
        prompt = f"""基于以下内容，创建一套测试题来帮助学习者识别知识缺口。

内容：
{transcript[:6000]}

设计不同层次的问题：
1. 基础理解题
2. 应用题
3. 分析题
4. 类比创造题

返回JSON数组，每题包含：
- question: 问题
- level: 层次（basic/application/analysis/creative）
- correct_answer: 正确答案
- knowledge_tested: 测试的知识点
- gap_indicator: 如果答错说明什么知识缺口
- remediation: 如何填补这个缺口

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return []

    def generate_rubber_duck_dialogue(self, transcript: str, language: str = "中文") -> str:
        """Generate a rubber duck debugging style dialogue for self-explanation"""
        prompt = f"""创建一个"橡皮鸭对话"格式的自我解释脚本。

原内容：
{transcript[:6000]}

橡皮鸭对话格式：
学习者通过向一只橡皮鸭（或任何无生命物体）解释来加深理解。

生成对话，包含：
1. 学习者尝试解释
2. 发现自己解释不清的地方
3. 重新组织语言
4. 最终清晰解释

格式：
🧑 学习者：[解释尝试]
🦆 （疑惑）
🧑 学习者：等等，让我再想想...[修正解释]
🦆 （点头）
...

语言使用{language}。"""

        return self.ai_client.chat(prompt)

    def simplify_iteratively(self, concept: str, iterations: int = 3, language: str = "中文") -> List[Dict[str, str]]:
        """Iteratively simplify a concept through multiple rounds"""
        prompt = f"""对以下概念进行{iterations}轮迭代简化。

概念：{concept}

每轮简化都比上一轮更简单、更基础。

返回JSON数组，每轮包含：
- iteration: 轮次
- explanation: 解释
- target_audience: 目标受众（如：专业人士、大学生、高中生、小学生、幼儿）
- word_count: 字数
- complexity_score: 复杂度（1-10）

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return []

    def export_notes(self, notes: Dict, format: str = "markdown") -> str:
        """Export Feynman notes in various formats"""
        if format == "markdown":
            md = "# 费曼笔记\n\n"

            if "eli5_version" in notes:
                md += "## 🧒 简单版本（像我5岁一样解释）\n\n"
                md += f"{notes['eli5_version']}\n\n"

            if "concepts" in notes:
                md += "## 📚 概念详解\n\n"
                for concept in notes["concepts"]:
                    md += f"### {concept.get('name', '')}\n\n"
                    md += f"**简单解释:** {concept.get('simple_explanation', '')}\n\n"
                    md += f"**类比:** {concept.get('analogy', '')}\n\n"
                    md += f"**核心洞察:** {concept.get('key_insight', '')}\n\n"
                    if concept.get('common_misconceptions'):
                        md += f"**常见误解:** {concept.get('common_misconceptions')}\n\n"
                    md += "---\n\n"

            if "story_version" in notes:
                md += "## 📖 故事版本\n\n"
                md += f"{notes['story_version']}\n\n"

            if "one_sentence_each" in notes:
                md += "## ✨ 一句话总结\n\n"
                if isinstance(notes["one_sentence_each"], list):
                    for sentence in notes["one_sentence_each"]:
                        md += f"- {sentence}\n"
                else:
                    md += f"{notes['one_sentence_each']}\n"

            return md

        elif format == "json":
            return json.dumps(notes, ensure_ascii=False, indent=2)

        return str(notes)
