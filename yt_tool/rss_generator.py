"""
RSS Generator - RSS订阅生成器
Generate RSS feeds from video analysis and learning content
"""

import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from xml.etree import ElementTree as ET
from .ai_client import get_ai_client


class RSSGenerator:
    """Generate RSS feeds for video content and learning updates"""

    def __init__(self, storage_path: str = ".rss_feeds.json"):
        self.ai_client = get_ai_client()
        self.storage_path = storage_path
        self.data = self._load_data()

    def _load_data(self) -> Dict:
        """Load RSS data"""
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "feeds": {},
                "items": []
            }

    def _save_data(self):
        """Save data"""
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def create_feed(self, title: str, description: str, link: str = "", feed_type: str = "video_analysis") -> Dict[str, Any]:
        """Create a new RSS feed"""
        feed_id = f"feed_{datetime.now().strftime('%Y%m%d%H%M%S')}"

        feed = {
            "id": feed_id,
            "title": title,
            "description": description,
            "link": link or f"/feeds/{feed_id}.xml",
            "type": feed_type,
            "language": "zh-CN",
            "created_at": datetime.now().isoformat(),
            "last_build": datetime.now().isoformat(),
            "items": []
        }

        self.data["feeds"][feed_id] = feed
        self._save_data()
        return feed

    def add_item(self, feed_id: str, item: Dict[str, Any]) -> Dict[str, Any]:
        """Add an item to a feed"""
        if feed_id not in self.data["feeds"]:
            return {"error": "Feed not found"}

        rss_item = {
            "guid": item.get("id", f"item_{datetime.now().timestamp()}"),
            "title": item.get("title", ""),
            "description": item.get("description", ""),
            "link": item.get("link", ""),
            "pubDate": item.get("pubDate", datetime.now().isoformat()),
            "author": item.get("author", ""),
            "categories": item.get("categories", []),
            "content": item.get("content", "")
        }

        self.data["feeds"][feed_id]["items"].insert(0, rss_item)
        self.data["feeds"][feed_id]["last_build"] = datetime.now().isoformat()

        # Keep only last 100 items
        self.data["feeds"][feed_id]["items"] = self.data["feeds"][feed_id]["items"][:100]

        self._save_data()
        return rss_item

    def add_video_analysis(self, feed_id: str, video_id: str, title: str, analysis: Dict) -> Dict[str, Any]:
        """Add video analysis as RSS item"""
        description = ""
        if analysis.get("summary"):
            description += f"<h3>摘要</h3><p>{analysis['summary']}</p>"
        if analysis.get("keypoints"):
            description += "<h3>要点</h3><ul>"
            for point in analysis.get("keypoints", [])[:5]:
                description += f"<li>{point}</li>"
            description += "</ul>"

        item = {
            "id": f"video_{video_id}",
            "title": f"视频分析: {title}",
            "description": description,
            "link": f"https://youtube.com/watch?v={video_id}",
            "categories": analysis.get("topics", []),
            "content": json.dumps(analysis, ensure_ascii=False)
        }

        return self.add_item(feed_id, item)

    def add_learning_update(self, feed_id: str, update_type: str, content: Dict) -> Dict[str, Any]:
        """Add learning progress update as RSS item"""
        descriptions = {
            "daily_summary": f"今日学习了 {content.get('videos_count', 0)} 个视频，共 {content.get('duration', 0)} 分钟",
            "milestone": f"达成里程碑: {content.get('milestone', '')}",
            "new_topic": f"开始学习新话题: {content.get('topic', '')}",
            "quiz_result": f"测验结果: {content.get('score', 0)}% 正确率"
        }

        item = {
            "id": f"{update_type}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "title": f"学习动态: {update_type}",
            "description": descriptions.get(update_type, str(content)),
            "categories": ["learning_update", update_type]
        }

        return self.add_item(feed_id, item)

    def generate_rss_xml(self, feed_id: str) -> str:
        """Generate RSS 2.0 XML"""
        if feed_id not in self.data["feeds"]:
            return "<error>Feed not found</error>"

        feed = self.data["feeds"][feed_id]

        # Create RSS structure
        rss = ET.Element("rss", version="2.0")
        channel = ET.SubElement(rss, "channel")

        # Channel metadata
        ET.SubElement(channel, "title").text = feed["title"]
        ET.SubElement(channel, "description").text = feed["description"]
        ET.SubElement(channel, "link").text = feed["link"]
        ET.SubElement(channel, "language").text = feed.get("language", "zh-CN")
        ET.SubElement(channel, "lastBuildDate").text = feed["last_build"]

        # Items
        for item in feed["items"]:
            item_elem = ET.SubElement(channel, "item")
            ET.SubElement(item_elem, "guid").text = item["guid"]
            ET.SubElement(item_elem, "title").text = item["title"]
            ET.SubElement(item_elem, "description").text = item["description"]
            ET.SubElement(item_elem, "link").text = item.get("link", "")
            ET.SubElement(item_elem, "pubDate").text = item["pubDate"]

            if item.get("author"):
                ET.SubElement(item_elem, "author").text = item["author"]

            for category in item.get("categories", []):
                ET.SubElement(item_elem, "category").text = category

        return ET.tostring(rss, encoding="unicode", method="xml")

    def generate_atom_xml(self, feed_id: str) -> str:
        """Generate Atom 1.0 XML"""
        if feed_id not in self.data["feeds"]:
            return "<error>Feed not found</error>"

        feed = self.data["feeds"][feed_id]

        atom_ns = "http://www.w3.org/2005/Atom"
        ET.register_namespace('', atom_ns)

        root = ET.Element(f"{{{atom_ns}}}feed")

        ET.SubElement(root, f"{{{atom_ns}}}title").text = feed["title"]
        ET.SubElement(root, f"{{{atom_ns}}}subtitle").text = feed["description"]
        ET.SubElement(root, f"{{{atom_ns}}}id").text = feed["id"]
        ET.SubElement(root, f"{{{atom_ns}}}updated").text = feed["last_build"]

        link = ET.SubElement(root, f"{{{atom_ns}}}link")
        link.set("href", feed["link"])
        link.set("rel", "self")

        for item in feed["items"]:
            entry = ET.SubElement(root, f"{{{atom_ns}}}entry")
            ET.SubElement(entry, f"{{{atom_ns}}}id").text = item["guid"]
            ET.SubElement(entry, f"{{{atom_ns}}}title").text = item["title"]
            ET.SubElement(entry, f"{{{atom_ns}}}updated").text = item["pubDate"]

            summary = ET.SubElement(entry, f"{{{atom_ns}}}summary")
            summary.set("type", "html")
            summary.text = item["description"]

            if item.get("link"):
                link = ET.SubElement(entry, f"{{{atom_ns}}}link")
                link.set("href", item["link"])

        return ET.tostring(root, encoding="unicode", method="xml")

    def generate_json_feed(self, feed_id: str) -> str:
        """Generate JSON Feed format"""
        if feed_id not in self.data["feeds"]:
            return json.dumps({"error": "Feed not found"})

        feed = self.data["feeds"][feed_id]

        json_feed = {
            "version": "https://jsonfeed.org/version/1.1",
            "title": feed["title"],
            "description": feed["description"],
            "home_page_url": feed["link"],
            "feed_url": f"{feed['link']}/feed.json",
            "language": feed.get("language", "zh-CN"),
            "items": []
        }

        for item in feed["items"]:
            json_feed["items"].append({
                "id": item["guid"],
                "title": item["title"],
                "content_html": item["description"],
                "url": item.get("link", ""),
                "date_published": item["pubDate"],
                "authors": [{"name": item.get("author", "Unknown")}] if item.get("author") else [],
                "tags": item.get("categories", [])
            })

        return json.dumps(json_feed, ensure_ascii=False, indent=2)

    def create_channel_feed(self, channel_id: str, channel_name: str) -> Dict[str, Any]:
        """Create RSS feed for a specific YouTube channel"""
        return self.create_feed(
            title=f"{channel_name} - 视频分析",
            description=f"自动分析 {channel_name} 频道的视频内容",
            feed_type="channel_analysis"
        )

    def create_topic_feed(self, topic: str) -> Dict[str, Any]:
        """Create RSS feed for a specific topic"""
        return self.create_feed(
            title=f"话题: {topic}",
            description=f"关于 {topic} 的视频分析和学习内容",
            feed_type="topic"
        )

    def create_learning_diary_feed(self, user_name: str = "学习者") -> Dict[str, Any]:
        """Create RSS feed for learning diary"""
        return self.create_feed(
            title=f"{user_name}的学习日记",
            description="每日学习记录和进度更新",
            feed_type="learning_diary"
        )

    def list_feeds(self) -> List[Dict[str, Any]]:
        """List all feeds"""
        return [
            {
                "id": feed["id"],
                "title": feed["title"],
                "type": feed["type"],
                "items_count": len(feed["items"]),
                "last_build": feed["last_build"]
            }
            for feed in self.data["feeds"].values()
        ]

    def get_feed(self, feed_id: str) -> Dict[str, Any]:
        """Get feed details"""
        return self.data["feeds"].get(feed_id, {"error": "Feed not found"})

    def delete_feed(self, feed_id: str) -> Dict[str, Any]:
        """Delete a feed"""
        if feed_id not in self.data["feeds"]:
            return {"error": "Feed not found"}

        del self.data["feeds"][feed_id]
        self._save_data()
        return {"deleted": True}

    def export_opml(self) -> str:
        """Export all feeds as OPML"""
        opml = '<?xml version="1.0" encoding="UTF-8"?>\n'
        opml += '<opml version="2.0">\n'
        opml += '  <head>\n'
        opml += '    <title>YouTube AI Tool Feeds</title>\n'
        opml += f'    <dateCreated>{datetime.now().isoformat()}</dateCreated>\n'
        opml += '  </head>\n'
        opml += '  <body>\n'

        for feed in self.data["feeds"].values():
            opml += f'    <outline text="{feed["title"]}" '
            opml += f'title="{feed["title"]}" '
            opml += f'type="rss" '
            opml += f'xmlUrl="{feed["link"]}" />\n'

        opml += '  </body>\n'
        opml += '</opml>'

        return opml
