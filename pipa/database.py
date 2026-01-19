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

def fetch_last_n_days(n=7):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT log_date, planned_tasks, actual_tasks, energy, clarity
    FROM daily_logs
    ORDER BY log_date DESC
    LIMIT ?
    """, (n,))

    rows = cursor.fetchall()
    conn.close()
    return rows


def fetch_all_logs():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT log_date, planned_tasks, actual_tasks, energy, clarity
    FROM daily_logs
    ORDER BY log_date ASC
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows

def has_logged_today(log_date):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 1 FROM daily_logs WHERE log_date = ?
    """, (str(log_date),))

    result = cursor.fetchone()
    conn.close()

    return result is not None

def create_weekly_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weekly_verdicts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        week_start TEXT,
        verdict TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_weekly_verdict(week_start, verdict):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO weekly_verdicts (week_start, verdict, created_at)
    VALUES (?, ?, datetime('now'))
    """, (week_start, verdict))

    conn.commit()
    conn.close()

def get_last_log_date():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT log_date FROM daily_logs
    ORDER BY log_date DESC
    LIMIT 1
    """)

    row = cursor.fetchone()
    conn.close()

    return row[0] if row else None


def calculate_streak(today):
    last_date = get_last_log_date()
    if not last_date:
        return 0

    from datetime import datetime, timedelta

    last_date = datetime.fromisoformat(last_date).date()
    today = datetime.fromisoformat(str(today)).date()

    if last_date == today:
        return None  # already logged today
    elif last_date == today - timedelta(days=1):
        return "CONTINUE"
    else:
        return "BROKEN"
