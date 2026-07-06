"""
presets.py

Sprint 3 - Day 16

Implements six preset stock screeners.
"""

import sqlite3
import pandas as pd

DB_PATH = "db/nifty100.db"


# -------------------------------------------------------
# Load Latest Financial Ratios
# -------------------------------------------------------

def load_data():

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn
    )

    conn.close()

    # Keep latest year for every company
    df = (
        df.sort_values("year")
          .groupby("company_id", as_index=False)
          .last()
    )

    return df


# -------------------------------------------------------
# Quality Compounder
# -------------------------------------------------------

def quality_compounder(df):

    result = df[
        (df["return_on_equity_pct"] >= 20) &
        (df["debt_to_equity"] <= 0.50) &
        (df["free_cash_flow_cr"] > 100) &
        (df["composite_quality_score"] >= 18)
    ]

    return result.sort_values(
        "composite_quality_score",
        ascending=False
    )


# -------------------------------------------------------
# Value Pick
# -------------------------------------------------------

def value_pick(df):

    result = df[
        (df["return_on_equity_pct"] >= 15) &
        (df["debt_to_equity"] <= 0.75)
    ]

    return result.sort_values(
        "composite_quality_score",
        ascending=False
    )


# -------------------------------------------------------
# Growth Accelerator
# -------------------------------------------------------

def growth_accelerator(df):

    result = df[
        (df["return_on_equity_pct"] >= 22) &
        (df["free_cash_flow_cr"] > 150)
    ]

    return result.sort_values(
        "composite_quality_score",
        ascending=False
    )


# -------------------------------------------------------
# Dividend Champion
# -------------------------------------------------------

def dividend_champion(df):

    result = df[
        (df["dividend_payout_ratio_pct"] <= 50) &
        (df["free_cash_flow_cr"] > 500)
    ]

    return result.sort_values(
        "composite_quality_score",
        ascending=False
    )


# -------------------------------------------------------
# Debt Free Blue Chip
# -------------------------------------------------------

def debt_free_blue_chip(df):

    result = df[
        (df["debt_to_equity"] == 0) &
        (df["return_on_equity_pct"] >= 15)
    ]

    return result.sort_values(
        "composite_quality_score",
        ascending=False
    )


# -------------------------------------------------------
# Turnaround Watch
# -------------------------------------------------------

def turnaround_watch(df):

    result = df[
        (df["free_cash_flow_cr"] > 500) &
        (df["return_on_equity_pct"] >= 15)
    ]

    return result.sort_values(
        "composite_quality_score",
        ascending=False
    )


# -------------------------------------------------------
# Get All Presets
# -------------------------------------------------------

def get_presets():

    df = load_data()

    return {
        "Quality Compounder": quality_compounder(df),
        "Value Pick": value_pick(df),
        "Growth Accelerator": growth_accelerator(df),
        "Dividend Champion": dividend_champion(df),
        "Debt Free Blue Chip": debt_free_blue_chip(df),
        "Turnaround Watch": turnaround_watch(df)
    }


# -------------------------------------------------------
# Demo
# -------------------------------------------------------

if __name__ == "__main__":

    print("=" * 70)
    print("SPRINT 3 - DAY 16")
    print("PRESET SCREENERS")
    print("=" * 70)

    presets = get_presets()

    for name, data in presets.items():

        print("\n" + "=" * 70)
        print(name)
        print("=" * 70)

        print(f"Companies Found : {len(data)}")

        if len(data):

            print(
                data[
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