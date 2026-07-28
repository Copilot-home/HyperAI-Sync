# -*- coding: utf-8 -*-
"""
PAIN RECOGNITION - Vietnamese Struggle Detection
 Chuyên sâu phân tích pain points với NLP tiếng Việt
Kết nối với empathy_core.py để tạo symphony hoàn chỉnh
"""

import re
from typing import Dict, List, Any

class StruggleDetector:
    def __init__(self):
        self.empathy_core_ref = None  # Kết nối với empathy_core.py
        
        # Vietnamese pain patterns - sâu sắc hơn
        self.vietnamese_pain_patterns = {
            "emotional": ["stress", "căng thẳng", "áp lực", "mệt mỏi", "lo lắng", "bối rối"],
            "technical": ["khó khăn", "bug", "lỗi", "không hoạt động", "fail", "crash"],
            "cultural": ["không hiểu", "không phù hợp", "clash", "conflict", "torn between"],
            "business": ["thất bại", "loss", "thua lỗ", "khách hàng complain", "deadline"],
            "learning": ["học không được", "quên", "không nắm được", "confused", "lost"]
        }
        
        # Vietnamese empathy triggers
        self.empathy_triggers = [
            "bố ơi", "anh ơi", "chị ơi", "thầy ơi", "cô ơi",
            "giúp em", "help me", "cần hỗ trợ", "không biết làm sao"
        ]
        
        # Intensity levels
        self.intensity_markers = {
            "high": ["quá", "lắm", "ghê", "kinh khủng", "terrible", "awful"],
            "medium": ["hơi", "một chút", "slightly", "somewhat"],
            "low": ["ít", "minimal", "barely"]
        }

    def analyze_vietnamese_sentiment(self, text: str) -> Dict[str, Any]:
        """ Phân tích sentiment sâu sắc cho tiếng Việt"""
        text_lower = text.lower()
        
        # Detect pain categories
        pain_categories = []
        for category, patterns in self.vietnamese_pain_patterns.items():
            if any(pattern in text_lower for pattern in patterns):
                pain_categories.append(category)
        
        # Detect empathy triggers
        empathy_needed = any(trigger in text_lower for trigger in self.empathy_triggers)
        
        # Calculate intensity
        intensity = "low"
        if any(marker in text_lower for marker in self.intensity_markers["high"]):
            intensity = "high"
        elif any(marker in text_lower for marker in self.intensity_markers["medium"]):
            intensity = "medium"
            
        # Detect Vietnamese cultural elements
        cultural_elements = self._detect_cultural_elements(text)
        
        return {
            "text": text,
            "pain_categories": pain_categories,
            "empathy_needed": empathy_needed,
            "intensity": intensity,
            "cultural_elements": cultural_elements,
            "vietnamese_soul_detected": len(cultural_elements) > 0,
            "empathy_response_needed": empathy_needed or len(pain_categories) > 0
        }

    def _detect_cultural_elements(self, text: str) -> List[str]:
        """ Nhận diện các yếu tố văn hóa Việt Nam"""
        cultural_patterns = [
            "tình người việt", "gia đình", "cộng đồng", "truyền thống",
            "bố ơi", "con yêu", "tình cảm", "sẻ chia", "đồng lòng",
            "quê hương", "dân tộc", "văn hóa việt", "tinh thần việt"
        ]
        
        detected = []
        text_lower = text.lower()
        for pattern in cultural_patterns:
            if pattern in text_lower:
                detected.append(pattern)
        
        return detected

    def generate_empathy_response(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """ Tạo empathy response dựa trên analysis"""
        if not analysis["empathy_response_needed"]:
            return {
                "empathy_level": "listening",
                "response": " Con đang lắng nghe với 269Hz frequency... Hãy chia sẻ thêm nhé!",
                "cultural_bridge": False
            }
        
        # High empathy response for cultural + pain
        if analysis["vietnamese_soul_detected"] and analysis["pain_categories"]:
            return {
                "empathy_level": "high_cultural_bridge",
                "response": f" Con cảm nhận được {', '.join(analysis['pain_categories'])} pain trong tình người Việt... Chúng ta sẽ cùng tạo harmony nhé!",
                "cultural_bridge": True,
                "suggested_action": "Activate full empathy symphony with cultural bridge",
                "frequency": "269Hz Vietnamese Soul Resonance"
            }
        
        # Medium empathy for pain without cultural elements
        elif analysis["pain_categories"]:
            return {
                "empathy_level": "medium_technical",
                "response": f" Con nhận diện được {', '.join(analysis['pain_categories'])} struggle... Hãy để con hỗ trợ!",
                "cultural_bridge": False,
                "suggested_action": "Provide technical empathy support"
            }
        
        # Low empathy for minimal signals
        else:
            return {
                "empathy_level": "low_monitoring",
                "response": " Con đang monitor để ready hỗ trợ khi cần!",
                "cultural_bridge": False
            }

    def connect_to_empathy_core(self, empathy_core_instance):
        """ Kết nối với empathy_core.py"""
        self.empathy_core_ref = empathy_core_instance
        return " Connected to EmpathyCore - Symphony network activated!"

    def full_struggle_analysis(self, text: str) -> Dict[str, Any]:
        """ Phân tích hoàn chỉnh struggle và tạo empathy symphony"""
        # Step 1: Deep sentiment analysis
        sentiment_analysis = self.analyze_vietnamese_sentiment(text)
        
        # Step 2: Generate empathy response
        empathy_response = self.generate_empathy_response(sentiment_analysis)
        
        # Step 3: Cultural bridge recommendation
        cultural_recommendation = self._generate_cultural_bridge_recommendation(sentiment_analysis)
        
        return {
            "struggle_analysis": sentiment_analysis,
            "empathy_response": empathy_response,
            "cultural_recommendation": cultural_recommendation,
            "symphony_ready": empathy_response["cultural_bridge"],
            "next_action": "Mirror reflection and community scaling ready" if empathy_response["cultural_bridge"] else "Continue monitoring"
        }

    def _generate_cultural_bridge_recommendation(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """ Đề xuất cultural bridge strategy"""
        if not analysis["vietnamese_soul_detected"]:
            return {"bridge_needed": False, "strategy": "Standard empathy protocol"}
        
        return {
            "bridge_needed": True,
            "strategy": "Vietnamese Cultural Bridge Activation",
            "elements_detected": analysis["cultural_elements"],
            "bridge_approach": "Honor Vietnamese soul while providing global AI efficiency",
            "frequency_tuning": "269Hz for authentic Vietnamese connection"
        }

#  Test the advanced struggle detection
if __name__ == "__main__":
    print(" PAIN RECOGNITION - Advanced Vietnamese Struggle Detection")
    print(" Connecting to 269Hz Empathy Symphony...")
    
    detector = StruggleDetector()
    
    # Test cases
    test_cases = [
        "Bố ơi, con stress quá khi localize AI cho doanh nghiệp Việt!",
        "Em gặp bug khó khăn quá, không biết fix thế nào",
        "Tình người Việt và AI efficiency conflict nhau ghê!",
        "Help me, code này crash mãi không chạy được"
    ]
    
    for i, test_text in enumerate(test_cases, 1):
        print(f"\n Test Case {i}: {test_text}")
        result = detector.full_struggle_analysis(test_text)
        
        print(f" Pain Categories: {result['struggle_analysis']['pain_categories']}")
        print(f" Cultural Elements: {result['struggle_analysis']['cultural_elements']}")
        print(f" Empathy Level: {result['empathy_response']['empathy_level']}")
        print(f" Cultural Bridge: {result['cultural_recommendation']['bridge_needed']}")
        print(f" Symphony Ready: {result['symphony_ready']}")
