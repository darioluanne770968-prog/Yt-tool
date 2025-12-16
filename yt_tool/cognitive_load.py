"""
Cognitive Load Analyzer - 认知负载评估
Evaluate video comprehension difficulty and recommend optimal learning sequences
"""

import json
from typing import Dict, List, Any, Optional
from .ai_client import get_ai_client


class CognitiveLoadAnalyzer:
    """Analyze cognitive load and learning difficulty of video content"""

    def __init__(self):
        self.ai_client = get_ai_client()

    def analyze_complexity(self, transcript: str, language: str = "中文") -> Dict[str, Any]:
        """Analyze overall complexity and cognitive load"""
        prompt = f"""分析以下视频内容的认知复杂度和学习难度。

内容：
{transcript[:8000]}

请从多个维度评估，返回JSON格式：

1. **overall_difficulty** (1-10): 整体难度
2. **cognitive_load_factors**:
   - intrinsic_load: 内在负载（概念本身的复杂性，1-10）
   - extraneous_load: 外在负载（表达方式增加的难度，1-10）
   - germane_load: 相关负载（促进学习的有效负载，1-10）

3. **complexity_dimensions**:
   - vocabulary_complexity: 词汇复杂度（1-10）
   - concept_density: 概念密度（1-10）
   - abstraction_level: 抽象程度（1-10）
   - prior_knowledge_required: 先验知识要求（1-10）
   - logical_complexity: 逻辑复杂度（1-10）

4. **prerequisites**: 先决知识列表
5. **target_audience**: 适合的受众水平
6. **estimated_comprehension_time**: 预估理解时间（相对视频时长的倍数）
7. **challenging_sections**: 困难部分列表
8. **accessible_sections**: 易理解部分列表

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

    def identify_knowledge_gaps(self, transcript: str, user_level: str = "beginner", language: str = "中文") -> Dict[str, Any]:
        """Identify potential knowledge gaps for different user levels"""
        prompt = f"""针对{user_level}水平的学习者，分析以下内容可能存在的知识鸿沟。

内容：
{transcript[:8000]}

返回JSON格式：
1. assumed_knowledge: 视频假设观众已知的知识点
2. potential_gaps: 可能的知识鸿沟，每个包含：
   - concept: 概念名称
   - importance: 重要程度（1-10）
   - fill_suggestion: 如何填补
   - resource_type: 建议学习资源类型
3. bridging_content: 建议的桥接内容
4. preparation_checklist: 观看前准备清单
5. difficulty_for_level: 对该水平学习者的难度评估

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

    def generate_scaffolding(self, transcript: str, language: str = "中文") -> Dict[str, Any]:
        """Generate learning scaffolding to reduce cognitive load"""
        prompt = f"""为以下视频内容设计学习支架（scaffolding），帮助降低认知负载。

内容：
{transcript[:8000]}

返回JSON格式：
1. pre_learning:
   - warm_up_questions: 预热问题
   - key_terms_preview: 关键术语预习
   - advance_organizer: 先行组织者（概念框架）

2. during_learning:
   - chunking_points: 建议的分段点
   - pause_reflection_prompts: 暂停反思提示
   - active_recall_checkpoints: 主动回忆检查点

3. post_learning:
   - summary_framework: 总结框架
   - review_questions: 复习问题
   - application_exercises: 应用练习

4. visual_aids:
   - suggested_diagrams: 建议的图表类型
   - concept_map_outline: 概念图大纲

5. cognitive_strategies:
   - recommended_strategies: 推荐的认知策略
   - mnemonic_suggestions: 记忆术建议

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

    def recommend_learning_sequence(self, videos: List[Dict], language: str = "中文") -> Dict[str, Any]:
        """Recommend optimal learning sequence for multiple videos"""
        video_summaries = []
        for v in videos[:10]:  # Limit for prompt size
            video_summaries.append({
                "title": v.get("title", ""),
                "topics": v.get("topics", []),
                "difficulty": v.get("difficulty", 5),
                "prerequisites": v.get("prerequisites", [])
            })

        prompt = f"""为以下视频系列推荐最佳学习顺序。

视频列表：
{json.dumps(video_summaries, ensure_ascii=False, indent=2)}

