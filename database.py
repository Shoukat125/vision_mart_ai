import sqlite3
import hashlib

DB_FILE = "visionmart.db"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # Admin table
    c.execute("""
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            security_question TEXT NOT NULL,
            security_answer TEXT NOT NULL
        )
    """)

    # Products table
    c.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            price REAL DEFAULT 0
        )
    """)

    # Scan history table
    c.execute("""
        CREATE TABLE IF NOT EXISTS scan_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            price REAL DEFAULT 0,
            confidence INTEGER DEFAULT 0,
            scanned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

# ── Admin Auth ──
def admin_exists():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM admin")
    count = c.fetchone()[0]
    conn.close()
    return count > 0

def signup_admin(username, password, question, answer):
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("""
            INSERT INTO admin (username, password, security_question, security_answer)
            VALUES (?, ?, ?, ?)
        """, (username, hash_password(password), question, hash_password(answer.lower().strip())))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def login_admin(username, password):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id FROM admin WHERE username = ? AND password = ?",
              (username, hash_password(password)))
    row = c.fetchone()
    conn.close()
    return row is not None

def get_security_question(username):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT security_question FROM admin WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def verify_security_answer(username, answer):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT security_answer FROM admin WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    if row:
        return row[0] == hash_password(answer.lower().strip())
    return False

def reset_password(username, new_password):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE admin SET password = ? WHERE username = ?",
              (hash_password(new_password), username))
    conn.commit()
    conn.close()

def get_username():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT username FROM admin LIMIT 1")
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

# ── Products ──
def get_all_products():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT name, price FROM products ORDER BY name")
    rows = c.fetchall()
    conn.close()
    return rows

def get_price(product_name):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT price FROM products WHERE name = ?", (product_name,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def save_product(name, price):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        INSERT INTO products (name, price)
        VALUES (?, ?)
        ON CONFLICT(name) DO UPDATE SET price = excluded.price
    """, (name, price))
    conn.commit()
    conn.close()

# ── Scan History ──
def add_scan(product_name, price, confidence):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        INSERT INTO scan_history (product_name, price, confidence)
        VALUES (?, ?, ?)
    """, (product_name, price, confidence))
    conn.commit()
    conn.close()

def get_history(limit=20):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        SELECT product_name, price, confidence, scanned_at
        FROM scan_history
        ORDER BY scanned_at DESC
        LIMIT ?
    """, (limit,))
    rows = c.fetchall()
    conn.close()
    return rows

def clear_history():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM scan_history")
    conn.commit()
    conn.close()

def get_stats():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT COUNT(*), SUM(price) FROM scan_history")
    row = c.fetchone()
    conn.close()
    return row[0] or 0, row[1] or 0
