"""
capital_allocation_report.py

Day 32 – Capital Allocation Report
"""

import os
import sqlite3
import pandas as pd

# -----------------------------------------------------
# Output Folder
# -----------------------------------------------------

os.makedirs("output", exist_ok=True)

# -----------------------------------------------------
# Database Connection
# -----------------------------------------------------

DB_PATH = "db/nifty100.db"

conn = sqlite3.connect(DB_PATH)

print("=" * 70)
print("DAY 32 - CAPITAL ALLOCATION REPORT")
print("=" * 70)

# -----------------------------------------------------
# Load Tables
# -----------------------------------------------------

capital_allocation = pd.read_sql(
    "SELECT * FROM sectors",
    conn
)

companies = pd.read_sql(
    "SELECT id, company_name FROM companies",
    conn
)

print(f"Capital Allocation Records : {len(capital_allocation)}")
print(f"Companies Loaded           : {len(companies)}")

print("\nCapital Allocation Columns")
print("-" * 70)
print(capital_allocation.columns.tolist())

# -----------------------------------------------------
# Check Company Coverage
# -----------------------------------------------------

company_count = capital_allocation["company_id"].nunique()

print("\nCompanies Available :", company_count)

missing = set(companies["id"]) - set(capital_allocation["company_id"])

print("Missing Companies :", len(missing))

if len(missing):

    print("\nMissing Company IDs")
    print(sorted(missing))

print("\nInitialization Completed Successfully.")
print("=" * 70)
# -----------------------------------------------------
# Merge Company Names
# -----------------------------------------------------

capital_df = capital_allocation.merge(
    companies,
    left_on="company_id",
    right_on="id",
    how="left"
)

capital_df.drop(columns=["id_y"], inplace=True)

capital_df.rename(
    columns={"id_x": "record_id"},
    inplace=True
)

# -----------------------------------------------------
# Sector Distribution
# -----------------------------------------------------

print("\nSector Distribution")
print("-" * 70)

sector_summary = (
    capital_df
    .groupby("broad_sector")
    .agg(
        companies=("company_id", "count"),
        total_weight=("index_weight_pct", "sum")
    )
    .reset_index()
    .sort_values(
        "total_weight",
        ascending=False
    )
)

print(sector_summary)

# -----------------------------------------------------
# Market Cap Distribution
# -----------------------------------------------------

print("\nMarket Cap Distribution")
print("-" * 70)

marketcap_summary = (
    capital_df
    .groupby("market_cap_category")
    .agg(
        companies=("company_id", "count"),
        total_weight=("index_weight_pct", "sum")
    )
    .reset_index()
)

print(marketcap_summary)

# -----------------------------------------------------
# Largest Sectors
# -----------------------------------------------------

print("\nTop 10 Sectors")
print("-" * 70)

print(
    sector_summary.head(10)
)

# -----------------------------------------------------
# Save Summary Tables
# -----------------------------------------------------

sector_summary.to_csv(
    "output/sector_distribution.csv",
    index=False
)

marketcap_summary.to_csv(
    "output/marketcap_distribution.csv",
    index=False
)

print("\nSector Distribution Saved")
print("Market Cap Distribution Saved")
# -----------------------------------------------------
# Company-wise Capital Allocation Report
# -----------------------------------------------------

print("\nPreparing Company Capital Allocation Report...")
print("-" * 70)

company_report = capital_df[
    [
        "company_id",
        "company_name",
        "broad_sector",
        "sub_sector",
        "market_cap_category",
        "index_weight_pct"
    ]
].copy()

company_report.rename(
    columns={
        "broad_sector": "sector",
        "sub_sector": "industry",
        "market_cap_category": "market_cap"
    },
    inplace=True
)

company_report = company_report.sort_values(
    ["sector", "company_name"]
).reset_index(drop=True)

print(company_report.head())

# -----------------------------------------------------
# Sector Summary Statistics
# -----------------------------------------------------

sector_stats = (
    company_report
    .groupby("sector")
    .agg(
        company_count=("company_id", "count"),
        average_weight=("index_weight_pct", "mean"),
        total_weight=("index_weight_pct", "sum")
    )
    .reset_index()
)

print("\nSector Summary")
print("-" * 70)
print(sector_stats)

# -----------------------------------------------------
# Export Reports
# -----------------------------------------------------

company_report.to_excel(
    "output/capital_allocation_report.xlsx",
    index=False
)

sector_stats.to_csv(
    "output/capital_allocation_sector_summary.csv",
    index=False
)

print("\nReports Exported Successfully")
print("-" * 70)
print("Capital Allocation Report : output/capital_allocation_report.xlsx")
print("Sector Summary           : output/capital_allocation_sector_summary.csv")

# -----------------------------------------------------
# Close Database
# -----------------------------------------------------

conn.close()

print("\nDay 32 Capital Allocation Report Completed Successfully.")