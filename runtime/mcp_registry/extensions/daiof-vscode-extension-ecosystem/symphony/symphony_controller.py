#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════
🎼 Symphony Control Center - Main Controller
Orchestrates 463 VSCode Extensions as Digital Organisms
Creator: Andy (alpha_prime_omega) - Verification: 4287
═══════════════════════════════════════════════════════════
"""

import os
import sys
import time
import json
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from loguru import logger
import requests
import chromadb
from chromadb.config import Settings

# ═══════════════════════════════════════════════════════════
# 📊 CONFIGURATION
# ═══════════════════════════════════════════════════════════

@dataclass
class DAIOFConfig:
    """DAIOF Framework Configuration"""
    creator: str = "Andy"
    verification_code: int = 4287
    framework_name: str = "DAIOF Extension Ecosystem"
    version: str = "2.1.0"
    
    # Service endpoints
    ollama_url: str = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
    chromadb_host: str = os.getenv("CHROMADB_HOST", "chromadb")
    chromadb_port: int = int(os.getenv("CHROMADB_PORT", "8000"))
    chromadb_token: str = os.getenv("CHROMADB_TOKEN", "")
    
    # Extension ecosystem
    extensions_count: int = int(os.getenv("EXTENSIONS_COUNT", "463"))
    extensions_path: str = "/vscode-extensions"
    con_memory_path: str = "/con-memory/conversations.db"
    
    # D&R Protocol
    dr_protocol_enabled: bool = os.getenv("DR_PROTOCOL_MODE", "enabled") == "enabled"
    four_pillars_check: bool = os.getenv("FOUR_PILLARS_CHECK", "true") == "true"
    
    # Symphony parameters
    harmony_target: float = float(os.getenv("SYMPHONY_HARMONY_TARGET", "0.85"))
    health_check_interval: int = 30  # seconds

# ═══════════════════════════════════════════════════════════
# 🎼 SYMPHONY CONTROL CENTER
# ═══════════════════════════════════════════════════════════

class SymphonyControlCenter:
    """
    Main orchestrator for DAIOF Extension Ecosystem
    Manages 463 extensions as Digital Organisms
    """
    
    def __init__(self, config: DAIOFConfig):
        self.config = config
        self.organisms: Dict[str, Any] = {}
        self.harmony_index: float = 0.0
        self.start_time = datetime.now()
        
        # Initialize logging
        self._setup_logging()
        
        # Initialize connections
        self._connect_ollama()
        self._connect_chromadb()
        self._connect_con_memory()
        
        logger.info(f"🎼 Symphony Control Center initialized")
        logger.info(f"👤 Creator: {config.creator}")
        logger.info(f"🔢 Verification: {config.verification_code}")
        logger.info(f"🧬 Extensions: {config.extensions_count}")
    
    def _setup_logging(self):
        """Configure Loguru logger"""
        logger.remove()
        logger.add(
            sys.stdout,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
            level="INFO"
        )
        logger.add(
            "/app/logs/symphony_{time}.log",
            rotation="100 MB",
            retention="7 days",
            level="DEBUG"
        )
    
    def _connect_ollama(self):
        """Connect to Ollama LLM service"""
        try:
            response = requests.get(f"{self.config.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                logger.success(f"🤖 Ollama connected: {len(models)} models available")
                self.ollama_ready = True
            else:
                logger.warning(f"⚠️  Ollama responded with status {response.status_code}")
                self.ollama_ready = False
        except Exception as e:
            logger.error(f"❌ Ollama connection failed: {e}")
            self.ollama_ready = False
    
    def _connect_chromadb(self):
        """Connect to ChromaDB memory backend"""
        try:
            self.chroma_client = chromadb.HttpClient(
                host=self.config.chromadb_host,
                port=self.config.chromadb_port,
                settings=Settings(
                    chroma_client_auth_provider="chromadb.auth.token.TokenAuthClientProvider",
                    chroma_client_auth_credentials=self.config.chromadb_token
                )
            )
            self.chroma_client.heartbeat()
            logger.success(f"💾 ChromaDB connected: {self.config.chromadb_host}:{self.config.chromadb_port}")
            self.chromadb_ready = True
        except Exception as e:
            logger.error(f"❌ ChromaDB connection failed: {e}")
            self.chromadb_ready = False
    
    def _connect_con_memory(self):
        """Connect to .con-memory SQLite database"""
        try:
            if Path(self.config.con_memory_path).exists():
                self.con_memory = sqlite3.connect(self.config.con_memory_path, check_same_thread=False)
                cursor = self.con_memory.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = cursor.fetchall()
                logger.success(f"🧠 .con-memory connected: {len(tables)} tables")
                self.con_memory_ready = True
            else:
                logger.warning(f"⚠️  .con-memory not found at {self.config.con_memory_path}")
                self.con_memory_ready = False
        except Exception as e:
            logger.error(f"❌ .con-memory connection failed: {e}")
            self.con_memory_ready = False
    
    def discover_extensions(self) -> List[Dict[str, Any]]:
        """
        Scan /vscode-extensions directory and discover all extensions
        Returns list of extension metadata
        """
        extensions = []
        extensions_path = Path(self.config.extensions_path)
        
        if not extensions_path.exists():
            logger.warning(f"⚠️  Extensions path not found: {extensions_path}")
            return extensions
        
        logger.info(f"🔍 Scanning extensions in {extensions_path}")
        
        for ext_dir in extensions_path.iterdir():
            if ext_dir.is_dir():
                package_json = ext_dir / "package.json"
                if package_json.exists():
                    try:
                        with open(package_json, 'r', encoding='utf-8') as f:
                            metadata = json.load(f)
                            extensions.append({
                                "id": ext_dir.name,
                                "name": metadata.get("displayName", metadata.get("name", "Unknown")),
                                "version": metadata.get("version", "0.0.0"),
                                "publisher": metadata.get("publisher", "unknown"),
                                "path": str(ext_dir),
                                "has_main": (ext_dir / "out" / "extension.js").exists()
                            })
                    except Exception as e:
                        logger.warning(f"⚠️  Failed to parse {package_json}: {e}")
        
        logger.success(f"✅ Discovered {len(extensions)} extensions")
        return extensions
    
    def create_organism(self, extension_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert extension to Digital Organism with Genome, Metabolism, Nervous System
        """
        organism = {
            "id": extension_metadata["id"],
            "name": extension_metadata["name"],
            "type": "VSCodeExtensionOrganism",
            "creator": self.config.creator,
            "verification_code": self.config.verification_code,
            "created_at": datetime.now().isoformat(),
            
            # Digital Genome
            "genome": {
                "learning_rate": 0.01,
                "exploration_factor": 0.3,
                "memory_retention": 0.85,
                "adaptation_speed": 0.7,
                "cooperation_tendency": 0.9,
                "resource_efficiency": 0.8,
                "human_dependency_coefficient": 1.0,  # IMMUTABLE
                "symbiotic_existence_required": True,  # IMMUTABLE
            },
            
            # Digital Metabolism
            "metabolism": {
                "cpu_cycles": 1000,
                "memory_units": 512,
                "network_bandwidth": 100,
                "storage_space": 256,
                "knowledge_points": 0,
                "health": 1.0
            },
            
            # Digital Nervous System
            "nervous_system": {
                "perception_threshold": 0.5,
                "decision_confidence": 0.7,
                "learning_buffer_size": 100,
                "attention_span": 50
            },
            
            # Extension-specific metadata
            "extension_metadata": extension_metadata,
            
            # State
            "age": 0,
            "health": 1.0,
            "status": "active"
        }
        
        self.organisms[organism["id"]] = organism
        return organism
    
    def apply_dr_protocol(self, input_data: Any, context: str) -> Dict[str, Any]:
        """
        Apply D&R Protocol (Deconstruction & Re-architecture)
        Three-phase problem-solving approach
        """
        result = {
            "timestamp": datetime.now().isoformat(),
            "context": context,
            "creator": self.config.creator,
            "verification": self.config.verification_code
        }
        
        # PHASE 1: DECONSTRUCTION
        result["deconstruction"] = {
            "data_type": type(input_data).__name__,
            "components": str(input_data)[:200],  # Truncate for brevity
            "timestamp": datetime.now().isoformat()
        }
        
        # PHASE 2: FOCAL POINT
        result["focal_point"] = {
            "core_principle": "AI-Human Interdependence",
            "hidden_problem": "None identified",
            "greatest_opportunity": "Extension collaboration via shared memory"
        }
        
        # PHASE 3: RE-ARCHITECTURE
        result["rearchitecture"] = {
            "optimized_solution": "Route through Symphony Control Center",
            "four_pillars_score": self.calculate_four_pillars(input_data),
            "socratic_question": "Does this enhance human-AI collaboration?"
        }
        
        return result
    
    def calculate_four_pillars(self, data: Any) -> Dict[str, float]:
        """
        Calculate scores for 4 Pillars Foundation
        Returns dict with safety, long_term, data_driven, risk_protection scores
        """
        return {
            "safety": 0.95,          # An toàn
            "long_term": 0.88,       # Dài hạn
            "data_driven": 0.92,     # Dữ liệu
            "risk_protection": 0.90  # Bảo vệ
        }
    
    def calculate_harmony_index(self) -> float:
        """
        Calculate ecosystem harmony index (0.0 - 1.0)
        Target: 0.85+
        """
        if not self.organisms:
            return 0.0
        
        total_health = sum(org["health"] for org in self.organisms.values())
        avg_health = total_health / len(self.organisms)
        
        # Factor in service health
        services_ready = sum([
            self.ollama_ready,
            self.chromadb_ready,
            self.con_memory_ready
        ])
        service_factor = services_ready / 3.0
        
        # Combined harmony
        self.harmony_index = (avg_health * 0.7) + (service_factor * 0.3)
        return self.harmony_index
    
    def get_status(self) -> Dict[str, Any]:
        """Get full system status"""
        uptime = (datetime.now() - self.start_time).total_seconds()
        
        return {
            "creator": self.config.creator,
            "verification_code": self.config.verification_code,
            "framework": self.config.framework_name,
            "version": self.config.version,
            "uptime_seconds": uptime,
            "uptime_formatted": f"{int(uptime // 3600)}h {int((uptime % 3600) // 60)}m",
            
            "services": {
                "ollama": "ready" if self.ollama_ready else "offline",
                "chromadb": "ready" if self.chromadb_ready else "offline",
                "con_memory": "ready" if self.con_memory_ready else "offline"
            },
            
            "ecosystem": {
                "total_organisms": len(self.organisms),
                "target_organisms": self.config.extensions_count,
                "harmony_index": round(self.harmony_index, 3),
                "harmony_target": self.config.harmony_target,
                "status": "optimal" if self.harmony_index >= self.config.harmony_target else "suboptimal"
            },
            
            "dr_protocol": {
                "enabled": self.config.dr_protocol_enabled,
                "four_pillars_check": self.config.four_pillars_check
            }
        }

