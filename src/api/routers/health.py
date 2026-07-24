import sqlite3
import time

from fastapi import APIRouter

router = APIRouter()

DB_PATH = "db/nifty100.db"

START_TIME = time.time()


@router.get("/health")
def health():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    tables = [
        "companies",
        "financial_ratios",
        "profit_loss",
        "balance_sheet",
        "cash_flow",
        "market_cap",
        "annual_reports",
        "peer_groups",
        "peer_percentiles",
        "sectors"
    ]

    counts = {}

    for table in tables:

        try:

            cursor.execute(f"SELECT COUNT(*) FROM {table}")

            counts[table] = cursor.fetchone()[0]

        except Exception:

            counts[table] = "Not Found"

    conn.close()

    return {

        "status": "ok",

        "version": "1.0.0",

        "uptime_seconds": round(time.time() - START_TIME, 2),

        "db_row_counts": counts

    }