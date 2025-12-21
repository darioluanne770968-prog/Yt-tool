"""
Learning Analytics - Deep analytics on learning patterns and efficiency
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from collections import defaultdict
from .ai_client import get_ai_client


class LearningAnalytics:
    """Advanced learning analytics and insights"""

    def __init__(self, data_dir: str = ".yt_tool_data"):
        self.client = get_ai_client()
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.analytics_file = self.data_dir / "learning_analytics.json"
        self.data = self._load_data()

    def _load_data(self) -> dict:
        if self.analytics_file.exists():
            return json.loads(self.analytics_file.read_text(encoding="utf-8"))
        return {
            "sessions": [],
            "topics": {},
            "skills": {},
            "daily_stats": {},
            "hourly_patterns": defaultdict(int),
            "weekly_patterns": defaultdict(int)
        }

    def _save_data(self):
        self.analytics_file.write_text(
            json.dumps(self.data, ensure_ascii=False, indent=2, default=str),
            encoding="utf-8"
        )

    def log_session(self, video_id: str, topic: str, duration_minutes: int, completion_rate: float, quiz_score: Optional[float] = None):
        """Log a learning session"""
        now = datetime.now()

        session = {
            "video_id": video_id,
            "topic": topic,
            "duration_minutes": duration_minutes,
            "completion_rate": completion_rate,
            "quiz_score": quiz_score,
            "timestamp": now.isoformat(),
            "hour": now.hour,
            "weekday": now.weekday(),
            "date": now.strftime("%Y-%m-%d")
        }

        self.data["sessions"].append(session)

        # Update patterns
        self.data["hourly_patterns"][str(now.hour)] = self.data.get("hourly_patterns", {}).get(str(now.hour), 0) + duration_minutes
        self.data["weekly_patterns"][str(now.weekday())] = self.data.get("weekly_patterns", {}).get(str(now.weekday()), 0) + duration_minutes

        # Update daily stats
        date_str = now.strftime("%Y-%m-%d")
        if date_str not in self.data["daily_stats"]:
            self.data["daily_stats"][date_str] = {"duration": 0, "sessions": 0, "topics": []}
        self.data["daily_stats"][date_str]["duration"] += duration_minutes
        self.data["daily_stats"][date_str]["sessions"] += 1
        if topic not in self.data["daily_stats"][date_str]["topics"]:
            self.data["daily_stats"][date_str]["topics"].append(topic)

        # Update topic stats
        if topic not in self.data["topics"]:
            self.data["topics"][topic] = {"total_time": 0, "sessions": 0, "scores": []}
        self.data["topics"][topic]["total_time"] += duration_minutes
        self.data["topics"][topic]["sessions"] += 1
        if quiz_score is not None:
            self.data["topics"][topic]["scores"].append(quiz_score)

        self._save_data()

        return session

    def get_best_learning_time(self) -> dict:
        """Analyze and find the best time for learning"""
        hourly = self.data.get("hourly_patterns", {})
        weekly = self.data.get("weekly_patterns", {})

        # Find peak hours
        if hourly:
            sorted_hours = sorted(hourly.items(), key=lambda x: x[1], reverse=True)
            peak_hours = sorted_hours[:3] if len(sorted_hours) >= 3 else sorted_hours
        else:
            peak_hours = []

        # Find peak days
        weekday_names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        if weekly:
            sorted_days = sorted(weekly.items(), key=lambda x: x[1], reverse=True)
            peak_days = [(weekday_names[int(d)], m) for d, m in sorted_days[:3]]
        else:
            peak_days = []

        return {
            "peak_hours": [{"hour": int(h), "minutes": m} for h, m in peak_hours],
            "peak_days": [{"day": d, "minutes": m} for d, m in peak_days],
            "recommendation": self._generate_time_recommendation(peak_hours, peak_days)
        }

    def _generate_time_recommendation(self, peak_hours: List, peak_days: List) -> str:
        """Generate time recommendation"""
        if not peak_hours:
            return "暂无足够数据，建议持续记录学习时间"

        hour = int(peak_hours[0][0]) if peak_hours else 9
        period = "上午" if 5 <= hour < 12 else "下午" if 12 <= hour < 18 else "晚上"

        return f"根据您的学习模式，{period}{hour}点左右是您学习效率最高的时段"

    def analyze_attention_patterns(self, session_data: List[Dict] = None) -> dict:
        """Analyze attention patterns during learning"""
        sessions = session_data or self.data.get("sessions", [])

        if not sessions:
            return {"message": "暂无学习数据"}

        # Analyze completion rates by duration
        duration_completion = defaultdict(list)
        for s in sessions:
            duration_bucket = s.get("duration_minutes", 0) // 15 * 15  # 15-minute buckets
            duration_completion[duration_bucket].append(s.get("completion_rate", 0))

        avg_by_duration = {
            k: sum(v) / len(v) for k, v in duration_completion.items()
        }

        # Find optimal session length
        optimal_duration = max(avg_by_duration.items(), key=lambda x: x[1])[0] if avg_by_duration else 30

        # Analyze by time of day
        hour_completion = defaultdict(list)
        for s in sessions:
            hour_completion[s.get("hour", 12)].append(s.get("completion_rate", 0))

        avg_by_hour = {
            k: sum(v) / len(v) for k, v in hour_completion.items()
        }

        return {
            "optimal_session_length": optimal_duration,
            "completion_by_duration": avg_by_duration,
            "completion_by_hour": avg_by_hour,
            "insights": [
                f"最佳学习时长约{optimal_duration}分钟",
                f"共分析{len(sessions)}个学习session"
            ]
        }

    def build_skill_radar(self, language: str = "中文") -> dict:
        """Build a skill radar chart data"""
        topics = self.data.get("topics", {})

        if not topics:
            return {"skills": [], "message": "暂无技能数据"}

        skill_data = []
        for topic, data in topics.items():
            avg_score = sum(data.get("scores", [0])) / len(data["scores"]) if data.get("scores") else 0
            skill_data.append({
                "skill": topic,
                "proficiency": min(100, avg_score * 100),
                "time_invested": data.get("total_time", 0),
                "sessions": data.get("sessions", 0)
            })

        # Sort by proficiency
        skill_data.sort(key=lambda x: x["proficiency"], reverse=True)

        return {
            "skills": skill_data[:10],  # Top 10 skills
            "total_topics": len(topics),
            "chart_type": "radar"
        }

    def calculate_learning_roi(self, topic: str = None, language: str = "中文") -> dict:
        """Calculate learning return on investment"""
        if topic:
            topic_data = self.data.get("topics", {}).get(topic, {})
            time_invested = topic_data.get("total_time", 0)
            scores = topic_data.get("scores", [])
            avg_score = sum(scores) / len(scores) if scores else 0
        else:
            total_time = sum(t.get("total_time", 0) for t in self.data.get("topics", {}).values())
            all_scores = []
            for t in self.data.get("topics", {}).values():
                all_scores.extend(t.get("scores", []))
            avg_score = sum(all_scores) / len(all_scores) if all_scores else 0
            time_invested = total_time

        # ROI calculation (simplified)
        if time_invested > 0:
            roi_score = (avg_score * 100) / (time_invested / 60)  # Score per hour
        else:
            roi_score = 0

        return {
            "topic": topic or "总体",
            "time_invested_minutes": time_invested,
            "time_invested_hours": round(time_invested / 60, 1),
            "average_score": round(avg_score * 100, 1),
            "roi_score": round(roi_score, 2),
            "interpretation": self._interpret_roi(roi_score)
        }

    def _interpret_roi(self, roi: float) -> str:
        if roi > 80:
            return "极高效率！您的学习投入产出比非常出色"
        elif roi > 60:
            return "高效学习！您能够很好地利用学习时间"
        elif roi > 40:
            return "中等效率，还有提升空间"
        elif roi > 20:
            return "效率偏低，建议调整学习方法"
        else:
            return "需要改进学习策略，考虑更主动的学习方式"

    def compare_periods(self, period1_start: str, period1_end: str, period2_start: str, period2_end: str) -> dict:
        """Compare learning performance between two periods"""
        def get_period_stats(start: str, end: str) -> dict:
            sessions = [
                s for s in self.data.get("sessions", [])
                if start <= s.get("date", "") <= end
            ]

            if not sessions:
                return {"sessions": 0, "total_time": 0, "avg_completion": 0, "avg_score": 0}

            total_time = sum(s.get("duration_minutes", 0) for s in sessions)
            avg_completion = sum(s.get("completion_rate", 0) for s in sessions) / len(sessions)
            scores = [s.get("quiz_score") for s in sessions if s.get("quiz_score") is not None]
            avg_score = sum(scores) / len(scores) if scores else 0

            return {
                "sessions": len(sessions),
                "total_time": total_time,
                "avg_completion": round(avg_completion, 2),
                "avg_score": round(avg_score, 2)
            }

        period1_stats = get_period_stats(period1_start, period1_end)
        period2_stats = get_period_stats(period2_start, period2_end)

        return {
            "period1": {
                "range": f"{period1_start} ~ {period1_end}",
                "stats": period1_stats
            },
            "period2": {
                "range": f"{period2_start} ~ {period2_end}",
                "stats": period2_stats
            },
            "comparison": {
                "sessions_change": period2_stats["sessions"] - period1_stats["sessions"],
                "time_change": period2_stats["total_time"] - period1_stats["total_time"],
                "completion_change": period2_stats["avg_completion"] - period1_stats["avg_completion"],
                "score_change": period2_stats["avg_score"] - period1_stats["avg_score"]
            }
        }

    def get_learning_trends(self, days: int = 30) -> dict:
        """Get learning trends over time"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        daily_data = []
        current = start_date

        while current <= end_date:
            date_str = current.strftime("%Y-%m-%d")
            day_stats = self.data.get("daily_stats", {}).get(date_str, {})
            daily_data.append({
                "date": date_str,
                "duration": day_stats.get("duration", 0),
                "sessions": day_stats.get("sessions", 0),
                "topics": len(day_stats.get("topics", []))
            })
            current += timedelta(days=1)

        # Calculate trends
        if len(daily_data) >= 7:
            first_week = sum(d["duration"] for d in daily_data[:7])
            last_week = sum(d["duration"] for d in daily_data[-7:])
            trend = "上升" if last_week > first_week else "下降" if last_week < first_week else "稳定"
        else:
            trend = "数据不足"

        return {
            "daily_data": daily_data,
            "trend": trend,
            "total_days": days,
            "active_days": len([d for d in daily_data if d["duration"] > 0]),
            "total_time": sum(d["duration"] for d in daily_data)
        }

    def generate_analytics_report(self, language: str = "中文") -> dict:
        """Generate comprehensive analytics report"""
        stats = {
            "total_sessions": len(self.data.get("sessions", [])),
            "total_topics": len(self.data.get("topics", {})),
            "total_time": sum(t.get("total_time", 0) for t in self.data.get("topics", {}).values())
        }

        prompt = f"""基于以下学习数据生成分析报告：

统计数据：
- 总学习session数：{stats['total_sessions']}
- 涉及主题数：{stats['total_topics']}
- 总学习时间：{stats['total_time']}分钟

请用{language}生成：
1. 学习概况总结
2. 学习模式分析
3. 强项与弱项
4. 效率评估
5. 个性化建议
6. 下一步目标

语气要数据驱动、专业但易懂。"""

        report = self.client.generate(prompt)

        return {
            "statistics": stats,
            "report": report,
            "generated_at": datetime.now().isoformat()
        }

    def export_data(self, format_type: str = "json") -> str:
        """Export analytics data"""
        if format_type == "json":
            return json.dumps(self.data, ensure_ascii=False, indent=2, default=str)
        elif format_type == "csv":
            # Export sessions as CSV
            lines = ["date,topic,duration,completion_rate,quiz_score"]
            for s in self.data.get("sessions", []):
                lines.append(f"{s.get('date','')},{s.get('topic','')},{s.get('duration_minutes',0)},{s.get('completion_rate',0)},{s.get('quiz_score','')}")
            return "\n".join(lines)
        else:
            return json.dumps(self.data, ensure_ascii=False, indent=2, default=str)
