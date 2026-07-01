"""
generate_capital_allocation.py

Generates capital_allocation.csv from SQLite database.
"""

import sqlite3
import pandas as pd
from pathlib import Path

from src.analytics.cashflow_kpis import capital_allocation_pattern


DB_PATH = "db/nifty100.db"


def main():

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT
        company_id,
        year,
        operating_activity,
        investing_activity,
        financing_activity
    FROM cash_flow
    """

    df = pd.read_sql(query, conn)

    conn.close()

    # Determine signs
    df["cfo_sign"] = df["operating_activity"].apply(
        lambda x: "+" if x > 0 else "-"
    )

    df["cfi_sign"] = df["investing_activity"].apply(
        lambda x: "+" if x > 0 else "-"
    )

    df["cff_sign"] = df["financing_activity"].apply(
        lambda x: "+" if x > 0 else "-"
    )

    # Pattern label
    df["pattern_label"] = df.apply(
        lambda row: capital_allocation_pattern(
            row["operating_activity"],
            row["investing_activity"],
            row["financing_activity"]
        ),
        axis=1
    )

    report = df[
        [
            "company_id",
            "year",
            "cfo_sign",
            "cfi_sign",
            "cff_sign",
            "pattern_label"
        ]
    ]

    Path("output").mkdir(exist_ok=True)

    output_file = "output/capital_allocation.csv"

    report.to_csv(output_file, index=False)

    print("=" * 60)
    print("CAPITAL ALLOCATION REPORT GENERATED")
    print("=" * 60)
    print(report.head())

    print(f"\nReport saved to: {output_file}")


if __name__ == "__main__":
    main()