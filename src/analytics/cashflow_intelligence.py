"""
cashflow_intelligence.py

Day 31 – Cash Flow Intelligence Module
"""

import os
import sqlite3
import pandas as pd
import numpy as np

# -----------------------------------------------------
# Import KPI Functions (Day 11)
# -----------------------------------------------------

from cashflow_kpis import (
    free_cash_flow,
    cfo_quality_score,
    capex_intensity,
    fcf_conversion_rate,
    capital_allocation_pattern
)

# -----------------------------------------------------
# Create Output Folder
# -----------------------------------------------------

os.makedirs("output", exist_ok=True)

# -----------------------------------------------------
# Database Connection
# -----------------------------------------------------

DB_PATH = "db/nifty100.db"

conn = sqlite3.connect(DB_PATH)

# -----------------------------------------------------
# Load Database Tables
# -----------------------------------------------------

companies = pd.read_sql(
    "SELECT * FROM companies",
    conn
)

cashflow = pd.read_sql(
    "SELECT * FROM cash_flow",
    conn
)

profit_loss = pd.read_sql(
    "SELECT * FROM profit_loss",
    conn
)

financial_ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)
print("\nCompanies Columns")
print("-" * 70)
print(companies.columns.tolist())
# -----------------------------------------------------
# Dataset Summary
# -----------------------------------------------------

print(f"Companies Loaded        : {len(companies)}")
print(f"Cash Flow Records       : {len(cashflow)}")
print(f"Profit Loss Records     : {len(profit_loss)}")
print(f"Financial Ratio Records : {len(financial_ratios)}")

# -----------------------------------------------------
# Latest Financial Ratio Records
# -----------------------------------------------------

if "year" in financial_ratios.columns:

    financial_ratios["year_num"] = (
        financial_ratios["year"]
        .astype(str)
        .str.extract(r"(\d{4})")
        .astype(float)
    )

    latest_ratios = (
        financial_ratios
        .sort_values("year_num")
        .groupby("company_id")
        .tail(1)
        .reset_index(drop=True)
    )

else:

    latest_ratios = financial_ratios.copy()

print("\nLatest Company Records :", len(latest_ratios))

print("\nSample Latest Records")
print("-" * 70)

sample_columns = [
    col
    for col in ["company_id", "company_name", "year"]
    if col in latest_ratios.columns
]

if sample_columns:
    print(latest_ratios[sample_columns].head())

# -----------------------------------------------------
# Output Containers
# -----------------------------------------------------

cashflow_records = []
distress_records = []

print("\nInitialization Completed Successfully.")
print("=" * 70)
# -----------------------------------------------------
# Helper Function
# -----------------------------------------------------

def get_value(row, column):
    """Safely return a value from a pandas Series."""
    if column not in row.index:
        return None

    value = row[column]

    if pd.isna(value):
        return None

    return value


print("\nCalculating CFO Quality Score & CapEx Intensity...")
print("-" * 70)

# -----------------------------------------------------
# Process Each Company
# -----------------------------------------------------

