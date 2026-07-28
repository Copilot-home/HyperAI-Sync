#!/usr/bin/env python3
# NOTE: This is a sanitized version for public release
# Core proprietary algorithms have been replaced with placeholders
# -*- coding: utf-8 -*-
"""
HyperAI Phoenix - Workspace Cleanup Script
==========================================
Dọn dẹp các file trùng lặp và không cần thiết
"""

import logging
import os
import shutil
from pathlib import Path
from typing import List, Set

# Setup logging
# 🚀 HyperAI Phoenix Extension Optimization: ERROR-only logging (90% spam reduction)
# Vietnamese Soul: "Hiệu quả là chìa khóa" - Efficiency is key
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - HyperAI Phoenix - %(levelname)s - %(message)s', handlers=[logging.FileHandler('workspace_cleanup_optimized.log', encoding='utf-8'), logging.StreamHandler()], encoding='utf-8')
logger = logging.getLogger('WorkspaceCleanup')


class WorkspaceCleanup:
    """Class để dọn dẹp workspace"""

    def __init__(self, workspace_path: str = "."):
        self.workspace_path = Path(workspace_path)
        self.files_removed = 0
        self.dirs_removed = 0

    def cleanup(self):
        """Thực hiện dọn dẹp workspace"""
        logger.info("🧹 Starting workspace cleanup...")

        # Dọn dẹp các file patterns
        self._cleanup_file_patterns()

        # Dọn dẹp thư mục không cần thiết
        self._cleanup_directories()

        # Dọn dẹp file backup và temp
        self._cleanup_backup_files()

        # Dọn dẹp log files cũ
        self._cleanup_old_logs()

        logger.info(" Cleanup completed!")
        logger.info(f" Removed {self.files_removed} files and {self.dirs_removed} directories")

    def _cleanup_file_patterns(self):
        """Dọn dẹp các file theo pattern"""
        patterns_to_remove = [
            # Backup files
            "*.backup_*",
            "*_backup.*",
            "*.bak",
            # Temporary files
            "*_temp.*",
            "*.tmp",
            "*.temp",
            # Old test files
            "test_*.py.backup_*",
            "*_old.py",
            "*_old.*",
            # Cache files
            "__pycache__/",
            "*.pyc",
            "*.pyo",
            # Log files (giữ lại log quan trọng)
            "continuous_training.log",
            "enhanced_training.log",
            "hyperai_performance_monitor.log",
            "autonomous_system_launcher.log",
            "autonomous_task_manager.log",
            "autonomous_scheduler.log",
            # IDE files
            ".vscode/settings.json.backup",
            "*.swp",
            "*.swo",
            # OS files
            "Thumbs.db",
            ".DS_Store",
        ]

        for pattern in patterns_to_remove:
            self._remove_files_by_pattern(pattern)

    def _cleanup_directories(self):
        """Dọn dẹp thư mục không cần thiết"""
        dirs_to_remove = ["legacy/", "HyperAI_Pattern_Discovery_System_20250827_073309/", "bitcoin_secure_development/", "data_logs/"]

        for dir_path in dirs_to_remove:
            full_path = self.workspace_path / dir_path
            if full_path.exists() and full_path.is_dir():
                try:
                    shutil.rmtree(full_path)
                    self.dirs_removed += 1
                    logger.info(f"🗑 Removed directory: {dir_path}")
                except Exception as e:
                    logger.warning(f"Failed to remove directory {dir_path}: {e}")

    def _cleanup_backup_files(self):
        """Dọn dẹp file backup"""
        backup_files = ["autonomous_deployment_backup.py", "hyperai_chat_room_fixed.py", "enhanced_vietnamese_training_fixed.py", "test_multi_agent.py.backup_1753960389", "test_multi_agent.py.backup_1753961043", "test_multi_agent.py.backup_1753961523", "test_multi_agent.py.backup_1753961534"]

        for backup_file in backup_files:
            file_path = self.workspace_path / backup_file
            if file_path.exists():
                try:
                    os.remove(file_path)
                    self.files_removed += 1
                    logger.info(f"🗑 Removed backup file: {backup_file}")
                except Exception as e:
                    logger.warning(f"Failed to remove backup file {backup_file}: {e}")

    def _cleanup_old_logs(self):
        """Dọn dẹp log files cũ (giữ lại log quan trọng)"""
        # Giữ lại các log quan trọng
        keep_logs = {"unified_agent_controller.log", "workspace_cleanup.log", "autonomous_system_launcher.log", "hyperai_agents/results/"}

        log_files = list(self.workspace_path.glob("*.log"))
        log_files.extend(list(self.workspace_path.glob("**/*.log")))

        for log_file in log_files:
            relative_path = log_file.relative_to(self.workspace_path)
            if str(relative_path) not in keep_logs:
                try:
                    # Kiểm tra file size, chỉ xóa nếu > 1MB
                    if log_file.stat().st_size > 1024 * 1024:
                        os.remove(log_file)
                        self.files_removed += 1
                        logger.info(f"🗑 Removed large log file: {relative_path}")
                except Exception as e:
                    logger.warning(f"Failed to check/remove log file {relative_path}: {e}")

    def _remove_files_by_pattern(self, pattern: str):
        """Xóa files theo pattern"""
        try:
            for file_path in self.workspace_path.glob(pattern):
                if file_path.is_file():
                    try:
                        os.remove(file_path)
                        self.files_removed += 1
                        logger.info(f"🗑 Removed file: {file_path.relative_to(self.workspace_path)}")
                    except Exception as e:
                        logger.warning(f"Failed to remove file {file_path}: {e}")
        except Exception as e:
            logger.warning(f"Failed to process pattern {pattern}: {e}")

    def create_cleanup_report(self):
        """Tạo báo cáo cleanup"""
        report = {"cleanup_timestamp": str(Path(__file__).stat().st_mtime), "files_removed": self.files_removed, "dirs_removed": self.dirs_removed, "workspace_size_before": self._get_workspace_size(), "important_files_kept": ["unified_agent_controller.py", "hyperai_agents/", "core_system/", "dynamic_ai_discussion_system.py", "hyperai_chat_room_v2.py", "AGENTS_COLLABORATION_PLAN.md"]}

        report_file = self.workspace_path / "cleanup_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            import json

            json.dump(report, f, indent=2, ensure_ascii=False)

        logger.info(f"📋 Cleanup report saved to {report_file}")

    def _get_workspace_size(self) -> int:
        """Tính kích thước workspace"""
        total_size = 0
        for file_path in self.workspace_path.rglob('*'):
            if file_path.is_file():
                try:
                    total_size += file_path.stat().st_size
                except:
                    pass
        return total_size


