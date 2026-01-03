import sqlite3
from datetime import datetime
from config import DATABASE_PATH
import os

def init_database():
    """Initialize database with required tables"""
    os.makedirs(os.path.dirname(DATABASE_PATH) or ".", exist_ok=True)
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT UNIQUE,
            preferred_language TEXT DEFAULT 'English',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Chat history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            response TEXT NOT NULL,
            language TEXT DEFAULT 'en',
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    # Mood tracking table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mood_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            mood TEXT NOT NULL,
            intensity INTEGER CHECK(intensity >= 1 AND intensity <= 10),
            notes TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    # Crisis alerts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS crisis_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            trigger_message TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    # Therapy progress table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS therapy_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            module_name TEXT NOT NULL,
            completion_percentage INTEGER DEFAULT 0,
            last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    conn.commit()
    conn.close()

def get_user_id(username):
    """Get user ID by username"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def save_chat_message(user_id, message, response, language="en"):
    """Save chat message and response"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO chat_history (user_id, message, response, language)
        VALUES (?, ?, ?, ?)
    """, (user_id, message, response, language))
    conn.commit()
    conn.close()

def save_mood_log(user_id, mood, intensity, notes=""):
    """Save mood log"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO mood_logs (user_id, mood, intensity, notes)
        VALUES (?, ?, ?, ?)
    """, (user_id, mood, intensity, notes))
    conn.commit()
    conn.close()

def get_mood_history(user_id, limit=30):
    """Get user's mood history"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT mood, intensity, timestamp FROM mood_logs
        WHERE user_id = ?
        ORDER BY timestamp DESC
        LIMIT ?
    """, (user_id, limit))
    results = cursor.fetchall()
    conn.close()
    return results

def log_crisis_alert(user_id, trigger_message):
    """Log a potential crisis alert"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO crisis_alerts (user_id, trigger_message)
        VALUES (?, ?)
    """, (user_id, trigger_message))
    conn.commit()
    conn.close()

def get_therapy_progress(user_id, module_name):
    """Get therapy module progress"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT completion_percentage FROM therapy_progress
        WHERE user_id = ? AND module_name = ?
    """, (user_id, module_name))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0

def update_therapy_progress(user_id, module_name, completion_percentage):
    """Update therapy module progress"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Check if record exists
    cursor.execute("""
        SELECT id FROM therapy_progress
        WHERE user_id = ? AND module_name = ?
    """, (user_id, module_name))
    
    if cursor.fetchone():
        cursor.execute("""
            UPDATE therapy_progress
            SET completion_percentage = ?, last_accessed = CURRENT_TIMESTAMP
            WHERE user_id = ? AND module_name = ?
        """, (completion_percentage, user_id, module_name))
    else:
        cursor.execute("""
            INSERT INTO therapy_progress (user_id, module_name, completion_percentage)
            VALUES (?, ?, ?)
        """, (user_id, module_name, completion_percentage))
    
    conn.commit()
    conn.close()
