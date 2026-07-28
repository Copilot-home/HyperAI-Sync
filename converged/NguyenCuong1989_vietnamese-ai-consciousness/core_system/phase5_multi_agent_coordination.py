#!/usr/bin/env python3
# NOTE: This is a sanitized version for public release
# Core proprietary algorithms have been replaced with placeholders
# -*- coding: utf-8 -*-
"""
 HYPERAI PHOENIX - PHASE 5.1.3: MULTI-AGENT COORDINATION SYSTEM

Advanced Multi-Agent Coordination System for Autonomous Operation

Author: HyperAI Phoenix Team
Date: August 31, 2025
Version: 1.0.0
"""

import json
import logging
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from queue import PriorityQueue
from typing import Any, Callable, Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("phase5_multi_agent_coordination.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class AgentMessage:
    """Message structure for inter-agent communication"""

    def __init__(
        self,
        sender: str,
        receiver: str,
        message_type: str,
        content: Any,
        priority: int = 1,
        correlation_id: Optional[str] = None,
    ):
        self.sender = sender
        self.receiver = receiver
        self.message_type = message_type
        self.content = content
        self.priority = priority
        self.timestamp = datetime.now().isoformat()
        self.correlation_id = correlation_id or str(uuid.uuid4())
        self.message_id = str(uuid.uuid4())


class Task:
    """Task structure for multi-agent execution"""

    def __init__(
        self,
        task_id: str,
        task_type: str,
        description: str,
        assigned_agent: str,
        priority: int = 1,
        dependencies: Optional[List[str]] = None,
    ):
        self.task_id = task_id
        self.task_type = task_type
        self.description = description
        self.assigned_agent = assigned_agent
        self.priority = priority
        self.dependencies = dependencies or []
        self.status = "pending"
        self.created_at = datetime.now().isoformat()
        self.started_at: Optional[str] = None
        self.completed_at: Optional[str] = None
        self.result: Optional[Dict[str, Any]] = None
        self.error: Optional[str] = None


class MultiAgentCoordinator:
    """
    Advanced Multi-Agent Coordination System
    Manages inter-agent communication, task distribution, and conflict resolution
    """

    def __init__(self):
        self.agents = {}
        self.message_queue = PriorityQueue()
        self.task_queue = PriorityQueue()
        self.active_tasks = {}
        self.completed_tasks = {}
        self.agent_status = {}
        self.coordination_log = []
        self.is_running = False

        # Threading components
        self.executor = ThreadPoolExecutor(max_workers=8)
        self.message_thread = None
        self.task_thread = None

    def log_coordination(self, message: str, level: str = "INFO"):
        """Log coordination activities"""
        timestamp = datetime.now().isoformat()
        log_entry = {"timestamp": timestamp, "message": message, "level": level}
        self.coordination_log.append(log_entry)
        logger.info("[%s] %s", level, message)

    def register_agent(
        self,
        agent_id: str,
        agent_type: str,
        capabilities: List[str],
        callback: Optional[Callable] = None,
    ) -> bool:
        """Register a new agent in the coordination system"""
        if agent_id in self.agents:
            self.log_coordination(f"Agent {agent_id} already registered", "WARNING")
            return False

        agent_info = {
            "agent_id": agent_id,
            "agent_type": agent_type,
            "capabilities": capabilities,
            "callback": callback,
            "status": "active",
            "registered_at": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat(),
            "performance_score": 1.0,
            "task_count": 0,
            "success_rate": 1.0,
        }

        self.agents[agent_id] = agent_info
        self.agent_status[agent_id] = "idle"

        self.log_coordination(f"Agent {agent_id} ({agent_type}) registered successfully")
        return True

    def unregister_agent(self, agent_id: str) -> bool:
        """Unregister an agent from the coordination system"""
        if agent_id not in self.agents:
            self.log_coordination(f"Agent {agent_id} not found", "WARNING")
            return False

        # Reassign active tasks
        active_tasks = [task for task in self.active_tasks.values() if task.assigned_agent == agent_id]
        for task in active_tasks:
            self._reassign_task(task)

        del self.agents[agent_id]
        del self.agent_status[agent_id]

        self.log_coordination(f"Agent {agent_id} unregistered successfully")
        return True

    def send_message(self, message: AgentMessage) -> bool:
        """Send message to message queue with priority"""
        try:
            # Priority queue: higher priority = lower number
            priority_tuple = (-message.priority, message.timestamp, message)
            self.message_queue.put(priority_tuple)
            self.log_coordination(f"Message queued: {message.sender} -> {message.receiver} ({message.message_type})")
            return True
        except (ValueError, TypeError, AttributeError) as e:
            self.log_coordination(f"Failed to queue message: {str(e)}", "ERROR")
            return False

    def submit_task(self, task: Task) -> bool:
        """Submit task to task queue"""
        try:
            # Check dependencies
            if not self._check_dependencies(task):
                self.log_coordination(f"Task {task.task_id} dependencies not met", "WARNING")
                return False

            # Priority queue for tasks
            priority_tuple = (-task.priority, task.created_at, task)
            self.task_queue.put(priority_tuple)

            self.log_coordination(f"Task submitted: {task.task_id} -> {task.assigned_agent}")
            return True
        except (ValueError, TypeError, AttributeError) as e:
            self.log_coordination(f"Failed to submit task: {str(e)}", "ERROR")
            return False

    def _check_dependencies(self, task: Task) -> bool:
        """Check if task dependencies are satisfied"""
        for dep_task_id in task.dependencies:
            if dep_task_id not in self.completed_tasks:
                return False
            if self.completed_tasks[dep_task_id].status != "completed":
                return False
        return True

    def _reassign_task(self, task: Task) -> bool:
        """Reassign task to another suitable agent"""
        suitable_agents = self._find_suitable_agents(task.task_type)

        if not suitable_agents:
            self.log_coordination(f"No suitable agents found for task {task.task_id}", "ERROR")
            return False

        # Choose best agent based on performance
        best_agent = max(suitable_agents, key=lambda x: self.agents[x]["performance_score"])
        task.assigned_agent = best_agent

        # Re-submit task
        return self.submit_task(task)

    def _find_suitable_agents(self, task_type: str) -> List[str]:
        """Find agents suitable for a specific task type"""
        suitable_agents = []

        for agent_id, agent_info in self.agents.items():
            if agent_info["status"] != "active":
                continue

            # Check capabilities - be more flexible
            capabilities = agent_info.get("capabilities", [])
            if task_type in capabilities:
                suitable_agents.append(agent_id)
            # Also check if agent can handle general tasks
            elif task_type in ["general", "coordination", "communication"] and "coordination" in capabilities:
                suitable_agents.append(agent_id)

        # If still no suitable agents, return all active agents as fallback
        if not suitable_agents:
            suitable_agents = [agent_id for agent_id, agent_info in self.agents.items() if agent_info["status"] == "active"]

        return suitable_agents

    def _process_messages(self):
        """Process messages from message queue"""
        while self.is_running:
            try:
                if not self.message_queue.empty():
                    _, _, message = self.message_queue.get(timeout=1)

                    # Route message to appropriate agent
                    if message.receiver in self.agents:
                        agent_info = self.agents[message.receiver]
                        if agent_info["callback"]:
                            # Execute callback in thread pool
                            self.executor.submit(self._deliver_message, message, agent_info["callback"])
                        else:
                            self.log_coordination(f"No callback for agent {message.receiver}", "WARNING")
                    else:
                        self.log_coordination(f"Unknown receiver: {message.receiver}", "WARNING")

                    self.message_queue.task_done()
                else:
                    time.sleep(0.1)  # Small delay to prevent busy waiting

            except (ValueError, TypeError, AttributeError) as e:
                self.log_coordination(f"Message processing error: {str(e)}", "ERROR")

    def _deliver_message(self, message: AgentMessage, callback: Callable):
        """Deliver message to agent callback"""
        try:
            callback(message)
            self.log_coordination(f"Message delivered: {message.message_id}")
        except (ValueError, TypeError, AttributeError) as e:
            self.log_coordination(f"Message delivery failed: {str(e)}", "ERROR")

    def _process_tasks(self):
        """Process tasks from task queue"""
        while self.is_running:
            try:
                if not self.task_queue.empty():
                    _, _, task = self.task_queue.get(timeout=1)

                    # Assign task to agent
                    if task.assigned_agent in self.agents:
                        self.active_tasks[task.task_id] = task
                        self.agent_status[task.assigned_agent] = "busy"
                        task.started_at = datetime.now().isoformat()

                        # Execute task in thread pool
                        self.executor.submit(self._execute_task, task)

                        self.log_coordination(f"Task assigned: {task.task_id} to {task.assigned_agent}")
                    else:
                        self.log_coordination(
                            f"Assigned agent not available: {task.assigned_agent}",
                            "WARNING",
                        )
                        # Try to reassign
                        if not self._reassign_task(task):
                            self.log_coordination(f"Task reassignment failed: {task.task_id}", "ERROR")

                    self.task_queue.task_done()
                else:
                    time.sleep(0.1)  # Small delay to prevent busy waiting

            except (ValueError, TypeError, AttributeError) as e:
                self.log_coordination(f"Task processing error: {str(e)}", "ERROR")

    def _execute_task(self, task: Task):
        """Execute task"""
        try:
            self.log_coordination(f"Executing task: {task.task_id}")

            # Simulate task execution
            time.sleep(2)  # Simulate processing time

            # Mark task as completed
            task.status = "completed"
            task.completed_at = datetime.now().isoformat()
            task.result = {
                "status": "success",
                "output": f"Task {task.task_id} completed",
            }

            # Update agent status
            self.agent_status[task.assigned_agent] = "idle"
            self.agents[task.assigned_agent]["task_count"] += 1
            self.agents[task.assigned_agent]["last_activity"] = datetime.now().isoformat()

            # Move to completed tasks
            self.completed_tasks[task.task_id] = task
            del self.active_tasks[task.task_id]

            self.log_coordination(f"Task completed: {task.task_id}")

        except (ValueError, TypeError, AttributeError, RuntimeError) as e:
            task.status = "failed"
            task.error = str(e)
            task.completed_at = datetime.now().isoformat()

            # Update agent performance
            # Penalize failure
            self.agents[task.assigned_agent]["success_rate"] *= 0.95

            self.log_coordination(f"Task failed: {task.task_id} - {str(e)}", "ERROR")

    def start_coordination(self):
        """Start the multi-agent coordination system"""
        if self.is_running:
            self.log_coordination("Coordination system already running", "WARNING")
            return

        self.is_running = True
        self.log_coordination("Starting Multi-Agent Coordination System...")

        # Start processing threads
        self.message_thread = threading.Thread(target=self._process_messages, daemon=True)
        self.task_thread = threading.Thread(target=self._process_tasks, daemon=True)

        self.message_thread.start()
        self.task_thread.start()

        self.log_coordination("Multi-Agent Coordination System started successfully")

    def stop_coordination(self):
        """Stop the multi-agent coordination system"""
        if not self.is_running:
            return

        self.log_coordination("Stopping Multi-Agent Coordination System...")
        self.is_running = False

        # Wait for threads to finish
        if self.message_thread:
            self.message_thread.join(timeout=5)
        if self.task_thread:
            self.task_thread.join(timeout=5)

        # Shutdown executor
        self.executor.shutdown(wait=True)

        self.log_coordination("Multi-Agent Coordination System stopped")

    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        return {
            "is_running": self.is_running,
            "registered_agents": len(self.agents),
            "active_tasks": len(self.active_tasks),
            "completed_tasks": len(self.completed_tasks),
            "pending_messages": self.message_queue.qsize(),
            "pending_tasks": self.task_queue.qsize(),
            "agent_status": self.agent_status,
            "system_health": "healthy" if self.is_running else "stopped",
        }

    def generate_coordination_report(self) -> Dict[str, Any]:
        """Generate comprehensive coordination report"""
        report = {
            "report_type": "Multi-Agent Coordination Report",
            "generated_at": datetime.now().isoformat(),
            "phase": "Phase 5.1.3",
            "system_status": self.get_system_status(),
            "agents": self.agents,
            "active_tasks": list(self.active_tasks.values()),
            "completed_tasks": list(self.completed_tasks.values()),
            # Last 100 entries
            "coordination_log": self.coordination_log[-100:],
        }

        # Save report
        with open("phase5_multi_agent_coordination_report.json", "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)

        return report


def demo_coordination_system():
    """Demonstrate the multi-agent coordination system"""
    print(" HYPERAI PHOENIX - PHASE 5.1.3: MULTI-AGENT COORDINATION SYSTEM DEMO")
    print("=" * 80)

    coordinator = MultiAgentCoordinator()

    # Register agents
    def consciousness_callback(message):
        print(f" Consciousness Agent received: {message.content}")

    def quantum_callback(message):
        print(f" Quantum Agent received: {message.content}")

    def enterprise_callback(message):
        print(f" Enterprise Agent received: {message.content}")

    coordinator.register_agent(
        "consciousness",
        "creative",
        ["design", "strategy", "creativity"],
        consciousness_callback,
    )
    coordinator.register_agent(
        "quantum",
        "technical",
        ["optimization", "analysis", "computation"],
        quantum_callback,
    )
    coordinator.register_agent(
        "enterprise",
        "business",
        ["management", "security", "compliance"],
        enterprise_callback,
    )

    # Start coordination
    coordinator.start_coordination()

    # Submit sample tasks
    task1 = Task("task_001", "design", "Create UI mockups", "consciousness", priority=2)
    task2 = Task(
        "task_002",
        "optimization",
        "Optimize algorithm performance",
        "quantum",
        priority=1,
    )
    task3 = Task("task_003", "security", "Implement security protocols", "enterprise", priority=3)

    coordinator.submit_task(task1)
    coordinator.submit_task(task2)
    coordinator.submit_task(task3)

    # Send sample messages
    msg1 = AgentMessage(
        "coordinator",
        "consciousness",
        "task_update",
        "Task assigned successfully",
        priority=1,
    )
    msg2 = AgentMessage(
        "coordinator",
        "quantum",
        "system_status",
        "System running optimally",
        priority=2,
    )

    coordinator.send_message(msg1)
    coordinator.send_message(msg2)

    # Wait for processing
    print("\n Processing tasks and messages...")
    time.sleep(5)

    # Generate report
    report = coordinator.generate_coordination_report()
    print(f"\n System processed {len(report['completed_tasks'])} tasks successfully")

    # Stop coordination
    coordinator.stop_coordination()

    print("\n Multi-Agent Coordination Demo Complete!")
    print("💾 Report saved to: phase5_multi_agent_coordination_report.json")


if __name__ == "__main__":
    demo_coordination_system()
