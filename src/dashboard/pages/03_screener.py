import streamlit as st
import pandas as pd
import sqlite3

from utils.db import (
    get_companies,
    get_ratios,
    get_market_cap
)

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Stock Screener",
    layout="wide"
)

st.title("🔎 Stock Screener")

st.markdown("---")

# ---------------------------------------------------------
# Load Data
# ---------------------------------------------------------

companies = get_companies()

# Rename id -> company_id for easy merging
companies = companies.rename(
    columns={"id": "company_id"}
)

ratios = get_ratios()

market = get_market_cap()

# ---------------------------------------------------------
# Load Sectors
# ---------------------------------------------------------

conn = sqlite3.connect("db/nifty100.db")

sectors = pd.read_sql(
    """
    SELECT
        company_id,
        broad_sector,
        sub_sector
    FROM sectors
    """,
    conn
)

conn.close()

# ---------------------------------------------------------
# Latest Financial Year
# ---------------------------------------------------------

ratios["year_num"] = (
    ratios["year"]
    .astype(str)
    .str.extract(r"(\d{4})")
    .astype(int)
)

latest_year = ratios["year_num"].max()

ratios = ratios[
    ratios["year_num"] == latest_year
]

market = market[
    market["year"] == latest_year
]

# ---------------------------------------------------------
# Merge Tables
# ---------------------------------------------------------

df = ratios.merge(
    companies,
    on="company_id",
    how="left"
)

df = df.merge(
    sectors,
    on="company_id",
    how="left"
)

df = df.merge(
    market,
    on="company_id",
    how="left"
)

# ---------------------------------------------------------
# Remove duplicate columns
# ---------------------------------------------------------

df = df.loc[:, ~df.columns.duplicated()]

# ---------------------------------------------------------
# Replace missing values
# ---------------------------------------------------------

numeric_cols = df.select_dtypes(include="number").columns

df[numeric_cols] = df[numeric_cols].fillna(0)


# ---------------------------------------------------------
# Verify Data
# ---------------------------------------------------------

st.success(f"Loaded {len(df)} company records")

st.write(df.head())
# ---------------------------------------------------------
# Sidebar Filters
# ---------------------------------------------------------

st.sidebar.header("📊 Stock Filters")

# ROE
roe_min = st.sidebar.slider(
    "Minimum ROE (%)",
    min_value=float(df["return_on_equity_pct"].min()),
    max_value=float(df["return_on_equity_pct"].max()),
    value=15.0,
)

# Debt / Equity
de_max = st.sidebar.slider(
    "Maximum Debt / Equity",
    min_value=0.0,
    max_value=float(df["debt_to_equity"].max()),
    value=1.0,
)

# Free Cash Flow
fcf_min = st.sidebar.slider(
    "Minimum Free Cash Flow",
    min_value=float(df["free_cash_flow_cr"].min()),
    max_value=float(df["free_cash_flow_cr"].max()),
    value=float(df["free_cash_flow_cr"].min()),
)

# Revenue CAGR
revenue_cagr_min = st.sidebar.slider(
    "Minimum Revenue CAGR (%)",
    min_value=float(df["revenue_cagr_5yr"].fillna(0).min()),
    max_value=float(df["revenue_cagr_5yr"].fillna(0).max()),
    value=10.0,
)

# PAT CAGR
pat_cagr_min = st.sidebar.slider(
    "Minimum PAT CAGR (%)",
    min_value=float(df["pat_cagr_5yr"].fillna(0).min()),
    max_value=float(df["pat_cagr_5yr"].fillna(0).max()),
    value=10.0,
)

# Operating Profit Margin
opm_min = st.sidebar.slider(
    "Minimum OPM (%)",
    min_value=float(df["operating_profit_margin_pct"].min()),
    max_value=float(df["operating_profit_margin_pct"].max()),
    value=15.0,
)

# PE Ratio
pe_max = st.sidebar.slider(
    "Maximum PE Ratio",
    min_value=float(df["pe_ratio"].min()),
    max_value=float(df["pe_ratio"].max()),
    value=40.0,
)

# PB Ratio
pb_max = st.sidebar.slider(
    "Maximum PB Ratio",
    min_value=float(df["pb_ratio"].min()),
    max_value=float(df["pb_ratio"].max()),
    value=8.0,
)