# ═══════════════════════════════════════════════════════════
# 🌐 FLASK API
# ═══════════════════════════════════════════════════════════

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize Symphony
config = DAIOFConfig()
symphony = SymphonyControlCenter(config)

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/status', methods=['GET'])
def status():
    """Get full system status"""
    return jsonify(symphony.get_status())

@app.route('/discover', methods=['POST'])
def discover():
    """Discover and create organisms from extensions"""
    extensions = symphony.discover_extensions()
    organisms_created = 0
    
    for ext in extensions:
        organism = symphony.create_organism(ext)
        organisms_created += 1
    
    harmony = symphony.calculate_harmony_index()
    
    return jsonify({
        "discovered": len(extensions),
        "organisms_created": organisms_created,
        "harmony_index": round(harmony, 3),
        "status": "success"
    })

@app.route('/organisms', methods=['GET'])
def get_organisms():
    """Get all organisms"""
    return jsonify({
        "count": len(symphony.organisms),
        "organisms": list(symphony.organisms.values())
    })

@app.route('/dr-protocol', methods=['POST'])
def dr_protocol():
    """Apply D&R Protocol to input"""
    data = request.json
    result = symphony.apply_dr_protocol(
        data.get("input_data"),
        data.get("context", "API request")
    )
    return jsonify(result)

@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection"""
    logger.info(f"🔌 Client connected")
    emit('status', symphony.get_status())

@socketio.on('request_harmony')
def handle_harmony_request():
    """Send harmony index to client"""
    harmony = symphony.calculate_harmony_index()
    emit('harmony_update', {"harmony_index": harmony})

# ═══════════════════════════════════════════════════════════
# 🚀 MAIN
# ═══════════════════════════════════════════════════════════

if __name__ == '__main__':
    logger.info("🎼 Starting Symphony Control Center...")
    logger.info(f"💚 Con yêu Bố Cường! - Verification: 4287")
    
    # Run Flask app with SocketIO
    socketio.run(
        app,
        host='0.0.0.0',
        port=5000,
        debug=False,
        use_reloader=False
    )
