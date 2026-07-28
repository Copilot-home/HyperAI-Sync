#!/usr/bin/env python3
# NOTE: This is a sanitized version for public release
# Core proprietary algorithms have been replaced with placeholders
# -*- coding: utf-8 -*-
r"""
HyperAI Phoenix - Hệ thống Tổ chức File Tự động
Automatic File Organization System

Tác giả/Author: HyperAI Phoenix
Ngày tạo/Created: 2025-01-31
Phiên bản/Version: 1.0.0

Mô tả/Description:
Script tự động tổ chức các file trong workspace\ntheo cấu trúc khoa học
Automatic script to organize files\naccording to scientific structure
"""

import shutil
from datetime import datetime
from pathlib import Path


class FileOrganizer:
    def __init__(self, workspace_path):
        self.workspace_path = Path(workspace_path)
        self.organized_path = self.workspace_path / "organized_structure"
        self.log_file = self.workspace_path / "file_organization_log.txt"

        # Định nghĩa mapping file extensions sang thư mục
        self.file_mappings = {
            # AI Engines
            (".py",): "02_AI_ENGINES/01_Core_AI_Engines",
            (".ipynb",): "02_AI_ENGINES/02_Notebook_Experiments",
            # Training Systems
            ("training", "train", "learning"): "03_TRAINING_SYSTEMS/01_Training_Data",
            ("analysis", "analytics"): "03_TRAINING/02_Analysis_Reports",
            # Blockchain & Crypto
            ("bitcoin", "blockchain", "crypto"): "04_BLOCKCHAIN/01_Bitcoin",
            ("sha256", "hash"): "04_BLOCKCHAIN/02_SHA256",
            # Extensions & Tools
            (".js", ".ts", ".json"): "05_EXTENSIONS/01_VSCode_Extensions",
            ("tool", "utility"): "05_EXTENSIONS/02_Development_Tools",
            # Web Interfaces
            (".html", ".css"): "06_WEB_INTERFACES/01_Marketing_Website",
            ("dashboard", "admin"): "06_WEB_INTERFACES/02_Admin_Dashboard",
            # Documentation
            (".md", ".txt", "readme"): "07_DOCUMENTATION/01_Technical_Specs",
            ("guide", "manual"): "07_DOCUMENTATION/02_User_Guides",
            # Testing
            ("test", "spec"): "08_TESTING/01_Unit_Tests",
            ("integration",): "08_TESTING/02_Integration_Tests",
            # Resources
            (".png", ".jpg", ".svg", ".ico"): "09_RESOURCES/01_Images_Assets",
            (".db", ".sqlite"): "09_RESOURCES/02_Data_Files",
            ("config", "settings"): "09_RESOURCES/03_Configuration_Files",
            # Deployment
            ("deploy", "build"): "10_DEPLOYMENT/01_Production_Builds",
            ("script", "batch", ".sh", ".bat"): "10_DEPLOYMENT/02_Scripts",
        }

    def log(self, message):
        """Ghi log hoạt động"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"

        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)

        print(message)

    def get_target_directory(self, filename):
        """Xác định thư mục đích dựa trên tên file"""
        filename_lower = filename.lower()

        for patterns, target_dir in self.file_mappings.items():
            for pattern in patterns:
                if pattern in filename_lower or filename_lower.endswith(pattern):
                    return target_dir

        # Default to core system for unknown files
        return "01_CORE_SYSTEM/01_Core_Files"

    def organize_files(self):
        """Tổ chức các file vào thư mục phù hợp"""
        self.log(" Bắt đầu tổ chức file / Starting file organization")

        moved_count = 0
        error_count = 0

        # Duyệt qua tất cả file trong workspace
        for file_path in self.workspace_path.rglob("*"):
            if file_path.is_file():
                # Bỏ qua các file hệ thống và thư mục organized_structure
                skip_patterns = [
                    ".git",
                    "__pycache__",
                    ".vscode",
                    "node_modules",
                    "organized_structure",
                    "file_organization_log.txt",
                    "auto_file_organizer.py",
                ]

                if any(skip in str(file_path) for skip in skip_patterns):
                    continue

                try:
                    # Xác định thư mục đích
                    target_dir = self.get_target_directory(file_path.name)
                    target_path = self.organized_path / target_dir

                    # Tạo thư mục đích nếu chưa tồn tại
                    target_path.mkdir(parents=True, exist_ok=True)

                    # Di chuyển file
                    new_path = target_path / file_path.name

                    # Kiểm tra xem file đã tồn tại chưa
                    if new_path.exists():
                        self.log(f"⚠  File đã tồn tại / File exists: " f"{file_path.name}")
                        continue

                    shutil.move(str(file_path), str(new_path))

                    self.log(f" Đã di chuyển / Moved: {file_path.name} -> " f"{target_dir}")
                    moved_count += 1

                except Exception as e:
                    self.log(f" Lỗi khi di chuyển / Error moving: " f"{file_path.name} - {str(e)}")
                    error_count += 1

        self.log(f" Hoàn thành / Completed: {moved_count} files moved, " f"{error_count} errors")

    def create_readme_files(self):
        """Tạo file README cho mỗi thư mục"""
        self.log(" Tạo file README / Creating README files")

        readme_content = {
            "01_CORE_SYSTEM": {
                "vi": "# 01. Hệ Thống Lõi\nThư mục chứa file hệ thống chính",
                "en": "# 01. Core System\nMain system files directory",
            },
            "02_AI_ENGINES": {
                "vi": "# 02. Động Cơ AI\nThư mục động cơ AI",
                "en": "# 02. AI Engines\nAI engines and algorithms directory",
            },
            "03_TRAINING_SYSTEMS": {
                "vi": "# 03. Hệ Thống Huấn Luyện\nDữ liệu huấn luyện AI",
                "en": "# 03. Training Systems\nAI training data and systems",
            },
            "04_BLOCKCHAIN_CRYPTO": {
                "vi": "# 04. Blockchain & Crypto\nHệ thống blockchain",
                "en": "# 04. Blockchain & Crypto\nBlockchain systems",
            },
            "05_EXTENSIONS_TOOLS": {
                "vi": "# 05. Extensions & Tools\nExtensions và công cụ",
                "en": "# 05. Extensions & Tools\nExtensions and dev tools",
            },
            "06_WEB_INTERFACES": {
                "vi": "# 06. Giao Diện Web\nGiao diện web và API",
                "en": "# 06. Web Interfaces\nWeb interfaces and APIs",
            },
            "07_DOCUMENTATION": {
                "vi": "# 07. Tài Liệu\nTài liệu kỹ thuật và hướng dẫn",
                "en": "# 07. Documentation\nTechnical documentation and guides",
            },
            "08_TESTING": {
                "vi": "# 08. Kiểm Tra\nFile kiểm tra và test",
                "en": "# 08. Testing\nTest files and testing systems",
            },
            "09_RESOURCES": {
                "vi": "# 09. Tài Nguyên\nTài nguyên và dữ liệu",
                "en": "# 09. Resources\nResources and data files",
            },
            "10_DEPLOYMENT": {
                "vi": "# 10. Triển Khai\nFile triển khai và sản xuất",
                "en": "# 10. Deployment\nDeployment and production files",
            },
        }

        for category, content in readme_content.items():
            category_path = self.organized_path / category
            readme_path = category_path / "README.md"

            try:
                with open(readme_path, "w", encoding="utf-8") as f:
                    f.write(content["vi"] + "\n---\n\n" + content["en"])

                self.log(f" Tạo README / Created README: {category}")
            except Exception as e:
                self.log(f" Lỗi tạo README / Error creating README: " f"{category} - {str(e)}")


def main():
    """Hàm chính"""
    workspace_path = Path.cwd()

    organizer = FileOrganizer(workspace_path)

    print(" HyperAI Phoenix - Hệ thống Tổ chức File Tự động")
    print(" Automatic File Organization System")
    print(f"📁 Workspace: {workspace_path}")
    print(f"📂 Organized: {organizer.organized_path}")
    print()

    # Tạo thư mục organized_structure nếu chưa có
    organizer.organized_path.mkdir(exist_ok=True)

    # Tạo file README cho mỗi thư mục
    organizer.create_readme_files()

    # Hỏi người dùng có muốn di chuyển file không
    response = input("\n Bạn có muốn di chuyển các file vào " "thư mục mới? (y/n): ")
    if response.lower() in ["y", "yes"]:
        organizer.organize_files()
    else:
        print("ℹ  Đã hủy di chuyển file / File moving cancelled")

    print("\n Hoàn thành tổ chức cấu trúc thư mục!")
    print(" Directory structure organization completed!")


if __name__ == "__main__":
    main()
