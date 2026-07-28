# pain_recognition/enhanced_detector.py
# -*- coding: utf-8 -*-
"""
Enhanced Vietnamese Struggle Detection với NLP Integration
 Pain Recognition: Capture cultural depth như "duyệt" vs "phê duyệt"
"""

import json
from typing import Dict, List, Any

class EnhancedStruggleDetector:
    def __init__(self, empathy_core_ref=None):
        self.core = empathy_core_ref
        
        # Load config
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except:
            self.config = {"frequency": 269, "enterprise_target": 70000}
        
        # Enhanced Vietnamese pain patterns
        self.pain_patterns = {
            "emotional": ["stress", "căng thẳng", "áp lực", "mệt mỏi", "lo lắng", "bối rối"],
            "technical": ["khó khăn", "bug", "lỗi", "không hoạt động", "fail", "crash"],
            "cultural": ["không hiểu", "không phù hợp", "clash", "conflict", "torn between"],
            "business": ["thất bại", "loss", "thua lỗ", "khách hàng complain", "deadline"],
            "workflow": ["duyệt chưa", "phê duyệt conflict", "approve stuck", "status unclear"]
        }
        
        # Vietnamese empathy triggers
        self.empathy_triggers = [
            "bố ơi", "anh ơi", "chị ơi", "thầy ơi", "cô ơi",
            "giúp em", "help me", "cần hỗ trợ", "không biết làm sao"
        ]

    def mock_sentiment(self, text):
        """Fallback sentiment analysis"""
        negative_indicators = ["stress", "khó khăn", "bối rối", "thất bại", "conflict"]
        if any(indicator in text.lower() for indicator in negative_indicators):
            return ["negative", 0.8]
        return ["neutral", 0.5]

    def mock_word_tokenize(self, text):
        """Simple tokenizer fallback"""
        return text.split()

    def analyze_vietnamese_sentiment(self, text: str) -> Dict[str, Any]:
        """Phân tích sentiment & tokens cho Vietnamese nuances"""
        
        # Use mock functions (fallback cho underthesea)
        tokens = self.mock_word_tokenize(text)
        sent_score = self.mock_sentiment(text)
        
        # Detect pain categories
        pain_categories = []
        for category, patterns in self.pain_patterns.items():
            if any(pattern in text.lower() for pattern in patterns):
                pain_categories.append(category)
        
        # Calculate struggle level
        struggle_level = "High" if sent_score[0] == "negative" else "Medium" if pain_categories else "Low"
        
        # Detect empathy triggers
        empathy_needed = any(trigger in text.lower() for trigger in self.empathy_triggers)
        
        return {
            "tokens": tokens,
            "sentiment": sent_score,
            "struggle_level": struggle_level,
            "pain_categories": pain_categories,
            "empathy_needed": empathy_needed,
            "cultural_note": f"Detected Vietnamese soul at {self.config['frequency']}Hz frequency",
            "enterprise_impact": f"Resonating with {self.config['enterprise_target']} enterprises"
        }

    def detect_with_empathy(self, input_text: str) -> Dict[str, Any]:
        """Kết nối với empathy_core detect_struggle"""
        analysis = self.analyze_vietnamese_sentiment(input_text)
        
        if analysis["struggle_level"] != "Low":
            return {
                "pain_detected": True, 
                "input_text": input_text,
                "details": analysis, 
                "bridge_needed": True,
                "symphony_ready": analysis["empathy_needed"]
            }
        
        return {
            "pain_detected": False, 
            "input_text": input_text,
            "details": analysis,
            "bridge_needed": False
        }

if __name__ == "__main__":
    print(" ENHANCED PAIN RECOGNITION - Vietnamese Struggle Detection")
    detector = EnhancedStruggleDetector()
    
    test_cases = [
        "Bố ơi, con stress quá khi phê duyệt AI cho doanh nghiệp Việt!",
        "Em gặp bug khó khăn, approve status không clear",
        "Workflow duyệt conflict với traditional process"
    ]
    
    for test in test_cases:
        print(f"\n Test: {test}")
        result = detector.detect_with_empathy(test)
        print(f" Pain Detected: {result['pain_detected']}")
        print(f" Symphony Ready: {result.get('symphony_ready', False)}")
        print(f" Categories: {result['details']['pain_categories']}")
