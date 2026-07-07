"""
peer.py

Sprint 3 - Day 18

Peer Percentile Ranking Engine
"""

import sqlite3
import pandas as pd

DB_PATH = "db/nifty100.db"


# ---------------------------------------------------------
# Load Financial Ratios
# ---------------------------------------------------------

def load_financial_ratios():

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn
    )

    conn.close()

    # Keep latest year only
    df = (
        df.sort_values("year")
          .groupby("company_id", as_index=False)
          .last()
    )

    return df


# ---------------------------------------------------------
# Load Peer Groups
# ---------------------------------------------------------

def load_peer_groups():

    """
    Expected Excel columns

    company_id
    peer_group_name
    """

    peer_df = pd.read_excel(
        "data/raw/peer_groups.xlsx"
    )

    return peer_df


# ---------------------------------------------------------
# Merge
# ---------------------------------------------------------

def merge_data():

    ratios = load_financial_ratios()

    peers = load_peer_groups()

    merged = pd.merge(
        ratios,
        peers,
        on="company_id",
        how="left"
    )

    merged["peer_group_name"] = (
        merged["peer_group_name"]
        .fillna("No peer group assigned")
    )

    return merged


# ---------------------------------------------------------
# Percentile Rank
# ---------------------------------------------------------

def percentile(series):

    return (
        series.rank(
            pct=True,
            method="average"
        ) * 100
    ).round(2)


# ---------------------------------------------------------
# Compute Peer Percentiles
# ---------------------------------------------------------

def compute_peer_percentiles(df):

    metrics = [

        "return_on_equity_pct",

        "net_profit_margin_pct",

        "debt_to_equity",

        "free_cash_flow_cr",

        "interest_coverage",

        "asset_turnover",

        "earnings_per_share",

        "book_value_per_share",

        "revenue_cagr_5yr",

        "pat_cagr_5yr"

    ]

    results = []

    peer_groups = sorted(
        df["peer_group_name"].unique()
    )

    for peer in peer_groups:

        peer_df = df[
            df["peer_group_name"] == peer
        ].copy()

        if len(peer_df) == 0:
            continue

        for metric in metrics:

            if metric not in peer_df.columns:
                continue

            peer_df[metric] = (
                peer_df[metric]
                .fillna(0)
            )

            # D/E Lower is Better
            if metric == "debt_to_equity":

                peer_df["percentile_rank"] = (

                    100
                    -
                    percentile(peer_df[metric])

                )

            else:

                peer_df["percentile_rank"] = (
                    percentile(peer_df[metric])
                )

            for _, row in peer_df.iterrows():

                results.append({

                    "company_id":
                        row["company_id"],

                    "peer_group_name":
                        peer,

                    "metric":
                        metric,

                    "value":
                        row[metric],

                    "percentile_rank":
                        row["percentile_rank"],

                    "year":
                        row["year"]

                })

    return pd.DataFrame(results)


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

if __name__ == "__main__":

    print("=" * 60)
    print("SPRINT 3 - DAY 18")
    print("PEER PERCENTILE ENGINE")
    print("=" * 60)

    df = merge_data()

    result = compute_peer_percentiles(df)

    print()

    print("Rows Generated :", len(result))

    print()

    print(result.head(20))