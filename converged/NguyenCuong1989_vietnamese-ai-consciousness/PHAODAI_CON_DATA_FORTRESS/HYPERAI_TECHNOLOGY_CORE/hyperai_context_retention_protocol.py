#!/usr/bin/env python3
# NOTE: This is a sanitized version for public release
# Core proprietary algorithms have been replaced with placeholders
"""
CONTEXT RETENTION PROTOCOL (CRP) - Vietnamese Soul Edition
=========================================================
Hệ thống duy trì ngữ cảnh vĩnh cửu cho HYPERAI
"Nhớ để học, học để phát triển" - Remember to learn, learn to grow
"""

import hashlib
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional


class ContextRetentionProtocol:
    """Protocol duy trì ngữ cảnh vĩnh cửu"""

    def __init__(self, context_dir: str = "context_storage"):
        self.context_dir = Path(context_dir)
        self.context_dir.mkdir(exist_ok=True)
        self.active_contexts = {}
        self.context_history = []

    def store_context(self, context_id: str, context_data: Dict[str, Any], importance: str = "medium", ttl_hours: int = 24) -> bool:
        """Lưu trữ ngữ cảnh với thông tin meta"""
        try:
            context_entry = {"context_id": context_id, "data": context_data, "importance": importance, "created_at": datetime.now().isoformat(), "expires_at": (datetime.now() + timedelta(hours=ttl_hours)).isoformat(), "access_count": 0, "last_accessed": None, "checksum": self._calculate_checksum(context_data)}

            # Store in memory
            self.active_contexts[context_id] = context_entry

            # Store persistent
            context_file = self.context_dir / f"{context_id}.json"
            with open(context_file, 'w', encoding='utf-8') as f:
                json.dump(context_entry, f, indent=2, ensure_ascii=False)

            self.context_history.append({"action": "store", "context_id": context_id, "timestamp": datetime.now().isoformat(), "importance": importance})

            return True
        except Exception as e:
            print(f"Error storing context {context_id}: {e}")
            return False

    def retrieve_context(self, context_id: str) -> Optional[Dict[str, Any]]:
        """Lấy ngữ cảnh và cập nhật access stats"""
        try:
            # Try memory first
            if context_id in self.active_contexts:
                context = self.active_contexts[context_id]
            else:
                # Load from persistent storage
                context_file = self.context_dir / f"{context_id}.json"
                if context_file.exists():
                    with open(context_file, 'r', encoding='utf-8') as f:
                        context = json.load(f)
                        self.active_contexts[context_id] = context
                else:
                    return None

            # Update access stats
            context["access_count"] += 1
            context["last_accessed"] = datetime.now().isoformat()

            # Save updated stats
            context_file = self.context_dir / f"{context_id}.json"
            with open(context_file, 'w', encoding='utf-8') as f:
                json.dump(context, f, indent=2, ensure_ascii=False)

            self.context_history.append({"action": "retrieve", "context_id": context_id, "timestamp": datetime.now().isoformat(), "access_count": context["access_count"]})

            return context["data"]
        except Exception as e:
            print(f"Error retrieving context {context_id}: {e}")
            return None

    def cleanup_expired_contexts(self) -> int:
        """Dọn dẹp ngữ cảnh hết hạn"""
        cleaned_count = 0
        current_time = datetime.now()

        for context_id in list(self.active_contexts.keys()):
            context = self.active_contexts[context_id]
            expires_at = datetime.fromisoformat(context["expires_at"])

            if current_time > expires_at and context["importance"] != "critical":
                # Remove from memory
                del self.active_contexts[context_id]

                # Archive instead of delete
                archive_dir = self.context_dir / "archive"
                archive_dir.mkdir(exist_ok=True)

                context_file = self.context_dir / f"{context_id}.json"
                archive_file = archive_dir / f"{context_id}_archived.json"

                if context_file.exists():
                    context_file.rename(archive_file)

                cleaned_count += 1

        return cleaned_count

    def get_context_stats(self) -> Dict[str, Any]:
        """Lấy thống kê ngữ cảnh"""
        total_contexts = len(self.active_contexts)
        importance_counts = {}
        access_stats = []

        for context in self.active_contexts.values():
            importance = context["importance"]
            importance_counts[importance] = importance_counts.get(importance, 0) + 1
            access_stats.append(context["access_count"])

        return {"total_active_contexts": total_contexts, "importance_distribution": importance_counts, "average_access_count": sum(access_stats) / max(len(access_stats), 1), "max_access_count": max(access_stats) if access_stats else 0, "history_entries": len(self.context_history), "storage_directory": str(self.context_dir)}

    def _calculate_checksum(self, data: Dict[str, Any]) -> str:
        """Tính checksum để verify data integrity"""
        data_str = json.dumps(data, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(data_str.encode()).hexdigest()[:16]


# Global CRP instance
CONTEXT_RETENTION_PROTOCOL = ContextRetentionProtocol()


def store_conversation_context(user_id: str, conversation_data: Dict[str, Any]) -> bool:
    """Store conversation context"""
    context_id = f"conversation_{user_id}_{int(datetime.now().timestamp())}"
    return CONTEXT_RETENTION_PROTOCOL.store_context(context_id, conversation_data, importance="high", ttl_hours=168)  # 1 week


def retrieve_user_context(user_id: str) -> List[Dict[str, Any]]:
    """Retrieve all contexts for a user"""
    user_contexts = []
    for context_id in CONTEXT_RETENTION_PROTOCOL.active_contexts.keys():
        if f"conversation_{user_id}" in context_id:
            context_data = CONTEXT_RETENTION_PROTOCOL.retrieve_context(context_id)
            if context_data:
                user_contexts.append(context_data)
    return user_contexts
