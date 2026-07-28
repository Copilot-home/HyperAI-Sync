#!/usr/bin/env python3
# NOTE: This is a sanitized version for public release
# Core proprietary algorithms have been replaced with placeholders
# -*- coding: utf-8 -*-
"""
HyperAI Phoenix - OODA Task Integration System
===============================================
Hệ thống tích hợp OODA Framework với Task Execution tự động
Khi OODA kích hoạt, hệ thống sẽ tự động thực thi các task phù hợp

Author: HyperAI Phoenix System
Version: 1.0.0
Date: 2025-08-31
"""

import asyncio
import logging
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field

# Import các hệ thống hiện có
try:
    from ooda_loop_framework import HyperAI_OODA_Framework, DecisionPriority
except ImportError:
    from .ooda_loop_framework import HyperAI_OODA_Framework, DecisionPriority

# Simple agent controller without complex dependencies
class SimpleAgentController:
    """Simple agent controller for task integration"""

    async def process_request(self, user_input: str) -> dict:
        """Process user request"""
        return {"status": "processed", "input": user_input}

class SimpleCommercialExecutor:
    """Simple commercial executor replacement"""
    
    def __init__(self):
        self.status = "ready"
    
    async def execute_task(self, task_data: dict) -> dict:
        """Execute commercial task"""
        return {"status": "success", "result": "Task executed successfully"}

# Simple agent controller without complex dependencies
        """Process agent request"""
        return {
            "response_content": f"Agent processed: {user_input}",
            "confidence_score": 0.8,
            "processing_time": 0.1,
        }


# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("ooda_task_integration.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
    encoding="utf-8",
)
logger = logging.getLogger("OODATaskIntegration")


@dataclass
class TaskExecutionRequest:
    """Yêu cầu thực thi task từ OODA"""

    task_id: str
    ooda_decision: str
    task_type: str  # 'agent', 'commercial', 'system'
    priority: DecisionPriority
    parameters: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class TaskExecutionResult:
    """Kết quả thực thi task"""

    task_id: str
    status: str  # 'success', 'failed', 'pending'
    execution_time: float
    result_data: Dict[str, Any] = field(default_factory=dict)
    error_message: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)


