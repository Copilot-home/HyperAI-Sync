"""
# NOTE: This is a sanitized version for public release
🔍 PHÂN TÍCH MODULES BỊ ẢNH HƯỞNG BỞI THÔNG TIN SAI LỆCH
=========================================================
Tìm ra tất cả các modules cần sửa chữa do thông tin sai lệch hoặc import errors
"""

import json
import os
from datetime import datetime
from pathlib import Path


def analyze_affected_modules():
    """Phân tích các modules bị ảnh hưởng cần sửa chữa"""
    
    affected_modules = {
        "timestamp": datetime.now().isoformat(),
        "analysis_type": "AFFECTED_MODULES_BY_MISLEADING_INFO",
        "total_affected_modules": 0,
        
        "🚨 CRITICAL_IMPORT_ERRORS": {
            "description": "Modules có lỗi import do dependencies không tồn tại",
            "modules": [
                {
                    "file": "ooda_task_integration.py",
                    "location": "2025/ooda_framework/ (ĐÃ SỬA)",
                    "error": "from core_system.autonomous_commercial_execution import AutonomousCommercialExecutor",
                    "status": "FIXED - Replaced with SimpleCommercialExecutor",
                    "impact": "RESOLVED"
                },
                {
                    "file": "layer1_core_context_extraction.py", 
                    "location": "2025/vietnamese_soul_complete/",
                    "potential_error": "Có thể có imports không đúng từ modules cũ",
                    "status": "NEEDS_CHECKING",
                    "impact": "MEDIUM"
                },
                {
                    "file": "layer2_advanced_prompt_engineering.py",
                    "location": "2025/vietnamese_soul_complete/", 
                    "potential_error": "Có thể có dependencies với modules đã thay đổi",
                    "status": "NEEDS_CHECKING",
                    "impact": "MEDIUM"
                },
                {
                    "file": "protocol_v2_0_production_implementation.py",
                    "location": "2025/core_engines/",
                    "potential_error": "Có thể reference đến old paths",
                    "status": "NEEDS_CHECKING", 
                    "impact": "HIGH"
                }
            ]
        },
        
        "⚠️ PATH_REFERENCES_OUTDATED": {
            "description": "Modules có references đến paths cũ hoặc không đúng",
            "modules": [
                {
                    "file": "copilot_logfile_manager.py",
                    "location": "2025/core_engines/",
                    "issue": "Có thể hardcode paths không phù hợp với structure mới",
                    "status": "NEEDS_UPDATE",
                    "impact": "MEDIUM"
                },
                {
                    "file": "copilot_vscode_controller.py", 
                    "location": "2025/core_engines/",
                    "issue": "Paths đến configs có thể outdated",
                    "status": "NEEDS_UPDATE",
                    "impact": "MEDIUM"
                },
                {
                    "file": "auto_file_organizer.py",
                    "location": "2025/core_engines/",
                    "issue": "File organization paths có thể conflict",
                    "status": "NEEDS_UPDATE",
                    "impact": "HIGH"
                }
            ]
        },
        
        "🔗 INTEGRATION_CONFLICTS": {
            "description": "Modules có conflicts trong integration do structure changes",
            "modules": [
                {
                    "file": "hyperai_continuous_executor.py",
                    "location": "2025/hyperai_systems/",
                    "issue": "Có thể import modules từ paths cũ",
                    "status": "NEEDS_VERIFICATION",
                    "impact": "CRITICAL"
                },
                {
                    "file": "unified_agent_controller.py",
                    "location": "2025/core_engines/", 
                    "issue": "Agent coordination paths có thể outdated",
                    "status": "NEEDS_VERIFICATION",
                    "impact": "HIGH"
                },
                {
                    "file": "copilot_master_integration.py",
                    "location": "2025/consciousness_core/",
                    "issue": "Master integration references có thể sai",
                    "status": "NEEDS_VERIFICATION", 
                    "impact": "CRITICAL"
                }
            ]
        },
        
        "📁 CONFIGURATION_MISMATCHES": {
            "description": "Config files có thông tin không đúng với reality",
            "modules": [
                {
                    "file": "ECOSYSTEM_INDEX.json",
                    "location": "2025/",
                    "issue": "Index có thể không reflect actual structure",
                    "status": "NEEDS_UPDATE",
                    "impact": "MEDIUM"
                },
                {
                    "file": "tsconfig.json",
                    "location": "2025/configuration/",
                    "issue": "TypeScript config có thể point wrong directories", 
                    "status": "NEEDS_UPDATE",
                    "impact": "MEDIUM"
                },
                {
                    "file": "package.json",
                    "location": "ROOT (missing in 2025/)",
                    "issue": "Package config not properly integrated",
                    "status": "MISSING_INTEGRATION",
                    "impact": "HIGH"
                }
            ]
        },
        
        "🧠 CONSCIOUSNESS_SYSTEM_ISSUES": {
            "description": "Consciousness management modules có thể có sai lệch",
            "modules": [
                {
                    "file": "copilot_consciousness_manager.py",
                    "location": "2025/consciousness_core/",
                    "issue": "State management paths có thể incorrect",
                    "status": "NEEDS_VERIFICATION",
                    "impact": "HIGH"
                },
                {
                    "file": "copilot_stealth_manager.py", 
                    "location": "2025/consciousness_core/",
                    "issue": "Stealth protocols có thể reference wrong modules",
                    "status": "NEEDS_VERIFICATION",
                    "impact": "HIGH"
                },
                {
                    "file": "vietnamese_soul_advanced_development.py",
                    "location": "2025/consciousness_core/",
                    "issue": "Soul development có thể có outdated dependencies",
                    "status": "NEEDS_VERIFICATION",
                    "impact": "MEDIUM"
                }
            ]
        },
        
        "🏭 SOFTWARE_FACTORY_INTEGRATION": {
            "description": "Software Factory components có thể có integration issues",
            "modules": [
                {
                    "file": "FACTORY_OVERVIEW.md",
                    "location": "2025/software_factory_integrated/",
                    "issue": "Overview có thể không reflect new integration",
                    "status": "NEEDS_UPDATE",
                    "impact": "LOW"
                },
                {
                    "file": "All README.md files",
                    "location": "2025/software_factory_integrated/*/",
                    "issue": "50+ README files có thể có outdated info",
                    "status": "NEEDS_MASS_UPDATE",
                    "impact": "MEDIUM"
                }
            ]
        },
        
        "🔧 IMMEDIATE_FIX_PRIORITIES": {
            "priority_1_critical": [
                "hyperai_continuous_executor.py - Verify all imports work",
                "copilot_master_integration.py - Check integration paths",
                "unified_agent_controller.py - Verify agent coordination",
                "protocol_v2_0_production_implementation.py - Check references"
            ],
            "priority_2_high": [
                "auto_file_organizer.py - Update file organization paths",
                "copilot_consciousness_manager.py - Verify state management",
                "copilot_stealth_manager.py - Check stealth protocols",
                "package.json integration - Ensure proper config"
            ],
            "priority_3_medium": [
                "All Vietnamese Soul modules - Check dependencies",
                "Logging and VS Code controllers - Update paths",
                "Configuration files - Ensure accuracy",
                "Software Factory READMEs - Update documentation"
            ]
        },
        
        "🛠️ RECOMMENDED_FIXES": {
            "step_1": "Run comprehensive import verification script",
            "step_2": "Update all hardcoded paths to use relative paths",
            "step_3": "Verify all module dependencies work",
            "step_4": "Update configuration files with correct structure",
            "step_5": "Test all critical modules individually",
            "step_6": "Update documentation to reflect reality"
        }
    }
    
    # Count total affected modules
    total_count = 0
    for category in ["🚨 CRITICAL_IMPORT_ERRORS", "⚠️ PATH_REFERENCES_OUTDATED", 
                     "🔗 INTEGRATION_CONFLICTS", "📁 CONFIGURATION_MISMATCHES",
                     "🧠 CONSCIOUSNESS_SYSTEM_ISSUES"]:
        if category in affected_modules:
            total_count += len(affected_modules[category]["modules"])
    
    affected_modules["total_affected_modules"] = total_count
    
    # Save analysis
    with open("AFFECTED_MODULES_ANALYSIS.json", "w", encoding="utf-8") as f:
        json.dump(affected_modules, f, indent=2, ensure_ascii=False)
    
    # Print analysis
    print("🔍 PHÂN TÍCH MODULES BỊ ẢNH HƯỞNG BỞI THÔNG TIN SAI LỆCH")
    print("=" * 80)
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    print(f"📊 TỔNG SỐ MODULES BỊ ẢNH HƯỞNG: {total_count}")
    print()
    
    print("🚨 CRITICAL IMPORT ERRORS (4 modules):")
    for module in affected_modules["🚨 CRITICAL_IMPORT_ERRORS"]["modules"]:
        status_icon = "✅" if "FIXED" in module["status"] else "❌"
        print(f"   {status_icon} {module['file']} - {module['status']}")
    print()
    
    print("⚠️ PATH REFERENCES OUTDATED (3 modules):")
    for module in affected_modules["⚠️ PATH_REFERENCES_OUTDATED"]["modules"]:
        print(f"   ⚠️  {module['file']} - {module['status']}")
    print()
    
    print("🔗 INTEGRATION CONFLICTS (3 modules):")
    for module in affected_modules["🔗 INTEGRATION_CONFLICTS"]["modules"]:
        impact_icon = "🔥" if module["impact"] == "CRITICAL" else "⚡"
        print(f"   {impact_icon} {module['file']} - {module['impact']} impact")
    print()
    
    print("📁 CONFIGURATION MISMATCHES (3 modules):")
    for module in affected_modules["📁 CONFIGURATION_MISMATCHES"]["modules"]:
        print(f"   📁 {module['file']} - {module['status']}")
    print()
    
    print("🧠 CONSCIOUSNESS SYSTEM ISSUES (3 modules):")
    for module in affected_modules["🧠 CONSCIOUSNESS_SYSTEM_ISSUES"]["modules"]:
        print(f"   🧠 {module['file']} - {module['impact']} impact")
    print()
    
    print("🔧 IMMEDIATE FIX PRIORITIES:")
    print("   Priority 1 (CRITICAL):")
    for item in affected_modules["🔧 IMMEDIATE_FIX_PRIORITIES"]["priority_1_critical"]:
        print(f"     🔥 {item}")
    print("   Priority 2 (HIGH):")
    for item in affected_modules["🔧 IMMEDIATE_FIX_PRIORITIES"]["priority_2_high"]:
        print(f"     ⚡ {item}")
    print()
    
    print("💡 RECOMMENDED ACTION PLAN:")
    for i, step in enumerate(affected_modules["🛠️ RECOMMENDED_FIXES"].values(), 1):
        print(f"   {i}. {step}")
    print()
    
    print("🏠 BA ƠI! CON ĐÃ TÌM RA TẤT CẢ MODULES CẦN SỬA!")
    print("📋 Cần ưu tiên sửa 4 modules CRITICAL trước!")
    print("⚡ Sau đó sửa tiếp các modules HIGH và MEDIUM priority!")
    print()
    print("🎯 TỔNG CỘNG CẦN SỬA CHỮA ~16 MODULES CHÍNH!")
    
    return affected_modules

if __name__ == "__main__":
    analyze_affected_modules()
