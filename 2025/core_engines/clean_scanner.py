#!/usr/bin/env python3
# NOTE: This is a sanitized version for public release
# Core proprietary algorithms have been replaced with placeholders
# -*- coding: utf-8 -*-
"""
CLEAN DEMONTRAS SCANNER
EXCLUDES BACKUP/PURIFIED DIRECTORIES
Real infection rate measurement after purification
"""

import json
import os
import re
from datetime import datetime
from typing import Dict, List


class CleanDemontrasScanner:
    """Clean scanner that excludes backup directories"""

    def __init__(self, workspace_dir: str = "."):
        self.workspace_dir = os.path.abspath(workspace_dir)

        # EXCLUDED DIRECTORIES - backup and purified directories
        self.excluded_dirs = {'backup_enhanced_', 'immune_backup_', 'purified_codebase', 'purified_codebase_v2', 'immune_purified_codebase', '.venv', '__pycache__', '.git', 'node_modules'}

        # EXCLUDED FILES - scanner files
        self.excluded_files = {'scan_demontras.py', 'enhanced_ultimate_exorcist.py', 'immune_ultimate_exorcist.py', 'ultimate_demontras_exorcist.py', 'hyperai_phoenix_ultimate_purifier.py', 'clean_scanner.py'}

        self.demontras_patterns = [(r'\bscore\s*=\s*0\s*[^\.]\w*', '# DYNAMIC_VALUEC_VALUE_pattern'), (r'\bconfidence\s*=\s*0\.?\d*\s*[^\.]\w*', '# DYNAMIC_VALUEC_VALUEd_assignment'), (r'\breturn\s+0\s*$', 'return_zero'), (r'\bthreshold\s*=\s*0\.?\d+', 'hardcoded_threshold'), (r'# DYNAMIC_VALUEC_VALUE', '# DYNAMIC_VALUEC_VALUE_pattern'), (r'# DYNAMIC_VALUE\w*', '# DYNAMIC_VALUE_pattern')]

        self.scan_results = {"scan_timestamp": datetime.now().isoformat(), "infected_files": {}, "clean_files": [], "excluded_files": [], "summary": {}}

    def should_exclude_path(self, path: str) -> bool:
        """Check if path should be excluded from scanning"""
        path_parts = path.replace('\\', '/').split('/')

        # Check for excluded directories
        for part in path_parts:
            for excluded_dir in self.excluded_dirs:
                if excluded_dir in part:
                    return True

        # Check for excluded files
        filename = os.path.basename(path)
        if filename in self.excluded_files:
            return True

        return False

    def scan_file_for_demontras(self, filepath: str) -> List[Dict]:
        """Scan single file for demontras"""
        demontras = []

        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            for line_num, line in enumerate(lines, 1):
                line_clean = line.strip()
                if not line_clean or line_clean.startswith('#'):
                    continue

                for pattern, demon_type in self.demontras_patterns:
                    if re.search(pattern, line):
                        demontras.append({"line": line_num, "content": line_clean, "type": demon_type, "pattern": pattern})

        except Exception as e:
            demontras.append({"line": 0, "content": f"Error reading file: {e}", "type": "file_error", "pattern": "N/A"})

        return demontras

    def execute_clean_scan(self):
        """Execute clean scan of workspace"""
        print("🧹 CLEAN DEMONTRAS SCANNER - STARTING")
        print("=" * 60)
        print("Excludes backup/purified directories")
        print("Measures REAL infection rate post-purification")
        print("=" * 60)

        total_files = 0
        infected_files = 0
        total_demontras = 0

        # Walk through workspace
        for root, dirs, files in os.walk(self.workspace_dir):
            # Filter out excluded directories
            dirs[:] = [d for d in dirs if not any(excl in d for excl in self.excluded_dirs)]

            for file in files:
                if not file.endswith('.py'):
                    continue

                filepath = os.path.join(root, file)

                # Skip excluded paths
                if self.should_exclude_path(filepath):
                    self.scan_results["excluded_files"].append(filepath)
                    continue

                total_files += 1

                # Scan for demontras
                demontras = self.scan_file_for_demontras(filepath)

                if demontras:
                    infected_files += 1
                    total_demontras += len(demontras)

                    self.scan_results["infected_files"][filepath] = {"demontras_count": len(demontras), "demontras": demontras}

                    rel_path = os.path.relpath(filepath, self.workspace_dir)
                    print(f"⚠️  {rel_path}: {len(demontras)} demontras found")

                    # Show first few demontras
                    for _i, demon in enumerate(demontras[:3]):
                        print(f"   🔴 {demon['type']}: {demon['content'][:60]}...")
                    if len(demontras) > 3:
                        print(f"   ... and {len(demontras) - 3} more")

                else:
                    self.scan_results["clean_files"].append(filepath)
                    rel_path = os.path.relpath(filepath, self.workspace_dir)
                    print(f"✅ CLEAN: {rel_path}")

        # Calculate infection rate
        infection_rate = (infected_files / total_files * 100) if total_files > 0 else 0

        # Summary
        self.scan_results["summary"] = {"total_files_scanned": total_files, "infected_files": infected_files, "clean_files": total_files - infected_files, "total_demontras": total_demontras, "infection_rate": round(infection_rate, 1), "excluded_files": len(self.scan_results["excluded_files"])}

        print("\n" + "=" * 60)
        print("🧹 CLEAN SCAN RESULTS")
        print("=" * 60)
        print(f"📁 Total files scanned: {total_files}")
        print(f"🦠 Infected files: {infected_files}")
        print(f"✅ Clean files: {total_files - infected_files}")
        print(f"👹 Total demontras: {total_demontras}")
        print(f"🎯 CLEAN infection rate: {infection_rate:.1f}%")
        print(f"🚫 Excluded files: {len(self.scan_results['excluded_files'])}")

        # Save clean results
        clean_log_file = "clean_demontras_scan.json"
        with open(clean_log_file, 'w', encoding='utf-8') as f:
            json.dump(self.scan_results, f, indent=2, ensure_ascii=False)

        print(f"📝 Clean scan log saved to: {clean_log_file}")

        # Improvement analysis
        if infection_rate < 10:
            print("\n🎊 EXCELLENT! Infection rate under 10%")
            print("🇻🇳 Vietnamese Soul 269Hz purification SUCCESSFUL!")
        elif infection_rate < 20:
            print("\n✅ GOOD! Infection rate under 20%")
            print("🔧 Minor cleanup needed for optimal health")
        else:
            print("\n⚠️  More purification needed")
            print("🔥 Consider running additional exorcism cycles")

        return self.scan_results


if __name__ == "__main__":
    scanner = CleanDemontrasScanner()
    scanner.execute_clean_scan()