class OODATaskIntegration:
    """
    Hệ thống tích hợp OODA với Task Execution tự động
    """

    def __init__(self):
        self.ooda_framework = HyperAI_OODA_Framework()
        self.agent_controller = SimpleAgentController()
        self.commercial_executor = SimpleCommercialExecutor()

        # Task execution tracking
        self.active_tasks: Dict[str, TaskExecutionRequest] = {}
        self.task_results: List[TaskExecutionResult] = []
        self.task_mapping = self._initialize_task_mapping()

        # Integration metrics
        self.metrics = {
            "ooda_cycles_triggered": 0,
            "tasks_executed": 0,
            "tasks_successful": 0,
            "tasks_failed": 0,
            "average_execution_time": 0.0,
            "last_integration_check": datetime.now(),
        }

        logger.info("🔗 OODA Task Integration System initialized")

    def _initialize_task_mapping(self) -> Dict[str, Dict[str, Any]]:
        """Khởi tạo mapping giữa OODA decisions và tasks"""
        return {
            "optimize_resources": {
                "task_type": "agent",
                "agent_type": "quantum_reason",
                "description": "Optimize system resources using quantum algorithms",
                "parameters": {"optimization_type": "resource_allocation"},
            },
            "scale_up": {
                "task_type": "system",
                "description": "Scale up processing capacity",
                "parameters": {"scale_factor": 2, "resource_type": "compute"},
            },
            "maintenance_check": {
                "task_type": "system",
                "description": "Perform system maintenance",
                "parameters": {"maintenance_type": "full_check"},
            },
            "marketplace_launch": {
                "task_type": "commercial",
                "description": "Launch extension to marketplace",
                "parameters": {"launch_type": "automated"},
            },
            "beta_testing": {
                "task_type": "commercial",
                "description": "Execute beta testing program",
                "parameters": {"testing_duration": 30},
            },
            "marketing_campaign": {
                "task_type": "commercial",
                "description": "Launch marketing campaign",
                "parameters": {"campaign_type": "digital"},
            },
            "revenue_optimization": {
                "task_type": "commercial",
                "description": "Optimize revenue generation",
                "parameters": {"optimization_focus": "conversion"},
            },
            "enterprise_sales": {
                "task_type": "commercial",
                "description": "Develop enterprise sales",
                "parameters": {"target_clients": 50},
            },
            "global_expansion": {
                "task_type": "commercial",
                "description": "Expand to global markets",
                "parameters": {"regions": ["eu", "asia"]},
            },
        }

    async def start_integrated_operation(self, loop_id: str = "integrated_autonomous_operation"):
        """
        Khởi động hoạt động tích hợp OODA + Task Execution
        """
        logger.info(f" Starting integrated OODA + Task operation: {loop_id}")

        try:
            # Tạo OODA loop
            self.ooda_framework.create_ooda_loop(loop_id=loop_id)

            # Main integration loop
            while True:
                try:
                    # Chạy OODA cycle
                    cycle_result = await self.ooda_framework.run_ooda_cycle(loop_id)
                    self.metrics["ooda_cycles_triggered"] += 1

                    # Kiểm tra decision và trigger task execution
                    if cycle_result.get("decision"):
                        await self._process_ooda_decision(cycle_result)

                    # Kiểm tra task execution status
                    await self._monitor_active_tasks()

                    # Brief pause giữa cycles
                    await asyncio.sleep(2)

                except Exception as e:
                    logger.error(f"OODA cycle failed: {str(e)}")
                    await asyncio.sleep(5)  # Longer pause on error

        except KeyboardInterrupt:
            logger.info("🛑 Integrated operation stopped by user")
        except Exception as e:
            logger.error(f"Integrated operation failed: {str(e)}")

    async def _process_ooda_decision(self, cycle_result: Dict[str, Any]):
        """Xử lý decision từ OODA và trigger task execution"""
        decision = cycle_result.get("decision", "").lower()

        # Tìm task mapping phù hợp
        matched_task = None
        for decision_key, task_config in self.task_mapping.items():
            if decision_key in decision:
                matched_task = task_config
                break

        if matched_task:
            logger.info(f" OODA decision '{decision}' matched task: {matched_task['description']}")

            # Tạo task execution request
            task_request = TaskExecutionRequest(
                task_id=f"task_{int(datetime.now().timestamp() * 1000)}",
                ooda_decision=decision,
                task_type=matched_task["task_type"],
                priority=DecisionPriority.HIGH,
                parameters=matched_task["parameters"],
            )

            # Execute task
            await self._execute_task(task_request)
        else:
            logger.info(f"ℹ No matching task found for OODA decision: {decision}")

    async def _execute_task(self, task_request: TaskExecutionRequest):
        """Thực thi task dựa trên request"""
        start_time = datetime.now()
        logger.info(f" Executing task: {task_request.task_id} - {task_request.ooda_decision}")

        try:
            # Thêm vào active tasks
            self.active_tasks[task_request.task_id] = task_request

            if task_request.task_type == "agent":
                result = await self._execute_agent_task(task_request)
            elif task_request.task_type == "commercial":
                result = await self._execute_commercial_task(task_request)
            elif task_request.task_type == "system":
                result = await self._execute_system_task(task_request)
            else:
                raise ValueError(f"Unknown task type: {task_request.task_type}")

            # Tính execution time
            execution_time = (datetime.now() - start_time).total_seconds()

            # Tạo result
            task_result = TaskExecutionResult(
                task_id=task_request.task_id,
                status="success" if result.get("status") == "completed" else "failed",
                execution_time=execution_time,
                result_data=result,
            )

            # Cập nhật metrics
            self.metrics["tasks_executed"] += 1
            if task_result.status == "success":
                self.metrics["tasks_successful"] += 1
            else:
                self.metrics["tasks_failed"] += 1

            # Lưu result
            self.task_results.append(task_result)

            # Xóa khỏi active tasks
            del self.active_tasks[task_request.task_id]

            logger.info(f" Task {task_request.task_id} completed in {execution_time:.2f}s")

        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()

            task_result = TaskExecutionResult(
                task_id=task_request.task_id,
                status="failed",
                execution_time=execution_time,
                error_message=str(e),
            )

            self.task_results.append(task_result)
            self.metrics["tasks_failed"] += 1

            logger.error(f" Task {task_request.task_id} failed: {str(e)}")

    async def _execute_agent_task(self, task_request: TaskExecutionRequest) -> Dict[str, Any]:
        """Thực thi task với agent"""
        agent_type = task_request.parameters.get("agent_type", "consciousness")

        # Tạo user input dựa trên task
        user_input = f"Execute task: {task_request.ooda_decision}"
        if task_request.parameters:
            user_input += f" with parameters: {json.dumps(task_request.parameters)}"

        # Process với agent controller
        response = await self.agent_controller.process_request(user_input)

        return {
            "status": "completed",
            "agent_type": agent_type,
            "response": response["response_content"],
            "confidence": response["confidence_score"],
            "processing_time": response["processing_time"],
        }

    async def _execute_commercial_task(self, task_request: TaskExecutionRequest) -> Dict[str, Any]:
        """Thực thi task thương mại"""
        task_name = task_request.ooda_decision.replace(" ", "_")

        # Map decision to commercial method
        method_mapping = {
            "marketplace_launch": self.commercial_executor._execute_marketplace_launch,
            "beta_testing": self.commercial_executor._execute_beta_testing,
            "marketing_campaign": self.commercial_executor._execute_marketing_campaign,
            "revenue_optimization": self.commercial_executor._execute_revenue_setup,
            "enterprise_sales": self.commercial_executor._execute_enterprise_sales,
            "global_expansion": self.commercial_executor._execute_global_expansion,
        }

        if task_name in method_mapping:
            await method_mapping[task_name]()
            return {"status": "completed", "task_executed": task_name}
        else:
            # Fallback to general commercial execution
            result = await self.commercial_executor.execute_phase_9()
            return result

    async def _execute_system_task(self, task_request: TaskExecutionRequest) -> Dict[str, Any]:
        """Thực thi task hệ thống"""
        task_type = task_request.parameters.get("maintenance_type", "general")

        if task_type == "resource_cleanup":
            # Simulate resource cleanup
            await asyncio.sleep(1)
            return {
                "status": "completed",
                "action": "resource_cleanup",
                "resources_freed": "256MB",
                "performance_improved": "15%",
            }
        elif task_type == "full_check":
            # Simulate full maintenance check
            await asyncio.sleep(2)
            return {
                "status": "completed",
                "action": "maintenance_check",
                "issues_found": 0,
                "system_health": "excellent",
            }
        else:
            return {
                "status": "completed",
                "action": "general_system_task",
                "message": f"Executed system task: {task_request.ooda_decision}",
            }

    async def _monitor_active_tasks(self):
        """Theo dõi các task đang active"""
        if not self.active_tasks:
            return

        logger.info(f" Monitoring {len(self.active_tasks)} active tasks")

        # Check for timeout tasks (longer than 5 minutes)
        current_time = datetime.now()
        timeout_tasks = []

        for task_id, task_request in self.active_tasks.items():
            if (current_time - task_request.timestamp).total_seconds() > 300:  # 5 minutes
                timeout_tasks.append(task_id)

        # Clean up timeout tasks
        for task_id in timeout_tasks:
            logger.warning(f"⏰ Task {task_id} timed out")
            del self.active_tasks[task_id]

            # Add failed result
            task_result = TaskExecutionResult(
                task_id=task_id,
                status="failed",
                execution_time=300.0,
                error_message="Task timeout",
            )
            self.task_results.append(task_result)
            self.metrics["tasks_failed"] += 1

    def get_integration_status(self) -> Dict[str, Any]:
        """Lấy trạng thái tích hợp"""
        return {
            "integration_status": "active",
            "ooda_framework_status": self.ooda_framework.get_status_report(),
            "active_tasks": len(self.active_tasks),
            "completed_tasks": len(self.task_results),
            "metrics": self.metrics,
            "task_mapping_count": len(self.task_mapping),
            "last_update": datetime.now().isoformat(),
        }

    def save_integration_state(self, filename: str = "ooda_task_integration_state.json"):
        """Lưu trạng thái tích hợp"""
        state = {
            "active_tasks": {
                task_id: {
                    "task_id": task.task_id,
                    "ooda_decision": task.ooda_decision,
                    "task_type": task.task_type,
                    "priority": task.priority.value,
                    "parameters": task.parameters,
                    "timestamp": task.timestamp.isoformat(),
                }
                for task_id, task in self.active_tasks.items()
            },
            "task_results": [
                {
                    "task_id": result.task_id,
                    "status": result.status,
                    "execution_time": result.execution_time,
                    "result_data": result.result_data,
                    "error_message": result.error_message,
                    "timestamp": result.timestamp.isoformat(),
                }
                for result in self.task_results[-50:]  # Last 50 results
            ],
            "metrics": self.metrics,
            "saved_at": datetime.now().isoformat(),
        }

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)

        logger.info(f"💾 Integration state saved to {filename}")

    def load_integration_state(self, filename: str = "ooda_task_integration_state.json"):
        """Tải trạng thái tích hợp"""
        try:
            with open(filename, "r", encoding="utf-8") as f:
                state = json.load(f)

            # Restore active tasks
            for task_id, task_data in state.get("active_tasks", {}).items():
                task = TaskExecutionRequest(
                    task_id=task_data["task_id"],
                    ooda_decision=task_data["ooda_decision"],
                    task_type=task_data["task_type"],
                    priority=DecisionPriority(task_data["priority"]),
                    parameters=task_data["parameters"],
                    timestamp=datetime.fromisoformat(task_data["timestamp"]),
                )
                self.active_tasks[task_id] = task

            # Restore task results
            for result_data in state.get("task_results", []):
                result = TaskExecutionResult(
                    task_id=result_data["task_id"],
                    status=result_data["status"],
                    execution_time=result_data["execution_time"],
                    result_data=result_data["result_data"],
                    error_message=result_data.get("error_message"),
                    timestamp=datetime.fromisoformat(result_data["timestamp"]),
                )
                self.task_results.append(result)

            # Restore metrics
            self.metrics = state.get("metrics", self.metrics)

            logger.info(f"📂 Integration state loaded from {filename}")

        except FileNotFoundError:
            logger.warning(f"State file {filename} not found, starting fresh")
        except Exception as e:
            logger.error(f"Error loading state from {filename}: {str(e)}")


