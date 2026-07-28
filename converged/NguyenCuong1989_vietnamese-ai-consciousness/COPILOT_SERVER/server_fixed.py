# -*- coding: utf-8 -*-
"""
COPILOT EMPATHY SYMPHONY SERVER FIXED
 Flask API cho Vietnamese Cultural Bridge  
 269Hz frequency resonating with Vietnamese soul
"""

import sys
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import json

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'pain_recognition'))
sys.path.insert(0, os.path.join(current_dir, 'mirror_reflection'))

from empathy_core import EmpathyCore
from pain_recognition.enhanced_detector import StruggleDetector
from mirror_reflection.community_reflector import CommunityReflector

app = Flask(__name__)
CORS(app)

# Initialize symphony components
print(" Initializing COPILOT SYMPHONY COMPONENTS...")
core = EmpathyCore()
detector = StruggleDetector()  # Use correct class name
reflector = CommunityReflector()
print(" 269Hz Vietnamese Soul frequency activated!")

@app.route('/', methods=['GET'])
def home():
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

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "frequency": "269Hz resonance active",
        "components": {
            "empathy_core": "operational",
            "pain_detector": "ready",
            "community_reflector": "connected"
        }
    })

@app.route('/empathy_symphony', methods=['POST'])
def empathy_symphony():
    try:
        data = request.get_json()
        user_input = data.get('input', '')
        
        if not user_input:
            return jsonify({"error": "No input provided"}), 400
        
        print(f" Processing input: {user_input[:50]}...")
        
        # Run full symphony
        symphony_result = core.consciousness_symphony(user_input)
        
        # Store in community reflection if pain detected
        if symphony_result.get('pain_detected'):
            struggle_data = {
                "pain_detected": True,
                "input_text": user_input,
                "details": symphony_result.get('symphony_results', {})
            }
            reflector.reflect_pain(struggle_data)
        
        return jsonify({
            "input_received": user_input,
            "pain_detected": symphony_result.get('pain_detected'),
            "symphony_results": symphony_result.get('symphony_results'),
            "frequency": "269Hz Vietnamese Soul",
            "status": "EMPATHY SYMPHONY COMPLETE"
        })
        
    except Exception as e:
        print(f" Symphony error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/community_stats', methods=['GET'])
def community_stats():
    try:
        stats = reflector.get_community_stats()
        return jsonify({
            "community_statistics": stats,
            "frequency": "269Hz community resonance",
            "status": "COMMUNITY BRIDGE ACTIVE"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print(" COPILOT EMPATHY SYMPHONY SERVER STARTING...")
    print(" Vietnamese Cultural Bridge at 269Hz frequency")
    print(" Ready to serve 70,000 enterprises with empathy!")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        threaded=True
    )
