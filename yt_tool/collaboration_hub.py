"""
Real-time Collaboration - Collaborative learning and annotation features
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import hashlib
from .ai_client import get_ai_client


class CollaborationHub:
    """Real-time collaboration features for learning"""

    def __init__(self, data_dir: str = ".yt_tool_data"):
        self.client = get_ai_client()
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.collab_file = self.data_dir / "collaboration.json"
        self.data = self._load_data()

    def _load_data(self) -> dict:
        if self.collab_file.exists():
            return json.loads(self.collab_file.read_text(encoding="utf-8"))
        return {
            "rooms": {},
            "annotations": {},
            "shared_notes": {},
            "watch_parties": {},
            "whiteboards": {}
        }

    def _save_data(self):
        self.collab_file.write_text(
            json.dumps(self.data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def _generate_room_id(self, name: str) -> str:
        """Generate a unique room ID"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        hash_input = f"{name}{timestamp}"
        return hashlib.md5(hash_input.encode()).hexdigest()[:8]

    def create_watch_party(self, video_id: str, video_title: str, host_name: str = "Host") -> dict:
        """Create a watch party room for synchronized viewing"""
        room_id = self._generate_room_id(video_id)

        party = {
            "room_id": room_id,
            "video_id": video_id,
            "video_title": video_title,
            "host": host_name,
            "created_at": datetime.now().isoformat(),
            "participants": [{"name": host_name, "role": "host", "joined_at": datetime.now().isoformat()}],
            "status": "waiting",  # waiting, playing, paused, ended
            "current_time": 0,
            "chat_messages": [],
            "reactions": []
        }

        self.data["watch_parties"][room_id] = party
        self._save_data()

        return party

    def join_watch_party(self, room_id: str, participant_name: str) -> dict:
        """Join an existing watch party"""
        if room_id not in self.data.get("watch_parties", {}):
            return {"error": "Room not found"}

        party = self.data["watch_parties"][room_id]
        party["participants"].append({
            "name": participant_name,
            "role": "viewer",
            "joined_at": datetime.now().isoformat()
        })

        self._save_data()

        return {
            "joined": True,
            "room": party
        }

    def add_chat_message(self, room_id: str, sender: str, message: str, timestamp: float = 0) -> dict:
        """Add a chat message to watch party"""
        if room_id not in self.data.get("watch_parties", {}):
            return {"error": "Room not found"}

        chat_msg = {
            "sender": sender,
            "message": message,
            "video_timestamp": timestamp,
            "sent_at": datetime.now().isoformat()
        }

        self.data["watch_parties"][room_id]["chat_messages"].append(chat_msg)
        self._save_data()

        return chat_msg

    def create_shared_annotation(self, video_id: str, user: str, timestamp: float,
                                 annotation: str, annotation_type: str = "note") -> dict:
        """Create a shared annotation on a video timestamp"""
        if video_id not in self.data["annotations"]:
            self.data["annotations"][video_id] = []

        annotation_data = {
            "id": f"{video_id}_{len(self.data['annotations'][video_id])}",
            "user": user,
            "timestamp": timestamp,
            "text": annotation,
            "type": annotation_type,  # note, question, highlight, insight
            "created_at": datetime.now().isoformat(),
            "replies": [],
            "reactions": {"👍": 0, "💡": 0, "❓": 0, "🎯": 0}
        }

        self.data["annotations"][video_id].append(annotation_data)
        self._save_data()

        return annotation_data

    def reply_to_annotation(self, video_id: str, annotation_id: str, user: str, reply: str) -> dict:
        """Reply to an existing annotation"""
        if video_id not in self.data.get("annotations", {}):
            return {"error": "Video not found"}

        for ann in self.data["annotations"][video_id]:
            if ann["id"] == annotation_id:
                reply_data = {
                    "user": user,
                    "text": reply,
                    "created_at": datetime.now().isoformat()
                }
                ann["replies"].append(reply_data)
                self._save_data()
                return reply_data

        return {"error": "Annotation not found"}

    def react_to_annotation(self, video_id: str, annotation_id: str, reaction: str) -> dict:
        """Add a reaction to an annotation"""
        if video_id not in self.data.get("annotations", {}):
            return {"error": "Video not found"}

        valid_reactions = ["👍", "💡", "❓", "🎯"]
        if reaction not in valid_reactions:
            reaction = "👍"

        for ann in self.data["annotations"][video_id]:
            if ann["id"] == annotation_id:
                ann["reactions"][reaction] = ann["reactions"].get(reaction, 0) + 1
                self._save_data()
                return {"reaction": reaction, "count": ann["reactions"][reaction]}

        return {"error": "Annotation not found"}

    def get_video_annotations(self, video_id: str, sort_by: str = "timestamp") -> List[Dict]:
        """Get all annotations for a video"""
        annotations = self.data.get("annotations", {}).get(video_id, [])

        if sort_by == "timestamp":
            annotations.sort(key=lambda x: x.get("timestamp", 0))
        elif sort_by == "popularity":
            annotations.sort(key=lambda x: sum(x.get("reactions", {}).values()), reverse=True)
        elif sort_by == "recent":
            annotations.sort(key=lambda x: x.get("created_at", ""), reverse=True)

        return annotations

    def create_study_room(self, name: str, topic: str, max_participants: int = 10) -> dict:
        """Create a virtual study room"""
        room_id = self._generate_room_id(name)

        room = {
            "room_id": room_id,
            "name": name,
            "topic": topic,
            "created_at": datetime.now().isoformat(),
            "max_participants": max_participants,
            "participants": [],
            "status": "open",
            "resources": [],
            "tasks": [],
            "chat_log": []
        }

        self.data["rooms"][room_id] = room
        self._save_data()

        return room

    def add_resource_to_room(self, room_id: str, resource_type: str, resource_url: str,
                             title: str, added_by: str) -> dict:
        """Add a learning resource to a study room"""
        if room_id not in self.data.get("rooms", {}):
            return {"error": "Room not found"}

        resource = {
            "type": resource_type,  # video, article, document, link
            "url": resource_url,
            "title": title,
            "added_by": added_by,
            "added_at": datetime.now().isoformat()
        }

        self.data["rooms"][room_id]["resources"].append(resource)
        self._save_data()

        return resource

    def create_collaborative_whiteboard(self, room_id: str, title: str) -> dict:
        """Create a collaborative whiteboard for a room"""
        whiteboard_id = f"wb_{room_id}_{datetime.now().strftime('%H%M%S')}"

        whiteboard = {
            "id": whiteboard_id,
            "room_id": room_id,
            "title": title,
            "created_at": datetime.now().isoformat(),
            "elements": [],  # Drawing elements
            "text_notes": [],
            "participants": []
        }

        self.data["whiteboards"][whiteboard_id] = whiteboard
        self._save_data()

        return whiteboard

    def add_whiteboard_element(self, whiteboard_id: str, element_type: str,
                                content: dict, author: str) -> dict:
        """Add an element to the whiteboard"""
        if whiteboard_id not in self.data.get("whiteboards", {}):
            return {"error": "Whiteboard not found"}

        element = {
            "id": f"el_{len(self.data['whiteboards'][whiteboard_id]['elements'])}",
            "type": element_type,  # text, shape, drawing, image, sticky_note
            "content": content,
            "author": author,
            "created_at": datetime.now().isoformat()
        }

        self.data["whiteboards"][whiteboard_id]["elements"].append(element)
        self._save_data()

        return element

    def create_shared_notes(self, video_id: str, title: str, creator: str) -> dict:
        """Create shared notes document for a video"""
        notes_id = f"notes_{video_id}"

        notes = {
            "id": notes_id,
            "video_id": video_id,
            "title": title,
            "creator": creator,
            "created_at": datetime.now().isoformat(),
            "last_modified": datetime.now().isoformat(),
            "contributors": [creator],
            "sections": [],
            "version_history": []
        }

        self.data["shared_notes"][notes_id] = notes
        self._save_data()

        return notes

    def add_notes_section(self, notes_id: str, heading: str, content: str,
                          author: str, timestamp: float = None) -> dict:
        """Add a section to shared notes"""
        if notes_id not in self.data.get("shared_notes", {}):
            return {"error": "Notes not found"}

        section = {
            "id": f"sec_{len(self.data['shared_notes'][notes_id]['sections'])}",
            "heading": heading,
            "content": content,
            "author": author,
            "video_timestamp": timestamp,
            "created_at": datetime.now().isoformat()
        }

        self.data["shared_notes"][notes_id]["sections"].append(section)
        self.data["shared_notes"][notes_id]["last_modified"] = datetime.now().isoformat()

        if author not in self.data["shared_notes"][notes_id]["contributors"]:
            self.data["shared_notes"][notes_id]["contributors"].append(author)

        self._save_data()

        return section

    def generate_discussion_prompt(self, transcript: str, topic: str = "", language: str = "中文") -> dict:
        """Generate discussion prompts for group study"""
        prompt = f"""基于以下内容生成小组讨论话题：

内容：
{transcript[:4000]}

主题：{topic or "根据内容确定"}

请用{language}生成：

## 讨论话题

### 热身问题（5分钟）
1. [简单问题1]
2. [简单问题2]

### 核心讨论（15分钟）
1. [深度问题1]
   - 引导提示
   - 可能的观点

2. [深度问题2]
   - 引导提示
   - 可能的观点

3. [深度问题3]
   - 引导提示
   - 可能的观点

### 应用讨论（10分钟）
1. [实践问题1]
2. [实践问题2]

### 总结反思（5分钟）
1. [反思问题]

## 讨论规则建议
[列出讨论规则]

## 记录模板
[提供记录格式]

生成促进深入讨论的话题。"""

        response = self.client.generate(prompt)

        return {
            "topic": topic,
            "discussion_prompts": response
        }

    def export_collaboration_data(self, room_id: str = None) -> dict:
        """Export collaboration data"""
        if room_id:
            return {
                "room": self.data.get("rooms", {}).get(room_id),
                "watch_party": self.data.get("watch_parties", {}).get(room_id),
                "whiteboard": self.data.get("whiteboards", {}).get(f"wb_{room_id}")
            }
        return self.data

    def get_collaboration_stats(self) -> dict:
        """Get collaboration statistics"""
        return {
            "total_rooms": len(self.data.get("rooms", {})),
            "total_watch_parties": len(self.data.get("watch_parties", {})),
            "total_annotations": sum(len(v) for v in self.data.get("annotations", {}).values()),
            "total_shared_notes": len(self.data.get("shared_notes", {})),
            "total_whiteboards": len(self.data.get("whiteboards", {}))
        }