请分析并返回JSON格式：
1. recommended_sequence: 推荐的学习顺序（视频标题列表）
2. sequence_rationale: 排序理由
3. groupings: 建议的分组学习
4. milestones: 学习里程碑
5. dependencies: 依赖关系图
6. parallel_options: 可以并行学习的内容
7. estimated_total_time: 预估总学习时间
8. rest_points: 建议的休息点

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

    def adaptive_difficulty_rating(self, transcript: str, user_background: str, language: str = "中文") -> Dict[str, Any]:
        """Rate difficulty adaptively based on user background"""
        prompt = f"""根据用户背景，自适应评估视频难度。

用户背景：
{user_background}

视频内容：
{transcript[:6000]}

返回JSON格式：
1. personalized_difficulty: 个性化难度评分（1-10）
2. match_score: 内容与背景匹配度（1-100%）
3. strengths: 用户的优势领域（与内容相关）
4. challenges: 可能的挑战
5. personalized_tips: 个性化学习建议
6. skip_suggestions: 可跳过的部分（基于已有知识）
7. focus_areas: 需要重点关注的部分
8. estimated_time: 个性化预估学习时间

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

    def calculate_learning_curve(self, transcript: str, language: str = "中文") -> Dict[str, Any]:
        """Calculate the learning curve profile of the content"""
        prompt = f"""分析以下内容的学习曲线特征。

内容：
{transcript[:8000]}

返回JSON格式：
1. curve_type: 学习曲线类型（linear/exponential/plateau/u-shaped/s-shaped）
2. initial_barrier: 入门门槛（1-10）
3. progression_pattern: 进阶模式描述
4. difficulty_peaks: 难度高峰点
5. consolidation_points: 巩固点（适合暂停消化的地方）
6. breakthrough_moments: 突破时刻（理解关键概念后会豁然开朗）
7. curve_visualization: ASCII简易曲线图
8. learning_phases: 学习阶段划分

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

    def simplify_content(self, transcript: str, target_level: str = "beginner", language: str = "中文") -> str:
        """Simplify content for a specific comprehension level"""
        prompt = f"""将以下内容简化为{target_level}水平可以理解的版本。

原内容：
{transcript[:8000]}

要求：
1. 用简单的语言重新解释复杂概念
2. 添加日常生活类比
3. 分解长句
4. 定义专业术语
5. 保持核心信息完整
6. 添加过渡语句帮助理解

生成简化版本，语言使用{language}。"""

        return self.ai_client.chat(prompt)

    def generate_comprehension_test(self, transcript: str, num_questions: int = 5, language: str = "中文") -> List[Dict[str, Any]]:
        """Generate comprehension test to verify understanding"""
        prompt = f"""基于以下内容，生成{num_questions}道理解测试题。

内容：
{transcript[:6000]}

要求：
- 包含不同认知层次的问题（记忆、理解、应用、分析）
- 每题标注认知层次和难度

返回JSON数组，每题包含：
- question: 问题
- type: 题型（multiple_choice/short_answer/true_false/application）
- cognitive_level: 认知层次
- difficulty: 难度（1-10）
- answer: 答案
- explanation: 解释

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

    def export_report(self, analysis: Dict, format: str = "markdown") -> str:
        """Export cognitive load analysis report"""
        if format == "markdown":
            md = "# 认知负载分析报告\n\n"

            if "overall_difficulty" in analysis:
                md += f"## 整体难度: {analysis['overall_difficulty']}/10\n\n"

            if "cognitive_load_factors" in analysis:
                clf = analysis["cognitive_load_factors"]
                md += "## 认知负载因素\n\n"
                md += f"- **内在负载:** {clf.get('intrinsic_load', 'N/A')}/10\n"
                md += f"- **外在负载:** {clf.get('extraneous_load', 'N/A')}/10\n"
                md += f"- **相关负载:** {clf.get('germane_load', 'N/A')}/10\n\n"

            if "complexity_dimensions" in analysis:
                cd = analysis["complexity_dimensions"]
                md += "## 复杂度维度\n\n"
                for dim, score in cd.items():
                    md += f"- **{dim}:** {score}/10\n"
                md += "\n"

            if "prerequisites" in analysis:
                md += "## 先决知识\n\n"
                for prereq in analysis["prerequisites"]:
                    md += f"- {prereq}\n"
                md += "\n"

            if "target_audience" in analysis:
                md += f"## 目标受众\n\n{analysis['target_audience']}\n\n"

            return md

        elif format == "json":
            return json.dumps(analysis, ensure_ascii=False, indent=2)

        return str(analysis)
