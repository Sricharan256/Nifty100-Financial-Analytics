"""
Sprint 3 – Day 17

Composite Quality Score Engine
"""

import sqlite3
import pandas as pd

DB_PATH = "db/nifty100.db"


def load_ratios():

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn
    )

    conn.close()

    return (
        df.sort_values("year")
          .groupby("company_id")
          .last()
          .reset_index()
    )


# -------------------------------
# Profitability Score
# -------------------------------

def profitability_score(row):

    roe = row["return_on_equity_pct"] * 0.15

    roce = row.get(
        "return_on_capital_employed_pct",
        row["return_on_equity_pct"]
    ) * 0.10

    npm = row["net_profit_margin_pct"] * 0.10

    return roe + roce + npm


# -------------------------------
# Cash Quality Score
# -------------------------------

def cash_quality_score(row):

    fcf = max(row["free_cash_flow_cr"], 0) * 0.15

    cfo = row["cash_from_operations_cr"] * 0.10

    positive = 5 if row["free_cash_flow_cr"] > 0 else 0

    return fcf + cfo + positive


# -------------------------------
# Growth Score
# -------------------------------

def growth_score(row):

    revenue = row.get("revenue_cagr_5yr", 0)

    pat = row.get("pat_cagr_5yr", 0)

    revenue = 0 if pd.isna(revenue) else revenue
    pat = 0 if pd.isna(pat) else pat

    return revenue * 0.10 + pat * 0.10


# -------------------------------
# Leverage Score
# -------------------------------

def leverage_score(row):

    debt = max(0, 10 - row["debt_to_equity"])

    icr = row["interest_coverage"]

    if pd.isna(icr):
        icr = 0

    return debt + icr * 0.05


# -------------------------------
# Composite Score
# -------------------------------

def calculate_composite(df):

    scores = []

    for _, row in df.iterrows():

        total = (
            profitability_score(row)
            + cash_quality_score(row)
            + growth_score(row)
            + leverage_score(row)
        )

        scores.append(round(total, 2))

    df["composite_score"] = scores

    return df


if __name__ == "__main__":

    print("=" * 60)
    print("SPRINT 3 - DAY 17")
    print("COMPOSITE QUALITY SCORE")
    print("=" * 60)

    df = load_ratios()

    df = calculate_composite(df)

    print(df[
        [
            "company_id",
            "composite_score"
        ]
    ].head(15))