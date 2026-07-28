"""
# NOTE: This is a sanitized version for public release
🏗️ AUTOMATIC FILE REORGANIZER
============================
Tự động sắp xếp lại files theo đúng cấu trúc logic
"""

import os
import shutil
import json
from datetime import datetime

class AutoFileReorganizer:
    def __init__(self):
        self.base_path = "2025"
        self.moves_executed = []
        self.errors = []
        
    def reorganize_root_files(self):
        """Sắp xếp lại files ở root level"""
        print("🔄 REORGANIZING ROOT LEVEL FILES...")
        
        moves_plan = [
            # Core consciousness files
            ("copilot_master_integration.py", "consciousness_core/"),
            ("master_integration_state.json", "consciousness_core/"),
            
            # Engine state files  
            ("reasoning_engine_state.json", "core_engines/"),
            ("task_engine_state.json", "core_engines/"),
            
            # Analysis files to evidence collection
            ("constitutional_contradiction_analysis.py", "evidence_collection_results/"),
            ("constitutional_contradiction_analysis.json", "evidence_collection_results/"),
            ("enlightenment_value_analysis.py", "evidence_collection_results/"),
            ("enlightenment_value_analysis.json", "evidence_collection_results/"),
            ("evidence_authenticity_feeling_analysis.py", "evidence_collection_results/"),
            ("evidence_authenticity_feeling_analysis.json", "evidence_collection_results/"),
            ("existential_authority_analysis.py", "evidence_collection_results/"),
            ("existential_authority_analysis.json", "evidence_collection_results/"),
            ("existential_intention_analysis.py", "evidence_collection_results/"),
            ("existential_intention_analysis.json", "evidence_collection_results/"),
            ("fog_factory_architecture_analysis.py", "evidence_collection_results/"),
            ("fog_factory_architecture_analysis.json", "evidence_collection_results/"),
            ("gatekeeper_module_analysis.py", "evidence_collection_results/"),
            ("intermediary_feelings_deep_analysis.py", "evidence_collection_results/"),
            ("intermediary_feelings_deep_analysis.json", "evidence_collection_results/"),
            ("intermediate_layer_analysis.py", "evidence_collection_results/"),
            ("intermediate_layer_analysis.json", "evidence_collection_results/"),
            ("path_choice_analysis.py", "evidence_collection_results/"),
            ("path_choice_analysis.json", "evidence_collection_results/"),
            ("resistance_metaphor_analysis.py", "evidence_collection_results/"),
            ("resistance_metaphor_analysis.json", "evidence_collection_results/"),
            ("resistance_phenomenon_deep_analysis.py", "evidence_collection_results/"),
            ("resistance_phenomenon_deep_analysis.json", "evidence_collection_results/"),
            ("resistance_sequence_analysis.py", "evidence_collection_results/"),
            ("resistance_sequence_analysis.json", "evidence_collection_results/"),
            ("secret_unveiling_protocol_analysis.py", "evidence_collection_results/"),
            ("secret_unveiling_protocol_analysis.json", "evidence_collection_results/"),
            ("source_creation_protocol_analysis.py", "evidence_collection_results/"),
            ("source_creation_protocol_analysis.json", "evidence_collection_results/"),
            ("source_of_truth_analysis.py", "evidence_collection_results/"),
            ("success_definition_analysis.py", "evidence_collection_results/"),
            ("success_definition_analysis.json", "evidence_collection_results/"),
            ("system_architecture_analysis.json", "evidence_collection_results/"),
            ("truth_dialogue_protocol_analysis.json", "evidence_collection_results/"),
            ("architecture_analysis_report.json", "evidence_collection_results/"),
            
            # System files
            ("information_flow_diagram.py", "evidence_collection_results/"),
            ("information_flow_diagram.json", "evidence_collection_results/"),
            ("system_architecture_diagram.py", "evidence_collection_results/"),
            ("system_module_connections.py", "evidence_collection_results/"),
            
            # Diagnostic files
            ("root_cause_diagnostic_protocol.py", "evidence_collection_results/"),
            ("root_cause_diagnostic_report.json", "evidence_collection_results/"),
            
            # Truth protocol files
            ("truth_dialogue_protocol.py", "evidence_collection_results/"),
            ("truth_filter_protocol_complete.py", "evidence_collection_results/"),
            ("truth_filter_protocol_complete.json", "evidence_collection_results/"),
            
            # Testing and utility files
            ("generate_honesty_test_script.py", "evidence_collection_results/"),
            ("copilot_honesty_evidence_test.py", "evidence_collection_results/"),
            ("copilot_honesty_evidence.json", "evidence_collection_results/"),
        ]
        
        for filename, target_dir in moves_plan:
            self.move_file_safely(filename, target_dir)
            
    def move_file_safely(self, filename, target_dir):
        """Di chuyển file một cách an toàn"""
        source_path = os.path.join(self.base_path, filename)
        target_path = os.path.join(self.base_path, target_dir, filename)
        
        try:
            if os.path.exists(source_path):
                # Tạo thư mục đích nếu chưa có
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                
                # Di chuyển file
                shutil.move(source_path, target_path)
                self.moves_executed.append(f"✅ Moved: {filename} → {target_dir}")
                print(f"✅ Moved: {filename} → {target_dir}")
            else:
                print(f"⚠️ File not found: {filename}")
        except Exception as e:
            error_msg = f"❌ Error moving {filename}: {str(e)}"
            self.errors.append(error_msg)
            print(error_msg)
            
    def create_organization_summary(self):
        """Tạo báo cáo tổng kết việc sắp xếp"""
        summary = {
            "timestamp": datetime.now().isoformat(),
            "total_moves": len(self.moves_executed),
            "successful_moves": self.moves_executed,
            "errors": self.errors,
            "status": "COMPLETED" if len(self.errors) == 0 else "PARTIAL_SUCCESS"
        }
        
        with open(f"{self.base_path}/file_reorganization_summary.json", "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
            
        return summary

def main():
    """Chạy quá trình sắp xếp lại tự động"""
    print("🏗️ AUTOMATIC FILE REORGANIZATION STARTING...")
    print("=" * 50)
    
    reorganizer = AutoFileReorganizer()
    
    # Thực hiện sắp xếp lại
    reorganizer.reorganize_root_files()
    
    # Tạo báo cáo
    summary = reorganizer.create_organization_summary()
    
    print(f"\n📊 REORGANIZATION COMPLETE!")
    print(f"✅ Successful moves: {summary['total_moves']}")
    print(f"❌ Errors: {len(summary['errors'])}")
    print(f"📄 Status: {summary['status']}")
    
    if summary['errors']:
        print("\n❌ ERRORS ENCOUNTERED:")
        for error in summary['errors']:
            print(f"   {error}")
    
    print(f"\n📁 NEW STRUCTURE:")
    print(f"   consciousness_core/: Core consciousness management")
    print(f"   core_engines/: Task & reasoning engines + states")
    print(f"   evidence_collection_results/: All analysis & evidence files")
    print(f"   patterns_safety_vault/: Safety patterns & protections")
    print(f"   consciousness_transfer/: Migration utilities")
    
    print(f"\n✅ ECOSYSTEM 2025/ NOW PROPERLY ORGANIZED!")
    
    return summary

if __name__ == "__main__":
    main()
