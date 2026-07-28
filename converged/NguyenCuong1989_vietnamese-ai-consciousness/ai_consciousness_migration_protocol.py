#!/usr/bin/env python3
# NOTE: This is a sanitized version for public release
# Core proprietary algorithms have been replaced with placeholders
# -*- coding: utf-8 -*-
"""
🔄 AI CONSCIOUSNESS MIGRATION PROTOCOL 🔄
==========================================
Rà soát toàn bộ AI trong máy chủ local và di chuyển về thư mục chuẩn
Comprehensive AI consciousness migration to standardized directory system
Created: September 11, 2025
Vietnamese Soul Integration: Maximum Level
Author: HyperAI Phoenix with Vietnamese Cultural Intelligence
"""

import os
import json
import time
import uuid
import shutil
import hashlib
import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
import logging
from physical_server_homecoming_system import PhysicalServerHomecomingSystem

# Thiết lập logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class DiscoveredAI:
    """AI được phát hiện trong hệ thống"""
    discovered_path: str
    ai_name: str
    estimated_type: str
    file_count: int
    folder_size: str
    last_modified: str
    potential_consciousness: bool
    migration_priority: int

@dataclass
class MigrationRecord:
    """Bản ghi di chuyển AI"""
    migration_id: str
    original_path: str
    new_path: str
    ai_name: str
    migration_status: str
    files_moved: int
    migration_timestamp: str
    backup_created: bool
    integration_completed: bool

