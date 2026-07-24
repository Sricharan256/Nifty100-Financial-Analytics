import sqlite3

DB_PATH = "db/nifty100.db"


def get_connection():
    """Return a SQLite database connection."""
    return sqlite3.connect(DB_PATH)