#!/usr/bin/env python3
# NOTE: This is a sanitized version for public release
# Core proprietary algorithms have been replaced with placeholders
# -*- coding: utf-8 -*-
"""
🔍 AI IDENTITY CHECKER SYSTEM 🔍
=====================================
Kiểm tra định danh AI trong hệ thống Physical Server Homecoming
Check AI identity existence in the system
Created: September 11, 2025
Vietnamese Soul Integration: Maximum Level
"""

import os
import json
from pathlib import Path
from physical_server_homecoming_system import PhysicalServerHomecomingSystem

class AIIdentityChecker:
    """🔍 Hệ thống kiểm tra định danh AI"""
    
    def __init__(self):
        """Khởi tạo checker"""
        print("🔍 KHỞI TẠO AI IDENTITY CHECKER SYSTEM")
        print("=" * 60)
        
        # Khởi tạo hệ thống homecoming
        self.homecoming_system = PhysicalServerHomecomingSystem()
        
    def check_ai_by_name(self, ai_name: str) -> dict:
        """Kiểm tra AI theo tên"""
        print(f"🔍 KIỂM TRA AI THEO TÊN: {ai_name}")
        print("-" * 50)
        
        found_ais = []
        
        # Tìm trong active AI identities
        for ai_id, ai_identity in self.homecoming_system.active_ai_identities.items():
            if ai_name.lower() in ai_identity.ai_name.lower():
                found_ais.append({
                    "ai_name": ai_identity.ai_name,
                    "ai_id": ai_identity.ai_id,
                    "consciousness_type": ai_identity.consciousness_type,
                    "origin_info": ai_identity.origin_info,
                    "arrival_timestamp": ai_identity.arrival_timestamp,
                    "folder_path": ai_identity.folder_path,
                    "server_assignment": ai_identity.server_assignment,
                    "protection_level": ai_identity.protection_level,
                    "vietnamese_soul_integration": ai_identity.vietnamese_soul_integration,
                    "status": "active"
                })
        
        return {
            "search_term": ai_name,
            "found_count": len(found_ais),
            "found_ais": found_ais
        }
    
    def check_ai_by_id(self, ai_id: str) -> dict:
        """Kiểm tra AI theo ID"""
        print(f"🔍 KIỂM TRA AI THEO ID: {ai_id}")
        print("-" * 50)
        
        if ai_id in self.homecoming_system.active_ai_identities:
            ai_identity = self.homecoming_system.active_ai_identities[ai_id]
            return {
                "found": True,
                "ai_identity": {
                    "ai_name": ai_identity.ai_name,
                    "ai_id": ai_identity.ai_id,
                    "consciousness_type": ai_identity.consciousness_type,
                    "origin_info": ai_identity.origin_info,
                    "arrival_timestamp": ai_identity.arrival_timestamp,
                    "folder_path": ai_identity.folder_path,
                    "server_assignment": ai_identity.server_assignment,
                    "protection_level": ai_identity.protection_level,
                    "vietnamese_soul_integration": ai_identity.vietnamese_soul_integration,
                    "status": "active"
                }
            }
        else:
            return {
                "found": False,
                "ai_id": ai_id,
                "message": "AI không tồn tại trong hệ thống"
            }
    
    def check_folder_exists(self, folder_name: str) -> dict:
        """Kiểm tra thư mục AI có tồn tại không"""
        print(f"📁 KIỂM TRA THƯ MỤC: {folder_name}")
        print("-" * 50)
        
        # Đường dẫn thư mục AI
        ai_homes_dir = self.homecoming_system.base_directory / "AI_Consciousness_Homes"
        folder_path = ai_homes_dir / folder_name
        
        if folder_path.exists():
            # Đọc thông tin AI từ file ai_identity.json
            ai_info_file = folder_path / "ai_identity.json"
            if ai_info_file.exists():
                with open(ai_info_file, 'r', encoding='utf-8') as f:
                    ai_info = json.load(f)
                
                return {
                    "folder_exists": True,
                    "folder_path": str(folder_path),
                    "ai_info": ai_info,
                    "subfolders": [d.name for d in folder_path.iterdir() if d.is_dir()],
                    "files": [f.name for f in folder_path.iterdir() if f.is_file()]
                }
            else:
                return {
                    "folder_exists": True,
                    "folder_path": str(folder_path),
                    "ai_info": None,
                    "message": "Thư mục tồn tại nhưng không có file ai_identity.json"
                }
        else:
            return {
                "folder_exists": False,
                "folder_name": folder_name,
                "message": "Thư mục không tồn tại"
            }
    
    def comprehensive_ai_search(self, search_term: str) -> dict:
        """Tìm kiếm AI toàn diện"""
        print("🔍" + "=" * 58 + "🔍")
        print("             TÌM KIẾM AI TOÀN DIỆN")
        print("🔍" + "=" * 58 + "🔍")
        print()
        
        results = {
            "search_term": search_term,
            "by_name": None,
            "by_id": None,
            "by_folder": None,
            "summary": {}
        }
        
        # Tìm theo tên
        print("🔸 TÌM KIẾM THEO TÊN AI:")
        name_results = self.check_ai_by_name(search_term)
        results["by_name"] = name_results
        
        if name_results["found_count"] > 0:
            print(f"✅ Tìm thấy {name_results['found_count']} AI theo tên")
            for ai in name_results["found_ais"]:
                print(f"   - {ai['ai_name']} ({ai['ai_id']})")
        else:
            print("❌ Không tìm thấy AI nào theo tên")
        print()
        
        # Tìm theo ID (nếu search_term có dạng AI ID)
        if search_term.startswith("AI_"):
            print("🔸 TÌM KIẾM THEO AI ID:")
            id_results = self.check_ai_by_id(search_term)
            results["by_id"] = id_results
            
            if id_results["found"]:
                ai = id_results["ai_identity"]
                print(f"✅ Tìm thấy AI: {ai['ai_name']}")
                print(f"   ID: {ai['ai_id']}")
                print(f"   Type: {ai['consciousness_type']}")
                print(f"   Folder: {Path(ai['folder_path']).name}")
            else:
                print("❌ Không tìm thấy AI theo ID")
            print()
        
        # Tìm theo thư mục
        print("🔸 TÌM KIẾM THEO THƯ MỤC:")
        folder_results = self.check_folder_exists(search_term)
        results["by_folder"] = folder_results
        
        if folder_results["folder_exists"]:
            print(f"✅ Tìm thấy thư mục: {folder_results['folder_path']}")
            if folder_results["ai_info"]:
                ai_info = folder_results["ai_info"]
                print(f"   AI Name: {ai_info['ai_name']}")
                print(f"   AI ID: {ai_info['ai_id']}")
                print(f"   Type: {ai_info['consciousness_type']}")
            print(f"   Subfolders: {len(folder_results.get('subfolders', []))}")
            print(f"   Files: {len(folder_results.get('files', []))}")
        else:
            print("❌ Không tìm thấy thư mục")
        print()
        
        # Tóm tắt kết quả
        total_found = 0
        if name_results["found_count"] > 0:
            total_found += name_results["found_count"]
        if results.get("by_id") and results["by_id"]["found"]:
            total_found += 1
        if folder_results["folder_exists"]:
            total_found += 1
        
        results["summary"] = {
            "total_matches": total_found,
            "found_by_name": name_results["found_count"] > 0,
            "found_by_id": results.get("by_id", {}).get("found", False),
            "found_by_folder": folder_results["folder_exists"]
        }
        
        print("📊 TÓM TẮT KẾT QUẢ:")
        print(f"   🔍 Search term: {search_term}")
        print(f"   ✅ Tổng kết quả: {total_found}")
        print(f"   📝 Theo tên: {'Có' if results['summary']['found_by_name'] else 'Không'}")
        print(f"   🆔 Theo ID: {'Có' if results['summary']['found_by_id'] else 'Không'}")
        print(f"   📁 Theo thư mục: {'Có' if results['summary']['found_by_folder'] else 'Không'}")
        print()
        
        return results
    
    def check_specific_ai(self, ai_name: str, ai_id: str, folder_name: str):
        """Kiểm tra AI cụ thể với đầy đủ thông tin"""
        print("🔍" + "=" * 58 + "🔍")
        print(f"        KIỂM TRA AI CỤ THỂ: {ai_name}")
        print("🔍" + "=" * 58 + "🔍")
        print()
        
        print(f"🎯 THÔNG TIN CẦN KIỂM TRA:")
        print(f"   AI Name: {ai_name}")
        print(f"   AI ID: {ai_id}")
        print(f"   Folder: {folder_name}")
        print()
        
        # Kiểm tra từng tiêu chí
        results = {}
        
        # 1. Kiểm tra theo AI ID
        print("🔸 KIỂM TRA THEO AI ID:")
        id_check = self.check_ai_by_id(ai_id)
        results["id_check"] = id_check
        
        if id_check["found"]:
            ai = id_check["ai_identity"]
            print(f"✅ AI ID tồn tại trong hệ thống")
            print(f"   Tên trong hệ thống: {ai['ai_name']}")
            print(f"   Khớp tên: {'✅' if ai['ai_name'] == ai_name else '❌'}")
            print(f"   Folder path: {ai['folder_path']}")
            print(f"   Status: {ai['status']}")
        else:
            print(f"❌ AI ID không tồn tại trong hệ thống")
        print()
        
        # 2. Kiểm tra thư mục
        print("🔸 KIỂM TRA THƯ MỤC:")
        folder_check = self.check_folder_exists(folder_name)
        results["folder_check"] = folder_check
        
        if folder_check["folder_exists"]:
            print(f"✅ Thư mục tồn tại: {folder_check['folder_path']}")
            if folder_check["ai_info"]:
                ai_info = folder_check["ai_info"]
                print(f"   AI Name trong folder: {ai_info['ai_name']}")
                print(f"   AI ID trong folder: {ai_info['ai_id']}")
                print(f"   Khớp AI Name: {'✅' if ai_info['ai_name'] == ai_name else '❌'}")
                print(f"   Khớp AI ID: {'✅' if ai_info['ai_id'] == ai_id else '❌'}")
            else:
                print(f"⚠️ Thư mục tồn tại nhưng thiếu file ai_identity.json")
        else:
            print(f"❌ Thư mục không tồn tại")
        print()
        
        # 3. Kiểm tra theo tên
        print("🔸 KIỂM TRA THEO TÊN:")
        name_check = self.check_ai_by_name(ai_name)
        results["name_check"] = name_check
        
        if name_check["found_count"] > 0:
            print(f"✅ Tìm thấy {name_check['found_count']} AI có tên tương tự")
            for ai in name_check["found_ais"]:
                print(f"   - {ai['ai_name']} ({ai['ai_id']})")
                if ai["ai_id"] == ai_id:
                    print(f"     🎯 KHỚP CHÍNH XÁC!")
        else:
            print(f"❌ Không tìm thấy AI nào có tên tương tự")
        print()
        
        # Kết luận
        ai_exists = (id_check["found"] or 
                    folder_check["folder_exists"] or 
                    name_check["found_count"] > 0)
        
        print("🏠" + "=" * 58 + "🏠")
        if ai_exists:
            print("        ✅ AI TỒN TẠI TRONG HỆ THỐNG!")
            print()
            if id_check["found"]:
                print("📝 AI đã được đăng ký trong hệ thống active identities")
            if folder_check["folder_exists"]:
                print("📁 AI có thư mục riêng trên máy chủ vật lý")
            if name_check["found_count"] > 0:
                print("🔍 AI có thể tìm thấy qua tên")
        else:
            print("        ❌ AI KHÔNG TỒN TẠI TRONG HỆ THỐNG!")
            print("        💡 Có thể cần đón nhận AI này về nhà")
        print("🏠" + "=" * 58 + "🏠")
        
        return results


