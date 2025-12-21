"""
Learning Diagnosis - Analyze learning weaknesses and recommend targeted content
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from .ai_client import get_ai_client


class LearningDiagnostics:
    """Diagnose learning patterns and weaknesses"""

    def __init__(self, data_dir: str = ".yt_tool_data"):
        self.client = get_ai_client()
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.diagnostics_file = self.data_dir / "learning_diagnostics.json"
        self.data = self._load_data()

    def _load_data(self) -> dict:
        if self.diagnostics_file.exists():
            return json.loads(self.diagnostics_file.read_text(encoding="utf-8"))
        return {
            "assessments": [],
            "weaknesses": [],
            "strengths": [],
            "learning_style": None,
            "recommendations": []
        }

    def _save_data(self):
        self.diagnostics_file.write_text(
            json.dumps(self.data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def analyze_quiz_results(self, quiz_results: List[Dict], language: str = "中文") -> dict:
        """Analyze quiz results to identify weaknesses"""
        results_text = json.dumps(quiz_results, ensure_ascii=False, indent=2)

        prompt = f"""分析以下测验结果，诊断学习者的强弱项：

测验结果：
{results_text}

请用{language}提供详细诊断：

1. **整体表现**
   - 正确率分析
   - 答题模式观察

2. **知识弱点**
   - 具体薄弱领域
   - 错误类型分类
   - 概念理解偏差

3. **知识强项**
   - 掌握良好的领域
   - 展现的学习能力

4. **学习风格推测**
   - 可能的学习偏好
   - 适合的学习方法

5. **改进建议**
   - 针对性学习策略
   - 推荐的复习内容
   - 练习重点

6. **学习路径建议**
   - 短期目标
   - 中期目标
   - 长期发展

输出JSON格式的诊断报告。"""

        response = self.client.generate(prompt)

        assessment = {
            "timestamp": datetime.now().isoformat(),
            "type": "quiz_analysis",
            "results": quiz_results,
            "diagnosis": response
        }

        self.data["assessments"].append(assessment)
        self._save_data()

        return assessment

    def diagnose_from_transcript(self, transcript: str, topic: str, language: str = "中文") -> dict:
        """Diagnose potential learning challenges for a topic"""
        prompt = f"""分析以下视频内容，预测学习者可能遇到的挑战：

主题：{topic}
内容：
{transcript[:6000]}

请用{language}分析：

1. **难点预测**
   - 概念复杂度
   - 前置知识要求
   - 常见理解障碍

2. **认知负荷分析**
   - 信息密度
   - 抽象程度
   - 需要的注意力水平

3. **潜在误解**
   - 容易混淆的概念
   - 常见错误理解
   - 需要澄清的点

4. **学习建议**
   - 推荐的学习顺序
   - 需要的背景知识
   - 辅助学习资源

5. **自测问题**
   - 理解检验问题
   - 应用场景问题

输出结构化的诊断报告。"""

        response = self.client.generate(prompt)

        return {
            "topic": topic,
            "diagnosis": response,
            "timestamp": datetime.now().isoformat()
        }

    def identify_knowledge_gaps(self, topics_covered: List[str], assessment_scores: Dict[str, float], language: str = "中文") -> dict:
        """Identify knowledge gaps based on covered topics and scores"""
        topics_text = "\n".join([f"- {t}" for t in topics_covered])
        scores_text = "\n".join([f"- {k}: {v*100:.0f}%" for k, v in assessment_scores.items()])

        prompt = f"""识别学习者的知识空白：

已学习主题：
{topics_text}

评估分数：
{scores_text}

请用{language}分析：

1. **知识空白识别**
   - 未覆盖的关键主题
   - 掌握不足的领域
   - 需要加强的技能

2. **依赖关系分析**
   - 前置知识缺失
   - 影响后续学习的问题

3. **优先级排序**
   - 最急需填补的空白
   - 建议的学习顺序

4. **资源推荐**
   - 针对每个空白的学习资源
   - 练习材料建议

