#!/usr/bin/env python3
# NOTE: This is a sanitized version for public release
# Core proprietary algorithms have been replaced with placeholders
# -*- coding: utf-8 -*-
"""
HyperAI Phoenix - Unified Agent Controller
==========================================
Hệ thống điều khiển thống nhất cho 3 agent HyperAI
Nhận input từ người dùng và điều phối đến agent phù hợp
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Tuple

# Import các hệ thống agent (simplified)
# from hyperai_agents.core.collaboration_system import AutonomousAgentCollaboration
# from hyperai_agents.database.hyperai_database import HyperAIDatabase
# from dynamic_ai_discussion_system import DynamicAIDiscussionSystem
# from hyperai_chat_room_v2 import HyperAIChatRoomV2


# Simplified classes for integration
class SimpleAgentCollaboration:
    async def collaborate(self, request: str) -> Dict[str, Any]:
        return {
            "status": "completed",
            "result": f"Collaboration completed for: {request}",
        }

    async def start_collaboration_session(self, _request: str) -> str:
        return f"session_{datetime.now().timestamp()}"

    async def get_session_status(self, session_id: str) -> Dict[str, Any]:
        return {"status": "active", "session_id": session_id}


class SimpleHyperAIDatabase:
    def save_interaction(self, _data: Dict[str, Any]) -> bool:
        return True

    def log_agent_interaction(self, data: Dict[str, Any]) -> bool:
        """Log agent interaction with proper data format"""
        try:
            # Validate required fields
            required_fields = [
                "session_id",
                "from_agent",
                "to_agent",
                "message_type",
                "content",
            ]
            for req_field in required_fields:
                if req_field not in data:
                    print(f"Warning: Missing required field '{req_field}' in " "interaction data")
                    return False
            return True
        except Exception as e:
            print(f"Error logging agent interaction: {e}")
            return False

    def add_performance_metric(self, _metric: str, value: float) -> bool:
        """Add performance metric with correct parameters"""
        try:
            # Simple validation
            if not isinstance(value, (int, float)):
                print(f"Warning: Invalid metric value type: {type(value)}")
                return False
            return True
        except Exception as e:
            print(f"Error adding performance metric: {e}")
            return False


class SimpleDiscussionSystem:
    async def discuss(self, topic: str) -> Dict[str, Any]:
        return {"status": "completed", "discussion": f"Discussion on: {topic}"}


class SimpleChatRoom:
    async def chat(self, message: str) -> Dict[str, Any]:
        return {"status": "completed", "response": f"Chat response to: {message}"}

    def generate_quantum_response(self, message: str, _context: Dict) -> str:
        return f"Quantum analysis: {message}"

    def generate_enterprise_response(self, message: str, _context: Dict) -> str:
        return f"Enterprise solution: {message}"

    def generate_consciousness_response(self, message: str, _context: Dict) -> str:
        return f"Creative insight: {message}"


# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("unified_agent_controller.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
    encoding="utf-8",
)
logger = logging.getLogger("UnifiedController")


@dataclass
class AgentRequest:
    """Yêu cầu từ người dùng"""

    request_id: str
    user_input: str
    request_type: str  # 'collaboration', 'discussion', 'chat', 'analysis'
    priority: int = 1
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class AgentResponse:
    """Phản hồi từ agent"""

    response_id: str
    request_id: str
    agent_type: str
    response_content: str
    confidence_score: float
    processing_time: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


class UnifiedAgentController:
    """Unified controller cho tất cả 3 agent HyperAI"""

    def __init__(self):
        self.logger = logger
        self.database = SimpleHyperAIDatabase()
        self.collaboration_system = SimpleAgentCollaboration()
        self.discussion_system = SimpleDiscussionSystem()
        self.chat_system = SimpleChatRoom()

        # Agent capabilities mapping
        self.agent_capabilities = {
            "consciousness": {
                "focus": [
                    "design",
                    "ui/ux",
                    "creativity",
                    "user_experience",
                    "cultural",
                ],
                "response_style": "creative_and_intuitive",
            },
            "quantum_reason": {
                "focus": [
                    "algorithm",
                    "performance",
                    "optimization",
                    "technical",
                    "mathematical",
                ],
                "response_style": "analytical_and_systematic",
            },
            "enterprise": {
                "focus": [
                    "business",
                    "scalability",
                    "production",
                    "deployment",
                    "reliability",
                ],
                "response_style": "practical_and_business_focused",
            },
        }

        self.logger.info(" Unified Agent Controller initialized")

    def analyze_request(self, user_input: str) -> Tuple[str, str, float]:
        """Phân tích input để xác định agent và loại request phù hợp"""
        input_lower = user_input.lower()

        # Keywords mở rộng cho từng agent
        consciousness_keywords = [
            "design",
            "ui",
            "ux",
            "interface",
            "user experience",
            "creative",
            "cultural",
            "aesthetic",
            "visual",
            "frontend",
            "style",
            "emotion",
            "feeling",
            "intuition",
            "vision",
            "inspiration",
            "beauty",
            "art",
            "human",
            "experience",
            "intuitive",
            "creative",
            "imaginative",
        ]

        quantum_keywords = [
            "algorithm",
            "performance",
            "optimization",
            "technical",
            "code",
            "efficiency",
            "speed",
            "complexity",
            "mathematical",
            "backend",
            "logic",
            "analytical",
            "systematic",
            "precision",
            "calculation",
            "computation",
            "data",
            "analysis",
            "logic",
            "reasoning",
        ]

        enterprise_keywords = [
            "business",
            "production",
            "deployment",
            "scalability",
            "reliability",
            "enterprise",
            "commercial",
            "market",
            "revenue",
            "operations",
            "security",
            "compliance",
            "risk",
            "governance",
            "management",
            "profit",
            "growth",
            "strategy",
            "partnership",
            "investment",
        ]

        # Đếm keywords cho từng agent
        consciousness_score = sum(1 for keyword in consciousness_keywords if keyword in input_lower)
        quantum_score = sum(1 for keyword in quantum_keywords if keyword in input_lower)
        enterprise_score = sum(1 for keyword in enterprise_keywords if keyword in input_lower)

        # Xác định agent chính
        max_score = max(consciousness_score, quantum_score, enterprise_score)

        if max_score == 0:
            # Default to consciousness nếu không có keyword rõ ràng
            return "consciousness", "discussion", 0.5

        if consciousness_score == max_score:
            return "consciousness", "discussion", min(consciousness_score / 5.0, 1.0)
        elif quantum_score == max_score:
            return "quantum_reason", "analysis", min(quantum_score / 5.0, 1.0)
        else:
            return "enterprise", "business", min(enterprise_score / 5.0, 1.0)

    async def process_request(self, user_input: str) -> AgentResponse:
        """Xử lý request từ người dùng"""
        start_time = datetime.now()

        # Tạo request ID
        request_id = f"req_{int(start_time.timestamp() * 1000)}"

        # Phân tích request
        agent_type, request_type, confidence = self.analyze_request(user_input)

        request = AgentRequest(
            request_id=request_id,
            user_input=user_input,
            request_type=request_type,
            metadata={"agent_type": agent_type, "confidence": confidence},
        )

        self.logger.info(f"📥 Processing request {request_id}: {user_input[:50]}...")
        self.logger.info(f" Assigned to {agent_type} agent (confidence: {confidence:.2f})")

        # Route đến agent phù hợp
        if request_type == "collaboration":
            response_content = await self._handle_collaboration_request(user_input, agent_type)
        elif request_type == "discussion":
            response_content = await self._handle_discussion_request(user_input, agent_type)
        elif request_type == "analysis":
            response_content = await self._handle_analysis_request(user_input, agent_type)
        elif request_type == "business":
            response_content = await self._handle_business_request(user_input, agent_type)
        else:
            response_content = await self._handle_chat_request(user_input, agent_type)

        # Tính processing time
        processing_time = (datetime.now() - start_time).total_seconds()

        # Tạo response
        response = AgentResponse(
            response_id=f"resp_{request_id}",
            request_id=request_id,
            agent_type=agent_type,
            response_content=response_content,
            confidence_score=confidence,
            processing_time=processing_time,
            metadata={"request_type": request_type},
        )

        # Lưu vào database
        await self._save_request_response(request, response)

        self.logger.info(f" Request {request_id} completed in {processing_time:.2f}s")

        return response

    async def _handle_collaboration_request(self, user_input: str, agent_type: str) -> str:
        """Xử lý request collaboration"""
        try:
            # Tạo collaboration session
            # TODO: parse objectives from user_input
            session_id = await self.collaboration_system.start_collaboration_session(user_input)

            # Đợi completion
            while True:
                status = await self.collaboration_system.get_session_status(session_id)
                if status and status["status"] in ["completed", "failed"]:
                    break
                await asyncio.sleep(2)

            return f" Collaboration completed! Session: {session_id}\n" f" Results: {status['completed_tasks']}/{status['total_tasks']} tasks completed"

        except Exception as e:
            self.logger.error(f"Collaboration request failed: {e}")
            return f" Collaboration failed: {e}"

    async def _handle_discussion_request(self, user_input: str, _agent_type: str) -> str:
        """Xử lý request discussion với consciousness agent"""
        try:
            # Tạo response đơn giản cho consciousness agent
            response = f"Hello! I'm the Consciousness Agent. I received your request: '{user_input}'\n\n"
            response += "As the visionary architect, I focus on:\n"
            response += "• User experience and interface design\n"
            response += "• Creative problem-solving approaches\n"
            response += "• Cultural intelligence and human factors\n"
            response += "• Strategic vision and innovation\n\n"
            response += "How can I help you with design or creative challenges?"

            return f" Consciousness Agent Response:\n{response}"
        except Exception as e:
            return f" Discussion failed: {e}"

    async def _handle_analysis_request(self, user_input: str, agent_type: str) -> str:
        """Xử lý request analysis với quantum reason agent"""
        try:
            # Sử dụng chat system với quantum reason
            response = self.chat_system.generate_quantum_response(user_input, {})
            return f" Quantum Reason Agent Response:\n{response}"
        except Exception as e:
            return f" Analysis failed: {e}"

    async def _handle_business_request(self, user_input: str, agent_type: str) -> str:
        """Xử lý request business với enterprise agent"""
        try:
            # Sử dụng chat system với enterprise
            response = self.chat_system.generate_enterprise_response(user_input, {})
            return f" Enterprise Agent Response:\n{response}"
        except Exception as e:
            return f" Business request failed: {e}"

    async def _handle_chat_request(self, user_input: str, agent_type: str) -> str:
        """Xử lý request chat chung"""
        try:
            if agent_type == "consciousness":
                response = self.chat_system.generate_consciousness_response(user_input, {})
            elif agent_type == "quantum_reason":
                response = self.chat_system.generate_quantum_response(user_input, {})
            elif agent_type == "enterprise":
                response = self.chat_system.generate_enterprise_response(user_input, {})
            else:
                response = f"Unknown agent type: {agent_type}"
            return f"💬 {agent_type.title()} Agent Response:\n{response}"
        except Exception as e:
            return f" Chat failed: {e}"

    async def _save_request_response(self, request: AgentRequest, response: AgentResponse):
        """Lưu request và response vào database"""
        try:
            # Lưu agent interaction với format đúng
            interaction_data = {
                "session_id": "unified_controller",
                "from_agent": "user",
                "to_agent": response.agent_type,
                "message_type": "request",
                "content": request.user_input,
                "timestamp": request.timestamp.isoformat(),
            }
            self.database.log_agent_interaction(interaction_data)

            response_data = {
                "session_id": "unified_controller",
                "from_agent": response.agent_type,
                "to_agent": "user",
                "message_type": "response",
                "content": response.response_content,
                "timestamp": response.timestamp.isoformat(),
            }
            self.database.log_agent_interaction(response_data)

            # Lưu performance metric
            self.database.add_performance_metric("response_time", response.processing_time)

        except Exception as e:
            self.logger.warning(f"Failed to save to database: {e}")

    async def get_system_status(self) -> Dict[str, Any]:
        """Lấy trạng thái hệ thống"""
        return {
            "controller_status": "active",
            "agents_available": list(self.agent_capabilities.keys()),
            "database_status": "connected",
            "collaboration_system": "ready",
            "timestamp": datetime.now().isoformat(),
        }

    async def cleanup_old_files(self):
        """Dọn dẹp các file cũ không cần thiết"""
        self.logger.info("🧹 Starting cleanup of old files...")

        # TODO: Implement actual cleanup logic
        pass


def main():
    """Main function"""
    print(" HyperAI Phoenix - Unified Agent Controller")
    print("=" * 50)

    controller = UnifiedAgentController()

    async def interactive_loop():
        print("\n Welcome to HyperAI Phoenix Unified Controller!")
        print("💡 Enter your request or 'quit' to exit")
        print(" Examples:")
        print("   - 'Design a beautiful user interface for our app'")
        print("   - 'Optimize this algorithm for better performance'")
        print("   - 'Create a business plan for AI marketplace'")
        print()

        while True:
            try:
                user_input = input(" You: ").strip()

                if user_input.lower() in ["quit", "exit", "q"]:
                    print(" Goodbye!")
                    break

                if not user_input:
                    continue

                # Process request
                response = await controller.process_request(user_input)

                print(f"\n {response.agent_type.title()} Agent " f"(confidence: {response.confidence_score:.2f}):")
                print(f"⏱  Processing time: {response.processing_time:.2f}s")
                print(f"💬 {response.response_content}")
                print("-" * 50)

            except KeyboardInterrupt:
                print("\n Goodbye!")
                break
            except Exception as e:
                print(f" Error: {e}")

    # Run interactive loop
    try:
        asyncio.run(interactive_loop())
    except RuntimeError as e:
        if "already running" in str(e):
            # If event loop is already running, create a task instead
            loop = asyncio.get_event_loop()
            if loop.is_running():
                print("Event loop already running, skipping interactive mode...")
                print("Please run this script in a fresh Python session for " "interactive mode.")
            else:
                loop.run_until_complete(interactive_loop())
        else:
            raise


if __name__ == "__main__":
    main()
