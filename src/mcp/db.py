import sqlite3
from pathlib import Path

DB_PATH = Path("data/academic.db")
SCHEMA_PATH = Path("data/schema.sql")
SEED = Path("data/seed.sql")


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db() -> None:
    conn = get_connection()
    cur = conn.cursor()
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    conn.executescript(schema)
    cur.execute("SELECT COUNT(*) FROM student")
    count = cur.fetchone()[0]
    if count == 0:
        seed = SEED.read_text(encoding="utf-8")
        conn.executescript(seed)
    conn.commit()
    conn.close()
