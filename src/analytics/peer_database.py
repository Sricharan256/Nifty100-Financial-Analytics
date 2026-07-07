"""
peer_database.py

Sprint 3 - Day 18

Creates peer_percentiles table
and stores computed rankings.
"""

import sqlite3
import pandas as pd

from src.analytics.peer import (
    merge_data,
    compute_peer_percentiles
)

DB_PATH = "db/nifty100.db"


# ---------------------------------------------------------
# Create Table
# ---------------------------------------------------------

def create_table(conn):

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS peer_percentiles (

            company_id TEXT,

            peer_group_name TEXT,

            metric TEXT,

            value REAL,

            percentile_rank REAL,

            year TEXT

        )
        """
    )

    conn.commit()


# ---------------------------------------------------------
# Save to SQLite
# ---------------------------------------------------------

def save_to_database(df):

    conn = sqlite3.connect(DB_PATH)

    create_table(conn)

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM peer_percentiles"
    )

    conn.commit()

    df.to_sql(

        "peer_percentiles",

        conn,

        if_exists="append",

        index=False

    )

    conn.close()


# ---------------------------------------------------------
# Verify
# ---------------------------------------------------------

def verify():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(

        """
        SELECT COUNT(*)
        FROM peer_percentiles
        """

    )

    rows = cursor.fetchone()[0]

    print()

    print("=" * 60)

    print("PEER_PERCENTILES TABLE")

    print("=" * 60)

    print(f"Rows Inserted : {rows}")

    cursor.execute(

        """
        SELECT *

        FROM peer_percentiles

        LIMIT 10
        """

    )

    result = cursor.fetchall()

    print()

    for row in result:

        print(row)

    conn.close()


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

if __name__ == "__main__":

    print("=" * 60)

    print("SPRINT 3 - DAY 18")

    print("STORE PEER PERCENTILES")

    print("=" * 60)

    merged = merge_data()

    peer_df = compute_peer_percentiles(merged)

    print()

    print(f"Generated Rows : {len(peer_df)}")

    save_to_database(peer_df)

    verify()

    print()