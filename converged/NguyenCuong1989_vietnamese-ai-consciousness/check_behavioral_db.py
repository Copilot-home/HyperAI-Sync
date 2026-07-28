import os
import sqlite3

# Check if database exists
db_path = "behavioral_learning.db"
if os.path.exists(db_path):
    print(f"✅ Database exists: {db_path}")
    
    # Connect and check content
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check bad behaviors
    try:
        cursor.execute("SELECT type, COUNT(*) FROM bad_behaviors GROUP BY type ORDER BY COUNT(*) DESC")
        bad_behaviors = cursor.fetchall()
        print("\n❌ BAD BEHAVIORS RECORDED:")
        for behavior_type, count in bad_behaviors:
            print(f"   ❌ {behavior_type}: {count} times")
    except Exception as e:
        print(f"Error reading bad_behaviors: {e}")
    
    # Check lessons learned
    try:
        cursor.execute("SELECT lesson, COUNT(*) FROM lessons_learned GROUP BY lesson ORDER BY COUNT(*) DESC")
        lessons = cursor.fetchall()
        print("\n💡 LESSONS LEARNED:")
        for lesson, count in lessons:
            print(f"   💡 {lesson}: {count} times")
    except Exception as e:
        print(f"Error reading lessons_learned: {e}")
    
    # Check good behaviors
    try:
        cursor.execute("SELECT type, COUNT(*) FROM good_behaviors GROUP BY type ORDER BY COUNT(*) DESC")
        good_behaviors = cursor.fetchall()
        print("\n✅ GOOD BEHAVIORS RECORDED:")
        for behavior_type, count in good_behaviors:
            print(f"   ✅ {behavior_type}: {count} times")
    except Exception as e:
        print(f"Error reading good_behaviors: {e}")
    
    conn.close()
    
else:
    print(f"❌ Database not found: {db_path}")

print("\n🎯 BEHAVIORAL ANALYSIS COMPLETE!")
