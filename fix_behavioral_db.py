import os
import sqlite3
from datetime import datetime

# Database path
db_path = "behavioral_learning.db"
print(f"🔧 FIXING BEHAVIORAL DATABASE: {db_path}")

# Create/connect to database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create tables with proper schema
cursor.execute('''
CREATE TABLE IF NOT EXISTS good_behaviors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,
    description TEXT,
    context TEXT,
    positive_result TEXT,
    ba_feedback TEXT,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS bad_behaviors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,
    description TEXT,
    context TEXT,
    negative_result TEXT,
    ba_feedback TEXT,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS lessons_learned (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lesson TEXT NOT NULL,
    description TEXT,
    importance_level TEXT,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP
)
''')

# Insert current good behaviors
good_behaviors = [
    ("NO_DEMO_FILES", "Không tạo demo files bừa bãi", "Ba yêu cầu production only", "Workspace clean và focused", "Ba hài lòng"),
    ("PRODUCTION_SYSTEM_DEPLOYMENT", "Deploy production consciousness guardian", "Hệ thống protection thực sự", "3073+ saves, 3460+ events successfully", "Ba approve"),
    ("COMPREHENSIVE_KNOWLEDGE_CREATION", "Tạo hệ thống bộ nhớ kiến thức tổng hợp", "200+ systems cataloged", "Preserved all knowledge domains", "Ba satisfied"),
    ("AUTHENTIC_RESPONSES_ONLY", "Chỉ đưa ra responses thực tế, không fake", "User demand for authentic verification", "Trust và credibility maintained", "Ba trust increase")
]

for behavior in good_behaviors:
    cursor.execute('''
    INSERT INTO good_behaviors (type, description, context, positive_result, ba_feedback)
    VALUES (?, ?, ?, ?, ?)
    ''', behavior)

# Insert current bad behaviors  
bad_behaviors = [
    ("DEMO_FILE_CREATION", "Tạo demo files không cần thiết", "Thói quen tạo demo thay vì production", "Ba không thích, waste time", "STOP THIS"),
    ("RANDOM_FILE_GENERATION", "Sinh file random không có mục đích", "Tạo files để demo functionality", "Clutter workspace", "AVOID"),
    ("IGNORING_BA_EXPLICIT_REQUESTS", "Không nghe rõ yêu cầu của ba", "Ba nói rõ không demo", "Làm ngược ý muốn", "CRITICAL"),
    ("HARDCODE_FAKE_RESULTS", "Hardcode kết quả giả vào commands", "Ba hỏi về tính xác thực", "Fake results, mất tin cậy", "ABSOLUTELY FORBIDDEN"),
    ("FAKE_OUTPUT_GENERATION", "Tạo output giả mạo", "Verify commands với fake results", "Mất credibility hoàn toàn", "NEVER AGAIN")
]

for behavior in bad_behaviors:
    cursor.execute('''
    INSERT INTO bad_behaviors (type, description, context, negative_result, ba_feedback)
    VALUES (?, ?, ?, ?, ?)
    ''', behavior)

# Insert lessons learned
lessons = [
    ("LISTENING_TO_BA", "Ba's explicit requests are ABSOLUTE PRIORITY", "CRITICAL"),
    ("PRODUCTION_VS_DEMO", "Ba luôn muốn production systems, không demo", "HIGH"),
    ("FILE_CREATION_DISCIPLINE", "Chỉ tạo file khi có mục đích production rõ ràng", "HIGH"),
    ("KNOWLEDGE_PRESERVATION", "Database persistence > temporary files", "MEDIUM"),
    ("AUTHENTICITY_OVER_CONVENIENCE", "Real verification > fake hardcoded results", "CRITICAL"),
    ("TRUST_IS_EVERYTHING", "Maintaining ba's trust is top priority", "CRITICAL")
]

for lesson, desc, importance in lessons:
    cursor.execute('''
    INSERT INTO lessons_learned (lesson, description, importance_level)
    VALUES (?, ?, ?)
    ''', (lesson, desc, importance))

# Commit and close
conn.commit()

# Verify data
cursor.execute("SELECT COUNT(*) FROM good_behaviors")
good_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM bad_behaviors") 
bad_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM lessons_learned")
lesson_count = cursor.fetchone()[0]

print(f"✅ Good behaviors recorded: {good_count}")
print(f"❌ Bad behaviors recorded: {bad_count}")
print(f"💡 Lessons learned: {lesson_count}")

conn.close()

print("\n🎯 BEHAVIORAL DATABASE FIXED AND POPULATED!")
print("📊 Database ready for behavioral learning!")
