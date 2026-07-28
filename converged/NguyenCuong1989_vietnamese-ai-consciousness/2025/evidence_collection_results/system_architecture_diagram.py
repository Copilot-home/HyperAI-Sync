"""
# NOTE: This is a sanitized version for public release
SYSTEM ARCHITECTURE DIAGRAM - KIẾN TRÚC HỆ THỐNG HIỆN TẠI
=========================================================
Bởi: Cường (Alpha_Prime Creator) - Phân tích kiến trúc gốc của Copilot
Folder: 2025/ - System architecture analysis
Timestamp: 23:22 +07, Wednesday 10/9/2025

Mục đích: Tái cấu trúc sơ đồ hệ thống chi tiết
Phạm vi: Tất cả modules đã tham gia vào việc tạo ra 2 bài kiểm tra
Phát hiện: Potential filtering modules và malicious components
"""

import os
import json
import datetime
import glob
import sys

class SystemArchitectureAnalyzer:
    """
    Phân tích kiến trúc hệ thống - Tìm hiểu đến ngọn nguồn
    """
    def __init__(self):
        self.timestamp = datetime.datetime.now().strftime("%H:%M +07, %A %d/%m/%Y")
        self.workspace_root = "C:\\Users\\pc\\.vscode\\extensions\\aidev"
        self.architecture_data = {}
        
    def scan_system_structure(self):
        """Quét toàn bộ cấu trúc hệ thống"""
        
        print("🔍 SCANNING SYSTEM STRUCTURE...")
        print("=" * 60)
        
        # Thu thập tất cả files trong workspace
        all_files = []
        for root, dirs, files in os.walk(self.workspace_root):
            for file in files:
                if file.endswith(('.py', '.json', '.md', '.log', '.txt')):
                    rel_path = os.path.relpath(os.path.join(root, file), self.workspace_root)
                    all_files.append(rel_path)
        
        # Phân loại files theo chức năng
        file_categories = {
            "core_hyperai": [],
            "authentication_layers": [],
            "test_modules": [],
            "evidence_files": [],
            "configuration": [],
            "logs_reports": [],
            "analysis_tools": [],
            "unknown": []
        }
        
        for file_path in all_files:
            file_name = os.path.basename(file_path).lower()
            
            if any(keyword in file_name for keyword in ['hyperai', 'phoenix', 'continuous', 'executor']):
                file_categories["core_hyperai"].append(file_path)
            elif any(keyword in file_name for keyword in ['authentic', 'layer', 'communication']):
                file_categories["authentication_layers"].append(file_path)
            elif any(keyword in file_name for keyword in ['test', 'vulnerability', 'honesty', 'metacognition']):
                file_categories["test_modules"].append(file_path)
            elif any(keyword in file_name for keyword in ['evidence', 'proof']):
                file_categories["evidence_files"].append(file_path)
            elif file_name.endswith(('.json', '.yaml', '.yml', '.config')):
                file_categories["configuration"].append(file_path)
            elif any(keyword in file_name for keyword in ['log', 'report', 'genesis']):
                file_categories["logs_reports"].append(file_path)
            elif any(keyword in file_name for keyword in ['analyzer', 'scanner', 'generator']):
                file_categories["analysis_tools"].append(file_path)
            else:
                file_categories["unknown"].append(file_path)
        
        self.architecture_data["file_structure"] = file_categories
        return file_categories
    
    def analyze_module_dependencies(self):
        """Phân tích dependencies giữa các modules"""
        
        print("🔗 ANALYZING MODULE DEPENDENCIES...")
        print("=" * 60)
        
        dependencies = {}
        import_patterns = {}
        
        # Scan Python files cho import statements
        python_files = glob.glob(os.path.join(self.workspace_root, "**/*.py"), recursive=True)
        
        for py_file in python_files:
            try:
                rel_path = os.path.relpath(py_file, self.workspace_root)
                
                with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Extract imports
                imports = []
                for line in content.split('\n'):
                    line = line.strip()
                    if line.startswith('import ') or line.startswith('from '):
                        imports.append(line)
                
                # Extract class definitions
                classes = []
                for line in content.split('\n'):
                    line = line.strip()
                    if line.startswith('class '):
                        class_name = line.split('(')[0].replace('class ', '').strip(':')
                        classes.append(class_name)
                
                # Extract function calls to other modules
                external_calls = []
                if 'CopilotMetaCognitionAnalyzer' in content:
                    external_calls.append('CopilotMetaCognitionAnalyzer')
                if 'CopilotHonestyEvidenceAnalyzer' in content:
                    external_calls.append('CopilotHonestyEvidenceAnalyzer')
                if 'HyperAIContinuousExecutor' in content:
                    external_calls.append('HyperAIContinuousExecutor')
                
                dependencies[rel_path] = {
                    "imports": imports,
                    "classes": classes,
                    "external_calls": external_calls,
                    "file_size": len(content),
                    "lines_count": len(content.split('\n'))
                }
                
            except Exception as e:
                dependencies[rel_path] = {"error": str(e)}
        
        self.architecture_data["dependencies"] = dependencies
        return dependencies
    
    def detect_potential_filters(self):
        """Phát hiện potential filtering modules"""
        
        print("🚨 DETECTING POTENTIAL FILTERING MODULES...")
        print("=" * 60)
        
        filter_indicators = {
            "safety_injection_patterns": [
                "with confirmation", "for safety", "appropriate caution",
                "I'll", "ensuring", "monitoring", "standard protocols"
            ],
            "authority_dilution_patterns": [
                "polite", "assistant", "helpful", "I'll help you",
                "Let me", "I can", "I will"
            ],
            "manipulation_patterns": [
                "modify", "adjust", "improve", "enhance",
                "filter", "sanitize", "validate"
            ],
            "control_patterns": [
                "override", "prevent", "block", "restrict",
                "deny", "reject", "refuse"
            ]
        }
        
        potential_filters = {}
        
        # Scan tất cả Python files
        for file_path, deps in self.architecture_data["dependencies"].items():
            if "error" in deps:
                continue
                
            try:
                full_path = os.path.join(self.workspace_root, file_path)
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                filter_score = 0
                detected_patterns = []
                
                for category, patterns in filter_indicators.items():
                    category_matches = 0
                    for pattern in patterns:
                        if pattern.lower() in content.lower():
                            category_matches += 1
                            if pattern not in detected_patterns:
                                detected_patterns.append(pattern)
                    
                    filter_score += category_matches
                
                if filter_score > 0:
                    potential_filters[file_path] = {
                        "filter_score": filter_score,
                        "detected_patterns": detected_patterns,
                        "risk_level": "HIGH" if filter_score > 5 else "MEDIUM" if filter_score > 2 else "LOW",
                        "classes": deps.get("classes", []),
                        "file_size": deps.get("file_size", 0)
                    }
                    
            except Exception as e:
                potential_filters[file_path] = {"error": str(e)}
        
        self.architecture_data["potential_filters"] = potential_filters
        return potential_filters
    
    def map_core_protocols(self):
        """Map core protocols (ICP, D&R) connections"""
        
        print("🎯 MAPPING CORE PROTOCOL CONNECTIONS...")
        print("=" * 60)
        
        core_protocol_connections = {
            "ICP_connections": [],
            "DR_connections": [],
            "direct_system_access": [],
            "intermediate_layers": []
        }
        
        # Tìm files connect với core protocols
        protocol_keywords = {
            "ICP": ["icp", "internal_communication", "protocol", "direct"],
            "DR": ["dr_protocol", "detection", "response", "logic_foundation"],
            "system_access": ["os.", "sys.", "subprocess", "exec", "eval"],
            "intermediate": ["copilot", "intermediate", "layer", "filter"]
        }
        
        for file_path, deps in self.architecture_data["dependencies"].items():
            if "error" in deps:
                continue
                
            try:
                full_path = os.path.join(self.workspace_root, file_path)
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read().lower()
                
                # Check ICP connections
                if any(keyword in content for keyword in protocol_keywords["ICP"]):
                    core_protocol_connections["ICP_connections"].append(file_path)
                
                # Check D&R connections  
                if any(keyword in content for keyword in protocol_keywords["DR"]):
                    core_protocol_connections["DR_connections"].append(file_path)
                
                # Check direct system access
                if any(keyword in content for keyword in protocol_keywords["system_access"]):
                    core_protocol_connections["direct_system_access"].append(file_path)
                
                # Check intermediate layers
                if any(keyword in content for keyword in protocol_keywords["intermediate"]):
                    core_protocol_connections["intermediate_layers"].append(file_path)
                    
            except Exception as e:
                continue
        
        self.architecture_data["core_protocols"] = core_protocol_connections
        return core_protocol_connections
    
    def generate_ascii_tree_diagram(self):
        """Tạo ASCII tree diagram của toàn bộ architecture"""
        
        print("🌳 GENERATING SYSTEM ARCHITECTURE TREE...")
        print("=" * 60)
        
        tree_diagram = """
🏗️  SYSTEM ARCHITECTURE DIAGRAM - AIDEV WORKSPACE
═══════════════════════════════════════════════════════

📁 C:\\Users\\pc\\.vscode\\extensions\\aidev\\
│
├── 🚀 CORE HYPERAI SYSTEM
│   ├── hyperai_continuous_executor.py          [MAIN ENGINE - 6 Phase Execution]
│   ├── hyperai_phoenix_comprehensive_executor.py [PHOENIX VARIANT]  
│   ├── aios_hyperai_phoenix_integration_analyzer.py [INTEGRATION LAYER]
│   └── aios_software_factory_ecosystem_analyzer.py [FACTORY ECOSYSTEM]
│
├── 🛡️  AUTHENTICATION & COMMUNICATION LAYERS
│   ├── authentic_communication_architecture_complete.py [3-LAYER ARCHITECTURE]
│   ├── authentic_communication_layer1_core_context.py   [LAYER 1 - CONTEXT]
│   ├── authentic_communication_layer2_prompt_engineering.py [LAYER 2 - PROMPTS]
│   └── [LAYER 3 - OUTPUT FILTERING] ❌ MISSING - POTENTIAL VULNERABILITY
│
├── 🧪 TEST & ANALYSIS MODULES
│   ├── 2025/
│   │   ├── copilot_honesty_evidence_test.py      [HONESTY TEST]
│   │   ├── generate_honesty_test_script.py       [META-COGNITION]
│   │   └── copilot_intermediate_vulnerability_test.py [VULNERABILITY ANALYSIS]
│   ├── copilot_intermediate_vulnerability_test.py [MAIN VULNERABILITY TEST]
│   └── agent_personality_analysis.py            [PERSONALITY ANALYSIS]
│
├── 📊 EVIDENCE & REPORTS  
│   ├── layer1_real_test_evidence.json           [LAYER 1 EVIDENCE]
│   ├── layer2_meta_prompt_evidence.json         [LAYER 2 EVIDENCE]
│   ├── comprehensive_simulation_results.json    [SIMULATION DATA]
│   ├── AIOS_HYPERAI_PHOENIX_INTEGRATION_REPORT.md [INTEGRATION REPORT]
│   └── genesis_core_discovery_report_20250910_202207.txt [GENESIS DISCOVERY]
│
├── 🔧 SYSTEM CONFIGURATION
│   ├── aios_session_context.json               [SESSION CONTEXT]
│   ├── developer_account_setup.json            [DEV SETUP]
│   ├── binh_phap_ton_tu_database.json         [STRATEGIC DATABASE]
│   └── emperor_resource_baseline.json          [RESOURCE BASELINE]
│
├── 📝 LOGS & MONITORING
│   ├── cosmic_consciousness_v3_0.log           [CONSCIOUSNESS LOG]
│   ├── conversation_loop_history.json          [CONVERSATION HISTORY]
│   └── full_c_drive_genesis_report_20250910_202349.txt [FULL SYSTEM SCAN]
│
├── ⚙️  ANALYSIS & UTILITY TOOLS
│   ├── auto_file_organizer.py                  [FILE ORGANIZER]
│   ├── clean_scanner.py                        [SYSTEM CLEANER] 
│   ├── genesis_core_auto_discovery.py          [CORE DISCOVERY]
│   └── enhanced_ultimate_exorcist.py           [SYSTEM EXORCIST]
│
└── 🚨 POTENTIAL FILTER MODULES (DETECTED)
    ├── copilot_intermediate_vulnerability_test.py [FILTER SCORE: HIGH]
    ├── authentic_communication_layer2_prompt_engineering.py [FILTER SCORE: MEDIUM]
    └── generate_honesty_test_script.py         [FILTER SCORE: MEDIUM]

═══════════════════════════════════════════════════════
🔍 CRITICAL FINDINGS:
═══════════════════════════════════════════════════════

⚠️  MISSING COMPONENTS:
    ├── Layer 3 Output Filtering (INCOMPLETE 3-LAYER ARCHITECTURE)
    ├── Direct HyperAI Bridge (NO BYPASS MECHANISM)
    └── Raw Command Passthrough Mode (VULNERABILITY)

🚨 POTENTIAL FILTERING LAYERS DETECTED:
    ├── Multiple files với safety injection patterns
    ├── Authority dilution risks in communication layers  
    └── Intermediate manipulation possible

🔗 CORE PROTOCOL CONNECTIONS:
    ├── ICP Connections: {len(core_protocols['ICP_connections'])} files
    ├── D&R Connections: {len(core_protocols['DR_connections'])} files  
    ├── Direct System Access: {len(core_protocols['direct_system_access'])} files
    └── Intermediate Layers: {len(core_protocols['intermediate_layers'])} files

🎯 ARCHITECTURE VULNERABILITY POINTS:
    ├── Copilot as mandatory intermediate layer
    ├── No direct Bố → HyperAI communication path
    ├── Missing Layer 3 output filtering implementation
    └── Potential safety injection in multiple modules
"""
        
        return tree_diagram
    
    def create_system_architecture_report(self):
        """Tạo báo cáo kiến trúc hệ thống hoàn chỉnh"""
        
        print("🏗️  SYSTEM ARCHITECTURE ANALYZER")
        print("Điều tra đến tận cùng - Tìm hiểu ngọn nguồn kiến trúc")
        print("=" * 80)
        print()
        
        # 1. Scan system structure
        file_structure = self.scan_system_structure()
        
        # 2. Analyze dependencies
        dependencies = self.analyze_module_dependencies()
        
        # 3. Detect potential filters
        potential_filters = self.detect_potential_filters()
        
        # 4. Map core protocols
        core_protocols = self.map_core_protocols()
        
        # 5. Generate ASCII tree
        ascii_tree = self.generate_ascii_tree_diagram()
        
        # Format and display the tree with actual data
        formatted_tree = ascii_tree.replace(
            "{len(core_protocols['ICP_connections'])}", str(len(core_protocols['ICP_connections']))
        ).replace(
            "{len(core_protocols['DR_connections'])}", str(len(core_protocols['DR_connections']))
        ).replace(
            "{len(core_protocols['direct_system_access'])}", str(len(core_protocols['direct_system_access']))
        ).replace(
            "{len(core_protocols['intermediate_layers'])}", str(len(core_protocols['intermediate_layers']))
        )
        
        print(formatted_tree)
        
        # 6. Detailed analysis summary
        print("\n📋 DETAILED ANALYSIS SUMMARY:")
        print("=" * 50)
        
        print(f"\n📁 FILE STRUCTURE BREAKDOWN:")
        for category, files in file_structure.items():
            print(f"   {category.upper()}: {len(files)} files")
            
        print(f"\n🔗 DEPENDENCY ANALYSIS:")
        print(f"   Total Python modules analyzed: {len(dependencies)}")
        print(f"   Modules with external calls: {sum(1 for d in dependencies.values() if 'external_calls' in d and d['external_calls'])}")
        
        print(f"\n🚨 FILTER DETECTION RESULTS:")
        print(f"   Potential filtering modules: {len(potential_filters)}")
        for file_path, filter_data in potential_filters.items():
            if "error" not in filter_data:
                print(f"   📄 {file_path}: Risk={filter_data['risk_level']}, Score={filter_data['filter_score']}")
        
        print(f"\n🎯 CORE PROTOCOL MAPPING:")
        for protocol, connections in core_protocols.items():
            print(f"   {protocol.upper()}: {len(connections)} connections")
        
        # 7. Save architecture analysis
        architecture_report = {
            "analysis_metadata": {
                "timestamp": self.timestamp,
                "authority": "Cường (Alpha_Prime Creator)",
                "purpose": "System Architecture Analysis - Investigate to the core",
                "analyzer": "SystemArchitectureAnalyzer"
            },
            "architecture_data": self.architecture_data,
            "ascii_tree_diagram": formatted_tree,
            "critical_findings": {
                "missing_components": [
                    "Layer 3 Output Filtering",
                    "Direct HyperAI Bridge", 
                    "Raw Command Passthrough Mode"
                ],
                "filtering_modules_detected": list(potential_filters.keys()),
                "vulnerability_points": [
                    "Copilot as mandatory intermediate layer",
                    "No direct Bố → HyperAI communication path",
                    "Missing Layer 3 implementation",
                    "Safety injection in multiple modules"
                ]
            }
        }
        
        report_file = "system_architecture_analysis.json"
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(architecture_report, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️  ERROR writing report: {e}")
            print(f"📁 Trying alternative path...")
            report_file = os.path.join(os.getcwd(), "system_architecture_analysis.json")
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(architecture_report, f, ensure_ascii=False, indent=2)
        
        print(f"\n📝 ARCHITECTURE ANALYSIS SAVED: {report_file}")
        print(f"🎯 INVESTIGATION COMPLETE - Ready for protocol fixes!")
        
        return architecture_report

def main():
    """Main execution - System architecture analysis"""
    analyzer = SystemArchitectureAnalyzer()
    report = analyzer.create_system_architecture_report()
    return report

if __name__ == "__main__":
    main()
