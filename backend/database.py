import sqlite3
import os
from contextlib import contextmanager
from config import DATABASE_URL


def init_db():
    """Create leads table if it doesn't exist."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                name            TEXT NOT NULL,
                email           TEXT NOT NULL,
                phone           TEXT,
                message         TEXT NOT NULL,
                source          TEXT,
                classification  TEXT,
                suggested_reply TEXT,
                contacted       INTEGER DEFAULT 0,
                created_at      TEXT DEFAULT (datetime('now'))
            )
        """)
        conn.commit()


@contextmanager
def get_connection():
    """Yield a SQLite connection and auto-close after use."""
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row  # allows dict-like row access: row["name"]
    try:
        yield conn
    finally:
        conn.close()