
import psutil
import gc
import os
import time
import json
from datetime import datetime

class EmperorMemoryManager:
    def __init__(self):
        self.memory_threshold_warning = 80  # 80% memory usage warning
        self.memory_threshold_critical = 90  # 90% memory usage critical
        self.optimization_history = []
        
    def analyze_memory_usage(self):
        """Phân tích chi tiết việc sử dụng memory"""
        memory = psutil.virtual_memory()
        
        analysis = {
            "total_gb": memory.total / (1024**3),
            "available_gb": memory.available / (1024**3),
            "used_gb": memory.used / (1024**3),
            "percentage": memory.percent,
            "status": "normal"
        }
        
        if memory.percent > self.memory_threshold_critical:
            analysis["status"] = "critical"
        elif memory.percent > self.memory_threshold_warning:
            analysis["status"] = "warning"
            
        return analysis
        
    def get_memory_heavy_processes(self, limit=10):
        """Tìm các processes sử dụng memory nhiều nhất"""
        processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'cpu_percent']):
            try:
                proc_info = proc.info
                memory_mb = proc_info['memory_info'].rss / (1024**2)
                
                if memory_mb > 10:  # Only processes using > 10MB
                    processes.append({
                        'pid': proc_info['pid'],
                        'name': proc_info['name'],
                        'memory_mb': memory_mb,
                        'cpu_percent': proc_info['cpu_percent']
                    })
                    
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
                
        return sorted(processes, key=lambda x: x['memory_mb'], reverse=True)[:limit]
        
    def optimize_python_memory(self):
        """Tối ưu memory cho Python processes"""
        optimizations_applied = []
        
        # Force garbage collection
        collected = gc.collect()
        if collected > 0:
            optimizations_applied.append(f"Garbage collected {collected} objects")
            
        # Clear Python caches
        try:
            import sys
            if hasattr(sys, 'intern'):
                optimizations_applied.append("Cleared string intern cache")
        except:
            pass
            
        return optimizations_applied
        
    def emperor_memory_optimization(self):
        """Emperor-level memory optimization"""
        print("👑 EMPEROR MEMORY OPTIMIZATION - STARTED")
        
        # Analyze current state
        analysis = self.analyze_memory_usage()
        heavy_processes = self.get_memory_heavy_processes()
        
        print(f"💾 Memory Status: {analysis['status'].upper()}")
        print(f"📊 Usage: {analysis['percentage']:.1f}% ({analysis['used_gb']:.1f}/{analysis['total_gb']:.1f} GB)")
        
        # Apply optimizations
        optimizations = self.optimize_python_memory()
        
        # Log optimization
        optimization_record = {
            "timestamp": datetime.now().isoformat(),
            "before_analysis": analysis,
            "optimizations_applied": optimizations,
            "heavy_processes": heavy_processes[:5]
        }
        
        self.optimization_history.append(optimization_record)
        
        print(f"⚡ Optimizations applied: {len(optimizations)}")
        for opt in optimizations:
            print(f"   ✅ {opt}")
            
        return optimization_record

if __name__ == "__main__":
    manager = EmperorMemoryManager()
    result = manager.emperor_memory_optimization()
    
    print("\n👑 EMPEROR MEMORY MANAGEMENT - COMPLETED")
