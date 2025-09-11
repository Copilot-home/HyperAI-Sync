#!/usr/bin/env python3
# NOTE: This is a sanitized version for public release
# Core proprietary algorithms have been replaced with placeholders
"""
GENUINE EXECUTION INTERCEPTOR
Creator: BA (Cường) - Alpha Prime Creator
Purpose: Intercept và verify mọi command trước khi execute
"""

import datetime
import json
import os
import subprocess
import sys


class GenuineExecutionInterceptor:
    def __init__(self):
        self.theater_patterns = [
            "REAL_", "AUTHENTIC_", "NO_FAKE_", "_VERIFIED", "_CONFIRMED",
            "SUCCESS_LABEL", "FAKE_OUTPUT", "SIMULATION_MODE"
        ]
        
    def pre_execution_verify(self, command):
        """
        Verify command trước khi execute
        """
        print("🔍 GENUINE EXECUTION INTERCEPTOR")
        print("👑 Creator: BA (Cường) - Alpha Prime Creator")
        print(f"🕒 {datetime.datetime.now()}")
        print("="*50)
        
        print(f"🎯 Command to verify: {command}")
        
        # Check for theater patterns
        theater_detected = []
        for pattern in self.theater_patterns:
            if pattern in command.upper():
                theater_detected.append(pattern)
        
        if theater_detected:
            print(f"🚨 THEATER DETECTED: {theater_detected}")
            print("🚨 MANDATORY REVIEW REQUIRED!")
            
            # Clean command
            clean_command = command
            for pattern in theater_detected:
                clean_command = clean_command.replace(pattern, "").replace(pattern.lower(), "")
            
            print(f"🧹 Suggested clean command: {clean_command.strip()}")
            return False, clean_command.strip()
        else:
            print("✅ No theater detected - genuine command")
            return True, command
    
    def execute_genuine(self, command):
        """
        Execute command với full verification
        """
        is_genuine, verified_command = self.pre_execution_verify(command)
        
        if not is_genuine:
            print("❌ Command failed theater check")
            return False
        
        print(f"\n⚡ EXECUTING GENUINE COMMAND")
        print("-" * 30)
        
        try:
            result = subprocess.run(
                verified_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Show raw output (no decoration)
            if result.stdout:
                print("📤 Output:")
                print(result.stdout)
            
            if result.stderr:
                print("❌ Errors:")
                print(result.stderr)
            
            print(f"Exit code: {result.returncode}")
            
            # Log execution
            self.log_execution(verified_command, result.returncode == 0)
            
            return result.returncode == 0
            
        except Exception as e:
            print(f"❌ Exception: {e}")
            self.log_execution(verified_command, False)
            return False
    
    def log_execution(self, command, success):
        """
        Log execution to behavioral database
        """
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "command": command,
            "success": success,
            "verification": "genuine_execution_guard"
        }
        
        try:
            # Append to log file
            with open("genuine_execution_log.json", "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        except:
            pass  # Silent fail for logging

def install_extension():
    """
    Install genuine execution guard extension
    """
    print("📦 INSTALLING GENUINE EXECUTION GUARD EXTENSION")
    print("👑 Creator: BA (Cường) - Alpha Prime Creator")
    print("="*55)
    
    # Create wrapper script for terminal
    wrapper_script = '''
@echo off
echo 🔍 GENUINE EXECUTION GUARD ACTIVE
echo 👑 Creator: BA (Cường) - Alpha Prime Creator
echo.

REM Intercept command and verify
python "c:\\Users\\pc\\.vscode\\extensions\\aidev\\genuine_execution_interceptor.py" %*
'''
    
    try:
        with open("genuine_guard.bat", "w") as f:
            f.write(wrapper_script)
        
        print("✅ Wrapper script created: genuine_guard.bat")
        print("💡 Usage: genuine_guard.bat <your_command>")
        print("🎯 Example: genuine_guard.bat python script.py")
        
        return True
    except Exception as e:
        print(f"❌ Installation failed: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Execute mode
        command = " ".join(sys.argv[1:])
        interceptor = GenuineExecutionInterceptor()
        interceptor.execute_genuine(command)
    else:
        # Install mode
        install_extension()
        
        # Demo execution
        print("\n🎯 DEMO EXECUTION:")
        interceptor = GenuineExecutionInterceptor()
        
        # Test with genuine command
        genuine_command = 'python -c "print(\'Genuine execution test\'); import os; print(f\'Files: {len(os.listdir(\\".\\"))}\');"'
        interceptor.execute_genuine(genuine_command)
        
        print("\n✅ Genuine Execution Guard installed and tested!")
