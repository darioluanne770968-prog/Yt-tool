"""
Cross Platform Sync - 跨平台同步
Support for Bilibili, Douyin, and other video platforms
"""

import json
import re
from typing import Dict, List, Any, Optional
from .ai_client import get_ai_client


class CrossPlatformSync:
    """Handle video content from multiple platforms"""

    SUPPORTED_PLATFORMS = {
        "youtube": {
            "name": "YouTube",
            "url_patterns": [
                r"(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]+)",
                r"(?:https?://)?youtu\.be/([a-zA-Z0-9_-]+)"
            ],
            "api_available": True
        },
        "bilibili": {
            "name": "哔哩哔哩",
            "url_patterns": [
                r"(?:https?://)?(?:www\.)?bilibili\.com/video/(BV[a-zA-Z0-9]+)",
                r"(?:https?://)?(?:www\.)?bilibili\.com/video/(av\d+)",
                r"(?:https?://)?b23\.tv/([a-zA-Z0-9]+)"
            ],
            "api_available": True
        },
        "douyin": {
            "name": "抖音",
            "url_patterns": [
                r"(?:https?://)?(?:www\.)?douyin\.com/video/(\d+)",
                r"(?:https?://)?v\.douyin\.com/([a-zA-Z0-9]+)"
            ],
            "api_available": False
        },
        "xiaohongshu": {
            "name": "小红书",
            "url_patterns": [
                r"(?:https?://)?(?:www\.)?xiaohongshu\.com/discovery/item/([a-zA-Z0-9]+)"
            ],
            "api_available": False
        },
        "tiktok": {
            "name": "TikTok",
            "url_patterns": [
                r"(?:https?://)?(?:www\.)?tiktok\.com/@[^/]+/video/(\d+)"
            ],
            "api_available": False
        }
    }

    def __init__(self, storage_path: str = ".cross_platform.json"):
        self.ai_client = get_ai_client()
        self.storage_path = storage_path
        self.data = self._load_data()

    def _load_data(self) -> Dict:
        """Load cross-platform data"""
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "videos": {},
                "platform_accounts": {},
                "sync_history": []
            }

    def _save_data(self):
        """Save data"""
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def detect_platform(self, url: str) -> Dict[str, Any]:
        """Detect which platform a URL is from"""
        for platform_id, platform_info in self.SUPPORTED_PLATFORMS.items():
            for pattern in platform_info["url_patterns"]:
                match = re.search(pattern, url)
                if match:
                    return {
                        "platform": platform_id,
                        "platform_name": platform_info["name"],
                        "video_id": match.group(1),
                        "api_available": platform_info["api_available"]
                    }

        return {"platform": "unknown", "error": "Unsupported platform"}

    def get_bilibili_info(self, video_id: str) -> Dict[str, Any]:
        """Get Bilibili video information (simulated - actual implementation needs API)"""
        # In a real implementation, this would call Bilibili API
        return {
            "platform": "bilibili",
            "video_id": video_id,
            "status": "api_call_needed",
            "note": "需要使用 bilibili-api-python 包获取实际数据",
            "example_api_usage": """
from bilibili_api import video, sync

v = video.Video(bvid="{video_id}")
info = sync(v.get_info())
"""
        }

    def extract_bilibili_transcript(self, video_id: str) -> Dict[str, Any]:
        """Extract transcript from Bilibili video"""
        return {
            "platform": "bilibili",
            "video_id": video_id,
            "status": "extraction_needed",
            "methods": [
                "1. 使用 bilibili-api 获取字幕",
                "2. 使用 you-get 下载后提取",
                "3. 使用语音识别转文字"
            ],
            "code_example": """
from bilibili_api import video, sync

v = video.Video(bvid=video_id)
# 获取字幕列表
subtitle_list = sync(v.get_subtitle(video_id))
"""
        }

    def convert_for_platform(self, content: Dict, target_platform: str, language: str = "中文") -> Dict[str, Any]:
        """Convert content for a specific platform's format"""
        platform_specs = {
            "bilibili": {
                "max_title_length": 80,
                "max_description_length": 2000,
                "supported_formats": ["mp4", "flv"],
                "aspect_ratio": "16:9"
            },
            "douyin": {
                "max_title_length": 55,
                "max_description_length": 300,
                "supported_formats": ["mp4"],
                "aspect_ratio": "9:16",
                "max_duration": 600
            },
            "xiaohongshu": {
                "max_title_length": 20,
                "max_description_length": 1000,
                "supported_formats": ["mp4"],
                "aspect_ratio": "3:4"
            },
            "youtube": {
                "max_title_length": 100,
                "max_description_length": 5000,
                "supported_formats": ["mp4", "webm", "mov"],
                "aspect_ratio": "16:9"
            }
        }

        specs = platform_specs.get(target_platform, platform_specs["youtube"])

        prompt = f"""将以下内容适配为{self.SUPPORTED_PLATFORMS.get(target_platform, {}).get('name', target_platform)}平台格式。

原内容：
{json.dumps(content, ensure_ascii=False)[:3000]}

平台规格：
- 标题最大长度: {specs['max_title_length']}字
- 描述最大长度: {specs['max_description_length']}字
- 推荐比例: {specs['aspect_ratio']}

请返回JSON格式：
1. title: 适配后的标题
2. description: 适配后的描述
3. tags: 推荐标签
4. cover_suggestion: 封面建议
5. platform_tips: 平台特定建议

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"raw": response}

    def find_cross_platform_video(self, title: str, platform: str = None, language: str = "中文") -> Dict[str, Any]:
        """Search for same video on different platforms"""
        prompt = f"""帮助查找视频"{title}"在不同平台上的版本。

