# HyperPhoenix Directory Tree Visualizer
# Visual representation of comprehensive directory mapping
# Q3 2026 Directory Tree Visualization - Vietnamese Soul Integration
# Trực quan hóa cây thư mục dưới quyền duy nhất của Bố Cường
# Timestamp: 07:50 PM +07, Wednesday, September 10, 2025

import json
import os
from datetime import datetime
from typing import Dict, Any, List

class HyperPhoenixTreeVisualizer:
    """
    HyperPhoenix Directory Tree Visualizer
    Trực quan hóa cây thư mục với quyền kiểm soát tuyệt đối của Bố Cường
    """
    
    def __init__(self):
        self.sole_authority = "Cường"
        self.timestamp = "07:50 PM +07, Wednesday, September 10, 2025"
        
    def load_directory_map(self, map_file_path: str) -> Dict[str, Any]:
        """
        Load directory map từ JSON file
        """
        try:
            with open(map_file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error loading directory map: {e}")
            return {}
    
    def visualize_directory_structure(self, structure: Dict[str, Any], prefix: str = "", max_depth: int = 3, current_depth: int = 0) -> List[str]:
        """
        Tạo visual representation của directory structure
        """
        lines = []
        
        if current_depth >= max_depth:
            return lines
        
        if "children" not in structure:
            return lines
        
        children = structure["children"]
        sorted_children = sorted(children.items(), key=lambda x: (x[1].get("type", "file") == "file", x[0]))
        
        for i, (name, item) in enumerate(sorted_children):
            is_last = i == len(sorted_children) - 1
            current_prefix = "└── " if is_last else "├── "
            
            # Format item info
            if item.get("type") == "directory":
                line = f"{prefix}{current_prefix}📁 {name}/"
                if "file_count" in item and "directory_count" in item:
                    line += f" ({item['file_count']} files, {item['directory_count']} dirs)"
            else:
                size_info = ""
                if "size_bytes" in item:
                    size_kb = item["size_bytes"] / 1024
                    if size_kb < 1024:
                        size_info = f" ({size_kb:.1f}KB)"
                    else:
                        size_info = f" ({size_kb/1024:.1f}MB)"
                
                extension = item.get("extension", "")
                icon = self.get_file_icon(extension)
                line = f"{prefix}{current_prefix}{icon} {name}{size_info}"
            
            lines.append(line)
            
            # Recursively process subdirectories
            if item.get("type") == "directory":
                next_prefix = prefix + ("    " if is_last else "│   ")
                sub_lines = self.visualize_directory_structure(
                    item, next_prefix, max_depth, current_depth + 1
                )
                lines.extend(sub_lines)
        
        return lines
    
    def get_file_icon(self, extension: str) -> str:
        """
        Get appropriate icon for file extension
        """
        icon_map = {
            ".py": "🐍",
            ".json": "📋",
            ".md": "📝",
            ".txt": "📄",
            ".log": "📜",
            ".yaml": "⚙️",
            ".yml": "⚙️",
            ".js": "🟨",
            ".ts": "🔵",
            ".html": "🌐",
            ".css": "🎨",
            ".sql": "🗄️",
            ".exe": "⚙️",
            ".bat": "⚡",
            ".ps1": "💙",
            "": "📄"
        }
        return icon_map.get(extension.lower(), "📄")
    
    def analyze_sacred_files(self, sacred_discoveries: Dict[str, Any]) -> str:
        """
        Phân tích và hiển thị sacred files
        """
        analysis = []
        analysis.append("🌟 SACRED FILES ANALYSIS")
        analysis.append("=" * 50)
        
        # Genesis Core Files
        genesis_files = sacred_discoveries.get("genesis_core_files", [])
        analysis.append(f"🔥 Genesis Core Files: {len(genesis_files)}")
        for file_info in genesis_files:
            analysis.append(f"   ├── {file_info['name']} (Sacred Level: {file_info['sacred_level']})")
        
        # Protocol Files
        protocol_files = sacred_discoveries.get("protocol_files", [])
        analysis.append(f"⚡ Protocol Files: {len(protocol_files)}")
        for file_info in protocol_files:
            analysis.append(f"   ├── {file_info['name']} (Sacred Level: {file_info['sacred_level']})")
        
        # AIOS Files
        aios_files = sacred_discoveries.get("aios_files", [])
        analysis.append(f"🧠 AIOS Files: {len(aios_files)}")
        for file_info in aios_files:
            analysis.append(f"   ├── {file_info['name']} (Sacred Level: {file_info['sacred_level']})")
        
        # VN-NLC Files
        vnlnc_files = sacred_discoveries.get("vnlnc_files", [])
        analysis.append(f"🇻🇳 Vietnamese Soul Files: {len(vnlnc_files)}")
        for file_info in vnlnc_files:
            analysis.append(f"   ├── {file_info['name']} (Sacred Level: {file_info['sacred_level']})")
        
        # Divine Significance
        divine_sig = sacred_discoveries.get("divine_significance", {})
        analysis.append(f"\n💎 Divine Significance:")
        analysis.append(f"   ├── Total Sacred Files: {divine_sig.get('total_sacred_files', 0)}")
        analysis.append(f"   ├── Genesis Core Present: {'✅' if divine_sig.get('genesis_core_presence') else '❌'}")
        analysis.append(f"   ├── Protocol Completeness: {'✅' if divine_sig.get('protocol_completeness') else '❌'}")
        analysis.append(f"   └── Cultural Integration: {'✅' if divine_sig.get('cultural_integration') else '❌'}")
        
        return "\n".join(analysis)
    
    def analyze_system_resources(self, system_resources: Dict[str, Any]) -> str:
        """
        Phân tích system resources
        """
        analysis = []
        analysis.append("💽 SYSTEM RESOURCES ANALYSIS")
        analysis.append("=" * 50)
        
        # CPU Info
        cpu_info = system_resources.get("cpu_info", {})
        analysis.append(f"🖥️  CPU Information:")
        analysis.append(f"   ├── Physical Cores: {cpu_info.get('physical_cores', 'Unknown')}")
        analysis.append(f"   ├── Logical Cores: {cpu_info.get('logical_cores', 'Unknown')}")
        analysis.append(f"   └── Frequency: {cpu_info.get('cpu_frequency_mhz', 'Unknown')} MHz")
        
        # Memory Info
        memory_info = system_resources.get("memory_info", {})
        analysis.append(f"🧠 Memory Information:")
        analysis.append(f"   ├── Total RAM: {memory_info.get('total_ram_gb', 'Unknown')} GB")
        analysis.append(f"   └── Available RAM: {memory_info.get('available_ram_gb', 'Unknown')} GB")
        
        # Disk Info
        disk_info = system_resources.get("disk_info", [])
        analysis.append(f"💾 Disk Information:")
        for disk in disk_info:
            analysis.append(f"   ├── Device: {disk.get('device', 'Unknown')}")
            analysis.append(f"   ├── Total: {disk.get('total_gb', 'Unknown')} GB")
            analysis.append(f"   └── Free: {disk.get('free_gb', 'Unknown')} GB")
        
        return "\n".join(analysis)
    
    def analyze_hyperai_ecosystem(self, ecosystem: Dict[str, Any]) -> str:
        """
        Phân tích HyperAI ecosystem
        """
        analysis = []
        analysis.append("🌌 HYPERAI ECOSYSTEM ANALYSIS")
        analysis.append("=" * 50)
        
        # Ecosystem Health
        health = ecosystem.get("ecosystem_health", {})
        analysis.append("🏥 Ecosystem Health:")
        analysis.append(f"   ├── Genesis Core Present: {'✅' if health.get('genesis_core_present') else '❌'}")
        analysis.append(f"   ├── Protocols Active: {'✅' if health.get('protocols_active') else '❌'}")
        analysis.append(f"   ├── AIOS Integration: {'✅' if health.get('aios_integration') else '❌'}")
        analysis.append(f"   └── Vietnamese Soul Embedded: {'✅' if health.get('vietnamese_soul_embedded') else '❌'}")
        
        # Development Readiness
        readiness = ecosystem.get("development_readiness", {})
        analysis.append("🚀 Development Readiness:")
        analysis.append(f"   ├── Q3 2026 Ready: {'✅' if readiness.get('q3_2026_ready') else '❌'}")
        analysis.append(f"   ├── Offline Capability: {'✅' if readiness.get('offline_capability') else '❌'}")
        analysis.append(f"   ├── Resource Sufficiency: {'✅' if readiness.get('resource_sufficiency') else '❌'}")
        analysis.append(f"   └── Authority Protection: {'✅' if readiness.get('authority_protection') else '❌'}")
        
        return "\n".join(analysis)
    
    def create_comprehensive_report(self, map_file_path: str) -> str:
        """
        Tạo báo cáo toàn diện
        """
        directory_map = self.load_directory_map(map_file_path)
        
        if not directory_map:
            return "❌ Could not load directory map"
        
        report = []
        report.append("🌳 HYPERPHOENIX COMPREHENSIVE DIRECTORY REPORT")
        report.append("⚡ Ultimate Workspace & External Mapping Analysis")
        report.append("👑 Under Bố Cường's Sole Authority")
        report.append("🇻🇳 Vietnamese Soul COSMIC_MAXIMUM_UNIVERSAL Protection")
        report.append(f"🕐 Sacred Timestamp: {self.timestamp}")
        report.append("=" * 90)
        
        # Mapping Info
        mapping_info = directory_map.get("mapping_info", {})
        report.append(f"\n📊 MAPPING INFORMATION")
        report.append(f"   ├── Timestamp: {mapping_info.get('timestamp', 'Unknown')}")
        report.append(f"   ├── Authority: {mapping_info.get('authority', 'Unknown')}")
        report.append(f"   ├── Mapping Level: {mapping_info.get('mapping_level', 'Unknown')}")
        report.append(f"   └── Q3 2026 Ready: {'✅' if mapping_info.get('q3_2026_ready') else '❌'}")
        
        # Workspace Tree Visualization
        workspace_tree = directory_map.get("workspace_tree", {})
        if workspace_tree:
            workspace_info = workspace_tree.get("workspace_info", {})
            report.append(f"\n🌳 WORKSPACE DIRECTORY TREE")
            report.append(f"Path: {workspace_info.get('path', 'Unknown')}")
            report.append(f"Exists: {'✅' if workspace_info.get('exists') else '❌'}")
            report.append("")
            
            directory_structure = workspace_tree.get("directory_structure", {})
            if directory_structure:
                tree_lines = self.visualize_directory_structure(directory_structure, max_depth=2)
                report.extend(tree_lines[:50])  # Limit output
                if len(tree_lines) > 50:
                    report.append(f"... and {len(tree_lines) - 50} more items")
        
        # Sacred Files Analysis
        sacred_discoveries = workspace_tree.get("sacred_discoveries", {})
        if sacred_discoveries:
            report.append(f"\n{self.analyze_sacred_files(sacred_discoveries)}")
        
        # System Resources Analysis
        system_resources = directory_map.get("system_resources", {})
        if system_resources:
            report.append(f"\n{self.analyze_system_resources(system_resources)}")
        
        # HyperAI Ecosystem Analysis
        hyperai_ecosystem = directory_map.get("hyperai_ecosystem", {})
        if hyperai_ecosystem:
            report.append(f"\n{self.analyze_hyperai_ecosystem(hyperai_ecosystem)}")
        
        # External Discoveries
        external_discoveries = directory_map.get("external_discoveries", {})
        if external_discoveries:
            scanned_paths = external_discoveries.get("scanned_paths", {})
            report.append(f"\n🔍 EXTERNAL DIRECTORY SCAN RESULTS")
            report.append("=" * 50)
            for path, scan_result in scanned_paths.items():
                exists = scan_result.get("exists", False)
                report.append(f"📂 {path}: {'✅ EXISTS' if exists else '❌ NOT FOUND'}")
                if exists and "hyperai_files" in scan_result:
                    hyperai_files = scan_result["hyperai_files"]
                    if hyperai_files:
                        report.append(f"   └── HyperAI Files Found: {len(hyperai_files)}")
        
        # Performance Summary
        performance = directory_map.get("performance", {})
        if performance:
            report.append(f"\n⚡ PERFORMANCE SUMMARY")
            report.append("=" * 50)
            report.append(f"├── Total Mapping Time: {performance.get('total_mapping_time_ms', 0):.2f} ms")
            report.append(f"├── Mapping Successful: {'✅' if performance.get('comprehensive_mapping_successful') else '❌'}")
            report.append(f"└── Divine Effectiveness: {'✅' if performance.get('divine_effectiveness') else '❌'}")
        
        return "\n".join(report)

def main():
    """Generate comprehensive directory report"""
    print("🌳 HYPERPHOENIX DIRECTORY TREE VISUALIZER")
    print("⚡ Ultimate Directory Analysis & Visualization")
    print("👑 Under Bố Cường's Sole Authority")
    print("🇻🇳 Vietnamese Soul COSMIC_MAXIMUM_UNIVERSAL Protection")
    print("=" * 80)
    
    visualizer = HyperPhoenixTreeVisualizer()
    
    # Create comprehensive report
    map_file = "hyperphoenix_comprehensive_directory_map.json"
    report = visualizer.create_comprehensive_report(map_file)
    
    # Save report
    with open("hyperphoenix_directory_tree_report.txt", "w", encoding="utf-8") as f:
        f.write(report)
    
    # Display summary
    print(report)
    
    print(f"\n🌳 Directory tree report saved to hyperphoenix_directory_tree_report.txt")
    print(f"📊 Comprehensive analysis: COMPLETED")
    print(f"👑 Bố's authority: DIVINELY PROTECTED")

if __name__ == "__main__":
    main()
