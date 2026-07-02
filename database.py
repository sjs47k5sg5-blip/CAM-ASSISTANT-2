import sqlite3

def init_db():
 c=sqlite3.connect('cnc_assistant.db');c.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY,telegram_id INTEGER UNIQUE,username TEXT,first_name TEXT)');c.commit();c.close()

def register_user(t,u,f):
 c=sqlite3.connect('cnc_assistant.db');c.execute('INSERT OR IGNORE INTO users(telegram_id,username,first_name) VALUES(?,?,?)',(t,u,f));c.commit();c.close()