for company_id in companies["id"]:

    cf = cashflow[cashflow["company_id"] == company_id].copy()
    pl = profit_loss[profit_loss["company_id"] == company_id].copy()

    if cf.empty or pl.empty:
        continue

    # Sort by Year
    cf["year_num"] = (
        cf["year"]
        .astype(str)
        .str.extract(r"(\d{4})")
        .astype(float)
    )

    pl["year_num"] = (
        pl["year"]
        .astype(str)
        .str.extract(r"(\d{4})")
        .astype(float)
    )

    cf = cf.sort_values("year_num").tail(5)
    pl = pl.sort_values("year_num").tail(5)

    cfo_scores = []

    latest_capex_pct = None
    latest_capex_label = None

    # -------------------------------------------------
    # Calculate 5-Year CFO Quality
    # -------------------------------------------------

    for _, cf_row in cf.iterrows():

        year = cf_row["year"]

        pl_match = pl[pl["year"] == year]

        if pl_match.empty:
            continue

        pl_row = pl_match.iloc[0]

        result = cfo_quality_score(
            get_value(cf_row, "operating_activity"),
            get_value(pl_row, "net_profit")
        )

        if result is not None:
            ratio, label = result
            cfo_scores.append(ratio)

    # -------------------------------------------------
    # Average CFO Quality
    # -------------------------------------------------

    if len(cfo_scores):

        avg_score = round(np.mean(cfo_scores), 2)

        if avg_score > 1:
            quality_label = "High Quality"

        elif avg_score >= 0.5:
            quality_label = "Moderate"

        else:
            quality_label = "Accrual Risk"

    else:

        avg_score = None
        quality_label = None

    # -------------------------------------------------
    # Latest Year CapEx Intensity
    # -------------------------------------------------

    latest_cf = cf.iloc[-1]

    latest_pl = pl[pl["year"] == latest_cf["year"]]

    if not latest_pl.empty:

        latest_pl = latest_pl.iloc[0]

        capex = capex_intensity(
            get_value(latest_cf, "investing_activity"),
            get_value(latest_pl, "sales")
        )

        if capex is not None:
            latest_capex_pct, latest_capex_label = capex

    # -------------------------------------------------
    # Store Results
    # -------------------------------------------------

    company_name = ""

    match = companies[companies["id"] == company_id]

    if not match.empty and "company_name" in match.columns:
        company_name = match.iloc[0]["company_name"]

    cashflow_records.append({

        "company_id": company_id,
        "company_name": company_name,

        "cfo_quality_score": avg_score,
        "cfo_quality_label": quality_label,

        "capex_intensity_pct": latest_capex_pct,
        "capex_label": latest_capex_label

    })

# -----------------------------------------------------
# Create DataFrame
# -----------------------------------------------------

cashflow_df = pd.DataFrame(cashflow_records)

print("\nCompanies Processed :", len(cashflow_df))

print("\nSample Results")
print("-" * 70)

print(cashflow_df.head())
# -----------------------------------------------------
# Part 3 - Distress Signal & Capital Allocation
# -----------------------------------------------------

print("\nCalculating Distress Signals & Capital Allocation...")
print("-" * 70)

for i, row in cashflow_df.iterrows():

    company_id = row["company_id"]

    # -----------------------------
    # Latest Cash Flow Record
    # -----------------------------

    cf = cashflow[cashflow["company_id"] == company_id].copy()

    cf["year_num"] = (
        cf["year"]
        .astype(str)
        .str.extract(r"(\d{4})")
        .astype(float)
    )

    cf = cf.sort_values("year_num")

    latest_cf = cf.iloc[-1]

    cfo = latest_cf["operating_activity"]
    cfi = latest_cf["investing_activity"]
    cff = latest_cf["financing_activity"]

    # -----------------------------
    # Latest Profit & Loss
    # -----------------------------

    pl = profit_loss[
        (profit_loss["company_id"] == company_id) &
        (profit_loss["year"] == latest_cf["year"])
    ]

    latest_profit = None
    operating_profit = None

    if not pl.empty:

        latest_profit = pl.iloc[0]["net_profit"]
        operating_profit = pl.iloc[0]["operating_profit"]

    # -----------------------------
    # Free Cash Flow
    # -----------------------------

    fcf = free_cash_flow(cfo, cfi)

    conversion = fcf_conversion_rate(
        fcf,
        operating_profit
    )

    # -----------------------------
    # Distress Signal
    # CFO < 0 and Financing > 0
    # -----------------------------

    distress = (cfo < 0) and (cff > 0)

    # -----------------------------
    # Deleveraging
    # Financing < 0
    # Debt decreasing YoY
    # -----------------------------

    deleveraging = False

    ratios = financial_ratios[
        financial_ratios["company_id"] == company_id
    ].copy()

    if len(ratios) >= 2:

        ratios["year_num"] = (
            ratios["year"]
            .astype(str)
            .str.extract(r"(\d{4})")
            .astype(float)
        )

        ratios = ratios.sort_values("year_num")

        latest = ratios.iloc[-1]
        previous = ratios.iloc[-2]

        if (
            cff < 0 and
            latest["total_debt_cr"] < previous["total_debt_cr"]
        ):
            deleveraging = True

    # -----------------------------
    # Capital Allocation Pattern
    # -----------------------------

    allocation = capital_allocation_pattern(
        cfo,
        cfi,
        cff,
        row["cfo_quality_score"]
    )

    # -----------------------------
    # Update DataFrame
    # -----------------------------

    cashflow_df.loc[i, "fcf_conversion_pct"] = conversion
    cashflow_df.loc[i, "distress_flag"] = distress
    cashflow_df.loc[i, "deleveraging_flag"] = deleveraging
    cashflow_df.loc[i, "capital_allocation_label"] = allocation

    # -----------------------------
    # Distress Alert Output
    # -----------------------------

    if distress:

        distress_records.append({

            "company_id": company_id,

            "company_name": row["company_name"],

            "cfo": cfo,

            "cff": cff,

            "latest_net_profit": latest_profit

        })

