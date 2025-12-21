"""
Knowledge Predictor - Predict learning time and knowledge decay
"""

import json
import math
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from .ai_client import get_ai_client


class KnowledgePredictor:
    """Predict learning outcomes and knowledge retention"""

    def __init__(self, data_dir: str = ".yt_tool_data"):
        self.client = get_ai_client()
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.predictions_file = self.data_dir / "knowledge_predictions.json"
        self.data = self._load_data()

    def _load_data(self) -> dict:
        if self.predictions_file.exists():
            return json.loads(self.predictions_file.read_text(encoding="utf-8"))
        return {
            "learning_history": [],
            "predictions": [],
            "retention_data": []
        }

    def _save_data(self):
        self.predictions_file.write_text(
            json.dumps(self.data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def predict_learning_time(self, transcript: str, learner_level: str = "intermediate", language: str = "中文") -> dict:
        """Predict time needed to learn the content"""
        word_count = len(transcript.split())

        prompt = f"""预测学习以下内容所需的时间：

内容概述（{word_count}字）：
{transcript[:4000]}

学习者水平：{learner_level}

请用{language}分析并预测：

1. **内容复杂度评估**
   - 概念密度（1-10）
   - 技术难度（1-10）
   - 前置知识要求

2. **时间预测**
   - 首次学习时间
   - 深度理解时间
   - 练习巩固时间
   - 总计建议时间

3. **学习阶段分解**
   - 预习阶段：X分钟
   - 学习阶段：X分钟
   - 复习阶段：X分钟
   - 练习阶段：X分钟

4. **效率建议**
   - 最佳学习时段
   - 推荐学习节奏
   - 休息安排

5. **个性化调整**
   - 针对{learner_level}水平的调整
   - 加速学习建议
   - 难点突破策略

输出具体的时间预测和学习建议。"""

        response = self.client.generate(prompt)

        prediction = {
            "content_length": word_count,
            "learner_level": learner_level,
            "prediction": response,
            "timestamp": datetime.now().isoformat()
        }

        self.data["predictions"].append(prediction)
        self._save_data()

        return prediction

    def calculate_forgetting_curve(self, topic: str, initial_strength: float = 1.0, days: int = 30) -> dict:
        """Calculate forgetting curve based on Ebbinghaus model"""
        # Ebbinghaus forgetting curve: R = e^(-t/S)
        # R = retention, t = time, S = stability

        stability = 1.5  # Base stability factor

        curve_data = []
        for day in range(days + 1):
            retention = initial_strength * math.exp(-day / stability)
            curve_data.append({
                "day": day,
                "retention": round(retention * 100, 1),
                "review_needed": retention < 0.5
            })

        # Calculate optimal review times
        review_times = []
        review_day = 1
        while review_day <= days:
            review_times.append(review_day)
            review_day = int(review_day * 2.5)  # Spaced intervals

        return {
            "topic": topic,
            "initial_strength": initial_strength,
            "curve": curve_data,
            "optimal_review_days": review_times,
            "retention_after_30_days": curve_data[-1]["retention"] if curve_data else 0
        }

    def predict_mastery_time(self, skills: List[str], current_levels: Dict[str, float], target_level: float = 0.9, language: str = "中文") -> dict:
        """Predict time to reach mastery for multiple skills"""
        skills_text = "\n".join([
            f"- {skill}: 当前{current_levels.get(skill, 0)*100:.0f}%，目标{target_level*100:.0f}%"
            for skill in skills
        ])

        prompt = f"""预测达到目标掌握度所需时间：

技能状态：
{skills_text}

请用{language}分析：

1. **每项技能的预测**
   - 技能名称
   - 当前水平
   - 目标水平
   - 预计所需时间
   - 每日建议学习时长

2. **总体规划**
   - 并行学习建议
   - 优先级排序
   - 总预计时间

3. **里程碑设置**
   - 第1周目标
   - 第2周目标
   - 第1月目标

4. **加速建议**
   - 如何缩短学习时间
   - 高效学习策略

输出详细的时间预测和规划。"""

        response = self.client.generate(prompt)

        return {
            "skills": skills,
            "current_levels": current_levels,
            "target_level": target_level,
            "prediction": response,
            "timestamp": datetime.now().isoformat()
        }

    def estimate_review_schedule(self, topics: List[str], learned_dates: Dict[str, str], language: str = "中文") -> dict:
        """Estimate optimal review schedule based on learning dates"""
        schedule = []
        today = datetime.now()

        for topic in topics:
            learned_str = learned_dates.get(topic, today.isoformat())
            try:
                learned_date = datetime.fromisoformat(learned_str.replace('Z', '+00:00').split('+')[0])
            except:
                learned_date = today

            days_since = (today - learned_date).days

            # Spaced repetition intervals: 1, 3, 7, 14, 30, 60 days
            intervals = [1, 3, 7, 14, 30, 60]
            next_review = None

            for interval in intervals:
                if days_since < interval:
                    next_review = learned_date + timedelta(days=interval)
                    break

            if next_review is None:
                next_review = today + timedelta(days=1)

            schedule.append({
                "topic": topic,
                "learned_date": learned_str,
                "days_since_learning": days_since,
                "next_review_date": next_review.strftime("%Y-%m-%d"),
                "urgency": "high" if days_since > 7 else "medium" if days_since > 3 else "low"
            })

        # Sort by urgency
        schedule.sort(key=lambda x: {"high": 0, "medium": 1, "low": 2}[x["urgency"]])

        return {
            "schedule": schedule,
            "today": today.strftime("%Y-%m-%d"),
            "topics_needing_review": len([s for s in schedule if s["urgency"] in ["high", "medium"]])
        }

    def predict_skill_decay(self, skill: str, last_practice: str, practice_frequency: str = "weekly", language: str = "中文") -> dict:
        """Predict skill decay based on practice patterns"""
        prompt = f"""预测技能衰退情况：

技能：{skill}
上次练习：{last_practice}
练习频率：{practice_frequency}

请用{language}分析：

1. **衰退预测**
   - 当前预估技能保持率
   - 1周后预估保持率
   - 1月后预估保持率
   - 3月后预估保持率

2. **关键衰退点**
   - 快速衰退期
   - 平稳期
   - 需要重新学习的临界点

3. **维护建议**
   - 最低练习频率
   - 推荐练习内容
   - 快速恢复方法

4. **风险提示**
   - 当前衰退风险
   - 需要立即行动的情况"""

        response = self.client.generate(prompt)

        return {
            "skill": skill,
            "last_practice": last_practice,
            "practice_frequency": practice_frequency,
            "prediction": response
        }

    def generate_learning_forecast(self, goals: List[str], daily_hours: float = 1.0, language: str = "中文") -> dict:
        """Generate a learning forecast for achieving goals"""
        goals_text = "\n".join([f"- {g}" for g in goals])

        prompt = f"""生成学习预测报告：

学习目标：
{goals_text}

每日可用学习时间：{daily_hours}小时

请用{language}预测：

1. **目标达成时间表**
   - 每个目标的预计完成时间
   - 整体完成时间

2. **周进度预测**
   - 第1周预期进度
   - 第2周预期进度
   - 第1月预期进度

3. **关键里程碑**
   - 重要节点
   - 预期成就

4. **风险因素**
   - 可能的延迟因素
   - 应对策略

5. **优化建议**
   - 如何提高效率
   - 时间分配建议

6. **成功概率评估**
   - 按时完成的可能性
   - 影响因素分析"""

        response = self.client.generate(prompt)

        return {
            "goals": goals,
            "daily_hours": daily_hours,
            "forecast": response,
            "generated_at": datetime.now().isoformat()
        }

    def track_prediction_accuracy(self, prediction_id: str, actual_result: dict) -> dict:
        """Track how accurate past predictions were"""
        # Find the prediction
        for pred in self.data.get("predictions", []):
            if pred.get("timestamp") == prediction_id:
                accuracy = {
                    "prediction_id": prediction_id,
                    "predicted": pred,
                    "actual": actual_result,
                    "tracked_at": datetime.now().isoformat()
                }
                return accuracy

        return {"error": "Prediction not found"}
