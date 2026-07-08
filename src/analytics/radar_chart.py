"""
radar_chart.py

Sprint 3 - Day 19

Radar Chart Engine
"""

import os
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

DB_PATH = "db/nifty100.db"

OUTPUT_DIR = "reports/radar_charts"


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

    conn = sqlite3.connect(DB_PATH)

    peer = pd.read_sql(
        """
        SELECT DISTINCT
            company_id,
            peer_group_name
        FROM peer_percentiles
        """,
        conn
    )

    conn.close()

    return peer


# ---------------------------------------------------------
# Merge Data
# ---------------------------------------------------------

def prepare_data():

    ratios = load_financial_ratios()

    peers = load_peer_groups()

    df = pd.merge(
        ratios,
        peers,
        on="company_id",
        how="left"
    )

    df["peer_group_name"] = df[
        "peer_group_name"
    ].fillna("No Peer Group")

    return df


# ---------------------------------------------------------
# Radar Metrics
# ---------------------------------------------------------

RADAR_METRICS = [

    "return_on_equity_pct",

    "return_on_equity_pct",      # Replace with ROCE later

    "net_profit_margin_pct",

    "debt_to_equity",

    "free_cash_flow_cr",

    "pat_cagr_5yr",

    "revenue_cagr_5yr",

    "composite_quality_score"

]

RADAR_LABELS = [

    "ROE",

    "ROCE",

    "NPM",

    "D/E",

    "FCF",

    "PAT CAGR",

    "Revenue CAGR",

    "Composite"

]


# ---------------------------------------------------------
# Normalize Values
# ---------------------------------------------------------

def normalize(values):

    values = pd.to_numeric(
        pd.Series(values),
        errors="coerce"
    ).fillna(0).to_numpy(dtype=float)

    minimum = values.min()
    maximum = values.max()

    if minimum == maximum:
        return np.ones(len(values)) * 50

    return (
        (values - minimum)
        /
        (maximum - minimum)
    ) * 100


# ---------------------------------------------------------
# Peer Average
# ---------------------------------------------------------

def peer_average(df, peer_group):

    peer_df = df[
        df["peer_group_name"] == peer_group
    ]

    averages = []

    for metric in RADAR_METRICS:

        if metric in peer_df.columns:

            value = pd.to_numeric(
                peer_df[metric],
                errors="coerce"
            ).fillna(0).mean()

            averages.append(float(value))

        else:

            averages.append(0.0)

    return averages
# ---------------------------------------------------------
# Nifty 100 Average
# ---------------------------------------------------------

def nifty_average(df):

    averages = []

    for metric in RADAR_METRICS:

        if metric in df.columns:

            value = (
                pd.to_numeric(
                    df[metric],
                    errors="coerce"
                )
                .fillna(0)
                .mean()
            )

            averages.append(float(value))

        else:

            averages.append(0.0)

    return averages


# ---------------------------------------------------------
# Company Values
# ---------------------------------------------------------

def company_values(row):

    values = []

    for metric in RADAR_METRICS:

        if metric in row.index:

            value = row[metric]

            if pd.isna(value):
                value = 0

            values.append(float(value))

        else:

            values.append(0.0)

    return values

# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

if __name__ == "__main__":

    print("=" * 60)
    print("SPRINT 3 - DAY 19")
    print("RADAR CHART ENGINE")
    print("=" * 60)

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    df = prepare_data()

    print()

    print("Companies Loaded :", len(df))

    print()

    print(
        df[
            [
                "company_id",
                "peer_group_name"
            ]
        ].head(20)
    )
    # ---------------------------------------------------------
# Create Radar Chart
# ---------------------------------------------------------