# -----------------------------------------------------
# Preview
# -----------------------------------------------------

print("\nDistress Companies :", len(distress_records))

print("\nCapital Allocation Distribution")
print("-" * 70)

print(
    cashflow_df["capital_allocation_label"]
    .value_counts()
)
# -----------------------------------------------------
# Part 4 - Final Output & Export
# -----------------------------------------------------

print("\nPreparing Final Report...")
print("-" * 70)

# -----------------------------------------------------
# Add Sector Information
# -----------------------------------------------------

sectors = pd.read_sql(
    "SELECT company_id, broad_sector FROM sectors",
    conn
)

sectors = sectors.rename(
    columns={
        "broad_sector": "sector"
    }
)

cashflow_df = cashflow_df.merge(
    sectors,
    on="company_id",
    how="left"
)

cashflow_df["sector"] = cashflow_df["sector"].fillna("Unknown")
# -----------------------------------------------------
# Add Latest Financial Ratio Metrics
# -----------------------------------------------------

latest_ratios = financial_ratios.copy()

latest_ratios["year_num"] = (
    latest_ratios["year"]
    .astype(str)
    .str.extract(r"(\d{4})")
    .astype(float)
)

latest_ratios = (
    latest_ratios
    .sort_values("year_num")
    .groupby("company_id")
    .tail(1)
)

ratio_columns = [
    "company_id",
    "free_cash_flow_cr"
]

latest_ratios = latest_ratios[ratio_columns]

latest_ratios = latest_ratios.rename(
    columns={
        "free_cash_flow_cr": "fcf_cagr_5yr"
    }
)

cashflow_df = cashflow_df.merge(
    latest_ratios,
    on="company_id",
    how="left"
)

# -----------------------------------------------------
# Arrange Columns
# -----------------------------------------------------

final_columns = [

    "company_id",
    "company_name",
    "sector",

    "cfo_quality_score",
    "cfo_quality_label",

    "capex_intensity_pct",
    "capex_label",

    "fcf_cagr_5yr",

    "fcf_conversion_pct",

    "distress_flag",

    "deleveraging_flag",

    "capital_allocation_label"

]

cashflow_df = cashflow_df[final_columns]

cashflow_df = cashflow_df.sort_values(
    "company_name"
)

# -----------------------------------------------------
# Export Excel
# -----------------------------------------------------

excel_path = "output/cashflow_intelligence.xlsx"

cashflow_df.to_excel(
    excel_path,
    index=False
)

# -----------------------------------------------------
# Export Distress Alerts
# -----------------------------------------------------

distress_df = pd.DataFrame(distress_records)

distress_path = "output/distress_alerts.csv"

distress_df.to_csv(
    distress_path,
    index=False
)

# -----------------------------------------------------
# Final Summary
# -----------------------------------------------------

print("\nExport Completed Successfully")
print("-" * 70)

print(f"Cash Flow Report : {excel_path}")
print(f"Distress Alerts  : {distress_path}")

print("\nSummary")
print("-" * 70)

print("Companies Analysed :", len(cashflow_df))
print("Distress Signals   :", len(distress_df))

print("\nCapital Allocation Distribution")
print("-" * 70)

print(
    cashflow_df["capital_allocation_label"]
    .value_counts()
)

print("\nSample Output")
print("-" * 70)

print(cashflow_df.head())

# -----------------------------------------------------
# Close Database
# -----------------------------------------------------

conn.close()

print("\nDay 31 Cash Flow Intelligence Module Completed Successfully.")