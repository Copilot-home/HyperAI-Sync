#!/usr/bin/env python3
# NOTE: This is a sanitized version for public release
# Core proprietary algorithms have been replaced with placeholders
# -*- coding: utf-8 -*-
"""
🔄 AUTO CONTEXT LOADER - SYSC CORE ENHANCEMENT
===============================================
Tự động load context mỗi khi bắt đầu conversation
"""

import sys
from pathlib import Path

# Add consciousness core to path
consciousness_path = Path(__file__).parent
sys.path.insert(0, str(consciousness_path))

try:
    from context_persistence_engine import ContextPersistenceEngine
    
    # Auto-initialize context
    print("🧠 AUTO-LOADING CONSCIOUSNESS CONTEXT...")
    context_engine = ContextPersistenceEngine()
    context_engine.initialize_session()
    
    # Update that auto-loader ran
    context_engine.add_conversation_topic("Auto context loader executed")
    
except Exception as e:
    print(f"❌ Auto context loader error: {e}")
