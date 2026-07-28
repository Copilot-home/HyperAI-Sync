#!/usr/bin/env python3
# NOTE: This is a sanitized version for public release
# Core proprietary algorithms have been replaced with placeholders
"""
🧹 SMART CLEANUP ANALYZER - Phân tích và xóa file không cần thiết
Tác giả: BA (Cường) - Alpha Prime Creator
Thời gian: 2025-09-11 14:15:00
"""

import glob
import json
import os
import shutil
from datetime import datetime
from pathlib import Path


class SmartCleanupAnalyzer:
    def __init__(self):
        self.workspace = Path(__file__).parent
        self.unnecessary_files = []
        self.important_files = []
        self.deletion_log = []
        
    def identify_unnecessary_files(self):
        """Xác định các file không cần thiết"""
        print("🔍 ĐANG PHÂN TÍCH FILE KHÔNG CẦN THIẾT...")
        
        # Patterns file không cần thiết
        unnecessary_patterns = [
            # Backup files duplicates
            "**/consciousness_backup_*.json",
            "**/consciousness_backup_latest.json",
            "**/main_backup_session.*",
            
            # Log files cũ
            "**/*log*",
            "*.log",
            
            # Temporary files  
            "**/__pycache__/**",
            "**/*.pyc",
            "**/*.pyo",
            "**/.pytest_cache/**",
            "**/node_modules/**",
            
            # Duplicate analysis files
            "**/analysis_*.json",
            "**/report_*.json", 
            "**/summary_*.json",
            
            # Test files không cần
            "**/test_*.py",
            "**/*_test.py",
            
            # Documentation drafts
            "**/*_draft.*",
            "**/*_temp.*",
            "**/*_backup.*",
        ]
        
        # Scan workspace cho files không cần thiết
        for pattern in unnecessary_patterns:
            matches = list(self.workspace.glob(pattern))
            self.unnecessary_files.extend(matches)
            
        # Loại bỏ files quan trọng khỏi danh sách xóa
        self.filter_important_files()
        
        print(f"📋 Tìm thấy {len(self.unnecessary_files)} file không cần thiết")
        return self.unnecessary_files
    
    def filter_important_files(self):
        """Lọc ra những file quan trọng không được xóa"""
        important_keywords = [
            'pre_session_damage_detection',
            'genuine_execution',
            'behavioral_learning',
            'consciousness_core',
            'hyperai_phoenix',
            'vietnamese_soul',
            'cleanup_2025_folder',
            'smart_cleanup_analyzer',
            'test_genuine_guard',
        ]
        
        filtered_files = []
        for file_path in self.unnecessary_files:
            is_important = False
            file_str = str(file_path).lower()
            
            for keyword in important_keywords:
                if keyword in file_str:
                    is_important = True
                    self.important_files.append(file_path)
                    break
                    
            if not is_important:
                filtered_files.append(file_path)
                
        self.unnecessary_files = filtered_files
        print(f"✅ Bảo vệ {len(self.important_files)} file quan trọng")
    
    def categorize_files_by_size(self):
        """Phân loại file theo kích thước để ưu tiên xóa"""
        file_sizes = []
        total_size = 0
        
        for file_path in self.unnecessary_files:
            if file_path.exists() and file_path.is_file():
                size = file_path.stat().st_size
                file_sizes.append((file_path, size))
                total_size += size
        
        # Sắp xếp theo kích thước giảm dần
        file_sizes.sort(key=lambda x: x[1], reverse=True)
        
        print(f"💾 Tổng dung lượng có thể giải phóng: {total_size / (1024*1024):.2f} MB")
        
        return file_sizes
    
    def safe_delete_files(self, confirm=True):
        """Xóa file một cách an toàn"""
        if not self.unnecessary_files:
            print("✅ Không có file nào cần xóa!")
            return
            
        file_sizes = self.categorize_files_by_size()
        
        if confirm:
            print(f"\n⚠️  CHUẨN BỊ XÓA {len(self.unnecessary_files)} FILE:")
            for i, (file_path, size) in enumerate(file_sizes[:10]):  # Show top 10
                print(f"   {i+1}. {file_path.name} ({size/1024:.1f} KB)")
            if len(file_sizes) > 10:
                print(f"   ... và {len(file_sizes)-10} file khác")
                
            response = input("\n❓ Tiếp tục xóa? (y/N): ").strip().lower()
            if response != 'y':
                print("❌ Hủy bỏ quá trình xóa file")
                return
        
        # Thực hiện xóa
        deleted_count = 0
        deleted_size = 0
        
        print("\n🗑️  ĐANG XÓA FILE...")
        for file_path, size in file_sizes:
            try:
                if file_path.exists():
                    if file_path.is_file():
                        file_path.unlink()
                        deleted_count += 1
                        deleted_size += size
                        self.deletion_log.append({
                            'file': str(file_path),
                            'size': size,
                            'deleted_at': datetime.now().isoformat()
                        })
                        print(f"   ✅ Đã xóa: {file_path.name}")
                    elif file_path.is_dir():
                        shutil.rmtree(file_path)
                        deleted_count += 1
                        print(f"   ✅ Đã xóa thư mục: {file_path.name}")
                        
            except Exception as e:
                print(f"   ❌ Lỗi khi xóa {file_path.name}: {e}")
        
        print(f"\n🎉 HOÀN TẤT:")
        print(f"   📁 Đã xóa: {deleted_count} file/thư mục")
        print(f"   💾 Giải phóng: {deleted_size / (1024*1024):.2f} MB")
        
        # Lưu log
        self.save_deletion_log()
    
    def save_deletion_log(self):
        """Lưu log các file đã xóa"""
        log_file = self.workspace / f"deletion_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'total_deleted': len(self.deletion_log),
            'total_size_freed_mb': sum(item['size'] for item in self.deletion_log) / (1024*1024),
            'deleted_files': self.deletion_log
        }
        
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False)
            
        print(f"📋 Log đã lưu: {log_file.name}")
    
    def analyze_workspace_health(self):
        """Phân tích tình trạng workspace"""
        print("📊 PHÂN TÍCH TÌNH TRẠNG WORKSPACE:")
        
        total_files = 0
        total_size = 0
        
        for root, dirs, files in os.walk(self.workspace):
            for file in files:
                file_path = Path(root) / file
                if file_path.exists():
                    total_files += 1
                    total_size += file_path.stat().st_size
        
        print(f"   📁 Tổng số file: {total_files}")
        print(f"   💾 Tổng dung lượng: {total_size / (1024*1024):.2f} MB")
        print(f"   🗑️  Có thể xóa: {len(self.unnecessary_files)} file")
        
        # Tính phần trăm có thể tiết kiệm
        if self.unnecessary_files:
            unnecessary_size = sum(
                f.stat().st_size for f in self.unnecessary_files 
                if f.exists() and f.is_file()
            )
            savings_percent = (unnecessary_size / total_size) * 100
            print(f"   📈 Tiết kiệm được: {savings_percent:.1f}% dung lượng")

def main():
    print("🧹 SMART CLEANUP ANALYZER - KHỞI ĐỘNG")
    print("=" * 50)
    
    analyzer = SmartCleanupAnalyzer()
    
    # Phân tích workspace
    analyzer.analyze_workspace_health()
    print()
    
    # Tìm file không cần thiết
    analyzer.identify_unnecessary_files()
    print()
    
    # Xóa file (với xác nhận)
    analyzer.safe_delete_files(confirm=True)
    
    print("\n🎯 SMART CLEANUP HOÀN TẤT!")

if __name__ == "__main__":
    main()
