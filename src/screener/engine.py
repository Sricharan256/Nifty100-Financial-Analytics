"""
engine.py

Sprint 3 - Day 15

Financial Screener Filter Engine
"""

import sqlite3
import pandas as pd
import yaml

DB_PATH = "db/nifty100.db"
CONFIG_PATH = "config/screener_config.yaml"


def load_config():
    """Load threshold values from YAML."""
    with open(CONFIG_PATH, "r") as file:
        return yaml.safe_load(file)


def load_financial_ratios():
    """Load latest financial ratios from SQLite."""
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn
    )

    conn.close()

    # Keep only the latest year for each company
    df = (
        df.sort_values("year")
          .groupby("company_id", as_index=False)
          .last()
    )

    return df


def apply_filters(df, config):
    """Apply configurable threshold filters."""

    filtered = df.copy()

    filtered = filtered[
        (filtered["return_on_equity_pct"] >= config["roe_min"]) &
        (filtered["debt_to_equity"] <= config["debt_to_equity_max"]) &
        (filtered["free_cash_flow_cr"] >= config["free_cash_flow_min"])
    ]

    filtered = filtered.sort_values(
        by="composite_quality_score",
        ascending=False
    )

    return filtered


def main():

    print("=" * 70)
    print("SPRINT 3 - DAY 15")
    print("FILTER ENGINE")
    print("=" * 70)

    config = load_config()

    df = load_financial_ratios()

    print(f"\nCompanies Loaded : {len(df)}")

    filtered = apply_filters(df, config)

    print(f"Companies After Filter : {len(filtered)}")

    print("\nTop 10 Companies\n")

    print(
        filtered[
            [
                "company_id",
                "year",
                "return_on_equity_pct",
                "debt_to_equity",
                "free_cash_flow_cr",
                "composite_quality_score"
            ]
        ].head(10)
    )

    filtered.to_csv(
        "output/day15_filter_results.csv",
        index=False
    )

    print("\nReport Saved:")
    print("output/day15_filter_results.csv")


if __name__ == "__main__":
    main()