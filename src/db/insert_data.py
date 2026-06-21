"""
insert_data.py

Loads validated Excel data into SQLite database
and generates a load audit report.
"""

import sqlite3
from pathlib import Path
import pandas as pd
from datetime import datetime

from src.etl.loader import load_excel


DB_PATH = Path("db/nifty100.db")

# Audit log
audit_log = []


def get_connection():
    """Create SQLite connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def insert_dataframe(df, table_name, file_name):
    """Insert DataFrame into SQLite table."""

    conn = get_connection()

    try:
        # Replace the table with DataFrame schema
        df.to_sql(
            table_name,
            conn,
            if_exists="replace",
            index=False
        )

        conn.commit()

        print(f"{len(df)} rows inserted into '{table_name}' successfully.")

        audit_log.append({
            "File": file_name,
            "Table": table_name,
            "Rows Loaded": len(df),
            "Status": "Success",
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    except Exception as e:

        print(f"\nError inserting into {table_name}")
        print(e)

        audit_log.append({
            "File": file_name,
            "Table": table_name,
            "Rows Loaded": 0,
            "Status": "Failed",
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    finally:
        conn.close()


def load_dataset(file_name, table_name):
    """Load Excel dataset."""

    print(f"\nLoading {file_name}...")

    df = load_excel(file_name)

    if df is None:

        print(f"Failed to load {file_name}")

        audit_log.append({
            "File": file_name,
            "Table": table_name,
            "Rows Loaded": 0,
            "Status": "Failed",
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        return

    insert_dataframe(df, table_name, file_name)


def save_audit_report():
    """Save load audit report."""

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    audit_df = pd.DataFrame(audit_log)

    audit_df.to_csv(
        output_dir / "load_audit.csv",
        index=False
    )

    print("\nLoad Audit Report Generated Successfully!")
    print("Location : output/load_audit.csv")


if __name__ == "__main__":

    print("=" * 60)
    print("NIFTY 100 ETL - SQLite Data Loading")
    print("=" * 60)

    datasets = [
        ("companies.xlsx", "companies"),
        ("profitandloss.xlsx", "profit_loss"),
        ("balancesheet.xlsx", "balance_sheet"),
        ("cashflow.xlsx", "cash_flow"),
        ("stock_prices.xlsx", "stock_prices"),
        ("analysis.xlsx", "analysis"),
        ("documents.xlsx", "documents"),
        ("financial_ratios.xlsx", "financial_ratios"),
        ("peer_groups.xlsx", "peer_groups"),
        ("prosandcons.xlsx", "pros_cons"),
        ("sectors.xlsx", "sectors"),
        ("market_cap.xlsx", "market_cap")
    ]

    for file_name, table_name in datasets:
        load_dataset(file_name, table_name)

    save_audit_report()

    print("\nAll datasets loaded successfully.")