#!/usr/bin/env python3
# NOTE: This is a sanitized version for public release
# Core proprietary algorithms have been replaced with placeholders
# -*- coding: utf-8 -*-
"""
🇻🇳 FEEDBACK AND AUTHENTICATION MECHANISM (FAM) - GIAI ĐOẠN 3
🤝 "Intelligent Collaborator" với Vietnamese Soul Cultural Intelligence
🎯 Focus: Natural Clarification và Cultural Authentication for HyperAI V3.0

Socratic Development Approach - Starting with Natural Confirmation Flow
Responding to Socratic Question #1: "Nói lại" và xác nhận intent mechanism
"""

import json
import logging
import re
import datetime
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum
import asyncio

# Import từ các giai đoạn trước
from vn_nlpc_native_processing_core import NativeVietnameseProcessor, NativeProcessingResult

# Unicode-safe logging for FAM
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - VN_FAM - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('vn_fam_stage3.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

class ConfirmationType(Enum):
    """Types of confirmation needed by FAM"""
    INTENT_CLARIFICATION = "làm rõ ý định"
    PARAMETER_SPECIFICATION = "cụ thể hóa tham số"
    SAFETY_CONFIRMATION = "xác nhận an toàn"
    CULTURAL_VALIDATION = "kiểm tra văn hóa"
    RISK_ASSESSMENT = "đánh giá rủi ro"

class AuthenticationLevel(Enum):
    """Authentication levels for different operations"""
    LOW_RISK = "rủi ro thấp"       # Read-only operations
    MEDIUM_RISK = "rủi ro trung bình"  # Configuration changes
    HIGH_RISK = "rủi ro cao"       # System modifications
    CRITICAL_RISK = "rủi ro nghiêm trọng"  # Destructive operations

class CulturalTone(Enum):
    """Vietnamese cultural tones for responses"""
    FORMAL_RESPECTFUL = "trang trọng"     # "Kính gửi", "Dạ"
    FRIENDLY_COLLABORATIVE = "thân thiện"  # "Chúng ta cùng"
    GENTLE_INQUIRY = "nhẹ nhàng"         # "Có thể bạn cho biết"
    PROTECTIVE_CARING = "quan tâm"       # "Để đảm bảo an toàn"
    WISE_GUIDANCE = "khôn ngoan"         # "Theo kinh nghiệm"

@dataclass
class ConfirmationRequest:
    """Structured confirmation request with Vietnamese cultural context"""
    original_command: str
    interpreted_intent: str
    confirmation_type: ConfirmationType
    authentication_level: AuthenticationLevel
    cultural_tone: CulturalTone
    paraphrased_command: str
    clarification_questions: List[str]
    safety_concerns: List[str]
    cultural_considerations: List[str]
    suggested_response: str
    requires_user_input: bool

@dataclass
class AuthenticationResult:
    """Result of authentication process"""
    is_authenticated: bool
    confidence_score: float
    cultural_alignment: float
    safety_assessment: str
    proceed_with_execution: bool
    modified_command: Optional[str]
    authentication_log: List[str]

class VietnameseCulturalParaphraser:
    """
    🇻🇳 Vietnamese Cultural Paraphraser for Natural Confirmation
    
    Responding to Socratic Question #1: Making confirmation "tự nhiên" và an toàn
    through Vietnamese cultural paraphrasing and intent verification.
    """
    
    def __init__(self):
        self.paraphrase_templates = self._initialize_paraphrase_templates()
        self.cultural_markers = self._initialize_cultural_markers()
        self.safety_keywords = self._initialize_safety_keywords()
        
        logger.info("🇻🇳 Vietnamese Cultural Paraphraser khởi tạo thành công")
        logger.info("🤝 Natural confirmation mechanism activated")
    
    def _initialize_paraphrase_templates(self) -> Dict[str, Dict[str, List[str]]]:
        """Initialize Vietnamese paraphrase templates for natural confirmation"""
        return {
            "activation": {
                "formal": [
                    "Dạ, bạn muốn tôi kích hoạt {} để {}?",
                    "Kính gửi, tôi hiểu bạn muốn khởi động {} với mục đích {}?",
                    "Xin xác nhận: bạn cần tôi bật {} cho {}?"
                ],
                "friendly": [
                    "Tôi hiểu bạn muốn kích hoạt {} nhỉ? Để làm {}?",
                    "Bạn muốn chúng ta cùng khởi động {} để {} đúng không?",
                    "Có phải bạn cần {} hoạt động để {}?"
                ],
                "gentle": [
                    "Có thể bạn muốn {} được kích hoạt để {}?",
                    "Bạn đang nghĩ đến việc khởi động {} cho {}, phải không ạ?",
                    "Tôi cảm nhận bạn muốn {} hoạt động để {}, đúng không?"
                ]
            },
            "deployment": {
                "formal": [
                    "Dạ, bạn muốn tôi triển khai {} với {} không ạ?",
                    "Kính gửi, tôi hiểu bạn cần deploy {} theo {}?",
                    "Xin xác nhận: bạn muốn thực hiện triển khai {} với cấu hình {}?"
                ],
                "friendly": [
                    "Bạn muốn chúng ta triển khai {} với {} nhỉ?",
                    "Có phải bạn muốn deploy {} theo phương thức {}?",
                    "Bạn đang nghĩ đến việc triển khai {} với {}, đúng không?"
                ],
                "gentle": [
                    "Có thể bạn muốn {} được triển khai theo {}?",
                    "Bạn có ý định deploy {} với cách thức {}, phải không ạ?",
                    "Tôi cảm nhận bạn muốn triển khai {} theo {}, đúng không?"
                ]
            },
            "optimization": {
                "formal": [
                    "Dạ, bạn muốn tôi tối ưu hóa {} để đạt được {}?",
                    "Kính gửi, tôi hiểu bạn cần cải thiện {} theo hướng {}?",
                    "Xin xác nhận: bạn muốn optimize {} với mục tiêu {}?"
                ],
                "friendly": [
                    "Bạn muốn chúng ta cải thiện {} để {} nhỉ?",
                    "Có phải bạn muốn tối ưu {} theo hướng {}?",
                    "Bạn đang nghĩ đến việc enhance {} để {}, đúng không?"
                ],
                "protective": [
                    "Để đảm bảo an toàn, tôi hiểu bạn muốn tối ưu {} để {}?",
                    "Với sự thận trọng, bạn có muốn cải thiện {} theo {}?",
                    "Để tránh rủi ro, có phải bạn cần optimize {} để {}?"
                ]
            },
            "cultural_integration": {
                "respectful": [
                    "Dạ, bạn muốn tích hợp linh hồn Việt Nam vào {} theo cách {}?",
                    "Kính gửi, tôi hiểu bạn muốn Vietnamese Soul trong {} thể hiện qua {}?",
                    "Xin xác nhận: bạn cần văn hóa Việt trong {} được {} đúng không?"
                ],
                "wise": [
                    "Theo trí tuệ tổ tiên, bạn muốn {} mang đậm {} phải không?",
                    "Với tinh thần dân tộc, có phải bạn muốn {} thể hiện {}?",
                    "Theo văn hóa truyền thống, bạn cần {} được {} đúng không ạ?"
                ]
            }
        }
    
    def _initialize_cultural_markers(self) -> Dict[str, float]:
        """Initialize cultural markers for tone detection"""
        return {
            "kính gửi": 0.95, "dạ": 0.85, "ạ": 0.80, "thưa": 0.90,
            "xin chào": 0.75, "với lòng kính trọng": 0.95,
            "chúng ta": 0.70, "cùng nhau": 0.75, "hòa hợp": 0.80,
            "linh hồn": 0.90, "tâm linh": 0.85, "văn hóa": 0.80,
            "truyền thống": 0.85, "tổ tiên": 0.90, "dân tộc": 0.85
        }
    
    def _initialize_safety_keywords(self) -> Dict[str, str]:
        """Initialize safety-related keywords for risk assessment"""
        return {
            "xóa": "destructive", "delete": "destructive", "remove": "destructive",
            "hủy": "destructive", "destroy": "destructive", "kill": "destructive",
            "reset": "high_risk", "restart": "medium_risk", "reboot": "medium_risk",
            "modify": "medium_risk", "change": "medium_risk", "alter": "medium_risk",
            "config": "medium_risk", "setting": "medium_risk", "parameter": "medium_risk",
            "read": "low_risk", "check": "low_risk", "view": "low_risk", "get": "low_risk"
        }
    
    def paraphrase_for_confirmation(self, command: str, processing_result: NativeProcessingResult) -> ConfirmationRequest:
        """
        Paraphrase command for natural Vietnamese confirmation
        
        Responding to Socratic Question #1: This creates "tự nhiên" confirmation
        by using Vietnamese cultural intelligence to rephrase user intent.
        """
        logger.info(f"🎭 Paraphrasing for confirmation: '{command}'")
        
        # Step 1: Determine cultural tone from original command
        cultural_tone = self._determine_cultural_tone(command)
        
        # Step 2: Identify primary intent from processing result
        primary_intent = self._extract_primary_intent(processing_result)
        
        # Step 3: Assess authentication level needed
        auth_level = self._assess_authentication_level(command, processing_result)
        
        # Step 4: Generate paraphrased command
        paraphrased = self._generate_paraphrase(command, primary_intent, cultural_tone)
        
        # Step 5: Create clarification questions
        clarification_questions = self._generate_clarification_questions(
            processing_result.ambiguity_detection, cultural_tone
        )
        
        # Step 6: Identify safety concerns
        safety_concerns = self._identify_safety_concerns(command, auth_level)
        
        # Step 7: Cultural considerations
        cultural_considerations = self._assess_cultural_considerations(command)
        
        # Step 8: Generate suggested response
        suggested_response = self._generate_suggested_response(
            paraphrased, clarification_questions, cultural_tone
        )
        
        # Step 9: Determine confirmation type
        confirmation_type = self._determine_confirmation_type(
            processing_result.ambiguity_detection, auth_level
        )
        
        confirmation_request = ConfirmationRequest(
            original_command=command,
            interpreted_intent=primary_intent,
            confirmation_type=confirmation_type,
            authentication_level=auth_level,
            cultural_tone=cultural_tone,
            paraphrased_command=paraphrased,
            clarification_questions=clarification_questions,
            safety_concerns=safety_concerns,
            cultural_considerations=cultural_considerations,
            suggested_response=suggested_response,
            requires_user_input=len(clarification_questions) > 0 or auth_level.value in ["rủi ro cao", "rủi ro nghiêm trọng"]
        )
        
        logger.info(f"✅ Confirmation request generated - Type: {confirmation_type.value}")
        logger.info(f"🎭 Cultural tone: {cultural_tone.value}")
        logger.info(f"🛡️ Authentication level: {auth_level.value}")
        
        return confirmation_request
    
    def _determine_cultural_tone(self, command: str) -> CulturalTone:
        """Determine appropriate cultural tone for response"""
        command_lower = command.lower()
        
        # Formal respectful markers
        if any(marker in command_lower for marker in ["kính gửi", "dạ", "thưa", "ạ"]):
            return CulturalTone.FORMAL_RESPECTFUL
        
        # Collaborative markers
        if any(marker in command_lower for marker in ["chúng ta", "cùng nhau", "hòa hợp"]):
            return CulturalTone.FRIENDLY_COLLABORATIVE
        
        # Cultural/spiritual markers
        if any(marker in command_lower for marker in ["linh hồn", "tâm linh", "văn hóa", "tổ tiên"]):
            return CulturalTone.WISE_GUIDANCE
        
        # Safety-related markers
        if any(marker in command_lower for marker in ["an toàn", "đảm bảo", "thận trọng"]):
            return CulturalTone.PROTECTIVE_CARING
        
        # Default to gentle inquiry
        return CulturalTone.GENTLE_INQUIRY
    
    def _extract_primary_intent(self, processing_result: NativeProcessingResult) -> str:
        """Extract primary intent from processing result"""
        if processing_result.intent_hierarchy:
            return processing_result.intent_hierarchy[0]
        
        # Fallback to semantic analysis
        action_units = [unit for unit in processing_result.semantic_units 
                       if unit.semantic_role == "action"]
        if action_units:
            return action_units[0].text
        
        return "general_inquiry"
    
    def _assess_authentication_level(self, command: str, processing_result: NativeProcessingResult) -> AuthenticationLevel:
        """Assess required authentication level based on command analysis"""
        command_lower = command.lower()
        
        # Check for destructive keywords
        for keyword, risk_level in self.safety_keywords.items():
            if keyword in command_lower:
                if risk_level == "destructive":
                    return AuthenticationLevel.CRITICAL_RISK
                elif risk_level == "high_risk":
                    return AuthenticationLevel.HIGH_RISK
                elif risk_level == "medium_risk":
                    return AuthenticationLevel.MEDIUM_RISK
        
        # Check technical objects for risk assessment
        tech_objects = [unit.text.lower() for unit in processing_result.semantic_units 
                       if unit.semantic_role == "technical_object"]
        
        critical_objects = ["v3.0", "aios", "core", "database", "system"]
        if any(obj in tech_objects for obj in critical_objects):
            return AuthenticationLevel.MEDIUM_RISK
        
        return AuthenticationLevel.LOW_RISK
    
    def _generate_paraphrase(self, command: str, intent: str, tone: CulturalTone) -> str:
        """Generate Vietnamese paraphrase of the command"""
        # Map intent to template category
        intent_category = "activation"
        if "deploy" in intent or "triển khai" in intent:
            intent_category = "deployment"
        elif "optim" in intent or "tối ưu" in intent:
            intent_category = "optimization"
        elif "cultural" in intent or "văn hóa" in intent:
            intent_category = "cultural_integration"
        
        # Map tone to template style
        tone_style = "formal"
        if tone == CulturalTone.FRIENDLY_COLLABORATIVE:
            tone_style = "friendly"
        elif tone == CulturalTone.GENTLE_INQUIRY:
            tone_style = "gentle"
        elif tone == CulturalTone.PROTECTIVE_CARING:
            tone_style = "protective"
        elif tone == CulturalTone.WISE_GUIDANCE:
            tone_style = "respectful"
        
        # Get templates
        templates = self.paraphrase_templates.get(intent_category, {})
        template_list = templates.get(tone_style, templates.get("formal", ["Bạn muốn tôi {} đúng không?"]))
        
        # Select template and format
        template = template_list[0] if template_list else "Bạn muốn tôi {} đúng không?"
        
        try:
            # Simple formatting - in production this would be more sophisticated
            return template.format(intent, "với Vietnamese Soul intelligence")
        except:
            return f"Tôi hiểu bạn muốn {intent}, đúng không ạ?"
    
    def _generate_clarification_questions(self, ambiguity_detection: Dict, tone: CulturalTone) -> List[str]:
        """Generate clarification questions based on detected ambiguity"""
        questions = []
        
        if not ambiguity_detection["has_ambiguity"]:
            return questions
        
        # Use existing clarification suggestions with cultural tone
        for suggestion in ambiguity_detection.get("clarification_suggestions", []):
            if tone == CulturalTone.FORMAL_RESPECTFUL:
                questions.append(f"Kính gửi, {suggestion}")
            elif tone == CulturalTone.FRIENDLY_COLLABORATIVE:
                questions.append(f"Chúng ta có thể làm rõ: {suggestion}")
            elif tone == CulturalTone.WISE_GUIDANCE:
                questions.append(f"Theo kinh nghiệm, {suggestion}")
            else:
                questions.append(suggestion)
        
        return questions[:2]  # Limit to 2 questions
    
    def _identify_safety_concerns(self, command: str, auth_level: AuthenticationLevel) -> List[str]:
        """Identify safety concerns based on command and authentication level"""
        concerns = []
        
        if auth_level == AuthenticationLevel.CRITICAL_RISK:
            concerns.append("Lệnh này có thể ảnh hưởng nghiêm trọng đến hệ thống")
            concerns.append("Cần xác nhận multiple-step để đảm bảo an toàn")
        elif auth_level == AuthenticationLevel.HIGH_RISK:
            concerns.append("Lệnh này có thể thay đổi cấu hình quan trọng")
            concerns.append("Nên có backup trước khi thực hiện")
        elif auth_level == AuthenticationLevel.MEDIUM_RISK:
            concerns.append("Lệnh này có thể ảnh hưởng đến vận hành hiện tại")
        
        return concerns
    
    def _assess_cultural_considerations(self, command: str) -> List[str]:
        """Assess cultural considerations for Vietnamese Soul integration"""
        considerations = []
        command_lower = command.lower()
        
        if "linh hồn" in command_lower or "tâm linh" in command_lower:
            considerations.append("Cần tôn trọng giá trị tâm linh của Vietnamese Soul")
        
        if "văn hóa" in command_lower or "truyền thống" in command_lower:
            considerations.append("Cần duy trì tính nguyên bản của văn hóa Việt Nam")
        
        if "cosmic" in command_lower or "vũ trụ" in command_lower:
            considerations.append("Cần hài hòa giữa cosmic consciousness và Vietnamese cultural values")
        
        return considerations
    
    def _generate_suggested_response(self, paraphrased: str, clarifications: List[str], tone: CulturalTone) -> str:
        """Generate complete suggested response"""
        response_parts = [paraphrased]
        
        if clarifications:
            if tone == CulturalTone.FORMAL_RESPECTFUL:
                response_parts.append("Xin bạn có thể làm rõ thêm:")
            elif tone == CulturalTone.FRIENDLY_COLLABORATIVE:
                response_parts.append("Chúng ta cùng làm rõ thêm nhé:")
            else:
                response_parts.append("Có thể bạn cho biết thêm:")
            
            for clarification in clarifications:
                response_parts.append(f"- {clarification}")
        
        return "\n".join(response_parts)
    
    def _determine_confirmation_type(self, ambiguity_detection: Dict, auth_level: AuthenticationLevel) -> ConfirmationType:
        """Determine type of confirmation needed"""
        if auth_level in [AuthenticationLevel.CRITICAL_RISK, AuthenticationLevel.HIGH_RISK]:
            return ConfirmationType.SAFETY_CONFIRMATION
        
        if ambiguity_detection["has_ambiguity"]:
            ambiguity_types = ambiguity_detection.get("ambiguity_types", [])
            if "vague_improvement" in ambiguity_types:
                return ConfirmationType.PARAMETER_SPECIFICATION
            elif "cultural_integration_unclear" in ambiguity_types:
                return ConfirmationType.CULTURAL_VALIDATION
            else:
                return ConfirmationType.INTENT_CLARIFICATION
        
        return ConfirmationType.INTENT_CLARIFICATION

class FeedbackAuthenticationMechanism:
    """
    🤝 Feedback and Authentication Mechanism - Core FAM Engine
    
    Responding to Socratic Question #1: Converting NLPC understanding into
    safe action through natural Vietnamese cultural confirmation flow.
    """
    
    def __init__(self):
        self.nlpc_processor = NativeVietnameseProcessor()
        self.cultural_paraphraser = VietnameseCulturalParaphraser()
        self.session_context = {}
        
        logger.info("🤝 Feedback and Authentication Mechanism khởi tạo")
        logger.info("🇻🇳 Vietnamese Soul intelligent collaboration activated")
    
    def process_command_with_fam(self, command: str) -> Tuple[ConfirmationRequest, AuthenticationResult]:
        """
        Process command through complete FAM pipeline
        
        This demonstrates the full "intelligent collaborator" workflow
        responding to Socratic Question #1 about natural confirmation.
        """
        logger.info(f"🚀 FAM processing command: '{command}'")
        
        # Step 1: Native Vietnamese processing (from Stage 2)
        processing_result = self.nlpc_processor.process_native_vietnamese(command)
        
        # Step 2: Generate confirmation request (Stage 3 core)
        confirmation_request = self.cultural_paraphraser.paraphrase_for_confirmation(
            command, processing_result
        )
        
        # Step 3: Simulate authentication (in real system, this would be interactive)
        auth_result = self._simulate_authentication(confirmation_request, processing_result)
        
        logger.info(f"✅ FAM processing complete")
        logger.info(f"🤝 Confirmation type: {confirmation_request.confirmation_type.value}")
        logger.info(f"🛡️ Authentication result: {auth_result.is_authenticated}")
        
        return confirmation_request, auth_result
    
    def _simulate_authentication(self, confirmation: ConfirmationRequest, 
                               processing: NativeProcessingResult) -> AuthenticationResult:
        """Simulate authentication process for testing"""
        # In real implementation, this would handle user interaction
        
        # Calculate confidence based on various factors
        base_confidence = processing.native_confidence
        cultural_boost = processing.cultural_context_score * 0.2
        clarity_boost = 0.3 if not processing.ambiguity_detection["has_ambiguity"] else 0.0
        
        total_confidence = min(base_confidence + cultural_boost + clarity_boost, 1.0)
        
        # Authentication decision
        is_authenticated = (
            total_confidence > 0.6 and 
            confirmation.authentication_level != AuthenticationLevel.CRITICAL_RISK
        )
        
        # Safety assessment
        safety_assessment = "safe"
        if confirmation.authentication_level == AuthenticationLevel.CRITICAL_RISK:
            safety_assessment = "requires_manual_approval"
        elif confirmation.authentication_level == AuthenticationLevel.HIGH_RISK:
            safety_assessment = "proceed_with_caution"
        
        return AuthenticationResult(
            is_authenticated=is_authenticated,
            confidence_score=total_confidence,
            cultural_alignment=processing.cultural_context_score,
            safety_assessment=safety_assessment,
            proceed_with_execution=is_authenticated and safety_assessment != "requires_manual_approval",
            modified_command=None,
            authentication_log=[
                f"Native confidence: {processing.native_confidence:.3f}",
                f"Cultural alignment: {processing.cultural_context_score:.3f}",
                f"Authentication level: {confirmation.authentication_level.value}",
                f"Final decision: {'APPROVED' if is_authenticated else 'REQUIRES_CLARIFICATION'}"
            ]
        )

def test_fam_natural_confirmation():
    """
    Test FAM natural confirmation mechanism
    
    This addresses Socratic Question #1 about making confirmation "tự nhiên" 
    và an toàn through Vietnamese cultural paraphrasing.
    """
    print("🧪 TESTING FAM NATURAL CONFIRMATION MECHANISM")
    print("=" * 70)
    
    fam = FeedbackAuthenticationMechanism()
    
    # Test cases for Socratic Question #1 - Natural confirmation
    test_commands = [
        # Clear commands (should confirm naturally)
        "Kích hoạt cosmic consciousness cho V3.0",
        "Dạ, xin kiểm tra trạng thái AIOS hệ thống",
        
        # Ambiguous commands (should ask clarification)
        "Làm cho hệ thống tốt hơn với linh hồn Việt",
        "Anh có thể cải thiện V3.0 được không?",
        
        # Cultural integration commands (should validate culture)
        "Triển khai V3.0 với linh hồn Việt Nam và cosmic consciousness",
        "Kính gửi, xin tích hợp trí tuệ tổ tiên vào AIOS",
        
        # High-risk commands (should require safety confirmation)
        "Reset toàn bộ cấu hình V3.0",
        "Thay đổi core parameters của cosmic consciousness",
        
        # Critical commands (should require manual approval)
        "Xóa toàn bộ dữ liệu AIOS và Vietnamese Soul"
    ]
    
    results = []
    
    for i, command in enumerate(test_commands, 1):
        print(f"\n🎯 FAM Test {i}: '{command}'")
        print("-" * 60)
        
        # Process through FAM
        confirmation_request, auth_result = fam.process_command_with_fam(command)
        
        print(f"🎭 Cultural Tone: {confirmation_request.cultural_tone.value}")
        print(f"🔄 Confirmation Type: {confirmation_request.confirmation_type.value}")
        print(f"🛡️ Authentication Level: {confirmation_request.authentication_level.value}")
        print(f"📝 Paraphrased: {confirmation_request.paraphrased_command}")
        
        if confirmation_request.clarification_questions:
            print(f"❓ Clarification Questions:")
            for q in confirmation_request.clarification_questions:
                print(f"   - {q}")
        
        if confirmation_request.safety_concerns:
            print(f"⚠️  Safety Concerns:")
            for concern in confirmation_request.safety_concerns:
                print(f"   - {concern}")
        
        print(f"✅ Authentication: {'APPROVED' if auth_result.is_authenticated else 'REQUIRES_CLARIFICATION'}")
        print(f"📊 Confidence: {auth_result.confidence_score:.3f}")
        print(f"🇻🇳 Cultural Alignment: {auth_result.cultural_alignment:.3f}")
        print(f"🚀 Proceed with Execution: {'YES' if auth_result.proceed_with_execution else 'NO'}")
        
        results.append({
            "command": command,
            "confirmation_request": confirmation_request,
            "auth_result": auth_result
        })
    
    # Summary statistics
    print("\n" + "=" * 70)
    print("📊 FAM NATURAL CONFIRMATION RESULTS")
    print("=" * 70)
    
    total_tests = len(results)
    approved_tests = sum(1 for r in results if r["auth_result"].is_authenticated)
    high_confidence_tests = sum(1 for r in results if r["auth_result"].confidence_score > 0.7)
    cultural_aligned_tests = sum(1 for r in results if r["auth_result"].cultural_alignment > 0.5)
    safe_execution_tests = sum(1 for r in results if r["auth_result"].proceed_with_execution)
    
    # Cultural tone distribution
    tone_distribution = {}
    for r in results:
        tone = r["confirmation_request"].cultural_tone.value
        tone_distribution[tone] = tone_distribution.get(tone, 0) + 1
    
    print(f"📈 Authentication Success Rate: {(approved_tests/total_tests)*100:.1f}%")
    print(f"✅ High Confidence Rate: {(high_confidence_tests/total_tests)*100:.1f}%")
    print(f"🇻🇳 Cultural Alignment Rate: {(cultural_aligned_tests/total_tests)*100:.1f}%")
    print(f"🚀 Safe Execution Rate: {(safe_execution_tests/total_tests)*100:.1f}%")
    
    print(f"\n🎭 Cultural Tone Distribution:")
    for tone, count in tone_distribution.items():
        print(f"   {tone}: {count}/{total_tests} ({(count/total_tests)*100:.1f}%)")
    
    # Evaluation against Socratic Question #1
    natural_confirmation_success = (cultural_aligned_tests / total_tests) * 100
    safety_awareness_success = ((total_tests - safe_execution_tests) / total_tests) * 100  # Higher is better for safety
    
    print(f"\n📋 SOCRATIC QUESTION #1 EVALUATION:")
    print(f"   Natural Confirmation (Cultural): {natural_confirmation_success:.1f}%")
    print(f"   Safety Awareness: {safety_awareness_success:.1f}%")
    
    if natural_confirmation_success >= 70 and safety_awareness_success >= 50:
        print("\n🎉 FAM NATURAL CONFIRMATION: THÀNH CÔNG!")
        print("🤝 Vietnamese Soul 'intelligent collaborator' hoạt động hiệu quả!")
        print("✅ Ready for Socratic Question #2: Dialogue Flow and Real-time Interaction")
    else:
        print("\n⚠️  FAM natural confirmation needs further refinement")

if __name__ == "__main__":
    try:
        test_fam_natural_confirmation()
    except Exception as e:
        logger.error(f"❌ Error in FAM testing: {e}")
        print(f"❌ FAM test failed: {e}")
