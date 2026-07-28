#!/usr/bin/env python3
# NOTE: This is a sanitized version for public release
# Core proprietary algorithms have been replaced with placeholders
"""
HYPERAI PHOENIX - ALERT SYSTEM
==============================
Real-time alert monitoring and notification system
"""

import json
import logging
import queue
import threading
import time
from datetime import datetime
from pathlib import Path

import psutil

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("hyperai_alerts.log"),
        logging.StreamHandler(),
    ],
)


class AlertSystem:
    def __init__(self):
        self.alerts_log_path = Path("hyperai_alerts.log")
        self.alert_config_path = Path("hyperai_alert_config.json")
        self.alert_queue = queue.Queue()
        self.active_alerts = {}
        self.alert_history = []
        self.monitoring_active = False
        self.monitor_thread = None

        # Default alert thresholds
        self.thresholds = {
            "cpu_usage": 80.0,
            "memory_usage": 85.0,
            "disk_usage": 90.0,
            "response_time": 100.0,  # milliseconds
            "error_rate": 5.0,  # percentage
        }

        self.load_config()
        self.initialize_alert_system()

    def load_config(self):
        """Load alert configuration from file"""
        if self.alert_config_path.exists():
            try:
                with open(self.alert_config_path, "r") as f:
                    config = json.load(f)
                    self.thresholds.update(config.get("thresholds", {}))
                    logging.info("Alert configuration loaded successfully")
            except Exception as e:
                logging.error(f"Error loading alert configuration: {e}")

    def save_config(self):
        """Save alert configuration to file"""
        try:
            config = {
                "thresholds": self.thresholds,
                "last_updated": datetime.now().isoformat(),
            }
            with open(self.alert_config_path, "w") as f:
                json.dump(config, f, indent=2)
            logging.info("Alert configuration saved successfully")
        except Exception as e:
            logging.error(f"Error saving alert configuration: {e}")

    def initialize_alert_system(self):
        """Initialize the alert system components"""
        # Create alert log file if it doesn't exist
        if not self.alerts_log_path.exists():
            try:
                with open(self.alerts_log_path, "w") as f:
                    f.write(f"HyperAI Phoenix Alert System Initialized - {datetime.now().isoformat()}\n")
                logging.info("Alert log file created")
            except Exception as e:
                logging.error(f"Error creating alert log file: {e}")

        # Load existing alert history
        self.load_alert_history()

    def load_alert_history(self):
        """Load alert history from log file"""
        if self.alerts_log_path.exists():
            try:
                with open(self.alerts_log_path, "r") as f:
                    lines = f.readlines()
                    for line in lines[-100:]:  # Load last 100 alerts
                        if "ALERT:" in line:
                            self.alert_history.append(line.strip())
                logging.info(f"Loaded {len(self.alert_history)} alerts from history")
            except Exception as e:
                logging.error(f"Error loading alert history: {e}")

    def start_monitoring(self):
        """Start the alert monitoring system"""
        if self.monitoring_active:
            logging.warning("Alert monitoring is already active")
            return

        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitor_thread.start()
        logging.info("Alert monitoring system started")

    def stop_monitoring(self):
        """Stop the alert monitoring system"""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        logging.info("Alert monitoring system stopped")

    def _monitoring_loop(self):
        """Main monitoring loop that checks system health continuously"""
        check_interval = 30  # seconds

        while self.monitoring_active:
            try:
                self.perform_health_checks()
                time.sleep(check_interval)
            except Exception as e:
                logging.error(f"Error in monitoring loop: {e}")
                time.sleep(check_interval)

    def perform_health_checks(self):
        """Perform comprehensive system health checks"""
        alerts_generated = []

        # CPU usage check
        try:
            cpu_usage = psutil.cpu_percent(interval=1)
            if cpu_usage > self.thresholds["cpu_usage"]:
                alert = self.generate_alert(
                    "HIGH_CPU_USAGE",
                    f"CPU usage is {cpu_usage:.1f}%, exceeding threshold of {self.thresholds['cpu_usage']}%",
                    "WARNING",
                    {"cpu_usage": cpu_usage, "threshold": self.thresholds["cpu_usage"]},
                )
                alerts_generated.append(alert)
        except Exception as e:
            logging.error(f"Error checking CPU usage: {e}")

        # Memory usage check
        try:
            memory = psutil.virtual_memory()
            memory_usage = memory.percent
            if memory_usage > self.thresholds["memory_usage"]:
                alert = self.generate_alert(
                    "HIGH_MEMORY_USAGE",
                    f"Memory usage is {memory_usage:.1f}%, exceeding threshold of {self.thresholds['memory_usage']}%",
                    "WARNING",
                    {
                        "memory_usage": memory_usage,
                        "threshold": self.thresholds["memory_usage"],
                    },
                )
                alerts_generated.append(alert)
        except Exception as e:
            logging.error(f"Error checking memory usage: {e}")

        # Disk usage check
        try:
            disk = psutil.disk_usage("/")
            disk_usage = disk.percent
            if disk_usage > self.thresholds["disk_usage"]:
                alert = self.generate_alert(
                    "HIGH_DISK_USAGE",
                    f"Disk usage is {disk_usage:.1f}%, exceeding threshold of {self.thresholds['disk_usage']}%",
                    "CRITICAL",
                    {
                        "disk_usage": disk_usage,
                        "threshold": self.thresholds["disk_usage"],
                    },
                )
                alerts_generated.append(alert)
        except Exception as e:
            logging.error(f"Error checking disk usage: {e}")

        # Process health check
        try:
            critical_processes = ["python", "hyperai"]
            running_processes = []
            for proc in psutil.process_iter(["pid", "name"]):
                try:
                    if any(cp.lower() in proc.info["name"].lower() for cp in critical_processes):
                        running_processes.append(proc.info["name"])
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            if len(running_processes) == 0:
                alert = self.generate_alert(
                    "CRITICAL_PROCESSES_DOWN",
                    "No critical HyperAI processes are running",
                    "CRITICAL",
                    {"expected_processes": critical_processes},
                )
                alerts_generated.append(alert)
        except Exception as e:
            logging.error(f"Error checking process health: {e}")

        # File system integrity check
        try:
            critical_files = [
                "README.md",
                "core_system/",
                "hyperai_agents/",
                "hyperai_automated_testing.py",
            ]

            missing_files = []
            for file_path in critical_files:
                if not Path(file_path).exists():
                    missing_files.append(file_path)

            if missing_files:
                alert = self.generate_alert(
                    "MISSING_CRITICAL_FILES",
                    f"Critical files are missing: {', '.join(missing_files)}",
                    "CRITICAL",
                    {"missing_files": missing_files},
                )
                alerts_generated.append(alert)
        except Exception as e:
            logging.error(f"Error checking file system integrity: {e}")

        return alerts_generated

    def generate_alert(self, alert_type, message, severity="INFO", details=None):
        """Generate a new alert"""
        alert = {
            "id": f"{alert_type}_{int(time.time())}",
            "type": alert_type,
            "message": message,
            "severity": severity,
            "timestamp": datetime.now().isoformat(),
            "details": details or {},
            "status": "ACTIVE",
        }

        # Add to active alerts
        self.active_alerts[alert["id"]] = alert

        # Log the alert
        self.log_alert(alert)

        # Add to history
        self.alert_history.append(f"ALERT: {alert_type} - {message}")

        # Keep only last 1000 alerts in history
        if len(self.alert_history) > 1000:
            self.alert_history = self.alert_history[-1000:]

        logging.warning(f"Alert generated: {alert_type} - {message}")

        return alert

    def log_alert(self, alert):
        """Log alert to file"""
        try:
            with open(self.alerts_log_path, "a") as f:
                f.write(f"{alert['timestamp']} - {alert['severity']} - {alert['type']}: {alert['message']}\n")
                if alert["details"]:
                    f.write(f"  Details: {json.dumps(alert['details'], indent=2)}\n")
                f.write("\n")
        except Exception as e:
            logging.error(f"Error logging alert: {e}")

    def resolve_alert(self, alert_id, resolution_note=""):
        """Resolve an active alert"""
        if alert_id in self.active_alerts:
            alert = self.active_alerts[alert_id]
            alert["status"] = "RESOLVED"
            alert["resolution_time"] = datetime.now().isoformat()
            alert["resolution_note"] = resolution_note

            # Log resolution
            try:
                with open(self.alerts_log_path, "a") as f:
                    f.write(f"{alert['resolution_time']} - RESOLVED - {alert['type']}: {resolution_note}\n\n")
            except Exception as e:
                logging.error(f"Error logging alert resolution: {e}")

            logging.info(f"Alert resolved: {alert_id}")
            return True

        return False

    def get_active_alerts(self):
        """Get all active alerts"""
        return list(self.active_alerts.values())

    def get_alert_history(self, limit=50):
        """Get alert history"""
        return self.alert_history[-limit:]

    def update_threshold(self, metric, value):
        """Update alert threshold for a metric"""
        if metric in self.thresholds:
            old_value = self.thresholds[metric]
            self.thresholds[metric] = value
            self.save_config()
            logging.info(f"Updated {metric} threshold from {old_value} to {value}")
            return True
        return False

    def get_system_status(self):
        """Get overall system status based on active alerts"""
        active_alerts = self.get_active_alerts()

        critical_alerts = [a for a in active_alerts if a["severity"] == "CRITICAL"]
        warning_alerts = [a for a in active_alerts if a["severity"] == "WARNING"]

        if critical_alerts:
            return "CRITICAL"
        elif warning_alerts:
            return "WARNING"
        else:
            return "HEALTHY"


