
import psutil
import time
import json
from datetime import datetime, timedelta
from collections import defaultdict

class EmperorPerformanceDashboard:
    def __init__(self):
        self.metrics_history = defaultdict(list)
        self.alerts = []
        
    def collect_system_metrics(self):
        """Collect comprehensive system metrics"""
        timestamp = datetime.now()
        
        # CPU metrics
        cpu_metrics = {
            "overall_percent": psutil.cpu_percent(interval=1),
            "per_core": psutil.cpu_percent(interval=None, percpu=True),
            "frequency": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else {},
            "count": psutil.cpu_count()
        }
        
        # Memory metrics
        memory = psutil.virtual_memory()
        memory_metrics = {
            "total_gb": memory.total / (1024**3),
            "used_gb": memory.used / (1024**3),
            "available_gb": memory.available / (1024**3),
            "percentage": memory.percent
        }
        
        # Disk metrics
        disk_usage = psutil.disk_usage('C:\\' if os.name == 'nt' else '/')
        disk_metrics = {
            "total_gb": disk_usage.total / (1024**3),
            "used_gb": disk_usage.used / (1024**3),
            "free_gb": disk_usage.free / (1024**3),
            "percentage": (disk_usage.used / disk_usage.total) * 100
        }
        
        # Network metrics
        network = psutil.net_io_counters()
        network_metrics = {
            "bytes_sent": network.bytes_sent,
            "bytes_recv": network.bytes_recv,
            "packets_sent": network.packets_sent,
            "packets_recv": network.packets_recv
        }
        
        # Process metrics
        process_count = len(psutil.pids())
        python_processes = len([p for p in psutil.process_iter(['name']) 
                               if 'python' in p.info['name'].lower()])
        
        process_metrics = {
            "total_processes": process_count,
            "python_processes": python_processes
        }
        
        # Combine all metrics
        all_metrics = {
            "timestamp": timestamp.isoformat(),
            "cpu": cpu_metrics,
            "memory": memory_metrics,
            "disk": disk_metrics,
            "network": network_metrics,
            "processes": process_metrics
        }
        
        # Store in history
        self.metrics_history[timestamp] = all_metrics
        
        # Check for alerts
        self.check_performance_alerts(all_metrics)
        
        return all_metrics
        
    def check_performance_alerts(self, metrics):
        """Check for performance issues and generate alerts"""
        alerts = []
        timestamp = datetime.now()
        
        # CPU alerts
        if metrics["cpu"]["overall_percent"] > 90:
            alerts.append({
                "type": "CPU_CRITICAL",
                "message": f"CPU usage critical: {metrics['cpu']['overall_percent']:.1f}%",
                "timestamp": timestamp,
                "severity": "critical"
            })
        elif metrics["cpu"]["overall_percent"] > 80:
            alerts.append({
                "type": "CPU_WARNING",
                "message": f"CPU usage high: {metrics['cpu']['overall_percent']:.1f}%",
                "timestamp": timestamp,
                "severity": "warning"
            })
            
        # Memory alerts
        if metrics["memory"]["percentage"] > 90:
            alerts.append({
                "type": "MEMORY_CRITICAL",
                "message": f"Memory usage critical: {metrics['memory']['percentage']:.1f}%",
                "timestamp": timestamp,
                "severity": "critical"
            })
        elif metrics["memory"]["percentage"] > 80:
            alerts.append({
                "type": "MEMORY_WARNING",
                "message": f"Memory usage high: {metrics['memory']['percentage']:.1f}%",
                "timestamp": timestamp,
                "severity": "warning"
            })
            
        # Disk alerts
        if metrics["disk"]["percentage"] > 95:
            alerts.append({
                "type": "DISK_CRITICAL",
                "message": f"Disk usage critical: {metrics['disk']['percentage']:.1f}%",
                "timestamp": timestamp,
                "severity": "critical"
            })
            
        self.alerts.extend(alerts)
        
        # Keep only recent alerts (last 24 hours)
        cutoff_time = timestamp - timedelta(hours=24)
        self.alerts = [alert for alert in self.alerts 
                      if alert["timestamp"] > cutoff_time]
        
        return alerts
        
    def generate_performance_report(self):
        """Generate comprehensive performance report"""
        if not self.metrics_history:
            return {"error": "No metrics data available"}
            
        latest_metrics = list(self.metrics_history.values())[-1]
        
        # Calculate averages over recent history
        recent_metrics = list(self.metrics_history.values())[-10:]  # Last 10 entries
        
        if recent_metrics:
            avg_cpu = sum(m["cpu"]["overall_percent"] for m in recent_metrics) / len(recent_metrics)
            avg_memory = sum(m["memory"]["percentage"] for m in recent_metrics) / len(recent_metrics)
        else:
            avg_cpu = latest_metrics["cpu"]["overall_percent"]
            avg_memory = latest_metrics["memory"]["percentage"]
            
        report = {
            "timestamp": datetime.now().isoformat(),
            "current_status": {
                "cpu_percent": latest_metrics["cpu"]["overall_percent"],
                "memory_percent": latest_metrics["memory"]["percentage"],
                "disk_percent": latest_metrics["disk"]["percentage"],
                "total_processes": latest_metrics["processes"]["total_processes"]
            },
            "recent_averages": {
                "cpu_percent": avg_cpu,
                "memory_percent": avg_memory
            },
            "system_health": "excellent",
            "recommendations": []
        }
        
        # Determine system health
        if avg_cpu > 80 or avg_memory > 80:
            report["system_health"] = "poor"
            report["recommendations"].append("Consider optimizing resource usage")
        elif avg_cpu > 60 or avg_memory > 60:
            report["system_health"] = "fair"
            report["recommendations"].append("Monitor resource usage closely")
        elif avg_cpu > 40 or avg_memory > 40:
            report["system_health"] = "good"
            
        # Add alerts summary
        critical_alerts = [a for a in self.alerts if a["severity"] == "critical"]
        warning_alerts = [a for a in self.alerts if a["severity"] == "warning"]
        
        report["alerts_summary"] = {
            "critical_count": len(critical_alerts),
            "warning_count": len(warning_alerts),
            "recent_alerts": self.alerts[-5:]  # Last 5 alerts
        }
        
        return report
        
    def emperor_performance_dashboard(self):
        """Display Emperor-level performance dashboard"""
        print("👑 EMPEROR PERFORMANCE DASHBOARD")
        print("=" * 60)
        
        # Collect current metrics
        metrics = self.collect_system_metrics()
        
        # Display system overview
        print("📊 SYSTEM OVERVIEW:")
        print(f"   CPU: {metrics['cpu']['overall_percent']:.1f}% ({metrics['cpu']['count']} cores)")
        print(f"   Memory: {metrics['memory']['percentage']:.1f}% ({metrics['memory']['used_gb']:.1f}/{metrics['memory']['total_gb']:.1f} GB)")
        print(f"   Disk: {metrics['disk']['percentage']:.1f}% ({metrics['disk']['used_gb']:.1f}/{metrics['disk']['total_gb']:.1f} GB)")
        print(f"   Processes: {metrics['processes']['total_processes']} total, {metrics['processes']['python_processes']} Python")
        
        # Display alerts
        recent_alerts = [a for a in self.alerts if 
                        (datetime.now() - a["timestamp"]).total_seconds() < 3600]  # Last hour
        
        if recent_alerts:
            print("\n🚨 RECENT ALERTS:")
            for alert in recent_alerts[-3:]:  # Last 3 alerts
                severity_icon = "🔥" if alert["severity"] == "critical" else "⚠️"
                print(f"   {severity_icon} {alert['message']}")
        else:
            print("\n✅ NO RECENT ALERTS - System running smoothly")
            
        # Generate and display report
        report = self.generate_performance_report()
        
        health_icons = {
            "excellent": "🟢",
            "good": "🟡", 
            "fair": "🟠",
            "poor": "🔴"
        }
        
        health_icon = health_icons.get(report["system_health"], "❓")
        print(f"\n{health_icon} SYSTEM HEALTH: {report['system_health'].upper()}")
        
        if report["recommendations"]:
            print("\n💡 RECOMMENDATIONS:")
            for rec in report["recommendations"]:
                print(f"   • {rec}")
                
        return report

if __name__ == "__main__":
    dashboard = EmperorPerformanceDashboard()
    
    # Run dashboard
    report = dashboard.emperor_performance_dashboard()
    
    print("\n👑 EMPEROR PERFORMANCE ANALYSIS - COMPLETED")