# Dividend Yield
dividend_min = st.sidebar.slider(
    "Minimum Dividend Yield (%)",
    min_value=float(df["dividend_yield_pct"].min()),
    max_value=float(df["dividend_yield_pct"].max()),
    value=0.0,
)

# Interest Coverage
icr_min = st.sidebar.slider(
    "Minimum Interest Coverage",
    min_value=float(df["interest_coverage"].fillna(0).min()),
    max_value=float(df["interest_coverage"].fillna(0).max()),
    value=3.0,
)

# ---------------------------------------------------------
# Presets
# ---------------------------------------------------------

st.sidebar.markdown("---")
st.sidebar.subheader("🎯 Presets")

preset = st.sidebar.radio(
    "Choose Preset",
    [
        "Custom",
        "Quality",
        "Value",
        "Growth",
        "Dividend",
        "Debt-Free",
        "Turnaround"
    ]
)

if preset == "Quality":
    roe_min = 20
    de_max = 0.5
    revenue_cagr_min = 15
    pat_cagr_min = 15

elif preset == "Value":
    pe_max = 20
    pb_max = 3

elif preset == "Growth":
    revenue_cagr_min = 20
    pat_cagr_min = 20

elif preset == "Dividend":
    dividend_min = 2

elif preset == "Debt-Free":
    de_max = 0

elif preset == "Turnaround":
    revenue_cagr_min = 5
    pat_cagr_min = 5
    roe_min = 5

st.sidebar.success(f"Current Preset: {preset}")
# ---------------------------------------------------------
# Apply Filters
# ---------------------------------------------------------

filtered = df.copy()

filtered = filtered[
    (filtered["return_on_equity_pct"] >= roe_min) &
    (filtered["debt_to_equity"] <= de_max) &
    (filtered["free_cash_flow_cr"] >= fcf_min) &
    (filtered["revenue_cagr_5yr"].fillna(0) >= revenue_cagr_min) &
    (filtered["pat_cagr_5yr"].fillna(0) >= pat_cagr_min) &
    (filtered["operating_profit_margin_pct"] >= opm_min) &
    (filtered["pe_ratio"] <= pe_max) &
    (filtered["pb_ratio"] <= pb_max) &
    (filtered["dividend_yield_pct"] >= dividend_min) &
    (filtered["interest_coverage"].fillna(0) >= icr_min)
]

# ---------------------------------------------------------
# Result Count
# ---------------------------------------------------------

st.markdown("---")

st.subheader("📈 Screening Results")

st.success(
    f"{len(filtered)} companies match your filters."
)

# ---------------------------------------------------------
# Display Columns
# ---------------------------------------------------------

display_cols = [
    "company_id",
    "company_name",
    "broad_sector",
    "composite_quality_score",
    "return_on_equity_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "operating_profit_margin_pct",
    "pe_ratio",
    "pb_ratio",
    "dividend_yield_pct",
    "interest_coverage"
]

available_cols = [
    col for col in display_cols
    if col in filtered.columns
]

result = filtered[available_cols].copy()

result = result.rename(
    columns={
        "company_id": "Ticker",
        "company_name": "Company",
        "broad_sector": "Sector",
        "composite_quality_score": "Quality Score",
        "return_on_equity_pct": "ROE %",
        "debt_to_equity": "D/E",
        "free_cash_flow_cr": "FCF",
        "revenue_cagr_5yr": "Revenue CAGR %",
        "pat_cagr_5yr": "PAT CAGR %",
        "operating_profit_margin_pct": "OPM %",
        "pe_ratio": "P/E",
        "pb_ratio": "P/B",
        "dividend_yield_pct": "Dividend Yield %",
        "interest_coverage": "ICR"
    }
)

# ---------------------------------------------------------
# Sort Results
# ---------------------------------------------------------

if "Quality Score" in result.columns:

    result = result.sort_values(
        "Quality Score",
        ascending=False
    )

# ---------------------------------------------------------
# Show Table
# ---------------------------------------------------------

st.dataframe(
    result,
    use_container_width=True,
    hide_index=True
)

# ---------------------------------------------------------
# CSV Download
# ---------------------------------------------------------

csv = result.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Results as CSV",
    data=csv,
    file_name="stock_screener_results.csv",
    mime="text/csv"
)