import sqlite3
from pathlib import Path
DB_FILE=Path("cnc_assistant.db")
def get_connection():
    return sqlite3.connect(DB_FILE)
def init_db():
    conn=get_connection()
    cur=conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER UNIQUE,
        username TEXT,
        first_name TEXT,
        registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit(); conn.close()
def register_user(tid, username, first_name):
    conn=get_connection()
    cur=conn.cursor()
    cur.execute("INSERT OR IGNORE INTO users(telegram_id,username,first_name) VALUES(?,?,?)",(tid,username,first_name))
    conn.commit(); conn.close()