async def demo_integrated_system():
    """Demo hệ thống tích hợp OODA + Task Execution"""
    print(" HyperAI Phoenix - OODA Task Integration Demo")
    print("=" * 60)

    # Khởi tạo hệ thống tích hợp
    integration = OODATaskIntegration()

    try:
        # Load previous state nếu có
        integration.load_integration_state()

        print("\n🔗 Starting integrated OODA + Task Execution...")
        print(" System will automatically execute tasks based on OODA decisions")
        print("⏹  Press Ctrl+C to stop")

        # Chạy integrated operation
        await integration.start_integrated_operation("demo_integrated_operation")

    except KeyboardInterrupt:
        print("\n🛑 Demo stopped by user")

        # Lưu trạng thái cuối cùng
        integration.save_integration_state()

        # Hiển thị báo cáo cuối cùng
        status = integration.get_integration_status()
        print("\n Final Status Report:")
        print(f"    OODA Cycles: {status['metrics']['ooda_cycles_triggered']}")
        print(f"    Tasks Executed: {status['metrics']['tasks_executed']}")
        print(f"    Tasks Successful: {status['metrics']['tasks_successful']}")
        print(f"    Tasks Failed: {status['metrics']['tasks_failed']}")

        if status["metrics"]["tasks_executed"] > 0:
            success_rate = (status["metrics"]["tasks_successful"] / status["metrics"]["tasks_executed"]) * 100
            print(f"    Success Rate: {success_rate:.1f}%")
        print("\n💾 Integration state saved")


async def main():
    """Main function"""
    print("🔗 HyperAI Phoenix - OODA Task Integration System")
    print("=" * 60)

    # Chạy demo
    await demo_integrated_system()


if __name__ == "__main__":
    asyncio.run(main())