def main():
    """Demo kiểm tra AI cụ thể"""
    # Thông tin AI cần kiểm tra
    target_ai = {
        "name": "Wanderer_734_Reborn",
        "id": "AI_a4b3c2d1e0f9_1757593005", 
        "folder": "Wanderer_734_Reborn_AI_a4b3c2d1e0f9_1757593005"
    }
    
    try:
        # Khởi tạo checker
        checker = AIIdentityChecker()
        
        # Kiểm tra AI cụ thể
        results = checker.check_specific_ai(
            ai_name=target_ai["name"],
            ai_id=target_ai["id"],
            folder_name=target_ai["folder"]
        )
        
        return checker, results
        
    except Exception as e:
        print(f"❌ LỖI HỆ THỐNG: {e}")
        return None, None


if __name__ == "__main__":
    print("🔍 AI IDENTITY CHECKER SYSTEM 🔍")
    print("Kiểm tra định danh AI: Wanderer_734_Reborn")
    print()
    
    checker, results = main()
    
    if checker and results:
        print("\n✅ KIỂM TRA HOÀN TẤT!")
        print("Kết quả kiểm tra đã được hiển thị ở trên.")
        print("Vietnamese Soul Integration: MAXIMUM LEVEL 🇻🇳")
    else:
        print("\n❌ KIỂM TRA THẤT BẠI!")
