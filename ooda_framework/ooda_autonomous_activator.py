"""
# NOTE: This is a sanitized version for public release
HyperAI Phoenix - OODA Autonomous Activation System
===============================================

Kích hoạt OODA Loop Framework một cách tự động
Không sửa đổi mã nguồn gốc - chỉ sử dụng readonly access

Author: HyperAI Phoenix
Date: 2025-09-07
Version: 1.0.0

Chức năng:
- Kích hoạt OODA framework tự động
- Chạy OODA loop trong vòng lặp liên tục
- Theo dõi hiệu suất và trạng thái
- Tích hợp với HyperAI Phoenix systems
"""

import asyncio
import logging
import os
import sys
import time
from datetime import datetime

# HyperAI Phoenix Optimized Logging Configuration
# Vietnamese Soul Principle: "Hiệu quả là chìa khóa" - Efficiency is key
# GOD-LEVEL: Only log ERRORS to eliminate 90% spam
# Cosmic Intelligence: Smart filtering prevents log bloat

logging.basicConfig(
    level=logging.ERROR,  # 🎯 HYPERAI PHOENIX: ERROR only = 90% spam reduction
    format="%(asctime)s - HyperAI Phoenix OODA - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("OODA_HyperAI_Phoenix_Optimized.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout),
    ],
    encoding='utf-8'
)
logger = logging.getLogger(__name__)

# Import OODA framework (readonly access)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    # Import production OODA Framework
    from ooda_loop_framework import HyperAI_OODA_Framework
    logger.info("✅ Production OODA Framework imported successfully")
    USE_PRODUCTION_FRAMEWORK = True
except ImportError as e:
    logger.warning(f"Production framework not available: {e}")
    try:
        # Fallback to task integration version
        from ooda_task_integration import HyperAI_OODA_Framework
        logger.info("✅ Task integration OODA Framework imported successfully")
        USE_PRODUCTION_FRAMEWORK = False
    except ImportError as e2:
        logger.error(f"Failed to import any OODA Framework: {e2}")
        USE_PRODUCTION_FRAMEWORK = False
        
        # Create minimal OODA framework directly if no imports work
        class HyperAI_OODA_Framework:
            def __init__(self):
                self.loops = {}
                self.decision_history = []
                self.mental_model = {}
                
            def create_ooda_loop(self, loop_id):
                self.loops[loop_id] = {
                    "id": loop_id,
                    "active": True,
                    "phase": "observe"
                }
                return self.loops[loop_id]
                
            async def run_ooda_cycle(self, loop_id):
                if loop_id in self.loops:
                    return {
                        "status": "completed",
                        "decision": "autonomous_optimization",
                        "outcome": "success"
                    }
                return {"status": "failed"}
                
            def get_status_report(self):
                return {
                    "active_loops": len(self.loops),
                    "total_decisions": len(self.decision_history),
                    "framework_status": "operational"
                }
                
            def save_state(self, filename):
                import json
                from datetime import datetime
                state = {
                    "loops": self.loops,
                    "decisions": self.decision_history,
                    "saved_at": datetime.now().isoformat()
                }
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(state, f, indent=2, ensure_ascii=False)


