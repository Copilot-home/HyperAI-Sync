
import psutil
import time
import threading
from collections import deque
import statistics

class EmperorCPUOptimizer:
    def __init__(self):
        self.cpu_history = deque(maxlen=60)  # 1 minute of history
        self.optimization_active = False
        self.cpu_threshold = 80  # 80% CPU threshold
        
    def monitor_cpu_realtime(self, duration=60):
        """Monitor CPU in real-time"""
        print("🔧 CPU Real-time monitoring started...")
        
        for i in range(duration):
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_per_core = psutil.cpu_percent(interval=None, percpu=True)
            
            self.cpu_history.append({
                'timestamp': time.time(),
                'overall': cpu_percent,
                'per_core': cpu_per_core,
                'load_avg': psutil.getloadavg() if hasattr(psutil, 'getloadavg') else [0,0,0]
            })
            
            if cpu_percent > self.cpu_threshold:
                print(f"⚠️ High CPU usage detected: {cpu_percent:.1f}%")
                self.apply_cpu_optimization()
                
            if i % 10 == 0:  # Report every 10 seconds
                avg_cpu = statistics.mean([h['overall'] for h in list(self.cpu_history)[-10:]])
                print(f"📊 Average CPU (last 10s): {avg_cpu:.1f}%")
                
        return list(self.cpu_history)
        
    def analyze_cpu_patterns(self):
        """Analyze CPU usage patterns"""
        if len(self.cpu_history) < 10:
            return {"status": "insufficient_data"}
            
        recent_usage = [h['overall'] for h in list(self.cpu_history)[-30:]]
        
        analysis = {
            "average": statistics.mean(recent_usage),
            "peak": max(recent_usage),
            "minimum": min(recent_usage),
            "variance": statistics.variance(recent_usage) if len(recent_usage) > 1 else 0,
            "trend": "stable"
        }
        
        # Determine trend
        if len(recent_usage) >= 20:
            first_half = statistics.mean(recent_usage[:10])
            second_half = statistics.mean(recent_usage[-10:])
            
            if second_half > first_half + 5:
                analysis["trend"] = "increasing"
            elif second_half < first_half - 5:
                analysis["trend"] = "decreasing"
                
        return analysis
        
    def get_cpu_intensive_processes(self):
        """Find CPU-intensive processes"""
        processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
            try:
                proc_info = proc.info
                if proc_info['cpu_percent'] > 1.0:  # > 1% CPU
                    processes.append({
                        'pid': proc_info['pid'],
                        'name': proc_info['name'],
                        'cpu_percent': proc_info['cpu_percent'],
                        'memory_mb': proc_info['memory_info'].rss / (1024**2)
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
                
        return sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:10]
        
    def apply_cpu_optimization(self):
        """Apply intelligent CPU optimization"""
        if self.optimization_active:
            return "Optimization already active"
            
        self.optimization_active = True
        optimizations = []
        
        try:
            # Get CPU-intensive processes
            intensive_processes = self.get_cpu_intensive_processes()
            
            # Apply process priority optimization
            for proc_info in intensive_processes[:3]:  # Top 3 CPU users
                try:
                    proc = psutil.Process(proc_info['pid'])
                    current_priority = proc.nice()
                    
                    # Lower priority for non-critical processes
                    if 'python' in proc_info['name'].lower() and current_priority == 0:
                        proc.nice(1)  # Lower priority
                        optimizations.append(f"Lowered priority for PID {proc_info['pid']}")
                        
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
            print(f"⚡ Applied {len(optimizations)} CPU optimizations")
            
        finally:
            self.optimization_active = False
            
        return optimizations
        
    def emperor_cpu_optimization(self):
        """Emperor-level CPU optimization"""
        print("👑 EMPEROR CPU OPTIMIZATION - STARTED")
        
        # Analyze current patterns
        analysis = self.analyze_cpu_patterns()
        intensive_processes = self.get_cpu_intensive_processes()
        
        print(f"📊 CPU Analysis:")
        print(f"   Average: {analysis.get('average', 0):.1f}%")
        print(f"   Peak: {analysis.get('peak', 0):.1f}%")
        print(f"   Trend: {analysis.get('trend', 'unknown')}")
        
        print(f"🔧 Top CPU processes:")
        for proc in intensive_processes[:5]:
            print(f"   {proc['name']} (PID {proc['pid']}): {proc['cpu_percent']:.1f}%")
            
        # Apply optimizations
        optimizations = self.apply_cpu_optimization()
        
        print(f"⚡ Optimizations applied: {len(optimizations)}")
        
        return {
            "analysis": analysis,
            "processes": intensive_processes,
            "optimizations": optimizations
        }

if __name__ == "__main__":
    optimizer = EmperorCPUOptimizer()
    result = optimizer.emperor_cpu_optimization()
    
    print("\n👑 EMPEROR CPU OPTIMIZATION - COMPLETED")
