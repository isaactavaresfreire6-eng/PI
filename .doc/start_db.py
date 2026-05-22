import sqlite3
import os
import hashlib

db_path = os.path.join(os.path.dirname(__file__), '../model/database.db')

def hash_password(password):
    salt = os.urandom(16).hex()
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 260000).hex()
    return f"{salt}${hashed}"

with sqlite3.connect(db_path) as conn:
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            power INTEGER NOT NULL CHECK(power BETWEEN 1 AND 9),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS storage_layout (
            id INTEGER PRIMARY KEY CHECK(id = 1),
            columns INTEGER NOT NULL DEFAULT 5,
            rows INTEGER NOT NULL DEFAULT 10
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS storage_sections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            letter TEXT NOT NULL UNIQUE CHECK(length(letter) = 1),
            keyword TEXT
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            categoria TEXT NOT NULL,
            descricao TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS storage_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            section TEXT NOT NULL CHECK(length(section) = 1),
            row INTEGER NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY (section) REFERENCES storage_sections(letter)
        )
    ''')

    conn.execute("INSERT OR IGNORE INTO storage_layout (id, columns, rows) VALUES (1, 5, 10)")

    for i in range(26):
        conn.execute("INSERT OR IGNORE INTO storage_sections (letter, keyword) VALUES (?, NULL)", (chr(65 + i),))

    conn.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ("sysop", hash_password("sysop")))
    row = conn.execute("SELECT id FROM users WHERE username = 'sysop'").fetchone()
    conn.execute("INSERT OR IGNORE INTO admin (user_id, power) VALUES (?, 9)", (row[0],))

    conn.commit()

print("Database initialized!")