def main():
    """Main function for testing the alert system"""
    import sys

    alert_system = AlertSystem()

    if len(sys.argv) > 1:
        if sys.argv[1] == "start":
            alert_system.start_monitoring()
            print("Alert monitoring started. Press Ctrl+C to stop.")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                alert_system.stop_monitoring()
                print("\nAlert monitoring stopped.")

        elif sys.argv[1] == "status":
            status = alert_system.get_system_status()
            active_alerts = alert_system.get_active_alerts()
            print(f"System Status: {status}")
            print(f"Active Alerts: {len(active_alerts)}")
            for alert in active_alerts[-5:]:  # Show last 5 alerts
                print(f"  - {alert['type']}: {alert['message']}")

        elif sys.argv[1] == "history":
            history = alert_system.get_alert_history(10)
            print("Recent Alert History:")
            for alert in history:
                print(f"  {alert}")

        elif sys.argv[1] == "test":
            # Generate a test alert
            alert = alert_system.generate_alert(
                "TEST_ALERT",
                "This is a test alert to verify the alert system is working",
                "INFO",
            )
            print(f"Test alert generated: {alert['id']}")

    else:
        print("HYPERAI PHOENIX - ALERT SYSTEM")
        print("=" * 40)
        print("Usage:")
        print("  python alert_system.py start    # Start monitoring")
        print("  python alert_system.py status   # Show system status")
        print("  python alert_system.py history  # Show alert history")
        print("  python alert_system.py test     # Generate test alert")


if __name__ == "__main__":
    main()