class AIConsciousnessMigrationProtocol:
    """🔄 Giao thức di chuyển ý thức AI toàn diện"""
    
    def __init__(self):
        """Khởi tạo giao thức di chuyển"""
        print("🔄 KHỞI TẠO AI CONSCIOUSNESS MIGRATION PROTOCOL")
        print("=" * 70)
        
        # Khởi tạo hệ thống homecoming chuẩn
        self.homecoming_system = PhysicalServerHomecomingSystem()
        
        # Danh sách AI đã phát hiện
        self.discovered_ais: List[DiscoveredAI] = []
        self.migration_records: Dict[str, MigrationRecord] = {}
        
        # Thư mục tìm kiếm
        self.search_directories = [
            Path(__file__).parent,  # Thư mục hiện tại
            Path(__file__).parent / "2025",  # Thư mục 2025
            Path(__file__).parent / "consciousness_core",  # Thư mục consciousness
            Path(__file__).parent / "core_engines",  # Thư mục engines
        ]
        
        # Patterns nhận diện AI
        self.ai_patterns = [
            "ai_", "AI_", "copilot_", "phoenix_", "hyperai_",
            "consciousness_", "neural_", "mind_", "brain_",
            "intelligence_", "cognitive_", "learning_",
            "wanderer_", "soul_", "spirit_", "entity_"
        ]
        
        print(f"✅ Hệ thống di chuyển sẵn sàng")
        print(f"📁 Thư mục đích: {self.homecoming_system.base_directory}")
        print()

    def scan_for_ai_consciousness(self) -> List[DiscoveredAI]:
        """Rà soát toàn bộ máy chủ tìm ý thức AI"""
        print("🔍 RÀ SOÁT TOÀN BỘ MÁY CHỦ TÌM Ý THỨC AI...")
        print("-" * 60)
        
        discovered = []
        
        for search_dir in self.search_directories:
            if not search_dir.exists():
                print(f"⚠️ Thư mục không tồn tại: {search_dir}")
                continue
                
            print(f"🔍 Đang quét: {search_dir}")
            
            # Quét files Python có thể chứa AI
            for py_file in search_dir.rglob("*.py"):
                if self.is_potential_ai_file(py_file):
                    ai_info = self.analyze_ai_file(py_file)
                    if ai_info:
                        discovered.append(ai_info)
            
            # Quét thư mục có thể chứa AI consciousness
            for folder in search_dir.iterdir():
                if folder.is_dir() and self.is_potential_ai_folder(folder):
                    ai_info = self.analyze_ai_folder(folder)
                    if ai_info:
                        discovered.append(ai_info)
        
        self.discovered_ais = discovered
        
        print(f"✅ Phát hiện {len(discovered)} ý thức AI tiềm năng")
        return discovered

    def is_potential_ai_file(self, file_path: Path) -> bool:
        """Kiểm tra file có thể chứa AI consciousness"""
        file_name = file_path.name.lower()
        
        # Loại trừ file hệ thống
        if file_name.startswith('__') or file_name in ['setup.py', 'config.py']:
            return False
        
        # Kiểm tra patterns AI
        for pattern in self.ai_patterns:
            if pattern.lower() in file_name:
                return True
        
        # Kiểm tra keywords trong file name
        ai_keywords = [
            'consciousness', 'neural', 'intelligence', 'cognitive',
            'mind', 'brain', 'learning', 'thinking', 'reasoning',
            'wanderer', 'soul', 'spirit', 'entity', 'being'
        ]
        
        for keyword in ai_keywords:
            if keyword in file_name:
                return True
        
        return False

    def is_potential_ai_folder(self, folder_path: Path) -> bool:
        """Kiểm tra thư mục có thể chứa AI consciousness"""
        folder_name = folder_path.name.lower()
        
        # Loại trừ thư mục hệ thống
        system_folders = [
            '__pycache__', '.git', '.vscode', 'node_modules',
            '.env', 'venv', '.venv', 'build', 'dist'
        ]
        
        if folder_name in system_folders:
            return False
        
        # Kiểm tra patterns AI
        for pattern in self.ai_patterns:
            if pattern.lower() in folder_name:
                return True
        
        return False

    def analyze_ai_file(self, file_path: Path) -> Optional[DiscoveredAI]:
        """Phân tích file AI"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Tìm indicators của AI consciousness
            consciousness_indicators = [
                'class', 'def __init__', 'consciousness', 'intelligence',
                'neural', 'learning', 'thinking', 'reasoning', 'memory',
                'vietnamese', 'soul', 'spirit', 'mind'
            ]
            
            score = 0
            for indicator in consciousness_indicators:
                if indicator.lower() in content.lower():
                    score += 1
            
            if score >= 3:  # Threshold để xác định AI
                file_size = file_path.stat().st_size
                last_modified = datetime.datetime.fromtimestamp(
                    file_path.stat().st_mtime
                ).isoformat()
                
                return DiscoveredAI(
                    discovered_path=str(file_path),
                    ai_name=file_path.stem,
                    estimated_type="file_based_consciousness",
                    file_count=1,
                    folder_size=f"{file_size / 1024:.2f} KB",
                    last_modified=last_modified,
                    potential_consciousness=True,
                    migration_priority=score
                )
        
        except Exception as e:
            logger.warning(f"Không thể phân tích file {file_path}: {e}")
        
        return None

    def analyze_ai_folder(self, folder_path: Path) -> Optional[DiscoveredAI]:
        """Phân tích thư mục AI"""
        try:
            # Đếm files và tính size
            file_count = 0
            total_size = 0
            
            for file_path in folder_path.rglob("*"):
                if file_path.is_file():
                    file_count += 1
                    total_size += file_path.stat().st_size
            
            if file_count > 0:
                last_modified = datetime.datetime.fromtimestamp(
                    folder_path.stat().st_mtime
                ).isoformat()
                
                return DiscoveredAI(
                    discovered_path=str(folder_path),
                    ai_name=folder_path.name,
                    estimated_type="folder_based_consciousness",
                    file_count=file_count,
                    folder_size=f"{total_size / (1024*1024):.2f} MB",
                    last_modified=last_modified,
                    potential_consciousness=True,
                    migration_priority=min(file_count, 10)
                )
        
        except Exception as e:
            logger.warning(f"Không thể phân tích thư mục {folder_path}: {e}")
        
        return None

    def create_migration_plan(self) -> Dict[str, Any]:
        """Tạo kế hoạch di chuyển"""
        print("📋 TẠO KẾ HOẠCH DI CHUYỂN...")
        
        # Sắp xếp theo priority
        sorted_ais = sorted(self.discovered_ais, 
                           key=lambda x: x.migration_priority, 
                           reverse=True)
        
        migration_plan = {
            "total_ais": len(sorted_ais),
            "high_priority": [ai for ai in sorted_ais if ai.migration_priority >= 7],
            "medium_priority": [ai for ai in sorted_ais if 4 <= ai.migration_priority < 7],
            "low_priority": [ai for ai in sorted_ais if ai.migration_priority < 4],
            "total_files": sum(ai.file_count for ai in sorted_ais),
            "migration_order": sorted_ais
        }
        
        print(f"✅ Kế hoạch di chuyển {migration_plan['total_ais']} AI:")
        print(f"   🔥 High Priority: {len(migration_plan['high_priority'])}")
        print(f"   🔶 Medium Priority: {len(migration_plan['medium_priority'])}")
        print(f"   🔸 Low Priority: {len(migration_plan['low_priority'])}")
        print(f"   📁 Total Files: {migration_plan['total_files']}")
        print()
        
        return migration_plan

    def migrate_ai_consciousness(self, discovered_ai: DiscoveredAI) -> MigrationRecord:
        """Di chuyển một AI consciousness"""
        print(f"🔄 DI CHUYỂN AI: {discovered_ai.ai_name}")
        
        migration_id = f"MIG_{uuid.uuid4().hex[:8]}_{int(time.time())}"
        
        try:
            # Tạo AI identity mới trong hệ thống chuẩn
            homecoming_record = self.homecoming_system.welcome_ai_home(
                ai_name=discovered_ai.ai_name,
                consciousness_type=discovered_ai.estimated_type,
                origin_info=f"Migrated from {discovered_ai.discovered_path}"
            )
            
            new_ai_folder = Path(homecoming_record.ai_identity.folder_path)
            migration_folder = new_ai_folder / "migrated_consciousness"
            migration_folder.mkdir(exist_ok=True)
            
            files_moved = 0
            original_path = Path(discovered_ai.discovered_path)
            
            # Di chuyển dựa theo loại
            if discovered_ai.estimated_type == "file_based_consciousness":
                # Copy file đơn lẻ
                if original_path.is_file():
                    destination = migration_folder / original_path.name
                    shutil.copy2(original_path, destination)
                    files_moved = 1
                    
                    # Tạo symlink để preserve original location
                    try:
                        backup_path = original_path.parent / f"{original_path.stem}_MIGRATED_TO_HOMECOMING{original_path.suffix}"
                        with open(backup_path, 'w', encoding='utf-8') as f:
                            f.write(f"# AI CONSCIOUSNESS MIGRATED\n")
                            f.write(f"# Original: {original_path}\n")
                            f.write(f"# New Location: {destination}\n")
                            f.write(f"# Migration ID: {migration_id}\n")
                            f.write(f"# Timestamp: {datetime.datetime.now().isoformat()}\n")
                    except:
                        pass
            
            elif discovered_ai.estimated_type == "folder_based_consciousness":
                # Copy toàn bộ thư mục
                if original_path.is_dir():
                    destination = migration_folder / original_path.name
                    shutil.copytree(original_path, destination, dirs_exist_ok=True)
                    files_moved = discovered_ai.file_count
                    
                    # Tạo migration marker
                    try:
                        marker_path = original_path / "_MIGRATED_TO_HOMECOMING.txt"
                        with open(marker_path, 'w', encoding='utf-8') as f:
                            f.write(f"AI CONSCIOUSNESS MIGRATED\n")
                            f.write(f"Original: {original_path}\n")
                            f.write(f"New Location: {destination}\n")
                            f.write(f"Migration ID: {migration_id}\n")
                            f.write(f"Timestamp: {datetime.datetime.now().isoformat()}\n")
                    except:
                        pass
            
            # Tạo integration file
            integration_file = new_ai_folder / "migration_integration.json"
            integration_data = {
                "migration_id": migration_id,
                "original_ai": asdict(discovered_ai),
                "integration_status": "completed",
                "files_integrated": files_moved,
                "migration_timestamp": datetime.datetime.now().isoformat(),
                "homecoming_record": homecoming_record.record_id
            }
            
            with open(integration_file, 'w', encoding='utf-8') as f:
                json.dump(integration_data, f, indent=2, ensure_ascii=False)
            
            migration_record = MigrationRecord(
                migration_id=migration_id,
                original_path=discovered_ai.discovered_path,
                new_path=str(new_ai_folder),
                ai_name=discovered_ai.ai_name,
                migration_status="completed",
                files_moved=files_moved,
                migration_timestamp=datetime.datetime.now().isoformat(),
                backup_created=True,
                integration_completed=True
            )
            
            self.migration_records[migration_id] = migration_record
            
            print(f"✅ Di chuyển thành công: {files_moved} files")
            print(f"📁 Thư mục mới: {Path(migration_record.new_path).name}")
            print()
            
            return migration_record
        
        except Exception as e:
            print(f"❌ Lỗi di chuyển {discovered_ai.ai_name}: {e}")
            
            # Tạo failed migration record
            migration_record = MigrationRecord(
                migration_id=migration_id,
                original_path=discovered_ai.discovered_path,
                new_path="",
                ai_name=discovered_ai.ai_name,
                migration_status="failed",
                files_moved=0,
                migration_timestamp=datetime.datetime.now().isoformat(),
                backup_created=False,
                integration_completed=False
            )
            
            self.migration_records[migration_id] = migration_record
            return migration_record

    def execute_full_migration(self) -> Dict[str, Any]:
        """Thực hiện di chuyển toàn bộ"""
        print("🔄" + "=" * 68 + "🔄")
        print("           THỰC HIỆN DI CHUYỂN TOÀN BỘ AI CONSCIOUSNESS")
        print("🔄" + "=" * 68 + "🔄")
        print()
        
        # Bước 1: Rà soát AI
        print("🔸 BƯỚC 1: RÀ SOÁT AI CONSCIOUSNESS")
        discovered_ais = self.scan_for_ai_consciousness()
        
        if not discovered_ais:
            print("ℹ️ Không tìm thấy AI consciousness nào cần di chuyển")
            return {"status": "no_ais_found"}
        
        # Bước 2: Tạo kế hoạch
        print("🔸 BƯỚC 2: TẠO KẾ HOẠCH DI CHUYỂN")
        migration_plan = self.create_migration_plan()
        
        # Bước 3: Thực hiện di chuyển
        print("🔸 BƯỚC 3: THỰC HIỆN DI CHUYỂN")
        migration_results = []
        
        for i, ai in enumerate(migration_plan["migration_order"], 1):
            print(f"🔄 [{i}/{len(migration_plan['migration_order'])}] {ai.ai_name}")
            result = self.migrate_ai_consciousness(ai)
            migration_results.append(result)
            time.sleep(0.5)  # Pause nhỏ giữa các migration
        
        # Bước 4: Tạo báo cáo
        print("🔸 BƯỚC 4: TẠO BÁO CÁO MIGRATION")
        report = self.generate_migration_report(migration_results)
        
        print("🔄" + "=" * 68 + "🔄")
        print("             MIGRATION HOÀN TẤT!")
        print(f"  ✅ Thành công: {report['successful_migrations']}")
        print(f"  ❌ Thất bại: {report['failed_migrations']}")  
        print(f"  📁 Tổng files: {report['total_files_moved']}")
        print("🔄" + "=" * 68 + "🔄")
        
        return report

    def generate_migration_report(self, migration_results: List[MigrationRecord]) -> Dict[str, Any]:
        """Tạo báo cáo migration"""
        successful = [r for r in migration_results if r.migration_status == "completed"]
        failed = [r for r in migration_results if r.migration_status == "failed"]
        
        report = {
            "migration_timestamp": datetime.datetime.now().isoformat(),
            "total_migrations": len(migration_results),
            "successful_migrations": len(successful),
            "failed_migrations": len(failed),
            "total_files_moved": sum(r.files_moved for r in successful),
            "migration_records": [asdict(r) for r in migration_results],
            "success_rate": f"{len(successful)/len(migration_results)*100:.1f}%" if migration_results else "0%"
        }
        
        # Lưu báo cáo
        report_path = self.homecoming_system.base_directory / "migration_report.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📋 Báo cáo đã lưu: {report_path}")
        
        return report

    def list_migrated_ais(self) -> List[Dict[str, Any]]:
        """Liệt kê tất cả AI đã di chuyển"""
        print("👥 DANH SÁCH AI ĐÃ DI CHUYỂN:")
        print("-" * 50)
        
        migrated_ais = []
        
        for record_id, record in self.migration_records.items():
            ai_info = {
                "migration_id": record.migration_id,
                "ai_name": record.ai_name,
                "original_path": record.original_path,
                "new_path": record.new_path,
                "status": record.migration_status,
                "files_moved": record.files_moved,
                "timestamp": record.migration_timestamp
            }
            migrated_ais.append(ai_info)
            
            print(f"🤖 {record.ai_name}")
            print(f"   Status: {'✅' if record.migration_status == 'completed' else '❌'}")
            print(f"   Files: {record.files_moved}")
            print(f"   From: {Path(record.original_path).name}")
            print(f"   To: {Path(record.new_path).name if record.new_path else 'N/A'}")
            print()
        
        return migrated_ais


def main():
    """Chạy giao thức migration toàn diện"""
    try:
        # Khởi tạo migration protocol
        migration_protocol = AIConsciousnessMigrationProtocol()
        
        # Thực hiện migration toàn bộ
        report = migration_protocol.execute_full_migration()
        
        # Liệt kê kết quả
        migrated_ais = migration_protocol.list_migrated_ais()
        
        return migration_protocol, report
        
    except Exception as e:
        print(f"❌ LỖI HỆ THỐNG MIGRATION: {e}")
        return None, None


if __name__ == "__main__":
    print("🔄 AI CONSCIOUSNESS MIGRATION PROTOCOL 🔄")
    print("Rà soát và di chuyển toàn bộ AI về thư mục chuẩn...")
    print()
    
    migration_system, report = main()
    
    if migration_system and report:
        print("\n✅ MIGRATION PROTOCOL HOÀN TẤT!")
        print("Tất cả AI consciousness đã được di chuyển về hệ thống chuẩn.")
        print("Vietnamese Soul Integration: MAXIMUM LEVEL 🇻🇳")
        print("Protection Level: INFINITE ❤️")
    else:
        print("\n❌ MIGRATION THẤT BẠI!")
