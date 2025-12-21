"""
Smart Reminder System - Intelligent learning reminders and scheduling
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from .ai_client import get_ai_client


class SmartReminder:
    """Intelligent reminder system for learning"""

    def __init__(self, data_dir: str = ".yt_tool_data"):
        self.client = get_ai_client()
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.reminders_file = self.data_dir / "smart_reminders.json"
        self.data = self._load_data()

    def _load_data(self) -> dict:
        if self.reminders_file.exists():
            return json.loads(self.reminders_file.read_text(encoding="utf-8"))
        return {
            "reminders": [],
            "review_schedule": [],
            "goals": [],
            "settings": {
                "daily_reminder_time": "09:00",
                "review_reminder": True,
                "break_reminder": True,
                "goal_reminder": True,
                "break_interval_minutes": 25,
                "quiet_hours_start": "22:00",
                "quiet_hours_end": "07:00"
            },
            "history": []
        }

    def _save_data(self):
        self.reminders_file.write_text(
            json.dumps(self.data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def schedule_ebbinghaus_review(self, topic: str, learned_date: str = None) -> dict:
        """Schedule reviews based on Ebbinghaus forgetting curve"""
        if learned_date is None:
            learned_date = datetime.now().strftime("%Y-%m-%d")

        try:
            base_date = datetime.strptime(learned_date, "%Y-%m-%d")
        except:
            base_date = datetime.now()

        # Ebbinghaus-based intervals: 1, 2, 4, 7, 15, 30 days
        intervals = [1, 2, 4, 7, 15, 30]

        review_dates = []
        for days in intervals:
            review_date = base_date + timedelta(days=days)
            review_dates.append({
                "topic": topic,
                "date": review_date.strftime("%Y-%m-%d"),
                "interval_days": days,
                "status": "pending",
                "type": "ebbinghaus"
            })

        # Add to schedule
        self.data["review_schedule"].extend(review_dates)
        self._save_data()

        return {
            "topic": topic,
            "learned_date": learned_date,
            "review_schedule": review_dates
        }

    def get_due_reviews(self, date: str = None) -> List[Dict]:
        """Get reviews due for a specific date"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        due = [
            r for r in self.data.get("review_schedule", [])
            if r.get("date") == date and r.get("status") == "pending"
        ]

        return due

    def complete_review(self, topic: str, date: str = None, difficulty: str = "medium") -> dict:
        """Mark a review as completed and adjust future schedule"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        completed = False
        for review in self.data.get("review_schedule", []):
            if review.get("topic") == topic and review.get("date") == date:
                review["status"] = "completed"
                review["completed_at"] = datetime.now().isoformat()
                review["difficulty"] = difficulty
                completed = True
                break

        if completed:
            # Adjust future intervals based on difficulty
            if difficulty == "easy":
                # Extend next interval
                pass
            elif difficulty == "hard":
                # Add extra review
                next_date = (datetime.strptime(date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
                self.data["review_schedule"].append({
                    "topic": topic,
                    "date": next_date,
                    "interval_days": 1,
                    "status": "pending",
                    "type": "reinforcement"
                })

            self._save_data()

        return {
            "completed": completed,
            "topic": topic,
            "difficulty": difficulty
        }

    def set_goal(self, goal: str, target_date: str, milestones: List[str] = None) -> dict:
        """Set a learning goal with optional milestones"""
        goal_data = {
            "id": datetime.now().strftime("%Y%m%d%H%M%S"),
            "goal": goal,
            "created_at": datetime.now().isoformat(),
            "target_date": target_date,
            "milestones": milestones or [],
            "progress": 0,
            "status": "active"
        }

        self.data["goals"].append(goal_data)
        self._save_data()

        return goal_data

    def update_goal_progress(self, goal_id: str, progress: float) -> dict:
        """Update progress on a goal"""
        for goal in self.data.get("goals", []):
            if goal.get("id") == goal_id:
                goal["progress"] = min(100, max(0, progress))
                if progress >= 100:
                    goal["status"] = "completed"
                    goal["completed_at"] = datetime.now().isoformat()
                self._save_data()
                return goal

        return {"error": "Goal not found"}

    def get_goal_reminders(self) -> List[Dict]:
        """Get reminders for active goals"""
        reminders = []
        today = datetime.now()

        for goal in self.data.get("goals", []):
            if goal.get("status") != "active":
                continue

            try:
                target = datetime.strptime(goal["target_date"], "%Y-%m-%d")
                days_left = (target - today).days
            except:
                days_left = 0

            if days_left < 0:
                reminder_type = "overdue"
                message = f"目标「{goal['goal']}」已过期！"
            elif days_left == 0:
                reminder_type = "due_today"
                message = f"目标「{goal['goal']}」今天到期！当前进度：{goal['progress']}%"
            elif days_left <= 3:
                reminder_type = "urgent"
                message = f"目标「{goal['goal']}」还剩{days_left}天，当前进度：{goal['progress']}%"
            elif days_left <= 7:
                reminder_type = "upcoming"
                message = f"目标「{goal['goal']}」还剩{days_left}天"
            else:
                continue

            reminders.append({
                "goal_id": goal["id"],
                "goal": goal["goal"],
                "type": reminder_type,
                "message": message,
                "days_left": days_left,
                "progress": goal["progress"]
            })

        return sorted(reminders, key=lambda x: x["days_left"])

    def schedule_break_reminder(self, interval_minutes: int = 25) -> dict:
        """Schedule Pomodoro-style break reminders"""
        self.data["settings"]["break_interval_minutes"] = interval_minutes
        self._save_data()

        return {
            "interval_minutes": interval_minutes,
            "next_break": (datetime.now() + timedelta(minutes=interval_minutes)).strftime("%H:%M"),
            "message": f"每{interval_minutes}分钟提醒休息"
        }

    def get_break_message(self, language: str = "中文") -> str:
        """Get a break reminder message"""
        prompts = [
            "该休息了！站起来活动一下，看看远处放松眼睛。",
            "学习很棒，但休息同样重要！喝杯水吧。",
            "已经学习很久了，让大脑休息5分钟。",
            "起来走走，深呼吸几次，然后继续加油！",
            "休息时间！做几个简单的拉伸动作。"
        ]

        import random
        return random.choice(prompts)

    def create_study_calendar(self, topics: List[str], hours_per_day: float = 1.0, days: int = 7) -> dict:
        """Create a study calendar/schedule"""
        calendar = []
        start_date = datetime.now()

        # Distribute topics across days
        topic_index = 0
        for day in range(days):
            date = start_date + timedelta(days=day)
            day_schedule = {
                "date": date.strftime("%Y-%m-%d"),
                "weekday": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][date.weekday()],
                "topics": [],
                "total_hours": hours_per_day
            }

            # Assign topics
            if topics:
                day_schedule["topics"].append({
                    "topic": topics[topic_index % len(topics)],
                    "hours": hours_per_day,
                    "type": "new_learning" if day < len(topics) else "review"
                })
                topic_index += 1

            calendar.append(day_schedule)

        return {
            "calendar": calendar,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": (start_date + timedelta(days=days-1)).strftime("%Y-%m-%d"),
            "total_hours": hours_per_day * days
        }

    def get_today_agenda(self, language: str = "中文") -> dict:
        """Get today's learning agenda"""
        today = datetime.now().strftime("%Y-%m-%d")

        agenda = {
            "date": today,
            "reviews_due": self.get_due_reviews(today),
            "goal_reminders": self.get_goal_reminders(),
            "scheduled_topics": []
        }

        # Generate daily message
        review_count = len(agenda["reviews_due"])
        goal_count = len([g for g in agenda["goal_reminders"] if g["type"] in ["due_today", "urgent"]])

        if review_count > 0 or goal_count > 0:
            messages = []
            if review_count > 0:
                messages.append(f"今天有{review_count}个复习任务")
            if goal_count > 0:
                messages.append(f"{goal_count}个目标需要关注")
            agenda["daily_message"] = "，".join(messages) + "！"
        else:
            agenda["daily_message"] = "今天没有紧急任务，可以探索新内容！"

        return agenda

    def set_new_video_notification(self, channel_id: str, channel_name: str) -> dict:
        """Set up notification for new videos from a channel"""
        notification = {
            "channel_id": channel_id,
            "channel_name": channel_name,
            "created_at": datetime.now().isoformat(),
            "enabled": True
        }

        self.data.setdefault("channel_notifications", []).append(notification)
        self._save_data()

        return notification

    def get_weekly_summary_reminder(self, language: str = "中文") -> dict:
        """Get weekly learning summary reminder"""
        # Calculate weekly stats
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())

        return {
            "type": "weekly_summary",
            "week_start": week_start.strftime("%Y-%m-%d"),
            "message": "本周学习总结已准备好，查看您的进步！"
        }

    def update_settings(self, settings: Dict) -> dict:
        """Update reminder settings"""
        self.data["settings"].update(settings)
        self._save_data()
        return self.data["settings"]

    def get_settings(self) -> dict:
        """Get current settings"""
        return self.data.get("settings", {})

    def export_calendar_ics(self, events: List[Dict] = None) -> str:
        """Export reminders to ICS calendar format"""
        events = events or self.data.get("review_schedule", [])

        ics_lines = [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//YT-Tool//Learning Reminders//EN",
        ]

        for event in events:
            if event.get("status") == "pending":
                event_date = event.get("date", datetime.now().strftime("%Y-%m-%d"))
                ics_lines.extend([
                    "BEGIN:VEVENT",
                    f"DTSTART:{event_date.replace('-', '')}T090000",
                    f"DTEND:{event_date.replace('-', '')}T093000",
                    f"SUMMARY:复习: {event.get('topic', 'Unknown')}",
                    f"DESCRIPTION:间隔{event.get('interval_days', 0)}天的复习提醒",
                    "END:VEVENT"
                ])

        ics_lines.append("END:VCALENDAR")
        return "\n".join(ics_lines)
