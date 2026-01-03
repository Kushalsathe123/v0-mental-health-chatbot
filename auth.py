import bcrypt
import sqlite3
from config import DATABASE_PATH

def hash_password(password):
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hash_value):
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode(), hash_value.encode())

def create_user(username, password, email=""):
    """Create new user"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    try:
        password_hash = hash_password(password)
        cursor.execute("""
            INSERT INTO users (username, password_hash, email)
            VALUES (?, ?, ?)
        """, (username, password_hash, email))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

def authenticate_user(username, password):
    """Authenticate user"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    
    if result and verify_password(password, result[1]):
        return result[0]
    return None

def get_user_language(user_id):
    """Get user's preferred language"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT preferred_language FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else "English"

def update_user_language(user_id, language):
    """Update user's preferred language"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET preferred_language = ? WHERE id = ?", (language, user_id))
    conn.commit()
    conn.close()
