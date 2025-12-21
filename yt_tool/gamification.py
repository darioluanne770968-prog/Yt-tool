"""
Gamification System - Learning gamification with achievements, levels, and challenges
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from .ai_client import get_ai_client


class GamificationSystem:
    """Gamified learning with achievements, levels, and challenges"""

    def __init__(self, data_dir: str = ".yt_tool_data"):
        self.client = get_ai_client()
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.game_file = self.data_dir / "gamification.json"
        self.data = self._load_data()

    def _load_data(self) -> dict:
        if self.game_file.exists():
            return json.loads(self.game_file.read_text(encoding="utf-8"))
        return {
            "user": {
                "level": 1,
                "xp": 0,
                "total_xp": 0,
                "streak": 0,
                "longest_streak": 0,
                "coins": 0,
                "joined_at": datetime.now().isoformat()
            },
            "achievements": [],
            "badges": [],
            "challenges": [],
            "daily_tasks": [],
            "leaderboard_history": [],
            "inventory": []
        }

    def _save_data(self):
        self.game_file.write_text(
            json.dumps(self.data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def _calculate_level(self, total_xp: int) -> int:
        """Calculate level from total XP"""
        # Level formula: each level requires level * 100 XP
        level = 1
        xp_needed = 0
        while xp_needed <= total_xp:
            level += 1
            xp_needed += level * 100
        return level - 1

    def add_xp(self, amount: int, reason: str = "") -> dict:
        """Add experience points"""
        self.data["user"]["xp"] += amount
        self.data["user"]["total_xp"] += amount

        old_level = self.data["user"]["level"]
        new_level = self._calculate_level(self.data["user"]["total_xp"])

        level_up = new_level > old_level
        if level_up:
            self.data["user"]["level"] = new_level
            self.data["user"]["coins"] += new_level * 10  # Bonus coins

        self._save_data()

        return {
            "xp_gained": amount,
            "total_xp": self.data["user"]["total_xp"],
            "current_xp": self.data["user"]["xp"],
            "level": new_level,
            "level_up": level_up,
            "reason": reason
        }

    def update_streak(self, learned_today: bool = True) -> dict:
        """Update learning streak"""
        if learned_today:
            self.data["user"]["streak"] += 1
            if self.data["user"]["streak"] > self.data["user"]["longest_streak"]:
                self.data["user"]["longest_streak"] = self.data["user"]["streak"]

            # Streak bonus XP
            bonus_xp = min(self.data["user"]["streak"] * 5, 100)
            self.add_xp(bonus_xp, f"连续学习第{self.data['user']['streak']}天")
        else:
            self.data["user"]["streak"] = 0

        self._save_data()

        return {
            "streak": self.data["user"]["streak"],
            "longest_streak": self.data["user"]["longest_streak"]
        }

    def get_available_achievements(self) -> List[Dict]:
        """Get list of all available achievements"""
        achievements = [
            {"id": "first_video", "name": "初出茅庐", "description": "观看第一个视频", "xp": 50, "icon": "🎬"},
            {"id": "streak_7", "name": "坚持一周", "description": "连续学习7天", "xp": 200, "icon": "🔥"},
            {"id": "streak_30", "name": "月度达人", "description": "连续学习30天", "xp": 1000, "icon": "🏆"},
            {"id": "streak_100", "name": "百日成就", "description": "连续学习100天", "xp": 5000, "icon": "💎"},
            {"id": "quiz_master", "name": "答题高手", "description": "完成10次测验", "xp": 300, "icon": "🧠"},
            {"id": "perfect_score", "name": "满分达成", "description": "测验获得满分", "xp": 500, "icon": "💯"},
            {"id": "note_taker", "name": "笔记达人", "description": "生成50份笔记", "xp": 400, "icon": "📝"},
            {"id": "explorer", "name": "探索者", "description": "学习10个不同主题", "xp": 300, "icon": "🔍"},
            {"id": "night_owl", "name": "夜猫子", "description": "深夜学习（22:00-6:00）", "xp": 100, "icon": "🦉"},
            {"id": "early_bird", "name": "早起鸟", "description": "清晨学习（5:00-7:00）", "xp": 100, "icon": "🐦"},
            {"id": "speed_learner", "name": "速学达人", "description": "一天内完成5个视频", "xp": 250, "icon": "⚡"},
            {"id": "deep_diver", "name": "深度学习", "description": "单个视频学习超过1小时", "xp": 200, "icon": "🤿"},
            {"id": "social_butterfly", "name": "社交达人", "description": "分享10次学习内容", "xp": 150, "icon": "🦋"},
            {"id": "polyglot", "name": "多语言者", "description": "学习3种语言的内容", "xp": 350, "icon": "🌍"},
            {"id": "level_10", "name": "见习学者", "description": "达到10级", "xp": 500, "icon": "📚"},
            {"id": "level_25", "name": "资深学者", "description": "达到25级", "xp": 1500, "icon": "🎓"},
            {"id": "level_50", "name": "大师", "description": "达到50级", "xp": 5000, "icon": "👑"},
        ]

        # Mark unlocked achievements
        unlocked_ids = [a["id"] for a in self.data.get("achievements", [])]
        for ach in achievements:
            ach["unlocked"] = ach["id"] in unlocked_ids

        return achievements

    def unlock_achievement(self, achievement_id: str) -> Optional[dict]:
        """Unlock an achievement"""
        achievements = self.get_available_achievements()
        achievement = next((a for a in achievements if a["id"] == achievement_id), None)

        if not achievement:
            return None

        if achievement["unlocked"]:
            return {"already_unlocked": True, "achievement": achievement}

        # Unlock the achievement
        unlock_data = {
            "id": achievement_id,
            "name": achievement["name"],
            "unlocked_at": datetime.now().isoformat()
        }
        self.data["achievements"].append(unlock_data)

        # Award XP
        self.add_xp(achievement["xp"], f"解锁成就：{achievement['name']}")

        self._save_data()

        return {
            "unlocked": True,
            "achievement": achievement,
            "xp_earned": achievement["xp"]
        }

    def generate_daily_challenges(self, language: str = "中文") -> List[Dict]:
        """Generate daily learning challenges"""
        today = datetime.now().strftime("%Y-%m-%d")

        # Check if already generated today
        if self.data.get("daily_tasks_date") == today:
            return self.data.get("daily_tasks", [])

        challenges = [
            {
                "id": f"daily_1_{today}",
                "title": "每日一学",
                "description": "完成至少1个视频的学习",
                "xp_reward": 50,
                "coin_reward": 10,
                "progress": 0,
                "target": 1,
                "type": "video_complete"
            },
            {
                "id": f"daily_2_{today}",
                "title": "笔记时间",
                "description": "生成学习笔记",
                "xp_reward": 30,
                "coin_reward": 5,
                "progress": 0,
                "target": 1,
                "type": "notes_generated"
            },
            {
                "id": f"daily_3_{today}",
                "title": "知识检验",
                "description": "完成一次测验",
                "xp_reward": 40,
                "coin_reward": 8,
                "progress": 0,
                "target": 1,
                "type": "quiz_complete"
            },
            {
                "id": f"daily_4_{today}",
                "title": "探索新领域",
                "description": "学习一个新主题",
                "xp_reward": 60,
                "coin_reward": 15,
                "progress": 0,
                "target": 1,
                "type": "new_topic"
            }
        ]

        self.data["daily_tasks"] = challenges
        self.data["daily_tasks_date"] = today
        self._save_data()

        return challenges

    def complete_challenge(self, challenge_id: str) -> dict:
        """Mark a challenge as completed"""
        for challenge in self.data.get("daily_tasks", []):
            if challenge["id"] == challenge_id:
                if challenge["progress"] < challenge["target"]:
                    challenge["progress"] = challenge["target"]
                    self.add_xp(challenge["xp_reward"], f"完成挑战：{challenge['title']}")
                    self.data["user"]["coins"] += challenge["coin_reward"]
                    self._save_data()
                    return {
                        "completed": True,
                        "challenge": challenge,
                        "xp_earned": challenge["xp_reward"],
                        "coins_earned": challenge["coin_reward"]
                    }

        return {"error": "Challenge not found or already completed"}

    def get_leaderboard(self, timeframe: str = "weekly") -> List[Dict]:
        """Get leaderboard (simulated for single-user)"""
        # For single-user, we'll simulate a leaderboard
        user_score = self.data["user"]["total_xp"]

        simulated_players = [
            {"name": "学霸小明", "xp": user_score + 500, "level": self._calculate_level(user_score + 500)},
            {"name": "努力的小红", "xp": user_score + 200, "level": self._calculate_level(user_score + 200)},
            {"name": "你", "xp": user_score, "level": self.data["user"]["level"], "is_user": True},
            {"name": "加油小刚", "xp": max(0, user_score - 100), "level": self._calculate_level(max(0, user_score - 100))},
            {"name": "新人小美", "xp": max(0, user_score - 300), "level": self._calculate_level(max(0, user_score - 300))},
        ]

        simulated_players.sort(key=lambda x: x["xp"], reverse=True)

        for i, player in enumerate(simulated_players):
            player["rank"] = i + 1

        return simulated_players

    def create_custom_challenge(self, title: str, description: str, target: int, xp_reward: int, deadline_days: int = 7) -> dict:
        """Create a custom learning challenge"""
        challenge = {
            "id": f"custom_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "title": title,
            "description": description,
            "target": target,
            "progress": 0,
            "xp_reward": xp_reward,
            "created_at": datetime.now().isoformat(),
            "deadline": (datetime.now() + timedelta(days=deadline_days)).isoformat(),
            "type": "custom"
        }

        self.data["challenges"].append(challenge)
        self._save_data()

        return challenge

    def get_stats(self) -> dict:
        """Get user's gamification statistics"""
        return {
            "level": self.data["user"]["level"],
            "xp": self.data["user"]["xp"],
            "total_xp": self.data["user"]["total_xp"],
            "xp_to_next_level": (self.data["user"]["level"] + 1) * 100 - (self.data["user"]["xp"] % ((self.data["user"]["level"] + 1) * 100)),
            "streak": self.data["user"]["streak"],
            "longest_streak": self.data["user"]["longest_streak"],
            "coins": self.data["user"]["coins"],
            "achievements_unlocked": len(self.data.get("achievements", [])),
            "total_achievements": len(self.get_available_achievements()),
            "days_since_joined": (datetime.now() - datetime.fromisoformat(self.data["user"]["joined_at"])).days
        }

    def get_progress_summary(self, language: str = "中文") -> str:
        """Get a narrative progress summary"""
        stats = self.get_stats()

        prompt = f"""生成一段鼓励性的学习进度总结：

用户数据：
- 等级：{stats['level']}
- 总经验值：{stats['total_xp']}
- 连续学习天数：{stats['streak']}
- 最长连续天数：{stats['longest_streak']}
- 已解锁成就：{stats['achievements_unlocked']}/{stats['total_achievements']}
- 学习天数：{stats['days_since_joined']}

请用{language}生成：
1. 鼓励性的进度总结（2-3句话）
2. 近期目标建议（1-2句话）
3. 一句励志名言

语气要积极、鼓励、个性化。"""

        return self.client.generate(prompt)

    def spend_coins(self, amount: int, item: str) -> dict:
        """Spend coins on rewards"""
        if self.data["user"]["coins"] >= amount:
            self.data["user"]["coins"] -= amount
            self.data.setdefault("inventory", []).append({
                "item": item,
                "purchased_at": datetime.now().isoformat()
            })
            self._save_data()
            return {
                "success": True,
                "item": item,
                "remaining_coins": self.data["user"]["coins"]
            }
        return {
            "success": False,
            "error": "Not enough coins",
            "required": amount,
            "available": self.data["user"]["coins"]
        }

    def get_shop_items(self) -> List[Dict]:
        """Get available items in the reward shop"""
        return [
            {"id": "double_xp", "name": "双倍经验卡", "description": "下次学习获得双倍经验", "price": 100, "icon": "⚡"},
            {"id": "streak_freeze", "name": "连续天数保护", "description": "保护一天的连续记录", "price": 50, "icon": "🛡️"},
            {"id": "theme_dark", "name": "暗色主题", "description": "解锁暗色界面主题", "price": 200, "icon": "🌙"},
            {"id": "badge_vip", "name": "VIP徽章", "description": "获得VIP专属徽章", "price": 500, "icon": "👑"},
            {"id": "hint_token", "name": "提示令牌", "description": "测验中获得提示", "price": 30, "icon": "💡"},
        ]