{"目标平台: " + platform if platform else "搜索所有平台"}

返回JSON格式：
1. search_queries: 各平台推荐搜索词
2. likely_titles: 可能的标题变体
3. search_tips: 搜索技巧
4. platform_specific: 各平台搜索建议

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"raw": response}

    def sync_video_data(self, source_url: str, target_platforms: List[str]) -> Dict[str, Any]:
        """Sync video analysis data across platforms"""
        source_info = self.detect_platform(source_url)

        sync_record = {
            "source": source_info,
            "targets": target_platforms,
            "synced_at": None,
            "status": "pending",
            "conversions": {}
        }

        for platform in target_platforms:
            sync_record["conversions"][platform] = {
                "status": "ready",
                "format_specs": self.SUPPORTED_PLATFORMS.get(platform, {})
            }

        self.data["sync_history"].append(sync_record)
        self._save_data()

        return sync_record

    def get_platform_commands(self, platform: str) -> Dict[str, str]:
        """Get platform-specific tool commands"""
        commands = {
            "bilibili": {
                "download_video": "you-get -o ./output 'BILIBILI_URL'",
                "download_audio": "you-get -O audio 'BILIBILI_URL'",
                "get_info": "you-get -i 'BILIBILI_URL'",
                "python_lib": "pip install bilibili-api-python"
            },
            "youtube": {
                "download_video": "yt-dlp -f best 'YOUTUBE_URL'",
                "download_audio": "yt-dlp -x --audio-format mp3 'YOUTUBE_URL'",
                "get_info": "yt-dlp --dump-json 'YOUTUBE_URL'",
                "subtitles": "yt-dlp --write-auto-sub --sub-lang zh 'YOUTUBE_URL'"
            },
            "douyin": {
                "download_video": "you-get 'DOUYIN_URL'",
                "note": "抖音视频下载可能需要登录cookie"
            }
        }

        return commands.get(platform, {"note": "Platform not fully supported yet"})

    def generate_cross_post_content(self, transcript: str, source_platform: str, target_platform: str, language: str = "中文") -> Dict[str, Any]:
        """Generate content optimized for cross-posting"""
        prompt = f"""将以下{self.SUPPORTED_PLATFORMS.get(source_platform, {}).get('name', source_platform)}内容改编为适合{self.SUPPORTED_PLATFORMS.get(target_platform, {}).get('name', target_platform)}的版本。

原内容：
{transcript[:4000]}

考虑：
1. 平台用户偏好差异
2. 内容长度限制
3. 标签和话题风格
4. 互动方式差异

返回JSON格式：
1. adapted_content: 改编后的内容
2. title: 标题
3. description: 描述
4. tags: 标签
5. call_to_action: 号召行动
6. best_posting_time: 最佳发布时间
7. engagement_tips: 互动技巧

语言使用{language}。"""

        response = self.ai_client.chat(prompt)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except json.JSONDecodeError:
            pass

        return {"raw": response}

    def list_supported_platforms(self) -> Dict[str, Any]:
        """List all supported platforms with their features"""
        return {
            platform_id: {
                "name": info["name"],
                "api_available": info["api_available"],
                "features": ["视频下载", "信息获取"] + (["API访问"] if info["api_available"] else [])
            }
            for platform_id, info in self.SUPPORTED_PLATFORMS.items()
        }

    def export_unified_format(self, videos: List[Dict], format: str = "json") -> str:
        """Export videos in unified format across platforms"""
        unified = []
        for v in videos:
            unified.append({
                "id": v.get("video_id", v.get("id", "")),
                "platform": v.get("platform", "unknown"),
                "title": v.get("title", ""),
                "url": v.get("url", ""),
                "duration": v.get("duration", 0),
                "topics": v.get("topics", []),
                "added_at": v.get("added_at", "")
            })

        if format == "json":
            return json.dumps(unified, ensure_ascii=False, indent=2)
        elif format == "csv":
            if not unified:
                return ""
            headers = list(unified[0].keys())
            lines = [",".join(headers)]
            for item in unified:
                lines.append(",".join(str(item.get(h, "")) for h in headers))
            return "\n".join(lines)

        return str(unified)
