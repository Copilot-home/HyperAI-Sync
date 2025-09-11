#!/usr/bin/env python3
# NOTE: This is a sanitized version for public release
# Core proprietary algorithms have been replaced with placeholders
# -*- coding: utf-8 -*-
"""
HyperAI Phoenix - Script Di Chuyển File Đơn Giản
Simple File Moving Script

Tác giả/Author: HyperAI Phoenix
Ngày tạo/Created: 2025-01-31
"""

import os
import shutil
from pathlib import Path


def move_file_to_category(filename, source_path, organized_path):
    """Di chuyển file vào thư mục phù hợp"""
    filename_lower = filename.lower()

    # Mapping file extensions và keywords sang thư mục đích
    mappings = {
        # AI Engines
        ('.py',): '02_AI_ENGINES/01_Core_AI_Engines',
        ('.ipynb',): '02_AI_ENGINES/02_Notebook_Experiments',
        # Training Systems
        ('training', 'train', 'learning'): '03_TRAINING_SYSTEMS/01_Training_Data',
        ('analysis', 'analytics'): '03_TRAINING_SYSTEMS/02_Analysis_Reports',
        # Blockchain & Crypto
        ('bitcoin', 'blockchain', 'crypto'): '04_BLOCKCHAIN_CRYPTO/01_Bitcoin_Systems',
        ('sha256', 'hash'): '04_BLOCKCHAIN_CRYPTO/02_SHA256_Algorithms',
        # Extensions & Tools
        ('.js', '.ts', '.json'): '05_EXTENSIONS_TOOLS/01_VSCode_Extensions',
        ('tool', 'utility'): '05_EXTENSIONS_TOOLS/02_Development_Tools',
        # Web Interfaces
        ('.html', '.css'): '06_WEB_INTERFACES/01_Marketing_Website',
        ('dashboard', 'admin'): '06_WEB_INTERFACES/02_Admin_Dashboard',
        # Documentation
        ('.md', '.txt', 'readme'): '07_DOCUMENTATION/01_Technical_Specs',
        ('guide', 'manual'): '07_DOCUMENTATION/02_User_Guides',
        # Testing
        ('test', 'spec'): '08_TESTING/01_Unit_Tests',
        ('integration',): '08_TESTING/02_Integration_Tests',
        # Resources
        ('.png', '.jpg', '.svg', '.ico'): '09_RESOURCES/01_Images_Assets',
        ('.db', '.sqlite'): '09_RESOURCES/02_Data_Files',
        ('config', 'settings'): '09_RESOURCES/03_Configuration_Files',
        # Deployment
        ('deploy', 'build'): '10_DEPLOYMENT/01_Production_Builds',
        ('script', 'batch', '.sh', '.bat'): '10_DEPLOYMENT/02_Deployment_Scripts',
    }

    target_dir = '01_CORE_SYSTEM/01_Core_Files'  # Default

    for patterns, target in mappings.items():
        for pattern in patterns:
            if pattern in filename_lower or filename_lower.endswith(pattern):
                target_dir = target
                break

    # Tạo thư mục đích
    target_path = organized_path / target_dir
    target_path.mkdir(parents=True, exist_ok=True)

    # Di chuyển file
    dest_file = target_path / filename
    if not dest_file.exists():
        shutil.move(str(source_path / filename), str(dest_file))
        print(f" Moved: {filename} -> {target_dir}")
        return True
    else:
        print(f"⚠  Skipped (exists): {filename}")
        return False


def main():
    workspace_path = Path.cwd()
    organized_path = workspace_path / "organized_structure"

    print(" HyperAI Phoenix - Di chuyển file đơn giản")
    print(" Simple File Moving Script")
    print(f"📁 Workspace: {workspace_path}")
    print()

    moved_count = 0
    skipped_count = 0

    # Duyệt qua tất cả file trong thư mục gốc
    for item in workspace_path.iterdir():
        if item.is_file():
            # Bỏ qua các file hệ thống
            skip_files = ['auto_file_organizer.py', 'file_organization_log.txt', 'simple_move.py']

            if item.name in skip_files:
                continue

            # Bỏ qua các thư mục ẩn và hệ thống
            if item.name.startswith('.') or item.name in ['__pycache__', 'node_modules']:
                continue

            try:
                if move_file_to_category(item.name, workspace_path, organized_path):
                    moved_count += 1
                else:
                    skipped_count += 1
            except Exception as e:
                print(f" Error moving {item.name}: {str(e)}")

    print()
    print(f" Kết quả / Results:")
    print(f"    Đã di chuyển / Moved: {moved_count} files")
    print(f"   ⚠  Bỏ qua / Skipped: {skipped_count} files")
    print()
    print(" Hoàn thành! / Completed!")


if __name__ == "__main__":
    main()
