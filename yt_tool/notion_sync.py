"""
Notion integration for syncing video analysis
"""

import os
from typing import Dict, List, Optional
from datetime import datetime


class NotionSync:
    """Sync video analysis to Notion"""

    def __init__(self, api_key: str = None, database_id: str = None):
        """
        Initialize Notion sync

        Args:
            api_key: Notion API key (or from NOTION_API_KEY env)
            database_id: Default database ID (or from NOTION_DATABASE_ID env)
        """
        self.api_key = api_key or os.getenv("NOTION_API_KEY")
        self.database_id = database_id or os.getenv("NOTION_DATABASE_ID")
        self.client = None

        if self.api_key:
            self._init_client()

    def _init_client(self):
        """Initialize Notion client"""
        try:
            from notion_client import Client
            self.client = Client(auth=self.api_key)
        except ImportError:
            raise ImportError("notion-client not installed. Run: pip install notion-client")

    def create_page(
        self,
        title: str,
        content: Dict,
        database_id: str = None,
        properties: Dict = None,
    ) -> Dict:
        """
        Create a new Notion page

        Args:
            title: Page title
            content: Content dictionary with sections
            database_id: Target database ID
            properties: Additional page properties

        Returns:
            Created page info
        """
        if not self.client:
            return {"error": "Notion client not initialized. Set NOTION_API_KEY."}

        db_id = database_id or self.database_id
        if not db_id:
            return {"error": "Database ID not provided"}

        # Build page properties
        page_properties = {
            "Name": {"title": [{"text": {"content": title}}]},
        }

        if properties:
            page_properties.update(properties)

        # Build page content
        children = self._build_blocks(content)

        try:
            response = self.client.pages.create(
                parent={"database_id": db_id},
                properties=page_properties,
                children=children,
            )

            return {
                "success": True,
                "page_id": response["id"],
                "url": response.get("url"),
            }

        except Exception as e:
            return {"error": str(e)}

    def _build_blocks(self, content: Dict) -> List[Dict]:
        """Build Notion blocks from content"""
        blocks = []

        for section_title, section_content in content.items():
            # Add heading
            blocks.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": section_title}}]
                }
            })

            # Add content
            if isinstance(section_content, str):
                # Split long text into paragraphs
                paragraphs = section_content.split("\n\n")
                for para in paragraphs:
                    if para.strip():
                        blocks.append({
                            "object": "block",
                            "type": "paragraph",
                            "paragraph": {
                                "rich_text": [{"type": "text", "text": {"content": para[:2000]}}]
                            }
                        })

            elif isinstance(section_content, list):
                # Add as bullet list
                for item in section_content:
                    blocks.append({
                        "object": "block",
                        "type": "bulleted_list_item",
                        "bulleted_list_item": {
                            "rich_text": [{"type": "text", "text": {"content": str(item)[:2000]}}]
                        }
                    })

            # Add divider
            blocks.append({"object": "block", "type": "divider", "divider": {}})

        return blocks

    def sync_video_analysis(
        self,
        video_id: str,
        analysis: Dict,
        database_id: str = None,
    ) -> Dict:
        """
        Sync video analysis to Notion

        Args:
            video_id: YouTube video ID
            analysis: Analysis data
            database_id: Target database ID

        Returns:
            Sync result
        """
        title = analysis.get("title", f"Video Analysis: {video_id}")

        content = {}

        if analysis.get("summary"):
            content["📝 Summary"] = analysis["summary"]

        if analysis.get("keypoints"):
            content["🎯 Key Points"] = analysis["keypoints"]

        if analysis.get("chapters"):
            content["📑 Chapters"] = analysis["chapters"]

        if analysis.get("transcript"):
            # Truncate long transcripts
            content["📜 Transcript"] = analysis["transcript"][:5000]

        properties = {
            "Video ID": {"rich_text": [{"text": {"content": video_id}}]},
            "Date": {"date": {"start": datetime.now().isoformat()}},
        }

        if analysis.get("url"):
            properties["URL"] = {"url": analysis["url"]}

        return self.create_page(title, content, database_id, properties)

    def sync_notes(
        self,
        title: str,
        notes: str,
        tags: List[str] = None,
        database_id: str = None,
    ) -> Dict:
        """
        Sync notes to Notion

        Args:
            title: Note title
            notes: Note content
            tags: Tags for the note
            database_id: Target database ID

        Returns:
            Sync result
        """
        content = {"📝 Notes": notes}

        properties = {
            "Date": {"date": {"start": datetime.now().isoformat()}},
        }

        if tags:
            properties["Tags"] = {"multi_select": [{"name": tag} for tag in tags]}

        return self.create_page(title, content, database_id, properties)

    def create_database(
        self,
        parent_page_id: str,
        title: str = "Video Analysis",
    ) -> Dict:
        """
        Create a new database for video analysis

        Args:
            parent_page_id: Parent page ID
            title: Database title

        Returns:
            Created database info
        """
        if not self.client:
            return {"error": "Notion client not initialized"}

        try:
            response = self.client.databases.create(
                parent={"type": "page_id", "page_id": parent_page_id},
                title=[{"type": "text", "text": {"content": title}}],
                properties={
                    "Name": {"title": {}},
                    "Video ID": {"rich_text": {}},
                    "URL": {"url": {}},
                    "Date": {"date": {}},
                    "Tags": {"multi_select": {}},
                    "Status": {
                        "select": {
                            "options": [
                                {"name": "To Watch", "color": "gray"},
                                {"name": "Watched", "color": "green"},
                                {"name": "Noted", "color": "blue"},
                            ]
                        }
                    },
                }
            )

            return {
                "success": True,
                "database_id": response["id"],
            }

        except Exception as e:
            return {"error": str(e)}

    def search_pages(
        self,
        query: str,
        database_id: str = None,
    ) -> List[Dict]:
        """
        Search pages in database

        Args:
            query: Search query
            database_id: Database to search in

        Returns:
            List of matching pages
        """
        if not self.client:
            return []

        db_id = database_id or self.database_id

        try:
            if db_id:
                response = self.client.databases.query(
                    database_id=db_id,
                    filter={
                        "property": "Name",
                        "title": {"contains": query}
                    }
                )
            else:
                response = self.client.search(query=query)

            return [
                {
                    "id": page["id"],
                    "title": self._get_page_title(page),
                    "url": page.get("url"),
                }
                for page in response.get("results", [])
            ]

        except Exception as e:
            return []

    def _get_page_title(self, page: Dict) -> str:
        """Extract page title from Notion page object"""
        try:
            props = page.get("properties", {})
            for prop in props.values():
                if prop.get("type") == "title":
                    title_list = prop.get("title", [])
                    if title_list:
                        return title_list[0].get("text", {}).get("content", "Untitled")
        except:
            pass
        return "Untitled"

    def append_to_page(
        self,
        page_id: str,
        content: str,
        heading: str = None,
    ) -> Dict:
        """
        Append content to existing page

        Args:
            page_id: Page ID to append to
            content: Content to append
            heading: Optional heading

        Returns:
            Result
        """
        if not self.client:
            return {"error": "Notion client not initialized"}

        blocks = []

        if heading:
            blocks.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": heading}}]
                }
            })

        blocks.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": content[:2000]}}]
            }
        })

        try:
            self.client.blocks.children.append(
                block_id=page_id,
                children=blocks,
            )
            return {"success": True}

        except Exception as e:
            return {"error": str(e)}


def get_notion_sync(api_key: str = None, database_id: str = None) -> NotionSync:
    """Factory function to get Notion sync instance"""
    return NotionSync(api_key, database_id)
