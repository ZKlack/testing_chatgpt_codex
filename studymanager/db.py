import sqlite3
from pathlib import Path
from datetime import date, timedelta
from .config import load_config

DB_FILE = Path('studymanager.db')

SCHEMA = '''
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT,
    file_path TEXT,
    question TEXT,
    question_file TEXT,
    course TEXT,
    chapter TEXT,
    max_cooldown INTEGER,
    due_date DATE,
    created_at DATE
);
'''

def connect():
    conn = sqlite3.connect(DB_FILE)
    return conn


def init_db():
    conn = connect()
    conn.execute(SCHEMA)
    conn.commit()
    conn.close()


def compute_due_date(start: date, cooldown: int, off_days=None) -> date:
    if off_days is None:
        off_days = []
    current = start
    added = 0
    while added < cooldown:
        current += timedelta(days=1)
        if current.weekday() not in off_days:
            added += 1
    return current


def add_note(content=None, file_path=None, question=None, question_file=None,
             course=None, chapter=None, max_cooldown=1):
    cfg = load_config()
    off_days = cfg.get('off_days', [])
    due = compute_due_date(date.today(), max_cooldown, off_days)
    conn = connect()
    conn.execute(
        'INSERT INTO notes (content, file_path, question, question_file, course, chapter, max_cooldown, due_date, created_at) '
        'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
        (content, file_path, question, question_file, course, chapter, max_cooldown, due.isoformat(), date.today().isoformat())
    )
    conn.commit()
    conn.close()


def fetch_due_notes():
    conn = connect()
    cur = conn.execute('SELECT * FROM notes WHERE due_date <= ?', (date.today().isoformat(),))
    rows = cur.fetchall()
    conn.close()
    return rows


def update_cooldown(note_id: int, new_cooldown: int):
    cfg = load_config()
    off_days = cfg.get('off_days', [])
    new_due = compute_due_date(date.today(), new_cooldown, off_days)
    conn = connect()
    conn.execute('UPDATE notes SET max_cooldown = ?, due_date = ? WHERE id = ?',
                 (new_cooldown, new_due.isoformat(), note_id))
    conn.commit()
    conn.close()

