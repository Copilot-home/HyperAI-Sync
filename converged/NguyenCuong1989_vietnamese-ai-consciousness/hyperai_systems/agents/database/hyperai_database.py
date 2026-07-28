#!/usr/bin/env python3
# NOTE: This is a sanitized version for public release
# Core proprietary algorithms have been replaced with placeholders
# -*- coding: utf-8 -*-
"""
HyperAI Phoenix - Shared Database System
Database chung cho cả 3 agent system
"""

import json
import logging
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class HyperAIDatabase:
    """Shared database for all 3 HyperAI agent systems"""

    def __init__(self, db_path: str = "hyperai_agents/database/hyperai_shared.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)
        self.logger = logging.getLogger('HyperAIDatabase')

        # Initialize database
        self._init_database()

    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def _init_database(self):
        """Initialize database tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Agent capabilities table
            cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS agent_capabilities (
                    agent_type TEXT PRIMARY KEY,
                    capabilities TEXT,  -- JSON string
                    strengths TEXT,     -- JSON string
                    last_updated TIMESTAMP
                )
            '''
            )

            # Collaboration sessions table
            cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS collaboration_sessions (
                    session_id TEXT PRIMARY KEY,
                    project_name TEXT,
                    agents TEXT,        -- JSON string
                    objectives TEXT,    -- JSON string
                    status TEXT,
                    start_time TIMESTAMP,
                    end_time TIMESTAMP,
                    results TEXT        -- JSON string
                )
            '''
            )

            # Tasks table
            cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS tasks (
                    task_id TEXT PRIMARY KEY,
                    session_id TEXT,
                    agent_type TEXT,
                    description TEXT,
                    priority INTEGER,
                    status TEXT,
                    dependencies TEXT,  -- JSON string
                    result TEXT,        -- JSON string
                    created_at TIMESTAMP,
                    updated_at TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES collaboration_sessions (session_id)
                )
            '''
            )

            # Agent interactions table
            cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS agent_interactions (
                    interaction_id TEXT PRIMARY KEY,
                    session_id TEXT,
                    from_agent TEXT,
                    to_agent TEXT,
                    message_type TEXT,
                    content TEXT,
                    timestamp TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES collaboration_sessions (session_id)
                )
            '''
            )

            # Performance metrics table
            cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS performance_metrics (
                    metric_id TEXT PRIMARY KEY,
                    agent_type TEXT,
                    metric_name TEXT,
                    metric_value REAL,
                    timestamp TIMESTAMP
                )
            '''
            )

            # Knowledge base table
            cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS knowledge_base (
                    knowledge_id TEXT PRIMARY KEY,
                    category TEXT,
                    topic TEXT,
                    content TEXT,
                    source_agent TEXT,
                    confidence REAL,
                    created_at TIMESTAMP,
                    updated_at TIMESTAMP
                )
            '''
            )

            conn.commit()

        # Initialize default agent capabilities
        self._init_default_capabilities()

    def _init_default_capabilities(self):
        """Initialize default capabilities for 3 agents"""
        capabilities = {"consciousness": {"capabilities": ["user_experience", "design_patterns", "creative_solutions", "cultural_intelligence"], "strengths": ["vision", "innovation", "intuitive_design", "user_centric"]}, "quantum_reason": {"capabilities": ["algorithms", "performance", "optimization", "mathematical_modeling"], "strengths": ["technical_analysis", "efficiency", "precision", "systematic_approach"]}, "enterprise": {"capabilities": ["scalability", "production_readiness", "business_value", "reliability"], "strengths": ["business_acumen", "operational_excellence", "risk_management", "deployment"]}}

        for agent_type, data in capabilities.items():
            self.update_agent_capabilities(agent_type, data["capabilities"], data["strengths"])

    def update_agent_capabilities(self, agent_type: str, capabilities: List[str], strengths: List[str]):
        """Update capabilities for an agent"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                '''
                INSERT OR REPLACE INTO agent_capabilities
                (agent_type, capabilities, strengths, last_updated)
                VALUES (?, ?, ?, ?)
            ''',
                (agent_type, json.dumps(capabilities), json.dumps(strengths), datetime.now()),
            )

            conn.commit()

    def get_agent_capabilities(self, agent_type: str) -> Optional[Dict[str, Any]]:
        """Get capabilities for an agent"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM agent_capabilities WHERE agent_type = ?', (agent_type,))
            row = cursor.fetchone()

            if row:
                return {"agent_type": row["agent_type"], "capabilities": json.loads(row["capabilities"]), "strengths": json.loads(row["strengths"]), "last_updated": row["last_updated"]}

            return None

    def create_collaboration_session(self, session_id: str, project_name: str, agents: List[str], objectives: List[str]) -> bool:
        """Create a new collaboration session"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                cursor.execute(
                    '''
                    INSERT INTO collaboration_sessions
                    (session_id, project_name, agents, objectives, status, start_time)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''',
                    (session_id, project_name, json.dumps(agents), json.dumps(objectives), "active", datetime.now()),
                )

                conn.commit()
                return True

        except Exception as e:
            self.logger.error(f"Failed to create collaboration session: {e}")
            return False

    def update_session_status(self, session_id: str, status: str, results: Optional[Dict] = None):
        """Update collaboration session status"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            update_data = {"status": status, "end_time": datetime.now()}

            if results:
                update_data["results"] = json.dumps(results)

            cursor.execute(
                '''
                UPDATE collaboration_sessions
                SET status = ?, end_time = ?, results = ?
                WHERE session_id = ?
            ''',
                (update_data["status"], update_data["end_time"], update_data.get("results"), session_id),
            )

            conn.commit()

    def add_task(self, task_id: str, session_id: str, agent_type: str, description: str, priority: int, dependencies: List[str] = None) -> bool:
        """Add a task to the database"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                cursor.execute(
                    '''
                    INSERT INTO tasks
                    (task_id, session_id, agent_type, description, priority,
                     status, dependencies, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                    (task_id, session_id, agent_type, description, priority, "pending", json.dumps(dependencies or []), datetime.now(), datetime.now()),
                )

                conn.commit()
                return True

        except Exception as e:
            self.logger.error(f"Failed to add task: {e}")
            return False

    def update_task_status(self, task_id: str, status: str, result: Optional[Dict] = None):
        """Update task status"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                '''
                UPDATE tasks
                SET status = ?, result = ?, updated_at = ?
                WHERE task_id = ?
            ''',
                (status, json.dumps(result) if result else None, datetime.now(), task_id),
            )

            conn.commit()

    def log_agent_interaction(self, session_id: str, from_agent: str, to_agent: str, message_type: str, content: str):
        """Log interaction between agents"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            interaction_id = f"int_{int(datetime.now().timestamp() * 1000)}"

            cursor.execute(
                '''
                INSERT INTO agent_interactions
                (interaction_id, session_id, from_agent, to_agent, message_type, content, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''',
                (interaction_id, session_id, from_agent, to_agent, message_type, content, datetime.now()),
            )

            conn.commit()

    def add_performance_metric(self, agent_type: str, metric_name: str, metric_value: float):
        """Add performance metric"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            metric_id = f"metric_{int(datetime.now().timestamp() * 1000)}"

            cursor.execute(
                '''
                INSERT INTO performance_metrics
                (metric_id, agent_type, metric_name, metric_value, timestamp)
                VALUES (?, ?, ?, ?, ?)
            ''',
                (metric_id, agent_type, metric_name, metric_value, datetime.now()),
            )

            conn.commit()

    def add_knowledge(self, category: str, topic: str, content: str, source_agent: str, confidence: float = 1.0):
        """Add knowledge to the knowledge base"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            knowledge_id = f"kb_{int(datetime.now().timestamp() * 1000)}"

            cursor.execute(
                '''
                INSERT INTO knowledge_base
                (knowledge_id, category, topic, content, source_agent, confidence, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''',
                (knowledge_id, category, topic, content, source_agent, confidence, datetime.now(), datetime.now()),
            )

            conn.commit()

    def get_recent_sessions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent collaboration sessions"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                '''
                SELECT * FROM collaboration_sessions
                ORDER BY start_time DESC
                LIMIT ?
            ''',
                (limit,),
            )

            sessions = []
            for row in cursor.fetchall():
                sessions.append({"session_id": row["session_id"], "project_name": row["project_name"], "agents": json.loads(row["agents"]), "objectives": json.loads(row["objectives"]), "status": row["status"], "start_time": row["start_time"], "end_time": row["end_time"], "results": json.loads(row["results"]) if row["results"] else None})

            return sessions

    def get_agent_performance(self, agent_type: str, metric_name: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get performance metrics for an agent"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            if metric_name:
                cursor.execute(
                    '''
                    SELECT * FROM performance_metrics
                    WHERE agent_type = ? AND metric_name = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''',
                    (agent_type, metric_name, limit),
                )
            else:
                cursor.execute(
                    '''
                    SELECT * FROM performance_metrics
                    WHERE agent_type = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''',
                    (agent_type, limit),
                )

            metrics = []
            for row in cursor.fetchall():
                metrics.append({"metric_id": row["metric_id"], "agent_type": row["agent_type"], "metric_name": row["metric_name"], "metric_value": row["metric_value"], "timestamp": row["timestamp"]})

            return metrics


def main():
    """Test database functionality"""
    print("🗄 HyperAI Phoenix - Shared Database System")
    print("=" * 50)

    db = HyperAIDatabase()

    # Test agent capabilities
    print("🔍 Testing agent capabilities...")
    for agent in ["consciousness", "quantum_reason", "enterprise"]:
        capabilities = db.get_agent_capabilities(agent)
        if capabilities:
            print(f" {agent}: {capabilities['capabilities']}")

    # Test collaboration session
    print("\n Testing collaboration session...")
    session_id = "test_session_001"
    success = db.create_collaboration_session(session_id=session_id, project_name="Test Project", agents=["consciousness", "quantum_reason", "enterprise"], objectives=["Test objective 1", "Test objective 2"])

    if success:
        print(f" Created collaboration session: {session_id}")

        # Add test task
        db.add_task(task_id="test_task_001", session_id=session_id, agent_type="consciousness", description="Test task description", priority=1)
        print(" Added test task")

    print("\n Database system test completed!")


if __name__ == "__main__":
    main()