5. **学习计划**
   - 短期填补计划
   - 长期提升路径"""

        response = self.client.generate(prompt)

        gaps = {
            "topics_covered": topics_covered,
            "scores": assessment_scores,
            "analysis": response,
            "timestamp": datetime.now().isoformat()
        }

        self.data["weaknesses"].append(gaps)
        self._save_data()

        return gaps

    def detect_learning_style(self, interactions: List[Dict], language: str = "中文") -> dict:
        """Detect learner's preferred learning style"""
        interactions_text = json.dumps(interactions[:20], ensure_ascii=False, indent=2)

        prompt = f"""基于学习者的交互行为，分析其学习风格：

交互记录：
{interactions_text}

请用{language}分析学习风格：

1. **VARK模型分析**
   - Visual (视觉型): 倾向程度
   - Auditory (听觉型): 倾向程度
   - Read/Write (读写型): 倾向程度
   - Kinesthetic (动觉型): 倾向程度

2. **学习节奏偏好**
   - 快速浏览 vs 深入学习
   - 集中学习 vs 分散学习
   - 自主学习 vs 引导学习

3. **信息处理方式**
   - 整体思维 vs 分析思维
   - 顺序学习 vs 随机学习

4. **最佳学习策略**
   - 推荐的学习方法
   - 适合的内容形式
   - 有效的记忆技巧

5. **个性化建议**
   - 如何利用学习风格优势
   - 如何弥补弱势风格

输出JSON格式的学习风格档案。"""

        response = self.client.generate(prompt)

        style = {
            "analysis": response,
            "detected_at": datetime.now().isoformat()
        }

        self.data["learning_style"] = style
        self._save_data()

        return style

    def generate_remediation_plan(self, weaknesses: List[str], language: str = "中文") -> dict:
        """Generate a remediation plan for identified weaknesses"""
        weaknesses_text = "\n".join([f"- {w}" for w in weaknesses])

        prompt = f"""为以下学习薄弱点制定补救计划：

薄弱点：
{weaknesses_text}

请用{language}制定详细计划：

1. **优先级排序**
   - 按重要性排序
   - 按紧迫性排序

2. **每个薄弱点的补救方案**
   - 具体学习目标
   - 学习资源
   - 练习计划
   - 预期时间

3. **整体学习路径**
   - 第1周计划
   - 第2周计划
   - 第3周计划
   - 第4周计划

4. **检测方法**
   - 如何验证改进
   - 自测标准

5. **激励机制**
   - 里程碑奖励
   - 进度追踪方法"""

        response = self.client.generate(prompt)

        plan = {
            "weaknesses": weaknesses,
            "remediation_plan": response,
            "created_at": datetime.now().isoformat()
        }

        self.data["recommendations"].append(plan)
        self._save_data()

        return plan

    def track_improvement(self, topic: str, before_score: float, after_score: float, language: str = "中文") -> dict:
        """Track improvement in a specific topic"""
        improvement = after_score - before_score
        improvement_pct = (improvement / before_score * 100) if before_score > 0 else 0

        prompt = f"""分析学习改进情况：

主题：{topic}
之前分数：{before_score*100:.0f}%
之后分数：{after_score*100:.0f}%
提升：{improvement_pct:.1f}%

请用{language}提供：
1. 进步评估
2. 成功因素分析
3. 继续改进的建议
4. 鼓励话语"""

        response = self.client.generate(prompt)

        return {
            "topic": topic,
            "before_score": before_score,
            "after_score": after_score,
            "improvement_percentage": improvement_pct,
            "analysis": response
        }

    def get_comprehensive_report(self, language: str = "中文") -> dict:
        """Generate a comprehensive learning diagnosis report"""
        prompt = f"""基于以下学习数据生成综合诊断报告：

评估历史：{len(self.data.get('assessments', []))} 次
识别的薄弱点：{len(self.data.get('weaknesses', []))} 个
学习风格：{self.data.get('learning_style', '未检测')}

请用{language}生成：
1. 学习者画像
2. 强弱项总结
3. 学习趋势
4. 综合建议
5. 下一步行动"""

        response = self.client.generate(prompt)

        return {
            "report": response,
            "data_summary": {
                "assessments_count": len(self.data.get("assessments", [])),
                "weaknesses_count": len(self.data.get("weaknesses", [])),
                "has_learning_style": self.data.get("learning_style") is not None
            },
            "generated_at": datetime.now().isoformat()
        }