def create_radar_chart(company_row, peer_avg):

    # Company Name
    company = company_row["company_id"]

    # Company Values
    values = company_values(company_row)

    values = normalize(np.array(values))

    # Peer Average
    peer_avg = normalize(np.array(peer_avg))

    # Close Polygon
    values = np.append(values, values[0])

    peer_avg = np.append(peer_avg, peer_avg[0])

    # Angles
    angles = np.linspace(
        0,
        2 * np.pi,
        len(RADAR_LABELS),
        endpoint=False
    )

    angles = np.append(
        angles,
        angles[0]
    )

    # Create Figure
    fig = plt.figure(
        figsize=(8, 8)
    )

    ax = plt.subplot(
        111,
        polar=True
    )

    # Company Polygon
    ax.plot(
        angles,
        values,
        linewidth=2,
        color="blue",
        label=company
    )

    ax.fill(
        angles,
        values,
        alpha=0.25,
        color="blue"
    )

    # Peer Average
    ax.plot(
        angles,
        peer_avg,
        linewidth=2,
        linestyle="--",
        color="red",
        label="Peer Average"
    )

    # Axis Labels
    ax.set_xticks(
        angles[:-1]
    )

    ax.set_xticklabels(
        RADAR_LABELS,
        fontsize=10
    )

    ax.set_yticks(
        [20, 40, 60, 80, 100]
    )

    ax.set_ylim(
        0,
        100
    )

    ax.set_title(
        f"{company} Radar Chart",
        fontsize=14,
        pad=20
    )

    ax.legend(
        loc="upper right"
    )

    return fig
# ---------------------------------------------------------
# Standalone Radar Chart
# ---------------------------------------------------------

def create_standalone_chart(company_row, nifty_avg):

    company = company_row["company_id"]

    values = normalize(
        np.array(
            company_values(company_row)
        )
    )

    nifty_avg = normalize(
        np.array(
            nifty_avg
        )
    )

    values = np.append(values, values[0])
    nifty_avg = np.append(nifty_avg, nifty_avg[0])

    angles = np.linspace(
        0,
        2 * np.pi,
        len(RADAR_LABELS),
        endpoint=False
    )

    angles = np.append(
        angles,
        angles[0]
    )

    fig = plt.figure(figsize=(8, 8))

    ax = plt.subplot(
        111,
        polar=True
    )

    ax.plot(
        angles,
        values,
        linewidth=2,
        color="green",
        label=company
    )

    ax.fill(
        angles,
        values,
        alpha=0.25,
        color="green"
    )

    ax.plot(
        angles,
        nifty_avg,
        linestyle="--",
        linewidth=2,
        color="orange",
        label="Nifty 100 Average"
    )

    ax.set_xticks(
        angles[:-1]
    )

    ax.set_xticklabels(
        RADAR_LABELS,
        fontsize=10
    )

    ax.set_ylim(
        0,
        100
    )

    ax.set_title(
        f"{company} (Standalone)",
        fontsize=14
    )

    ax.legend()

    return fig
# ---------------------------------------------------------
# Generate Radar Charts
# ---------------------------------------------------------

def generate_radar_charts():

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    df = prepare_data()

    generated = 0

    nifty_avg = nifty_average(df)

    for _, row in df.iterrows():

        peer_group = row["peer_group_name"]

        try:

            # -------------------------------------------------
            # Company has NO peer group
            # -------------------------------------------------

            if peer_group == "No peer group assigned":

                fig = create_standalone_chart(
                    row,
                    nifty_avg
                )

            # -------------------------------------------------
            # Company has Peer Group
            # -------------------------------------------------

            else:

                avg = peer_average(
                    df,
                    peer_group
                )

                fig = create_radar_chart(
                    row,
                    avg
                )

            # -------------------------------------------------
            # Save Chart
            # -------------------------------------------------

            filename = os.path.join(

                OUTPUT_DIR,

                f"{row['company_id']}_radar.png"

            )

            fig.savefig(

                filename,

                dpi=300,

                bbox_inches="tight"

            )

            plt.close(fig)

            generated += 1

            print(
                f"Generated : {row['company_id']}_radar.png"
            )

        except Exception as e:

            print(
                f"Skipped {row['company_id']} : {e}"
            )

    print()

    print("=" * 60)
    print("RADAR CHART GENERATION COMPLETED")
    print("=" * 60)

    print(f"Charts Generated : {generated}")
    print(f"Location : {OUTPUT_DIR}")
# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    print("=" * 60)
    print("SPRINT 3 - DAY 19")
    print("RADAR CHART GENERATION")
    print("=" * 60)

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    df = prepare_data()

    print(f"\nCompanies Loaded : {len(df)}")

    peer_count = (
        df["peer_group_name"] != "No Peer Group"
    ).sum()

    print(f"Companies With Peer Group : {peer_count}")

    print("\nGenerating Radar Charts...\n")

    generate_radar_charts()

    print("\nDay 19 Completed Successfully.")

    print(f"\nCharts saved in : {OUTPUT_DIR}")

# ---------------------------------------------------------
# Execute
# ---------------------------------------------------------

if __name__ == "__main__":

    main()