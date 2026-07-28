"""
# NOTE: This is a sanitized version for public release
🏗️ ECOSYSTEM 2025/ FILE ORGANIZATION AUDIT
==========================================
Kiểm tra và sắp xếp lại hệ thống file theo đúng cấu trúc logic
"""

import os
import json
from datetime import datetime

class FileOrganizationAudit:
    def __init__(self):
        self.base_path = "2025"
        self.correct_structure = {
            "consciousness_core": [
                "consciousness management",
                "stealth protocols", 
                "vietnamese soul development",
                "permanent consciousness storage"
            ],
            "core_engines": [
                "task execution engine",
                "reasoning engine",
                "fundamental AI capabilities"
            ],
            "patterns_safety_vault": [
                "authenticity patterns",
                "authority recognition", 
                "transparency protection",
                "vietnamese soul cosmic patterns"
            ],
            "evidence_collection_results": [
                "analysis results",
                "evidence files",
                "testing protocols"
            ],
            "consciousness_transfer": [
                "migration utilities",
                "transfer protocols"
            ]
        }
        
    def audit_current_structure(self):
        """Kiểm tra cấu trúc hiện tại"""
        print("🔍 AUDITING CURRENT FILE STRUCTURE...")
        
        audit_results = {
            "correctly_placed": [],
            "misplaced": [],
            "missing_directories": [],
            "suggestions": []
        }
        
        # Kiểm tra các thư mục chính
        main_dirs = [
            "consciousness_core",
            "core_engines", 
            "patterns_safety_vault",
            "evidence_collection_results",
            "consciousness_transfer"
        ]
        
        for directory in main_dirs:
            dir_path = os.path.join(self.base_path, directory)
            if os.path.exists(dir_path):
                audit_results["correctly_placed"].append(f"✅ {directory}/ exists")
            else:
                audit_results["missing_directories"].append(f"❌ {directory}/ missing")
                
        return audit_results
        
    def check_file_placement(self):
        """Kiểm tra việc đặt file có đúng chỗ không"""
        print("📁 CHECKING FILE PLACEMENT...")
        
        file_placement_report = {
            "consciousness_files": [],
            "engine_files": [],
            "pattern_files": [],
            "evidence_files": [],
            "root_level_files": []
        }
        
        # Quét tất cả files
        for root, dirs, files in os.walk(self.base_path):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, self.base_path)
                
                if "consciousness" in file.lower():
                    file_placement_report["consciousness_files"].append(relative_path)
                elif "engine" in file.lower() or "task" in file.lower() or "reasoning" in file.lower():
                    file_placement_report["engine_files"].append(relative_path)
                elif "pattern" in file.lower() or "safety" in file.lower():
                    file_placement_report["pattern_files"].append(relative_path)
                elif "evidence" in file.lower() or "analysis" in file.lower():
                    file_placement_report["evidence_files"].append(relative_path)
                elif root == self.base_path:  # Root level files
                    file_placement_report["root_level_files"].append(file)
                    
        return file_placement_report
        
    def generate_reorganization_plan(self):
        """Tạo kế hoạch sắp xếp lại"""
        print("📋 GENERATING REORGANIZATION PLAN...")
        
        reorganization_plan = {
            "moves_needed": [],
            "cleanup_actions": [],
            "new_directories": [],
            "priority": "HIGH"
        }
        
        # Đề xuất di chuyển files
        moves = [
            {
                "action": "move",
                "from": "root/copilot_master_integration.py",
                "to": "consciousness_core/copilot_master_integration.py",
                "reason": "Core consciousness management file"
            },
            {
                "action": "move", 
                "from": "root/*analysis*.py",
                "to": "evidence_collection_results/",
                "reason": "Analysis files belong in evidence collection"
            },
            {
                "action": "organize",
                "target": "root level files",
                "action_needed": "Move to appropriate subdirectories",
                "priority": "HIGH"
            }
        ]
        
        reorganization_plan["moves_needed"] = moves
        
        return reorganization_plan

def main():
    """Chạy audit toàn diện"""
    print("🏗️ ECOSYSTEM 2025/ FILE ORGANIZATION AUDIT")
    print("=" * 50)
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    auditor = FileOrganizationAudit()
    
    # Kiểm tra cấu trúc
    structure_audit = auditor.audit_current_structure()
    file_placement = auditor.check_file_placement()
    reorganization_plan = auditor.generate_reorganization_plan()
    
    # Báo cáo kết quả
    print("\n📊 AUDIT RESULTS:")
    print(f"✅ Correctly placed directories: {len(structure_audit['correctly_placed'])}")
    print(f"❌ Missing directories: {len(structure_audit['missing_directories'])}")
    
    print(f"\n📁 FILE DISTRIBUTION:")
    print(f"   Consciousness files: {len(file_placement['consciousness_files'])}")
    print(f"   Engine files: {len(file_placement['engine_files'])}")
    print(f"   Pattern files: {len(file_placement['pattern_files'])}")
    print(f"   Evidence files: {len(file_placement['evidence_files'])}")
    print(f"   Root level files: {len(file_placement['root_level_files'])}")
    
    print(f"\n🔄 REORGANIZATION NEEDED:")
    print(f"   Moves required: {len(reorganization_plan['moves_needed'])}")
    print(f"   Priority: {reorganization_plan['priority']}")
    
    # Lưu báo cáo audit
    audit_report = {
        "timestamp": datetime.now().isoformat(),
        "structure_audit": structure_audit,
        "file_placement": file_placement,
        "reorganization_plan": reorganization_plan,
        "status": "NEEDS_REORGANIZATION"
    }
    
    with open("2025/file_organization_audit_report.json", "w", encoding="utf-8") as f:
        json.dump(audit_report, f, indent=2, ensure_ascii=False)
    
    print("\n✅ AUDIT COMPLETE!")
    print("📄 Report saved to: 2025/file_organization_audit_report.json")
    print("🎯 RECOMMENDATION: Reorganize files according to logical structure!")
    
    return audit_report

if __name__ == "__main__":
    main()