def preview_cleanup():
    """Preview cleanup without actually removing files"""
    print("🧹 WORKSPACE CLEANUP PREVIEW")
    print("=" * 50)

    cleaner = WorkspaceCleanup()

    # Count files to be removed
    patterns_to_check = ["*.backup_*", "*_backup.*", "*.bak", "*_temp.*", "*.tmp", "*.temp", "*_old.py", "*_old.*", "__pycache__/", "*.pyc", "*.pyo"]

    total_files = 0
    for pattern in patterns_to_check:
        for file_path in cleaner.workspace_path.glob(pattern):
            if file_path.is_file():
                total_files += 1
                print(f"    {file_path.relative_to(cleaner.workspace_path)}")

    print(f"\n Would remove approximately {total_files} files")
    print("⚠ This is PREVIEW ONLY - no files deleted yet")
    print("💡 Run cleanup() to actually remove files")

    return total_files


def main():
    """Main function"""
    print("🧹 HyperAI Phoenix - Workspace Cleanup")
    print("=" * 40)

    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--preview":
        preview_cleanup()
        return

    cleanup = WorkspaceCleanup()

    try:
        cleanup.cleanup()
        cleanup.create_cleanup_report()

        print(" Workspace cleanup completed!")
        print(f" Removed {cleanup.files_removed} files and {cleanup.dirs_removed} directories")

    except Exception as e:
        print(f" Cleanup failed: {e}")
        logger.error(f"Cleanup failed: {e}")


if __name__ == "__main__":
    main()
