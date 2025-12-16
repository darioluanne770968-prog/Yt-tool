"""
Study Group Matcher - 学习小组匹配系统
Match learners with similar interests and goals for collaborative learning
"""

import json
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional
from .ai_client import get_ai_client


class StudyGroupMatcher:
    """Match learners into study groups based on interests and goals"""

    def __init__(self, storage_path: str = ".study_groups.json"):
        self.ai_client = get_ai_client()
        self.storage_path = storage_path
        self.data = self._load_data()

    def _load_data(self) -> Dict:
        """Load study group data"""
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "learners": {},
                "groups": {},
                "matches": [],
                "topics": {}
            }

    def _save_data(self):
        """Save data"""
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2, default=str)

    def create_learner_profile(self, user_id: str, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Create or update learner profile"""
        learner = {
            "user_id": user_id,
            "name": profile.get("name", user_id),
            "interests": profile.get("interests", []),
            "current_topics": profile.get("current_topics", []),
            "skill_level": profile.get("skill_level", "intermediate"),
            "learning_goals": profile.get("learning_goals", []),
            "preferred_group_size": profile.get("preferred_group_size", 4),
            "availability": profile.get("availability", {}),
            "timezone": profile.get("timezone", "UTC+8"),
            "communication_style": profile.get("communication_style", "balanced"),
            "videos_watched": profile.get("videos_watched", []),
            "created_at": datetime.now().isoformat(),
            "active": True
        }

        self.data["learners"][user_id] = learner
        self._save_data()
        return learner

    def update_learning_history(self, user_id: str, video_id: str, topics: List[str]):
        """Update learner's video watching history"""
        if user_id not in self.data["learners"]:
            return {"error": "Learner not found"}

        learner = self.data["learners"][user_id]
        learner["videos_watched"].append({
            "video_id": video_id,
            "topics": topics,
            "watched_at": datetime.now().isoformat()
        })

        # Update current topics
        for topic in topics:
            if topic not in learner["current_topics"]:
                learner["current_topics"].append(topic)

        self._save_data()

    def find_matches(self, user_id: str, max_matches: int = 10) -> List[Dict[str, Any]]:
        """Find potential study partners for a user"""
        if user_id not in self.data["learners"]:
            return []

        target = self.data["learners"][user_id]
        matches = []

        for other_id, other in self.data["learners"].items():
            if other_id == user_id or not other.get("active", True):
                continue

            # Calculate compatibility score
            score = self._calculate_compatibility(target, other)
            if score > 0:
                matches.append({
                    "user_id": other_id,
                    "name": other.get("name", other_id),
                    "compatibility_score": score,
                    "common_interests": list(set(target["interests"]) & set(other["interests"])),
                    "common_topics": list(set(target["current_topics"]) & set(other["current_topics"])),
                    "skill_level": other["skill_level"]
                })

        matches.sort(key=lambda x: x["compatibility_score"], reverse=True)
        return matches[:max_matches]

    def _calculate_compatibility(self, learner1: Dict, learner2: Dict) -> float:
        """Calculate compatibility score between two learners"""
        score = 0

        # Interest overlap (40%)
        common_interests = len(set(learner1["interests"]) & set(learner2["interests"]))
        total_interests = len(set(learner1["interests"]) | set(learner2["interests"]))
        if total_interests > 0:
            score += (common_interests / total_interests) * 40

        # Topic overlap (30%)
        common_topics = len(set(learner1["current_topics"]) & set(learner2["current_topics"]))
        total_topics = len(set(learner1["current_topics"]) | set(learner2["current_topics"]))
        if total_topics > 0:
            score += (common_topics / total_topics) * 30

        # Skill level compatibility (15%)
        levels = {"beginner": 1, "intermediate": 2, "advanced": 3, "expert": 4}
        level_diff = abs(levels.get(learner1["skill_level"], 2) - levels.get(learner2["skill_level"], 2))
        score += (3 - level_diff) / 3 * 15

        # Goals alignment (15%)
        common_goals = len(set(learner1["learning_goals"]) & set(learner2["learning_goals"]))
        if learner1["learning_goals"] and learner2["learning_goals"]:
            score += (common_goals / max(len(learner1["learning_goals"]), len(learner2["learning_goals"]))) * 15

        return round(score, 1)

    def create_study_group(self, name: str, topic: str, creator_id: str, max_size: int = 6) -> Dict[str, Any]:
        """Create a new study group"""
        group_id = hashlib.md5(f"{name}{datetime.now()}".encode()).hexdigest()[:12]

        group = {
            "group_id": group_id,
            "name": name,
            "topic": topic,
            "creator_id": creator_id,
            "members": [creator_id],
            "max_size": max_size,
            "created_at": datetime.now().isoformat(),
            "status": "active",
            "videos": [],
            "discussions": [],
            "schedule": [],
            "description": ""
        }

        self.data["groups"][group_id] = group
        self._save_data()
        return group

    def join_group(self, group_id: str, user_id: str) -> Dict[str, Any]:
        """Join an existing study group"""
        if group_id not in self.data["groups"]:
            return {"error": "Group not found"}

        group = self.data["groups"][group_id]

        if len(group["members"]) >= group["max_size"]:
            return {"error": "Group is full"}

        if user_id in group["members"]:
            return {"error": "Already a member"}

        group["members"].append(user_id)
        self._save_data()

        return {"success": True, "group": group}

    def add_video_to_group(self, group_id: str, video_id: str, video_title: str):
        """Add a video to group's learning list"""
        if group_id not in self.data["groups"]:
            return {"error": "Group not found"}

        self.data["groups"][group_id]["videos"].append({
            "video_id": video_id,
            "title": video_title,
            "added_at": datetime.now().isoformat(),
            "status": "pending"
        })

        self._save_data()

    def generate_group_activities(self, group_id: str, language: str = "中文") -> Dict[str, Any]:
        """Generate suggested activities for the study group"""
        if group_id not in self.data["groups"]:
            return {"error": "Group not found"}

        group = self.data["groups"][group_id]

        prompt = f"""为以下学习小组设计活动建议。

小组信息：
- 名称: {group['name']}
- 主题: {group['topic']}
- 成员数: {len(group['members'])}
- 学习视频: {json.dumps(group['videos'][:5], ensure_ascii=False)}

请设计：
1. weekly_activities: 每周活动计划
2. discussion_topics: 讨论话题
3. collaborative_projects: 协作项目建议
4. peer_teaching: 互相教学安排
5. challenges: 小组挑战
6. milestones: 里程碑目标

返回JSON格式，语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"raw_activities": response}

    def generate_role_assignments(self, group_id: str, language: str = "中文") -> Dict[str, Any]:
        """Generate role assignments for group members"""
        if group_id not in self.data["groups"]:
            return {"error": "Group not found"}

        group = self.data["groups"][group_id]
        members = [self.data["learners"].get(m, {"user_id": m}) for m in group["members"]]

        prompt = f"""为学习小组成员分配角色。

成员信息：
{json.dumps(members, ensure_ascii=False)}

角色类型：
1. 组长（Leader）- 协调整体
2. 记录员（Note-taker）- 记录讨论
3. 时间管理（Timekeeper）- 控制进度
4. 提问者（Questioner）- 提出问题
5. 总结者（Summarizer）- 总结要点
6. 研究员（Researcher）- 查找资料

根据成员特点分配角色，返回JSON格式，语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"raw_assignments": response}

    def find_groups_for_topic(self, topic: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Find active groups for a specific topic"""
        matching_groups = []

        for group_id, group in self.data["groups"].items():
            if group["status"] != "active":
                continue

            if topic.lower() in group["topic"].lower() or topic.lower() in group["name"].lower():
                matching_groups.append({
                    "group_id": group_id,
                    "name": group["name"],
                    "topic": group["topic"],
                    "member_count": len(group["members"]),
                    "max_size": group["max_size"],
                    "openings": group["max_size"] - len(group["members"])
                })

        matching_groups.sort(key=lambda x: x["openings"], reverse=True)
        return matching_groups[:max_results]

    def auto_create_groups(self, topic: str, min_group_size: int = 3, max_group_size: int = 6, language: str = "中文") -> List[Dict[str, Any]]:
        """Automatically create groups from available learners interested in a topic"""
        # Find learners interested in the topic
        interested = []
        for user_id, learner in self.data["learners"].items():
            if not learner.get("active", True):
                continue
            if topic.lower() in [t.lower() for t in learner.get("interests", [])] or \
               topic.lower() in [t.lower() for t in learner.get("current_topics", [])]:
                interested.append(user_id)

        if len(interested) < min_group_size:
            return []

        # Create groups
        groups_created = []
        while len(interested) >= min_group_size:
            group_members = interested[:max_group_size]
            interested = interested[max_group_size:]

            group = self.create_study_group(
                name=f"{topic}学习小组 #{len(groups_created) + 1}",
                topic=topic,
                creator_id=group_members[0],
                max_size=max_group_size
            )

            for member in group_members[1:]:
                self.join_group(group["group_id"], member)

            groups_created.append(group)

        return groups_created

    def get_group_stats(self, group_id: str) -> Dict[str, Any]:
        """Get statistics for a study group"""
        if group_id not in self.data["groups"]:
            return {"error": "Group not found"}

        group = self.data["groups"][group_id]

        return {
            "group_id": group_id,
            "name": group["name"],
            "member_count": len(group["members"]),
            "videos_count": len(group["videos"]),
            "discussions_count": len(group["discussions"]),
            "created_at": group["created_at"],
            "days_active": (datetime.now() - datetime.fromisoformat(group["created_at"])).days,
            "status": group["status"]
        }

    def export_group_info(self, group_id: str, format: str = "markdown") -> str:
        """Export group information"""
        if group_id not in self.data["groups"]:
            return "Group not found"

        group = self.data["groups"][group_id]

        if format == "markdown":
            md = f"# 学习小组: {group['name']}\n\n"
            md += f"**主题:** {group['topic']}\n"
            md += f"**成员:** {len(group['members'])}/{group['max_size']}\n"
            md += f"**创建时间:** {group['created_at']}\n\n"

            md += "## 成员\n\n"
            for member_id in group["members"]:
                member = self.data["learners"].get(member_id, {})
                md += f"- {member.get('name', member_id)}"
                if member_id == group["creator_id"]:
                    md += " (组长)"
                md += "\n"

            if group["videos"]:
                md += "\n## 学习视频\n\n"
                for v in group["videos"]:
                    md += f"- {v.get('title', v['video_id'])} [{v.get('status', 'pending')}]\n"

            return md

        elif format == "json":
            return json.dumps(group, ensure_ascii=False, indent=2)

        return str(group)
