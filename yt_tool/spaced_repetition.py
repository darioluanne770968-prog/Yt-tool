"""
Spaced Repetition System - 艾宾浩斯复习系统
Implement spaced repetition for video content based on forgetting curve
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from .ai_client import get_ai_client


class SpacedRepetitionSystem:
    """Implement Ebbinghaus forgetting curve-based review system"""

    # Default review intervals (in days)
    DEFAULT_INTERVALS = [1, 2, 4, 7, 15, 30, 60, 120]

    def __init__(self, storage_path: str = ".spaced_repetition.json"):
        self.ai_client = get_ai_client()
        self.storage_path = storage_path
        self.data = self._load_data()

    def _load_data(self) -> Dict:
        """Load review data from file"""
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "cards": {},
                "review_history": [],
                "settings": {
                    "intervals": self.DEFAULT_INTERVALS,
                    "daily_limit": 50
                }
            }

    def _save_data(self):
        """Save review data to file"""
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2, default=str)

    def extract_review_items(self, transcript: str, video_id: str, video_title: str = "", language: str = "中文") -> List[Dict[str, Any]]:
        """Extract items suitable for spaced repetition from video"""
        prompt = f"""从以下视频内容中提取适合间隔重复学习的知识点。

内容：
{transcript[:8000]}

提取要求：
1. 每个知识点独立完整
2. 适合制作成问答卡片
3. 涵盖核心概念和细节
4. 难度适中，可记忆

