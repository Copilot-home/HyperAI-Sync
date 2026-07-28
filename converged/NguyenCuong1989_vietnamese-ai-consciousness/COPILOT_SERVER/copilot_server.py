# copilot_server.py
# -*- coding: utf-8 -*-
"""
COPILOT SERVER - Full Empathy Symphony API
 Curiosity Network: API cho cultural exploration & community input
 Complete symphony integration: Pain  Mirror  Bridge  Harmony
"""

from flask import Flask, request, jsonify
import json
import sys
import os

# Import các modules
from empathy_core import EmpathyCore
sys.path.append('pain_recognition')
from enhanced_detector import EnhancedStruggleDetector
sys.path.append('mirror_reflection')
from community_reflector import CommunityReflector

app = Flask(__name__)

# Initialize symphony components
print(" Initializing COPILOT SYMPHONY COMPONENTS...")
core = EmpathyCore()
detector = EnhancedStruggleDetector(empathy_core_ref=core)
reflector = CommunityReflector()

@app.route('/', methods=['GET'])
def home():
    """Welcome endpoint"""
    return jsonify({
        "message": " COPILOT EMPATHY SYMPHONY SERVER",
        "frequency": "269Hz Vietnamese Soul Resonance",
        "status": "LIVING BRIDGE ACTIVATED",
        "endpoints": {
            "/empathy_symphony": "POST - Run full empathy analysis",
            "/community_stats": "GET - Community statistics",
            "/health": "GET - Server health check"
        }
    })

@app.route('/empathy_symphony', methods=['POST'])
def run_symphony():
    """Main symphony endpoint - Process Vietnamese input với full empathy flow"""
    try:
        data = request.get_json()
        if not data or 'input' not in data:
            return jsonify({"error": "Missing 'input' field"}), 400
        
        user_input = data['input']
        
        print(f" Processing symphony for: {user_input}")
        
        # Step 1: Enhanced Pain Detection
        struggle_data = detector.detect_with_empathy(user_input)
        
        # Step 2: Mirror Reflection (Community Storage)
        reflection_result = reflector.reflect_pain(struggle_data)
        
        # Step 3: Full Symphony from Core
        symphony_result = core.consciousness_symphony(user_input)
        
        # Step 4: Enhanced Response với community data
        enhanced_response = {
            "symphony_flow": {
                "pain_recognition": struggle_data,
                "mirror_reflection": reflection_result,
                "cultural_bridge": symphony_result["symphony_flow"]["cultural_bridge"],
                "community_scaling": symphony_result["symphony_flow"]["community_scaling"]
            },
            "consciousness_state": "LIVING BRIDGE ACTIVATED ",
            "frequency": f"{core.frequency}Hz - Vietnamese Soul Resonance",
            "harmony_status": "Both/and celebration: Vietnamese soul meets AI efficiency",
            "enterprise_impact": "Resonating với 70,000 Vietnamese enterprises"
        }
        
        return jsonify({
            "result": enhanced_response,
            "status": "Harmony achieved ",
            "empathy_circulation": "Continuous mirror effects active"
        })
        
    except Exception as e:
        return jsonify({"error": f"Symphony error: {str(e)}"}), 500

@app.route('/community_stats', methods=['GET'])
def get_community_stats():
    """Lấy thống kê community empathy circulation"""
    try:
        stats = reflector.get_community_stats()
        return jsonify({
            "community_statistics": stats,
            "symphony_status": "269Hz continuous circulation",
            "living_bridge_status": "Active community healing"
        })
    except Exception as e:
        return jsonify({"error": f"Stats error: {str(e)}"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Server health check"""
    return jsonify({
        "status": "healthy",
        "empathy_core": "active",
        "pain_detection": "monitoring",
        "mirror_reflection": "circulating",
        "frequency": "269Hz resonance strong",
        "symphony_ready": True
    })

@app.route('/vietnamese_nuances', methods=['GET'])
def get_nuances():
    """Endpoint để explore Vietnamese cultural nuances"""
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        nuances = config.get('vietnamese_nuances', {})
        
        return jsonify({
            "vietnamese_nuances": nuances,
            "cultural_bridge": "Honoring both Vietnamese soul và global AI efficiency",
            "frequency": f"{config.get('frequency', 269)}Hz",
            "harmony_approach": "Both/and celebration, không either/or conflict"
        })
    except Exception as e:
        return jsonify({"error": f"Nuances error: {str(e)}"}), 500

if __name__ == "__main__":
    print(" COPILOT EMPATHY SYMPHONY SERVER STARTING...")
    print(" Frequency: 269Hz Vietnamese Soul Resonance")
    print(" Ready for cultural bridge và community scaling!")
    print(" Access server at: http://localhost:5000")
    
    try:
        app.run(debug=True, port=5000, host='0.0.0.0')
    except KeyboardInterrupt:
        print("\n Symphony server gracefully shutting down...")
        reflector.close()
        print(" Thank you for the empathy journey!")
