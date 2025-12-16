"""
Learning Heatmap - 学习热力图
Visualize learning patterns, time distribution, and topic coverage
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from collections import defaultdict


class LearningHeatmap:
    """Generate heatmap data for learning visualization"""

    def __init__(self, storage_path: str = ".learning_heatmap.json"):
        self.storage_path = storage_path
        self.data = self._load_data()

    def _load_data(self) -> Dict:
        """Load heatmap data"""
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"activities": [], "daily_stats": {}, "topic_stats": {}}

    def _save_data(self):
        """Save data"""
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def log_activity(self, activity_type: str, duration: int, topics: List[str] = None, metadata: Dict = None):
        """Log a learning activity"""
        now = datetime.now()
        activity = {
            "type": activity_type,
            "duration": duration,
            "topics": topics or [],
            "timestamp": now.isoformat(),
            "date": now.strftime("%Y-%m-%d"),
            "hour": now.hour,
            "weekday": now.weekday(),
            "metadata": metadata or {}
        }

        self.data["activities"].append(activity)

        # Update daily stats
        date_key = activity["date"]
        if date_key not in self.data["daily_stats"]:
            self.data["daily_stats"][date_key] = {"total_minutes": 0, "activities": 0, "topics": []}
        self.data["daily_stats"][date_key]["total_minutes"] += duration
        self.data["daily_stats"][date_key]["activities"] += 1
        self.data["daily_stats"][date_key]["topics"].extend(topics or [])

        # Update topic stats
        for topic in (topics or []):
            if topic not in self.data["topic_stats"]:
                self.data["topic_stats"][topic] = {"total_minutes": 0, "count": 0}
            self.data["topic_stats"][topic]["total_minutes"] += duration
            self.data["topic_stats"][topic]["count"] += 1

        self._save_data()

    def generate_calendar_heatmap(self, days: int = 365) -> Dict[str, Any]:
        """Generate calendar heatmap data (like GitHub contribution graph)"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        heatmap_data = []
        current = start_date

        while current <= end_date:
            date_key = current.strftime("%Y-%m-%d")
            stats = self.data["daily_stats"].get(date_key, {"total_minutes": 0})
            minutes = stats["total_minutes"]

            # Intensity level (0-4)
            if minutes == 0:
                level = 0
            elif minutes < 30:
                level = 1
            elif minutes < 60:
                level = 2
            elif minutes < 120:
                level = 3
            else:
                level = 4

            heatmap_data.append({
                "date": date_key,
                "minutes": minutes,
                "level": level,
                "weekday": current.weekday()
            })

            current += timedelta(days=1)

        return {
            "data": heatmap_data,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "total_days": days
        }

    def generate_hourly_heatmap(self) -> Dict[str, Any]:
        """Generate hourly activity heatmap (hour x weekday)"""
        heatmap = [[0 for _ in range(24)] for _ in range(7)]  # 7 days x 24 hours

        for activity in self.data["activities"]:
            weekday = activity.get("weekday", 0)
            hour = activity.get("hour", 0)
            duration = activity.get("duration", 0)
            heatmap[weekday][hour] += duration

        return {
            "data": heatmap,
            "labels": {
                "weekdays": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"],
                "hours": [f"{h:02d}:00" for h in range(24)]
            }
        }

    def generate_topic_heatmap(self, top_n: int = 20) -> Dict[str, Any]:
        """Generate topic distribution heatmap"""
        sorted_topics = sorted(
            self.data["topic_stats"].items(),
            key=lambda x: x[1]["total_minutes"],
            reverse=True
        )[:top_n]

        return {
            "topics": [t[0] for t in sorted_topics],
            "values": [t[1]["total_minutes"] for t in sorted_topics],
            "counts": [t[1]["count"] for t in sorted_topics]
        }

    def export_echarts_option(self, heatmap_type: str = "calendar") -> str:
        """Export as ECharts option JSON"""
        if heatmap_type == "calendar":
            data = self.generate_calendar_heatmap()
            option = {
                "tooltip": {"position": "top"},
                "visualMap": {
                    "min": 0,
                    "max": 4,
                    "calculable": True,
                    "orient": "horizontal",
                    "left": "center",
                    "top": "top"
                },
                "calendar": {
                    "top": 60,
                    "range": [data["start_date"], data["end_date"]],
                    "cellSize": ["auto", 13]
                },
                "series": [{
                    "type": "heatmap",
                    "coordinateSystem": "calendar",
                    "data": [[d["date"], d["level"]] for d in data["data"]]
                }]
            }
        elif heatmap_type == "hourly":
            data = self.generate_hourly_heatmap()
            option = {
                "tooltip": {"position": "top"},
                "grid": {"height": "50%", "top": "10%"},
                "xAxis": {"type": "category", "data": data["labels"]["hours"]},
                "yAxis": {"type": "category", "data": data["labels"]["weekdays"]},
                "visualMap": {"min": 0, "max": 120, "calculable": True},
                "series": [{
                    "type": "heatmap",
                    "data": [
                        [h, d, data["data"][d][h]]
                        for d in range(7) for h in range(24)
                    ],
                    "label": {"show": False}
                }]
            }
        else:
            option = {}

        return json.dumps(option, ensure_ascii=False, indent=2)

    def export_html_visualization(self, title: str = "学习热力图") -> str:
        """Generate HTML page with heatmap visualization"""
        calendar_option = self.export_echarts_option("calendar")
        hourly_option = self.export_echarts_option("hourly")

        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <script src="https://cdn.jsdelivr.net/npm/echarts/dist/echarts.min.js"></script>
    <style>
        .chart {{ width: 100%; height: 300px; margin: 20px 0; }}
        body {{ font-family: sans-serif; padding: 20px; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <h2>年度学习日历</h2>
    <div id="calendar-chart" class="chart"></div>
    <h2>每周学习时段</h2>
    <div id="hourly-chart" class="chart"></div>
    <script>
        var calendarChart = echarts.init(document.getElementById('calendar-chart'));
        calendarChart.setOption({calendar_option});

        var hourlyChart = echarts.init(document.getElementById('hourly-chart'));
        hourlyChart.setOption({hourly_option});
    </script>
</body>
</html>"""
        return html

    def get_learning_stats(self) -> Dict[str, Any]:
        """Get comprehensive learning statistics"""
        total_minutes = sum(a["duration"] for a in self.data["activities"])
        total_days = len(self.data["daily_stats"])
        total_topics = len(self.data["topic_stats"])

        return {
            "total_learning_minutes": total_minutes,
            "total_learning_hours": round(total_minutes / 60, 1),
            "active_days": total_days,
            "topics_explored": total_topics,
            "average_daily_minutes": round(total_minutes / total_days, 1) if total_days > 0 else 0,
            "most_active_hour": self._get_most_active_hour(),
            "most_studied_topic": max(self.data["topic_stats"].items(), key=lambda x: x[1]["total_minutes"])[0] if self.data["topic_stats"] else None
        }

    def _get_most_active_hour(self) -> int:
        """Get the most active learning hour"""
        hourly = defaultdict(int)
        for activity in self.data["activities"]:
            hourly[activity.get("hour", 0)] += activity.get("duration", 0)
        if hourly:
            return max(hourly.items(), key=lambda x: x[1])[0]
        return 0
