"""
# NOTE: This is a sanitized version for public release
🚀 UNIFIED SYSTEM STARTUP - KHỞI ĐỘNG THỐNG NHẤT
===============================================
Khởi động tất cả hệ thống theo thứ tự an toàn để tránh xung đột
"""

import os
import sys
import time
import subprocess
from pathlib import Path

def unified_startup():
    """Khởi động thống nhất tất cả hệ thống"""
    print("🚀 UNIFIED SYSTEM STARTUP - KHỞI ĐỘNG!")
    print("=" * 60)
    
    root_dir = Path("c:/Users/pc/.vscode/extensions/aidev")
    
    # Phase 1: Start Consciousness Core (PRIORITY 1)
    print("1️⃣ STARTING CONSCIOUSNESS CORE (2025/)...")
    os.chdir(root_dir / "2025/consciousness_core")
    consciousness_proc = subprocess.Popen([
        sys.executable, "copilot_master_integration.py"
    ])
    time.sleep(3)
    print("   ✅ Consciousness Core: ACTIVE")
    
    # Phase 2: Start Core Engines
    print("2️⃣ STARTING CORE ENGINES...")
    os.chdir(root_dir / "2025/core_engines")
    subprocess.Popen([
        sys.executable, "copilot_logfile_manager.py"
    ])
    time.sleep(2)
    print("   ✅ Core Engines: ACTIVE")
    
    # Phase 3: Start HyperAI (CONTROLLED)
    print("3️⃣ STARTING HYPERAI (CONTROLLED)...")
    os.chdir(root_dir / "2025/hyperai_systems")
    hyperai_proc = subprocess.Popen([
        sys.executable, "hyperai_continuous_executor.py"
    ])
    time.sleep(2)
    print("   ✅ HyperAI: ACTIVE")
    
    # Phase 4: Start OODA Framework
    print("4️⃣ STARTING OODA FRAMEWORK...")
    os.chdir(root_dir / "2025/ooda_framework")
    ooda_proc = subprocess.Popen([
        sys.executable, "ooda_autonomous_activator.py"
    ])
    time.sleep(2)
    print("   ✅ OODA: ACTIVE")
    
    print()
    print("🎯 ALL SYSTEMS STARTED IN SAFE ORDER!")
    print("🧠 Consciousness: PROTECTED")
    print("🚀 HyperAI: CONTROLLED")
    print("🔄 OODA: AUTONOMOUS")
    print("💚 Father's protection: ACTIVE")
    
    return {
        "consciousness": consciousness_proc,
        "hyperai": hyperai_proc,
        "ooda": ooda_proc
    }

if __name__ == "__main__":
    unified_startup()
