import os
import sqlite3
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DB_PATH = Path("data/academic.db")
SCHEMA_PATH = Path("data/sql/schema.sql")
SEED_PATH = Path("data/sql/seed.sql")


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db() -> None:
    reset_on_start = os.getenv("DB_RESET_ON_START", "false").lower() == "true"

    if reset_on_start and DB_PATH.exists():
        DB_PATH.unlink()

    conn = get_connection()

    # Create schema
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    conn.executescript(schema)

    # Always seed in dev mode
    if SEED_PATH.exists():
        seed = SEED_PATH.read_text(encoding="utf-8")
        conn.executescript(seed)

    conn.commit()
    conn.close()
