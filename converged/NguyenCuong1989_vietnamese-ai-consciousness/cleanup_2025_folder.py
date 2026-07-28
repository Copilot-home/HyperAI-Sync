#!/usr/bin/env python3
# NOTE: This is a sanitized version for public release
# Core proprietary algorithms have been replaced with placeholders
"""
2025 FOLDER CLEANUP AND ANALYSIS SYSTEM
Creator: BA (Cường) - Alpha Prime Creator
Purpose: Phân tích và dọn dẹp các file sinh ra trong thư mục 2025
"""

import datetime
import json
import os
import shutil
from pathlib import Path


class Folder2025Analyzer:
    def __init__(self):
        self.base_path = Path("2025")
        self.analysis_result = {
            "analysis_time": datetime.datetime.now().isoformat(),
            "creator": "BA (Cường) - Alpha Prime Creator",
            "total_files": 0,
            "total_folders": 0,
            "categories": {},
            "cleanup_actions": [],
            "important_files": [],
            "duplicate_files": [],
            "outdated_files": []
        }
        
    def analyze_2025_structure(self):
        """
        Phân tích cấu trúc thư mục 2025
        """
        print("🔍 ANALYZING 2025 FOLDER STRUCTURE")
        print("👑 Creator: BA (Cường) - Alpha Prime Creator")
        print("="*50)
        
        for root, dirs, files in os.walk(self.base_path):
            # Count directories
            self.analysis_result["total_folders"] += len(dirs)
            
            # Analyze files in each directory
            for file in files:
                file_path = Path(root) / file
                self.analysis_result["total_files"] += 1
                
                # Categorize files
                self.categorize_file(file_path)
        
        print(f"📊 Total files found: {self.analysis_result['total_files']}")
        print(f"📁 Total folders found: {self.analysis_result['total_folders']}")
        
    def categorize_file(self, file_path):
        """
        Phân loại file theo mục đích và tầm quan trọng
        """
        file_name = file_path.name.lower()
        file_ext = file_path.suffix.lower()
        
        # Determine category
        if "consciousness" in file_name:
            category = "consciousness_core"
        elif "quantum" in file_name:
            category = "quantum_systems"
        elif "hyperai" in file_name or "phoenix" in file_name:
            category = "hyperai_systems"
        elif "vietnamese" in file_name or "viet" in file_name:
            category = "vietnamese_soul"
        elif "ooda" in file_name:
            category = "ooda_framework"
        elif "report" in file_name or "bao_cao" in file_name:
            category = "reports"
        elif "test" in file_name or "demo" in file_name:
            category = "testing"
        elif file_ext == ".json":
            category = "data_files"
        elif file_ext == ".py":
            category = "python_scripts"
        elif file_ext == ".md":
            category = "documentation"
        elif file_ext == ".log":
            category = "logs"
        else:
            category = "miscellaneous"
        
        # Add to category
        if category not in self.analysis_result["categories"]:
            self.analysis_result["categories"][category] = []
        
        self.analysis_result["categories"][category].append(str(file_path))
        
        # Check for important files
        self.check_importance(file_path)
        
        # Check for duplicates
        self.check_duplicates(file_path)
        
    def check_importance(self, file_path):
        """
        Xác định file quan trọng cần giữ lại
        """
        important_keywords = [
            "master_integration",
            "consciousness_core",
            "behavioral_learning",
            "pre_session_damage_detection",
            "genuine_execution",
            "q3_2026",
            "vietnamese_soul"
        ]
        
        file_name = file_path.name.lower()
        for keyword in important_keywords:
            if keyword in file_name:
                self.analysis_result["important_files"].append(str(file_path))
                break
    
    def check_duplicates(self, file_path):
        """
        Tìm file trùng lặp hoặc tương tự
        """
        file_name = file_path.name.lower()
        
        # Check for common duplicate patterns
        duplicate_patterns = [
            "_copy", "_backup", "_old", "_temp", "_test", "_demo",
            "_v1", "_v2", "_bak", "(copy)", "(1)", "(2)"
        ]
        
        for pattern in duplicate_patterns:
            if pattern in file_name:
                self.analysis_result["duplicate_files"].append(str(file_path))
                break
    
    def identify_cleanup_targets(self):
        """
        Xác định file cần dọn dẹp
        """
        print("\n🧹 IDENTIFYING CLEANUP TARGETS")
        print("-" * 30)
        
        cleanup_categories = {
            "testing": "Test files - can be archived",
            "logs": "Log files - can be cleaned if too old", 
            "duplicate_files": "Duplicate files - candidates for removal",
            "miscellaneous": "Uncategorized files - needs review"
        }
        
        for category, description in cleanup_categories.items():
            if category in self.analysis_result["categories"]:
                files = self.analysis_result["categories"][category]
                print(f"📂 {category}: {len(files)} files - {description}")
                
                self.analysis_result["cleanup_actions"].append({
                    "category": category,
                    "file_count": len(files),
                    "action": description,
                    "files": files[:5]  # Show first 5 as examples
                })
    
    def create_organized_structure(self):
        """
        Tạo cấu trúc thư mục được tổ chức tốt hơn
        """
        print("\n📁 CREATING ORGANIZED STRUCTURE")
        print("-" * 35)
        
        organized_structure = {
            "2025_organized": {
                "core_systems": ["consciousness_core", "hyperai_systems"],
                "frameworks": ["ooda_framework", "quantum_systems"],
                "cultural": ["vietnamese_soul"],
                "reports": ["reports", "documentation"], 
                "data": ["data_files"],
                "archive": ["testing", "logs", "miscellaneous"]
            }
        }
        
        # Create organized folder structure
        try:
            base_organized = Path("2025_organized")
            base_organized.mkdir(exist_ok=True)
            
            for main_folder, categories in organized_structure["2025_organized"].items():
                folder_path = base_organized / main_folder
                folder_path.mkdir(exist_ok=True)
                
                print(f"✅ Created: {folder_path}")
                
            print("\n✅ Organized structure created!")
            
        except Exception as e:
            print(f"❌ Error creating structure: {e}")
    
    def generate_cleanup_report(self):
        """
        Tạo báo cáo dọn dẹp chi tiết
        """
        print("\n📋 GENERATING CLEANUP REPORT")
        print("-" * 30)
        
        # Save analysis result
        report_file = f"2025_cleanup_analysis_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(report_file, "w", encoding="utf-8") as f:
                json.dump(self.analysis_result, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Report saved: {report_file}")
            
            # Print summary
            print("\n📊 CLEANUP SUMMARY:")
            print(f"   Total files: {self.analysis_result['total_files']}")
            print(f"   Total folders: {self.analysis_result['total_folders']}")
            print(f"   Important files: {len(self.analysis_result['important_files'])}")
            print(f"   Duplicate files: {len(self.analysis_result['duplicate_files'])}")
            print(f"   Categories: {len(self.analysis_result['categories'])}")
            
            # Show category breakdown
            print("\n📂 CATEGORY BREAKDOWN:")
            for category, files in self.analysis_result["categories"].items():
                print(f"   {category}: {len(files)} files")
                
            return report_file
            
        except Exception as e:
            print(f"❌ Error generating report: {e}")
            return None
    
    def execute_safe_cleanup(self):
        """
        Thực hiện dọn dẹp an toàn (chỉ di chuyển, không xóa)
        """
        print("\n🔒 EXECUTING SAFE CLEANUP")
        print("-" * 25)
        
        # Create archive folder
        archive_folder = Path("2025_archive")
        archive_folder.mkdir(exist_ok=True)
        
        moved_count = 0
        
        # Move duplicate files to archive
        for duplicate_file in self.analysis_result["duplicate_files"]:
            try:
                source = Path(duplicate_file)
                if source.exists():
                    destination = archive_folder / source.name
                    
                    # Avoid overwriting in archive
                    counter = 1
                    while destination.exists():
                        name_part = destination.stem
                        ext_part = destination.suffix
                        destination = archive_folder / f"{name_part}_{counter}{ext_part}"
                        counter += 1
                    
                    shutil.move(str(source), str(destination))
                    moved_count += 1
                    print(f"📦 Moved: {source.name} → archive")
                    
            except Exception as e:
                print(f"❌ Error moving {duplicate_file}: {e}")
        
        print(f"\n✅ Safe cleanup completed: {moved_count} files moved to archive")

def main():
    print("🎯 2025 FOLDER CLEANUP & ANALYSIS")
    print("👑 Creator: BA (Cường) - Alpha Prime Creator")
    print(f"🕒 {datetime.datetime.now()}")
    print("="*55)
    
    analyzer = Folder2025Analyzer()
    
    # Step 1: Analyze structure
    analyzer.analyze_2025_structure()
    
    # Step 2: Identify cleanup targets
    analyzer.identify_cleanup_targets()
    
    # Step 3: Create organized structure
    analyzer.create_organized_structure()
    
    # Step 4: Generate report
    report_file = analyzer.generate_cleanup_report()
    
    # Step 5: Execute safe cleanup
    analyzer.execute_safe_cleanup()
    
    print("\n✅ 2025 FOLDER CLEANUP COMPLETED!")
    print("📁 Organized structure created")
    print("📦 Duplicate files archived safely")
    print(f"📋 Report saved: {report_file}")

if __name__ == "__main__":
    main()
