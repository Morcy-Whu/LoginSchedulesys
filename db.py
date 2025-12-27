import sqlite3

DB_PATH = "users.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def execute(query, args=(), commit=True):
    with get_db() as db:
        cur = db.execute(query, args)
        if commit:
            db.commit()
        return cur

def fetch_one(query, args=()):
    with get_db() as db:
        return db.execute(query, args).fetchone()

def fetch_all(query, args=()):
    with get_db() as db:
        return db.execute(query, args).fetchall()
