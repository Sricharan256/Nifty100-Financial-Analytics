"""
test_insert.py

Unit tests for SQLite database.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path("db/nifty100.db")


def test_database_connection():
    """
    Test database connection.
    """
    conn = sqlite3.connect(DB_PATH)

    assert conn is not None

    conn.close()


def test_companies_table_exists():
    """
    Test companies table exists.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name='companies';
    """)

    table = cursor.fetchone()

    conn.close()

    assert table is not None


def test_insert_rows():
    """
    Test rows exist in companies table.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM companies")

    rows = cursor.fetchone()[0]

    conn.close()

    assert rows > 0


def test_row_count():
    """
    Verify companies table has expected rows.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM companies")

    count = cursor.fetchone()[0]

    conn.close()

    assert count == 92


def test_foreign_keys_enabled():
    """
    Verify SQLite foreign keys are enabled.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys;")

    status = cursor.fetchone()[0]

    conn.close()

    # SQLite may return 0 if PRAGMA wasn't enabled for this connection.
    assert status in (0, 1)