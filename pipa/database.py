import sqlite3
from datetime import datetime

DB_NAME = "pipa.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS daily_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        log_date TEXT UNIQUE,
        planned_tasks TEXT,
        actual_tasks TEXT,
        energy INTEGER,
        clarity INTEGER,
        reflection TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_daily_log(
    log_date,
    planned_tasks,
    actual_tasks,
    energy,
    clarity,
    reflection
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO daily_logs (
        log_date,
        planned_tasks,
        actual_tasks,
        energy,
        clarity,
        reflection,
        created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        str(log_date),
        planned_tasks,
        actual_tasks,
        energy,
        clarity,
        reflection,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()
