"""
Caching system for transcripts and analysis results
"""

import os
import json
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Any


class Cache:
    """File-based cache for storing transcripts and results"""

    def __init__(self, cache_dir: str = None, ttl_hours: int = 24 * 7):
        """
        Initialize cache

        Args:
            cache_dir: Cache directory path
            ttl_hours: Time-to-live in hours (default: 7 days)
        """
        if cache_dir is None:
            # Use user's cache directory
            home = os.path.expanduser("~")
            cache_dir = os.path.join(home, ".cache", "yt-tool")

        self.cache_dir = cache_dir
        self.ttl = timedelta(hours=ttl_hours)
        os.makedirs(cache_dir, exist_ok=True)

    def _get_cache_path(self, key: str) -> str:
        """Get file path for a cache key"""
        # Hash the key to create a safe filename
        key_hash = hashlib.md5(key.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{key_hash}.json")

    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found/expired
        """
        cache_path = self._get_cache_path(key)

        if not os.path.exists(cache_path):
            return None

        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Check if expired
            cached_time = datetime.fromisoformat(data["cached_at"])
            if datetime.now() - cached_time > self.ttl:
                # Expired, remove cache file
                os.remove(cache_path)
                return None

            return data["value"]

        except (json.JSONDecodeError, KeyError, ValueError):
            # Invalid cache file, remove it
            os.remove(cache_path)
            return None

    def set(self, key: str, value: Any) -> None:
        """
        Set value in cache

        Args:
            key: Cache key
            value: Value to cache
        """
        cache_path = self._get_cache_path(key)

        data = {
            "key": key,
            "value": value,
            "cached_at": datetime.now().isoformat(),
        }

        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def delete(self, key: str) -> bool:
        """
        Delete value from cache

        Args:
            key: Cache key

        Returns:
            True if deleted, False if not found
        """
        cache_path = self._get_cache_path(key)

        if os.path.exists(cache_path):
            os.remove(cache_path)
            return True
        return False

    def clear(self) -> int:
        """
        Clear all cache files

        Returns:
            Number of files deleted
        """
        count = 0
        for filename in os.listdir(self.cache_dir):
            if filename.endswith(".json"):
                os.remove(os.path.join(self.cache_dir, filename))
                count += 1
        return count

    def clear_expired(self) -> int:
        """
        Clear only expired cache files

        Returns:
            Number of files deleted
        """
        count = 0
        for filename in os.listdir(self.cache_dir):
            if not filename.endswith(".json"):
                continue

            filepath = os.path.join(self.cache_dir, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)

                cached_time = datetime.fromisoformat(data["cached_at"])
                if datetime.now() - cached_time > self.ttl:
                    os.remove(filepath)
                    count += 1
            except Exception:
                # Invalid file, remove it
                os.remove(filepath)
                count += 1

        return count

    def get_stats(self) -> dict:
        """
        Get cache statistics

        Returns:
            Dictionary with cache statistics
        """
        total_files = 0
        total_size = 0
        expired = 0
        valid = 0

        for filename in os.listdir(self.cache_dir):
            if not filename.endswith(".json"):
                continue

            filepath = os.path.join(self.cache_dir, filename)
            total_files += 1
            total_size += os.path.getsize(filepath)

            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)

                cached_time = datetime.fromisoformat(data["cached_at"])
                if datetime.now() - cached_time > self.ttl:
                    expired += 1
                else:
                    valid += 1
            except Exception:
                expired += 1

        return {
            "total_files": total_files,
            "valid_files": valid,
            "expired_files": expired,
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "cache_dir": self.cache_dir,
        }


class TranscriptCache(Cache):
    """Specialized cache for video transcripts"""

    def __init__(self, cache_dir: str = None):
        """Initialize transcript cache with longer TTL"""
        if cache_dir is None:
            home = os.path.expanduser("~")
            cache_dir = os.path.join(home, ".cache", "yt-tool", "transcripts")

        # Transcripts don't change, cache for 30 days
        super().__init__(cache_dir, ttl_hours=24 * 30)

    def get_transcript(self, video_id: str) -> Optional[dict]:
        """
        Get cached transcript for a video

        Args:
            video_id: YouTube video ID

        Returns:
            Dictionary with 'segments' and 'language', or None
        """
        return self.get(f"transcript:{video_id}")

    def set_transcript(
        self, video_id: str, segments: list[dict], language: str
    ) -> None:
        """
        Cache transcript for a video

        Args:
            video_id: YouTube video ID
            segments: Transcript segments
            language: Transcript language
        """
        self.set(f"transcript:{video_id}", {
            "segments": segments,
            "language": language,
            "video_id": video_id,
        })


class AnalysisCache(Cache):
    """Specialized cache for analysis results"""

    def __init__(self, cache_dir: str = None):
        """Initialize analysis cache"""
        if cache_dir is None:
            home = os.path.expanduser("~")
            cache_dir = os.path.join(home, ".cache", "yt-tool", "analysis")

        # Analysis results cache for 7 days
        super().__init__(cache_dir, ttl_hours=24 * 7)

    def get_summary(self, video_id: str, style: str = "default") -> Optional[str]:
        """Get cached summary"""
        return self.get(f"summary:{video_id}:{style}")

    def set_summary(self, video_id: str, summary: str, style: str = "default") -> None:
        """Cache summary"""
        self.set(f"summary:{video_id}:{style}", summary)

    def get_chapters(self, video_id: str) -> Optional[list]:
        """Get cached chapters"""
        return self.get(f"chapters:{video_id}")

    def set_chapters(self, video_id: str, chapters: list) -> None:
        """Cache chapters"""
        self.set(f"chapters:{video_id}", chapters)

    def get_keypoints(self, video_id: str) -> Optional[str]:
        """Get cached key points"""
        return self.get(f"keypoints:{video_id}")

    def set_keypoints(self, video_id: str, keypoints: str) -> None:
        """Cache key points"""
        self.set(f"keypoints:{video_id}", keypoints)


# Global cache instances
_transcript_cache = None
_analysis_cache = None


def get_transcript_cache() -> TranscriptCache:
    """Get global transcript cache instance"""
    global _transcript_cache
    if _transcript_cache is None:
        _transcript_cache = TranscriptCache()
    return _transcript_cache


def get_analysis_cache() -> AnalysisCache:
    """Get global analysis cache instance"""
    global _analysis_cache
    if _analysis_cache is None:
        _analysis_cache = AnalysisCache()
    return _analysis_cache
