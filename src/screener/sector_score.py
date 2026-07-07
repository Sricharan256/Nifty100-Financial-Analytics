"""
sector_score.py

Sprint 3 - Day 17

Sector Relative Composite Score
"""

import sqlite3
import pandas as pd

DB_PATH = "db/nifty100.db"


def load_data():
    """Load financial ratios and company information."""

    conn = sqlite3.connect(DB_PATH)

    ratios = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn
    )

    companies = pd.read_sql(
        "SELECT * FROM companies",
        conn
    )

    conn.close()

    # Rename id -> company_id
    if "id" in companies.columns:
        companies.rename(
            columns={"id": "company_id"},
            inplace=True
        )

    df = pd.merge(
        ratios,
        companies,
        on="company_id",
        how="left"
    )

    return df


def calculate_sector_score(df):
    """
    Calculate sector-relative score.

    If broad_sector column is unavailable,
    use composite_quality_score directly.
    """

    if "broad_sector" not in df.columns:

        print("broad_sector column not found.")
        print("Using composite_quality_score as sector score.")

        df["sector_relative_score"] = (
            df["composite_quality_score"]
        )

        return df

    # Calculate sector average
    sector_average = (
        df.groupby("broad_sector")[
            "composite_quality_score"
        ].transform("mean")
    )

    df["sector_relative_score"] = (
        (
            df["composite_quality_score"]
            / sector_average
        ) * 100
    ).round(2)

    return df


def save_output(df):

    output = df[
        [
            "company_id",
            "company_name",
            "composite_quality_score",
            "sector_relative_score"
        ]
    ]

    output.to_csv(
        "output/sector_relative_scores.csv",
        index=False
    )

    print("\nReport Saved")
    print("Location : output/sector_relative_scores.csv")


def main():

    print("=" * 60)
    print("SPRINT 3 - DAY 17")
    print("SECTOR RELATIVE SCORING")
    print("=" * 60)

    df = load_data()

    df = calculate_sector_score(df)

    print("\nPreview\n")

    print(
        df[
            [
                "company_id",
                "company_name",
                "composite_quality_score",
                "sector_relative_score"
            ]
        ].head(15)
    )

    save_output(df)

    print("\nDay 17 Sector Relative Score Completed Successfully.")


if __name__ == "__main__":
    main()