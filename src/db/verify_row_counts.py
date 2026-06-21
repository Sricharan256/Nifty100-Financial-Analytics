"""
verify_row_counts.py

Verifies row counts in SQLite tables.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path("db/nifty100.db")


def verify_row_counts():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    tables = [
        "companies",
        "profit_loss",
        "balance_sheet",
        "cash_flow",
        "stock_prices",
        "analysis",
        "documents",
        "financial_ratios",
        "peer_groups",
        "pros_cons",
        "sectors",
        "market_cap"
    ]

    print("=" * 60)
    print("ROW COUNT VERIFICATION")
    print("=" * 60)

    for table in tables:

        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")

            count = cursor.fetchone()[0]

            print(f"{table:<20} : {count} rows")

        except Exception as e:

            print(f"{table:<20} : ERROR")
            print(e)

    conn.close()

    print("\nVerification Completed Successfully.")


if __name__ == "__main__":
    verify_row_counts()