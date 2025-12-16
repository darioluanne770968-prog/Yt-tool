"""
Scheduled Reports - 定时报告生成
Generate periodic learning reports and progress summaries
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from .ai_client import get_ai_client


class ScheduledReports:
    """Generate scheduled learning reports"""

    def __init__(self, storage_path: str = ".scheduled_reports.json"):
        self.ai_client = get_ai_client()
        self.storage_path = storage_path
        self.data = self._load_data()

    def _load_data(self) -> Dict:
        """Load report data"""
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "schedules": {},
                "generated_reports": [],
                "learning_data": {
                    "videos_watched": [],
                    "topics_studied": [],
                    "time_spent": {}
                }
            }

    def _save_data(self):
        """Save data"""
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2, default=str)

    def log_video_activity(self, video_id: str, video_title: str, topics: List[str], duration: int):
        """Log video watching activity"""
        activity = {
            "video_id": video_id,
            "title": video_title,
            "topics": topics,
            "duration_minutes": duration,
            "watched_at": datetime.now().isoformat()
        }

        self.data["learning_data"]["videos_watched"].append(activity)

        # Update topics
        for topic in topics:
            if topic not in self.data["learning_data"]["topics_studied"]:
                self.data["learning_data"]["topics_studied"].append(topic)

        # Update time spent
        date_key = datetime.now().strftime("%Y-%m-%d")
        if date_key not in self.data["learning_data"]["time_spent"]:
            self.data["learning_data"]["time_spent"][date_key] = 0
        self.data["learning_data"]["time_spent"][date_key] += duration

        self._save_data()

    def create_schedule(self, name: str, frequency: str, report_type: str, delivery: Dict = None) -> Dict[str, Any]:
        """Create a report schedule"""
        schedule_id = f"sched_{datetime.now().strftime('%Y%m%d%H%M%S')}"

        schedule = {
            "id": schedule_id,
            "name": name,
            "frequency": frequency,  # daily, weekly, monthly
            "report_type": report_type,  # summary, detailed, analytics
            "delivery": delivery or {"method": "file", "path": "reports/"},
            "enabled": True,
            "last_generated": None,
            "next_generation": self._calculate_next_generation(frequency),
            "created_at": datetime.now().isoformat()
        }

        self.data["schedules"][schedule_id] = schedule
        self._save_data()
        return schedule

    def _calculate_next_generation(self, frequency: str) -> str:
        """Calculate next generation time"""
        now = datetime.now()
        if frequency == "daily":
            next_time = now + timedelta(days=1)
        elif frequency == "weekly":
            next_time = now + timedelta(weeks=1)
        elif frequency == "monthly":
            next_time = now + timedelta(days=30)
        else:
            next_time = now + timedelta(days=1)

        return next_time.replace(hour=9, minute=0, second=0).isoformat()

    def generate_daily_report(self, date: str = None, language: str = "中文") -> Dict[str, Any]:
        """Generate daily learning report"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        # Get today's activities
        today_videos = [
            v for v in self.data["learning_data"]["videos_watched"]
            if v["watched_at"].startswith(date)
        ]

        total_time = self.data["learning_data"]["time_spent"].get(date, 0)

        # Generate insights
        topics_today = []
        for v in today_videos:
            topics_today.extend(v.get("topics", []))
        topics_today = list(set(topics_today))

        report = {
            "report_type": "daily",
            "date": date,
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "videos_watched": len(today_videos),
                "total_time_minutes": total_time,
                "topics_covered": topics_today
            },
            "videos": today_videos,
            "insights": self._generate_insights(today_videos, language)
        }

        self.data["generated_reports"].append(report)
        self._save_data()

        return report

    def generate_weekly_report(self, language: str = "中文") -> Dict[str, Any]:
        """Generate weekly learning report"""
        week_ago = datetime.now() - timedelta(days=7)
        week_start = week_ago.strftime("%Y-%m-%d")

        # Get this week's activities
        week_videos = [
            v for v in self.data["learning_data"]["videos_watched"]
            if v["watched_at"] >= week_start
        ]

        # Calculate stats
        total_time = sum(
            minutes for date, minutes in self.data["learning_data"]["time_spent"].items()
            if date >= week_start
        )

        topics = []
        for v in week_videos:
            topics.extend(v.get("topics", []))
        topic_counts = {}
        for t in topics:
            topic_counts[t] = topic_counts.get(t, 0) + 1

        # Generate AI insights
        prompt = f"""分析以下一周学习数据，生成学习报告洞察。

视频观看: {len(week_videos)}个
总时长: {total_time}分钟
话题分布: {json.dumps(topic_counts, ensure_ascii=False)}

请提供：
1. 学习模式分析
2. 重点话题识别
3. 建议下周学习重点
4. 学习效率评估
5. 激励性总结

返回JSON格式，语言使用{language}。"""

        insights = self.ai_client.chat(prompt)

        try:
            json_start = insights.find('{')
            json_end = insights.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                ai_insights = json.loads(insights[json_start:json_end])
            else:
                ai_insights = {"raw": insights}
        except json.JSONDecodeError:
            ai_insights = {"raw": insights}

        report = {
            "report_type": "weekly",
            "period": f"{week_start} to {datetime.now().strftime('%Y-%m-%d')}",
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_videos": len(week_videos),
                "total_time_minutes": total_time,
                "unique_topics": len(set(topics)),
                "topic_distribution": topic_counts
            },
            "daily_breakdown": self._get_daily_breakdown(week_start),
            "top_topics": sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)[:5],
            "insights": ai_insights
        }

        self.data["generated_reports"].append(report)
        self._save_data()

        return report

    def generate_monthly_report(self, language: str = "中文") -> Dict[str, Any]:
        """Generate monthly learning report"""
        month_ago = datetime.now() - timedelta(days=30)
        month_start = month_ago.strftime("%Y-%m-%d")

        # Get month's data
        month_videos = [
            v for v in self.data["learning_data"]["videos_watched"]
            if v["watched_at"] >= month_start
        ]

        total_time = sum(
            minutes for date, minutes in self.data["learning_data"]["time_spent"].items()
            if date >= month_start
        )

        # Topic analysis
        topics = []
        for v in month_videos:
            topics.extend(v.get("topics", []))
        topic_counts = {}
        for t in topics:
            topic_counts[t] = topic_counts.get(t, 0) + 1

        # Weekly breakdown
        weeks = []
        for i in range(4):
            week_end = datetime.now() - timedelta(days=i*7)
            week_start = week_end - timedelta(days=7)
            week_videos_count = len([
                v for v in month_videos
                if week_start.strftime("%Y-%m-%d") <= v["watched_at"][:10] < week_end.strftime("%Y-%m-%d")
            ])
            weeks.append({
                "week": i + 1,
                "videos": week_videos_count
            })

        report = {
            "report_type": "monthly",
            "period": f"{month_start} to {datetime.now().strftime('%Y-%m-%d')}",
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_videos": len(month_videos),
                "total_time_hours": round(total_time / 60, 1),
                "average_daily_minutes": round(total_time / 30, 1),
                "topics_explored": len(set(topics))
            },
            "weekly_breakdown": weeks,
            "topic_mastery": topic_counts,
            "achievements": self._calculate_achievements(month_videos, total_time),
            "recommendations": self._generate_recommendations(topic_counts, language)
        }

        self.data["generated_reports"].append(report)
        self._save_data()

        return report

    def _generate_insights(self, videos: List[Dict], language: str) -> Dict[str, Any]:
        """Generate AI insights from video data"""
        if not videos:
            return {"message": "暂无数据"}

        video_summaries = [{"title": v["title"], "topics": v.get("topics", [])} for v in videos[:10]]

        prompt = f"""基于今日学习内容生成简短洞察：
{json.dumps(video_summaries, ensure_ascii=False)}

返回JSON: highlights(今日亮点), suggestion(明日建议), quote(激励语句)
语言使用{language}。"""

        response = self.ai_client.chat(prompt, max_tokens=500)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"raw": response}

    def _get_daily_breakdown(self, start_date: str) -> List[Dict]:
        """Get daily breakdown of learning"""
        breakdown = []
        start = datetime.strptime(start_date, "%Y-%m-%d")

        for i in range(7):
            date = (start + timedelta(days=i)).strftime("%Y-%m-%d")
            videos_count = len([
                v for v in self.data["learning_data"]["videos_watched"]
                if v["watched_at"].startswith(date)
            ])
            time_spent = self.data["learning_data"]["time_spent"].get(date, 0)

            breakdown.append({
                "date": date,
                "videos": videos_count,
                "minutes": time_spent
            })

        return breakdown

    def _calculate_achievements(self, videos: List[Dict], total_time: int) -> List[Dict]:
        """Calculate achievements based on activity"""
        achievements = []

        if len(videos) >= 30:
            achievements.append({"name": "月度学霸", "description": "本月观看30+视频"})
        if total_time >= 600:
            achievements.append({"name": "时间投入者", "description": "本月学习10+小时"})
        if len(videos) >= 7:
            achievements.append({"name": "持续学习", "description": "连续7天学习"})

        return achievements

    def _generate_recommendations(self, topic_counts: Dict, language: str) -> List[str]:
        """Generate learning recommendations"""
        if not topic_counts:
            return ["开始观看一些视频吧！"]

        top_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)[:3]

        prompt = f"""基于用户学习的主题分布，给出3条简短的学习建议：
主题分布：{json.dumps(dict(top_topics), ensure_ascii=False)}
语言使用{language}，每条不超过20字。"""

        response = self.ai_client.chat(prompt, max_tokens=300)
        return response.split('\n')[:3]

    def export_report(self, report: Dict, format: str = "markdown") -> str:
        """Export report in various formats"""
        if format == "markdown":
            md = f"# 学习报告 - {report.get('report_type', '').upper()}\n\n"
            md += f"**周期:** {report.get('period', report.get('date', 'N/A'))}\n"
            md += f"**生成时间:** {report.get('generated_at', 'N/A')}\n\n"

            md += "## 概览\n\n"
            summary = report.get("summary", {})
            for key, value in summary.items():
                md += f"- **{key}:** {value}\n"

            if report.get("top_topics"):
                md += "\n## 热门话题\n\n"
                for topic, count in report["top_topics"]:
                    md += f"- {topic}: {count}次\n"

            if report.get("insights"):
                md += "\n## AI洞察\n\n"
                insights = report["insights"]
                if isinstance(insights, dict):
                    for key, value in insights.items():
                        md += f"**{key}:** {value}\n\n"
                else:
                    md += str(insights)

            if report.get("achievements"):
                md += "\n## 成就\n\n"
                for achievement in report["achievements"]:
                    md += f"🏆 **{achievement['name']}** - {achievement['description']}\n"

            return md

        elif format == "json":
            return json.dumps(report, ensure_ascii=False, indent=2)

        elif format == "html":
            html = f"<h1>学习报告 - {report.get('report_type', '').upper()}</h1>"
            html += f"<p><strong>周期:</strong> {report.get('period', report.get('date', 'N/A'))}</p>"
            html += "<h2>概览</h2><ul>"
            for key, value in report.get("summary", {}).items():
                html += f"<li><strong>{key}:</strong> {value}</li>"
            html += "</ul>"
            return html

        return str(report)

    def list_schedules(self) -> List[Dict]:
        """List all report schedules"""
        return list(self.data["schedules"].values())

    def get_recent_reports(self, limit: int = 10) -> List[Dict]:
        """Get recent generated reports"""
        return self.data["generated_reports"][-limit:]
