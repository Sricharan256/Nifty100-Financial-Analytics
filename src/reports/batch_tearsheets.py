import os
import sqlite3
import pandas as pd

from tearsheet import build_tearsheet

# ----------------------------------------
# Configuration
# ----------------------------------------

DB_PATH = "db/nifty100.db"

OUTPUT_DIR = "output"

REPORT_DIR = "reports/tearsheets"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

conn = sqlite3.connect(DB_PATH)

# ----------------------------------------
# Load Companies
# ----------------------------------------

companies = pd.read_sql(
    """
    SELECT
        id,
        company_name
    FROM companies
    ORDER BY company_name
    """,
    conn
)

print("Companies Found :", len(companies))

# ----------------------------------------
# Batch Generation
# ----------------------------------------

skipped = []

generated = 0

for _, row in companies.iterrows():

    ticker = row["id"]
    company = row["company_name"]

    years = pd.read_sql(
        """
        SELECT DISTINCT year
        FROM profit_loss
        WHERE company_id=?
        """,
        conn,
        params=[ticker]
    )

    if len(years) < 3:

        skipped.append(
            {
                "ticker": ticker,
                "company": company,
                "reason": "Less than 3 years data"
            }
        )

        continue

    try:

        print(f"Generating {ticker}")

        build_tearsheet(
            company,
            ticker
        )

        generated += 1

    except Exception as e:

        skipped.append(
            {
                "ticker": ticker,
                "company": company,
                "reason": str(e)
            }
        )

# ----------------------------------------
# Save Skipped Companies
# ----------------------------------------

pd.DataFrame(skipped).to_csv(
    "output/skipped_tearsheets.csv",
    index=False
)

print()

print("Generated :", generated)

print("Skipped :", len(skipped))

conn.close()