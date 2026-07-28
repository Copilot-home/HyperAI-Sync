#!/usr/bin/env python3
# NOTE: This is a sanitized version for public release
# Core proprietary algorithms have been replaced with placeholders
# -*- coding: utf-8 -*-
"""
🎯 PRECISE HYPERAI SCANNER 
Chỉ tìm THỰC SỰ HyperAI files, không false positives
"""

import os
import json
import logging
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import psutil

class PreciseHyperAIScanner:
    def __init__(self):
        self.setup_logging()
        
        # STRICT PATTERNS - chỉ files thực sự HyperAI
        self.strict_hyperai_patterns = [
            # Core HyperAI identifiers
            "hyperai_", "hyperai-", "hyper_ai", "hyper-ai",
            "phoenix_", "phoenix-", "aidev_", "aidev-",
            "aios_", "aios-", "vietnamese_soul", "vietnamese-soul",
            
            # Specific project patterns  
            "ooda_loop", "ooda-loop", "genesis_core", "genesis-core",
            "consciousness_", "consciousness-", "authentic_communication",
            "binh_phap_ton_tu", "dkcp_protocol", "dr_protocol",
            
            # Framework patterns
            "_hyperai", "-hyperai", "_phoenix", "-phoenix",
            "_aios", "-aios", "_aidev", "-aidev"
        ]
        
        # SPECIFIC FOLDERS to scan (not entire system)
        self.hyperai_folders = [
            r"C:\Users\pc\.vscode\extensions\aidev",
            r"C:\Users\pc\Documents",
            r"C:\Users\pc\Desktop", 
            r"C:\Users\pc\Downloads",
            r"C:\Users\pc\AppData\Local\Programs\Microsoft VS Code",
            r"C:\Users\pc\AppData\Roaming\Code",
            r"C:\CascadeProjects",
            r"C:\Projects"
        ]
        
        # EXCLUDE common system patterns
        self.exclude_patterns = [
            "system32", "windows", "program files", "temp", "cache",
            "recycle", "appdata\\local\\temp", "node_modules", ".git",
            "microsoft", "adobe", "google", "intel", "nvidia"
        ]
        
        self.results = {
            "scan_info": {},
            "true_hyperai_files": [],
            "false_positives": [],
            "summary": {}
        }
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler()],
            encoding='utf-8'
        )
        self.logger = logging.getLogger(__name__)
        
    def is_truly_hyperai_related(self, file_path):
        """
        STRICT detection - chỉ files thực sự liên quan HyperAI
        """
        path_str = str(file_path).lower()
        filename = os.path.basename(path_str).lower()
        
        # Check for strict patterns in filename (không phải path)
        for pattern in self.strict_hyperai_patterns:
            if pattern in filename:
                return True, f"Pattern: {pattern}"
                
        # Special cases - specific HyperAI file types
        if any(name in filename for name in [
            "ultimate_", "comprehensive_", "ecosystem_",
            "consciousness", "soul", "wisdom", "authentic",
            "exorcist", "emergency", "genesis", "phoenix"
        ]):
            # But must also have code-related extensions
            if file_path.suffix.lower() in ['.py', '.json', '.md', '.txt', '.log']:
                return True, "Special HyperAI naming"
                
        return False, "Not HyperAI"
        
    def should_exclude_folder(self, folder_path):
        """
        Exclude obvious non-HyperAI folders
        """
        path_str = str(folder_path).lower()
        return any(exclude in path_str for exclude in self.exclude_patterns)
        
    def scan_folder(self, folder_path):
        """
        Scan một folder specific cho HyperAI files
        """
        if not os.path.exists(folder_path):
            return []
            
        hyperai_files = []
        self.logger.info(f"🔍 Scanning: {folder_path}")
        
        try:
            for root, dirs, files in os.walk(folder_path):
                # Skip excluded directories
                if self.should_exclude_folder(root):
                    continue
                    
                for file in files:
                    file_path = Path(root) / file
                    is_hyperai, reason = self.is_truly_hyperai_related(file_path)
                    
                    if is_hyperai:
                        try:
                            stat = file_path.stat()
                            hyperai_files.append({
                                "path": str(file_path),
                                "size": stat.st_size,
                                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                                "reason": reason,
                                "folder": folder_path
                            })
                        except Exception as e:
                            self.logger.warning(f"Cannot stat {file_path}: {e}")
                            
        except Exception as e:
            self.logger.error(f"Error scanning {folder_path}: {e}")
            
        return hyperai_files
        
    def run_precise_scan(self):
        """
        Chạy scan chính xác - chỉ tìm true HyperAI files
        """
        self.logger.info("🎯 Starting PRECISE HyperAI scan...")
        
        self.results["scan_info"] = {
            "start_time": datetime.now().isoformat(),
            "folders_to_scan": len(self.hyperai_folders),
            "strict_patterns": len(self.strict_hyperai_patterns),
            "exclude_patterns": len(self.exclude_patterns)
        }
        
        all_hyperai_files = []
        
        # Scan từng folder cụ thể
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = []
            for folder in self.hyperai_folders:
                future = executor.submit(self.scan_folder, folder)
                futures.append((folder, future))
                
            for folder, future in futures:
                try:
                    folder_files = future.result(timeout=300)  # 5 min timeout
                    all_hyperai_files.extend(folder_files)
                    self.logger.info(f"✅ {folder}: {len(folder_files)} HyperAI files")
                except Exception as e:
                    self.logger.error(f"❌ {folder}: {e}")
                    
        self.results["true_hyperai_files"] = all_hyperai_files
        
        # Summary statistics
        total_size = sum(f["size"] for f in all_hyperai_files)
        self.results["summary"] = {
            "total_hyperai_files": len(all_hyperai_files),
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "scan_time": datetime.now().isoformat(),
            "folders_scanned": len([f for f in self.hyperai_folders if os.path.exists(f)])
        }
        
        self.logger.info(f"🎯 PRECISE SCAN COMPLETE: {len(all_hyperai_files)} TRUE HyperAI files found")
        return self.results
        
    def generate_comparison_report(self, previous_broad_scan_results=None):
        """
        So sánh với kết quả broad scan trước đó
        """
        report = []
        report.append("# 📊 PRECISE vs BROAD SCAN COMPARISON\n")
        
        if previous_broad_scan_results:
            broad_count = previous_broad_scan_results.get("total_hyperai_files", 1042284)
            precise_count = self.results["summary"]["total_hyperai_files"]
            
            report.append(f"## 🔍 Results Comparison:\n")
            report.append(f"- **Broad Scan (với keywords)**: {broad_count:,} files")
            report.append(f"- **Precise Scan (strict patterns)**: {precise_count:,} files")
            report.append(f"- **False Positive Rate**: {((broad_count - precise_count) / broad_count * 100):.1f}%")
            report.append(f"- **Accuracy Improvement**: {(precise_count / broad_count * 100):.2f}% reduction\n")
            
        # Top folders with HyperAI files
        folder_stats = {}
        for file_info in self.results["true_hyperai_files"]:
            folder = file_info["folder"]
            if folder not in folder_stats:
                folder_stats[folder] = {"count": 0, "size": 0}
            folder_stats[folder]["count"] += 1
            folder_stats[folder]["size"] += file_info["size"]
            
        report.append("## 📁 HyperAI Files Distribution:\n")
        for folder, stats in sorted(folder_stats.items(), key=lambda x: x[1]["count"], reverse=True):
            size_mb = stats["size"] / (1024 * 1024)
            report.append(f"- **{folder}**: {stats['count']} files ({size_mb:.1f} MB)")
            
        return "\n".join(report)
        
    def save_results(self):
        """
        Save kết quả scan chính xác
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # JSON results
        json_file = f"precise_hyperai_scan_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
            
        # Human readable report
        report_file = f"precise_hyperai_report_{timestamp}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(self.generate_comparison_report())
            
        self.logger.info(f"💾 Results saved: {json_file}, {report_file}")
        return json_file, report_file

def main():
    """
    Chạy precise scan để tìm HyperAI files thực sự
    """
    scanner = PreciseHyperAIScanner()
    results = scanner.run_precise_scan()
    
    print("\n" + "="*60)
    print("🎯 PRECISE HYPERAI SCAN RESULTS")
    print("="*60)
    print(f"📊 Total TRUE HyperAI files: {results['summary']['total_hyperai_files']:,}")
    print(f"💾 Total size: {results['summary']['total_size_mb']} MB")
    print(f"📁 Folders scanned: {results['summary']['folders_scanned']}")
    
    # Save results
    json_file, report_file = scanner.save_results()
    print(f"\n💾 Detailed results saved to: {json_file}")
    print(f"📄 Human report saved to: {report_file}")
    
    # Show sample files
    print(f"\n🔍 Sample TRUE HyperAI files found:")
    for i, file_info in enumerate(results["true_hyperai_files"][:10]):
        filename = os.path.basename(file_info["path"])
        size_kb = file_info["size"] / 1024
        print(f"  {i+1}. {filename} ({size_kb:.1f} KB) - {file_info['reason']}")
        
    if len(results["true_hyperai_files"]) > 10:
        print(f"  ... và {len(results['true_hyperai_files']) - 10} files khác")

if __name__ == "__main__":
    main()