返回JSON数组，每个知识点包含：
- id: 唯一标识
- front: 卡片正面（问题/提示）
- back: 卡片背面（答案/解释）
- category: 分类
- difficulty: 难度（easy/medium/hard）
- importance: 重要性（1-10）
- keywords: 关键词列表
- mnemonic_hint: 记忆提示（可选）

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            if json_start != -1 and json_end > json_start:
                items = json.loads(response[json_start:json_end])

                # Add metadata
                for item in items:
                    item["video_id"] = video_id
                    item["video_title"] = video_title
                    item["created_at"] = datetime.now().isoformat()
                    item["box"] = 0  # Leitner system box
                    item["next_review"] = datetime.now().isoformat()
                    item["review_count"] = 0
                    item["ease_factor"] = 2.5  # SM-2 algorithm
                    item["interval"] = 0

                return items
        except json.JSONDecodeError:
            pass

        return []

    def add_cards(self, items: List[Dict]):
        """Add review cards to the system"""
        for item in items:
            card_id = item.get("id") or f"card_{len(self.data['cards'])}"
            self.data["cards"][card_id] = item

        self._save_data()

    def get_due_cards(self, limit: int = None) -> List[Dict[str, Any]]:
        """Get cards that are due for review"""
        if limit is None:
            limit = self.data["settings"]["daily_limit"]

        now = datetime.now()
        due_cards = []

        for card_id, card in self.data["cards"].items():
            next_review = datetime.fromisoformat(card.get("next_review", now.isoformat()))
            if next_review <= now:
                card["card_id"] = card_id
                due_cards.append(card)

        # Sort by priority (importance * overdue factor)
        for card in due_cards:
            next_review = datetime.fromisoformat(card.get("next_review"))
            overdue_days = (now - next_review).days
            card["priority"] = card.get("importance", 5) * (1 + overdue_days * 0.1)

        due_cards.sort(key=lambda x: x["priority"], reverse=True)
        return due_cards[:limit]

    def review_card(self, card_id: str, quality: int) -> Dict[str, Any]:
        """
        Process a card review with quality rating (SM-2 algorithm)
        quality: 0-5 (0=complete blackout, 5=perfect response)
        """
        if card_id not in self.data["cards"]:
            return {"error": "Card not found"}

        card = self.data["cards"][card_id]
        now = datetime.now()

        # SM-2 Algorithm
        if quality < 3:
            # Failed - reset
            card["box"] = 0
            card["interval"] = 1
        else:
            # Success - advance
            if card["interval"] == 0:
                card["interval"] = 1
            elif card["interval"] == 1:
                card["interval"] = 6
            else:
                card["interval"] = int(card["interval"] * card["ease_factor"])

            # Update ease factor
            card["ease_factor"] = max(1.3, card["ease_factor"] + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))

            # Update Leitner box
            card["box"] = min(card["box"] + 1, 7)

        card["next_review"] = (now + timedelta(days=card["interval"])).isoformat()
        card["review_count"] = card.get("review_count", 0) + 1
        card["last_reviewed"] = now.isoformat()

        # Record history
        self.data["review_history"].append({
            "card_id": card_id,
            "timestamp": now.isoformat(),
            "quality": quality,
            "interval": card["interval"]
        })

        self._save_data()

        return {
            "card_id": card_id,
            "new_interval": card["interval"],
            "next_review": card["next_review"],
            "box": card["box"]
        }

    def get_review_stats(self) -> Dict[str, Any]:
        """Get review statistics"""
        total_cards = len(self.data["cards"])
        now = datetime.now()

        due_today = 0
        mastered = 0
        learning = 0

        box_distribution = {i: 0 for i in range(8)}

        for card in self.data["cards"].values():
            next_review = datetime.fromisoformat(card.get("next_review", now.isoformat()))
            if next_review <= now:
                due_today += 1

            box = card.get("box", 0)
            box_distribution[box] = box_distribution.get(box, 0) + 1

            if box >= 5:
                mastered += 1
            else:
                learning += 1

        # Calculate retention rate from recent reviews
        recent_reviews = [r for r in self.data["review_history"][-100:]]
        if recent_reviews:
            successful = len([r for r in recent_reviews if r["quality"] >= 3])
            retention_rate = successful / len(recent_reviews) * 100
        else:
            retention_rate = 0

        return {
            "total_cards": total_cards,
            "due_today": due_today,
            "mastered": mastered,
            "learning": learning,
            "box_distribution": box_distribution,
            "retention_rate": round(retention_rate, 1),
            "total_reviews": len(self.data["review_history"]),
            "streak_days": self._calculate_streak()
        }

    def _calculate_streak(self) -> int:
        """Calculate current review streak in days"""
        if not self.data["review_history"]:
            return 0

        dates = set()
        for review in self.data["review_history"]:
            date = datetime.fromisoformat(review["timestamp"]).date()
            dates.add(date)

        streak = 0
        current_date = datetime.now().date()

        while current_date in dates:
            streak += 1
            current_date -= timedelta(days=1)

        return streak

    def generate_review_schedule(self, days: int = 30, language: str = "中文") -> Dict[str, Any]:
        """Generate review schedule for upcoming days"""
        schedule = {}
        now = datetime.now()

        for card in self.data["cards"].values():
            next_review = datetime.fromisoformat(card.get("next_review", now.isoformat()))
            days_until = (next_review.date() - now.date()).days

            if 0 <= days_until < days:
                date_str = next_review.strftime("%Y-%m-%d")
                if date_str not in schedule:
                    schedule[date_str] = []
                schedule[date_str].append({
                    "front": card.get("front", "")[:50],
                    "difficulty": card.get("difficulty", "medium")
                })

        return {
            "schedule": schedule,
            "total_upcoming": sum(len(cards) for cards in schedule.values()),
            "busiest_day": max(schedule.keys(), key=lambda k: len(schedule[k])) if schedule else None
        }

    def generate_review_session(self, num_cards: int = 10, language: str = "中文") -> Dict[str, Any]:
        """Generate an optimized review session"""
        due_cards = self.get_due_cards(num_cards)

        if not due_cards:
            return {
                "message": "没有需要复习的卡片",
                "cards": [],
                "next_review_time": self._get_next_review_time()
            }

        # Mix difficulties for optimal learning
        easy = [c for c in due_cards if c.get("difficulty") == "easy"]
        medium = [c for c in due_cards if c.get("difficulty") == "medium"]
        hard = [c for c in due_cards if c.get("difficulty") == "hard"]

        # Interleave: hard -> medium -> easy -> medium -> hard...
        session_order = []
        while easy or medium or hard:
            if hard:
                session_order.append(hard.pop(0))
            if medium:
                session_order.append(medium.pop(0))
            if easy:
                session_order.append(easy.pop(0))

        return {
            "session_cards": session_order[:num_cards],
            "total_cards": len(session_order[:num_cards]),
            "estimated_time": len(session_order[:num_cards]) * 30,  # 30 seconds per card
            "tips": self._get_review_tips(language)
        }

    def _get_next_review_time(self) -> Optional[str]:
        """Get the next scheduled review time"""
        now = datetime.now()
        next_times = []

        for card in self.data["cards"].values():
            next_review = datetime.fromisoformat(card.get("next_review", now.isoformat()))
            if next_review > now:
                next_times.append(next_review)

        return min(next_times).isoformat() if next_times else None

    def _get_review_tips(self, language: str = "中文") -> List[str]:
        """Get tips for effective review"""
        tips = [
            "尝试在看答案前大声说出你的回答",
            "如果不确定，选择较低的评分",
            "将新知识与已知内容建立联系",
            "每次复习后休息5分钟",
            "使用记忆宫殿技术辅助记忆"
        ]
        return tips

    def export_to_anki(self, video_id: str = None) -> str:
        """Export cards to Anki-compatible format"""
        cards = self.data["cards"].values()
        if video_id:
            cards = [c for c in cards if c.get("video_id") == video_id]

        lines = []
        for card in cards:
            front = card.get("front", "").replace("\t", " ").replace("\n", "<br>")
            back = card.get("back", "").replace("\t", " ").replace("\n", "<br>")
            tags = " ".join(card.get("keywords", []))
            lines.append(f"{front}\t{back}\t{tags}")

        return "\n".join(lines)

    def get_forgetting_curve_data(self, card_id: str = None) -> Dict[str, Any]:
        """Get data for visualizing forgetting curve"""
        if card_id:
            reviews = [r for r in self.data["review_history"] if r["card_id"] == card_id]
        else:
            reviews = self.data["review_history"]

        # Group by interval
        interval_success = {}
        for review in reviews:
            interval = review.get("interval", 0)
            success = review.get("quality", 0) >= 3

            if interval not in interval_success:
                interval_success[interval] = {"success": 0, "total": 0}

            interval_success[interval]["total"] += 1
            if success:
                interval_success[interval]["success"] += 1

        # Calculate retention rate per interval
        curve_data = []
        for interval, data in sorted(interval_success.items()):
            if data["total"] > 0:
                retention = data["success"] / data["total"] * 100
                curve_data.append({
                    "interval_days": interval,
                    "retention_rate": round(retention, 1),
                    "sample_size": data["total"]
                })

        return {
            "curve_data": curve_data,
            "optimal_intervals": self.data["settings"]["intervals"]
        }