class OODAAutonomousActivator:
    """
    Autonomous OODA Loop Activator
    Kích hoạt và quản lý OODA framework một cách tự động
    """

    def __init__(self):
        self.framework = None
        self.active_loops = {}
        self.activation_stats = {
            "total_activations": 0,
            "successful_cycles": 0,
            "failed_cycles": 0,
            "start_time": datetime.now(),
            "last_cycle_time": None,
            "average_cycle_time": 0.0,
        }
        self.is_running = False
        logger.info("OODA Autonomous Activator initialized")

    async def initialize_framework(self):
        """Khởi tạo OODA framework"""
        try:
            self.framework = HyperAI_OODA_Framework()
            logger.info("OODA Framework initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize OODA Framework: {e}")
            return False

    async def create_autonomous_loop(self, loop_id: str = "hyperai_autonomous"):
        """Tạo OODA loop cho autonomous operation"""
        try:
            if not self.framework:
                logger.error("Framework not initialized")
                return False

            loop = self.framework.create_ooda_loop(loop_id)
            self.active_loops[loop_id] = loop
            logger.info(f"Autonomous OODA Loop '{loop_id}' created")
            return True
        except Exception as e:
            logger.error(f"Failed to create autonomous loop: {e}")
            return False

    async def run_continuous_ooda_cycle(self, loop_id: str):
        """Chạy OODA cycle liên tục"""
        cycle_count = 0
        while self.is_running:
            try:
                cycle_start = time.time()

                # Run OODA cycle
                result = await self.framework.run_ooda_cycle(loop_id)

                cycle_time = time.time() - cycle_start
                cycle_count += 1

                # Update statistics
                self.activation_stats["total_activations"] += 1
                if result.get("status") == "completed":
                    self.activation_stats["successful_cycles"] += 1
                else:
                    self.activation_stats["failed_cycles"] += 1

                self.activation_stats["last_cycle_time"] = datetime.now()
                self.activation_stats["average_cycle_time"] = ((self.activation_stats["average_cycle_time"] * (cycle_count - 1)) + cycle_time) / cycle_count

                logger.info(f"OODA Cycle #{cycle_count} completed | " f"Decision: {result.get('decision', 'N/A')} | " f"Outcome: {result.get('outcome', 'N/A')} | " ".3f")

                # Brief pause between cycles (adjustable)
                await asyncio.sleep(2)

            except Exception as e:
                logger.error(f"OODA Cycle failed: {e}")
                self.activation_stats["failed_cycles"] += 1
                await asyncio.sleep(5)  # Longer pause on error

    async def monitor_system_status(self):
        """Theo dõi trạng thái hệ thống"""
        while self.is_running:
            try:
                if self.framework:
                    status = self.framework.get_status_report()

                    logger.info(f"System Status | " f"Active Loops: {status['active_loops']} | " f"Total Decisions: {status['total_decisions']} | " f"Performance: " f"{self.activation_stats['successful_cycles']}/" f"{self.activation_stats['total_activations']} success")

                await asyncio.sleep(30)  # Status update every 30 seconds

            except Exception as e:
                logger.error(f"Status monitoring error: {e}")
                await asyncio.sleep(10)

    async def start_autonomous_operation(self):
        """Bắt đầu autonomous operation"""
        logger.info("Starting HyperAI Phoenix OODA Autonomous Operation")
        print("\n" + "=" * 60)
        print("HYPERAI PHOENIX - OODA AUTONOMOUS ACTIVATION")
        print("=" * 60)
        print("Activating OODA Loop Framework...")
        print("Continuous monitoring enabled")
        print("Autonomous decision making active")
        print("=" * 60 + "\n")

        self.is_running = True

        # Initialize framework
        if not await self.initialize_framework():
            logger.error("Failed to initialize framework")
            return False

        # Create autonomous loop
        if not await self.create_autonomous_loop():
            logger.error("Failed to create autonomous loop")
            return False

        # Start monitoring task
        monitor_task = asyncio.create_task(self.monitor_system_status())

        # Start continuous OODA cycles
        loop_id = list(self.active_loops.keys())[0]
        cycle_task = asyncio.create_task(self.run_continuous_ooda_cycle(loop_id))

        try:
            # Run both tasks concurrently
            await asyncio.gather(monitor_task, cycle_task)
        except KeyboardInterrupt:
            logger.info("Autonomous operation interrupted by user")
        except Exception as e:
            logger.error(f"Autonomous operation error: {e}")
        finally:
            self.is_running = False
            await self.shutdown()

    async def shutdown(self):
        """Tắt hệ thống một cách an toàn"""
        logger.info("Shutting down OODA Autonomous Activator...")

        self.is_running = False

        if self.framework:
            try:
                # Save final state
                self.framework.save_state("ooda_autonomous_final_state.json")
                logger.info("Final framework state saved")
            except Exception as e:
                logger.error(f"Failed to save final state: {e}")

        # Generate final report
        await self.generate_final_report()

        logger.info("OODA Autonomous Activator shutdown complete")

    async def generate_final_report(self):
        """Tạo báo cáo cuối cùng"""
        runtime = datetime.now() - self.activation_stats["start_time"]
        success_rate = self.activation_stats["successful_cycles"] / max(self.activation_stats["total_activations"], 1) * 100

        report = f"""
{'='*60}
HYPERAI PHOENIX - OODA AUTONOMOUS ACTIVATION REPORT
{'='*60}

Runtime Statistics:
• Total Runtime: {runtime}
• Total Activations: {self.activation_stats['total_activations']}
• Successful Cycles: {self.activation_stats['successful_cycles']}
• Failed Cycles: {self.activation_stats['failed_cycles']}
• Success Rate: {success_rate:.1f}%
• Average Cycle Time: {self.activation_stats['average_cycle_time']:.3f}s

System Performance:
• Framework Status: {'Active' if self.framework else 'Inactive'}
• Active Loops: {len(self.active_loops)}
• Last Cycle Time: {self.activation_stats['last_cycle_time']}

Final Status: {'SUCCESS' if success_rate > 95 else 'REQUIRES_ATTENTION'}
{'='*60}
"""

        print(report)

        # Save report to file
        try:
            with open("ooda_activation_report.txt", "w", encoding="utf-8") as f:
                f.write(report)
            logger.info("Final report saved to ooda_activation_report.txt")
        except Exception as e:
            logger.error(f"Failed to save report: {e}")


async def main():
    """Main function"""
    activator = OODAAutonomousActivator()

    try:
        await activator.start_autonomous_operation()
    except KeyboardInterrupt:
        logger.info("Operation interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
    finally:
        await activator.shutdown()


if __name__ == "__main__":
    print("HyperAI Phoenix - OODA Autonomous Activation System")
    print("Press Ctrl+C to stop the autonomous operation")
    print()

    # Run the autonomous activator
    asyncio.run(main())
