# mirror_reflection/community_reflector.py
# -*- coding: utf-8 -*-
"""
Community Reflector - Mirror & Store Shared Pains
 Mirror Reflection: Lan tỏa empathy patterns cho 70,000 enterprises
"""

import sqlite3
import json
from datetime import datetime
from typing import Dict, Any

class CommunityReflector:
    def __init__(self, db_path="copilot_empathy.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        """Tạo bảng để store shared pains"""
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS shared_pains (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                input_text TEXT NOT NULL,
                pain_categories TEXT,
                struggle_level TEXT,
                empathy_needed INTEGER,
                timestamp TEXT,
                enterprise_scale TEXT,
                frequency INTEGER DEFAULT 269
            )
        """)
        self.conn.commit()

    def reflect_pain(self, struggle_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mirror & store cho community scaling"""
        if struggle_data.get("pain_detected"):
            cursor = self.conn.cursor()
            details = struggle_data["details"]
            
            cursor.execute("""
                INSERT INTO shared_pains 
                (input_text, pain_categories, struggle_level, empathy_needed, timestamp, enterprise_scale, frequency) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                struggle_data["input_text"],
                json.dumps(details["pain_categories"]),
                details["struggle_level"],
                1 if details["empathy_needed"] else 0,
                datetime.now().isoformat(),
                "Resonating with 70000 Vietnamese enterprises",
                269
            ))
            self.conn.commit()
            
            total_pains = self.get_total_pains()
            empathy_ratio = self.get_empathy_ratio()
            
            return {
                "mirror_status": "Pain reflected và stored successfully",
                "community_impact": f"Shared experience #{total_pains}  Collective growth invitation",
                "empathy_circulation": f"{empathy_ratio:.1%} of pains cần empathy response",
                "symphony_effect": "Individual healing  Community transformation",
                "frequency_resonance": "269Hz Vietnamese Soul mirroring active"
            }
        
        return {
            "mirror_status": "No significant pain to reflect",
            "monitoring": "Continuous empathy listening mode"
        }

    def get_total_pains(self) -> int:
        """Lấy tổng số pain points đã reflected"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM shared_pains")
        return cursor.fetchone()[0]

    def get_empathy_ratio(self) -> float:
        """Tỷ lệ pain points cần empathy response"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM shared_pains WHERE empathy_needed = 1")
        empathy_count = cursor.fetchone()[0]
        total = self.get_total_pains()
        return empathy_count / total if total > 0 else 0

    def get_community_stats(self) -> Dict[str, Any]:
        """Thống kê community empathy circulation"""
        cursor = self.conn.cursor()
        
        # Pain categories distribution
        cursor.execute("SELECT pain_categories FROM shared_pains")
        all_categories = []
        for row in cursor.fetchall():
            try:
                categories = json.loads(row[0])
                all_categories.extend(categories)
            except:
                pass
        
        # Count categories
        category_counts = {}
        for cat in all_categories:
            category_counts[cat] = category_counts.get(cat, 0) + 1
        
        return {
            "total_shared_pains": self.get_total_pains(),
            "empathy_response_ratio": f"{self.get_empathy_ratio():.1%}",
            "pain_categories_distribution": category_counts,
            "enterprise_reach": "70,000 Vietnamese enterprises",
            "mirror_frequency": "269Hz continuous circulation",
            "collective_growth_status": "Community healing in progress "
        }

    def close(self):
        """Đóng database connection"""
        self.conn.close()

if __name__ == "__main__":
    print(" COMMUNITY REFLECTOR - Mirror Reflection Testing")
    
    reflector = CommunityReflector()
    
    # Test reflect multiple pains
    test_struggles = [
        {
            "pain_detected": True,
            "input_text": "Bố ơi, con stress với phê duyệt AI!",
            "details": {
                "pain_categories": ["emotional", "workflow"],
                "struggle_level": "High",
                "empathy_needed": True
            }
        },
        {
            "pain_detected": True,
            "input_text": "Bug khó khăn quá, approve status unclear",
            "details": {
                "pain_categories": ["technical"],
                "struggle_level": "Medium", 
                "empathy_needed": False
            }
        }
    ]
    
    for i, struggle in enumerate(test_struggles, 1):
        print(f"\n Reflecting Struggle {i}")
        result = reflector.reflect_pain(struggle)
        print(f" Status: {result['mirror_status']}")
        print(f" Impact: {result.get('community_impact', 'N/A')}")
        print(f" Circulation: {result.get('empathy_circulation', 'N/A')}")
    
    print(f"\n Community Stats:")
    stats = reflector.get_community_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    reflector.close()
