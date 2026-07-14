"""
Sprint 4 - Day 23

Home Dashboard
"""

import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px

from utils.db import (
    get_companies,
    get_sectors,
    get_valuation
)

# ----------------------------------------------------------
# Page Configuration
# ----------------------------------------------------------

st.set_page_config(
    page_title="Home Dashboard",
    layout="wide"
)

st.title("🏠 Home Dashboard")
st.markdown("---")

# ----------------------------------------------------------
# Sidebar
# ----------------------------------------------------------

selected_year = st.sidebar.selectbox(
    "Select Financial Year",
    [2019, 2020, 2021, 2022, 2023, 2024],
    index=5
)

# ----------------------------------------------------------
# Load Companies
# ----------------------------------------------------------

companies = get_companies()

# ----------------------------------------------------------
# Load Financial Ratios
# ----------------------------------------------------------

conn = sqlite3.connect("db/nifty100.db")

ratios = pd.read_sql(
    """
    SELECT *
    FROM financial_ratios
    """,
    conn
)

market_cap = pd.read_sql(
    """
    SELECT *
    FROM market_cap
    """,
    conn
)

sectors = pd.read_sql(
    """
    SELECT *
    FROM sectors
    """,
    conn
)

conn.close()

# ----------------------------------------------------------
# Prepare Year Column
# ----------------------------------------------------------

ratios["year_num"] = (
    ratios["year"]
    .astype(str)
    .str.extract(r"(\d{4})")
    .astype(int)
)

latest = ratios[
    ratios["year_num"] == selected_year
].copy()

market_latest = market_cap[
    market_cap["year"] == selected_year
].copy()

# ----------------------------------------------------------
# KPI Calculations
# ----------------------------------------------------------

average_roe = round(
    latest["return_on_equity_pct"].mean(),
    2
)

median_de = round(
    latest["debt_to_equity"].median(),
    2
)

median_revenue = round(
    pd.to_numeric(
        latest["revenue_cagr_5yr"],
        errors="coerce"
    ).median(),
    2
)

median_pe = round(
    market_latest["pe_ratio"].median(),
    2
)

total_companies = companies.shape[0]

debt_free = latest[
    latest["debt_to_equity"] <= 0
].shape[0]
# ----------------------------------------------------------
# KPI Cards
# ----------------------------------------------------------

st.subheader("📊 Financial Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Average ROE",
        f"{average_roe:.2f}%"
    )

with col2:
    st.metric(
        "Median P/E",
        f"{median_pe:.2f}"
    )

with col3:
    st.metric(
        "Median D/E",
        f"{median_de:.2f}"
    )

col4, col5, col6 = st.columns(3)

with col4:
    st.metric(
        "Total Companies",
        total_companies
    )

with col5:
    st.metric(
        "Median Revenue CAGR (5Y)",
        f"{median_revenue:.2f}%"
    )

with col6:
    st.metric(
        "Debt-Free Companies",
        debt_free
    )

st.markdown("---")

# ----------------------------------------------------------
# Sector Breakdown Donut Chart
# ----------------------------------------------------------

st.subheader("🏭 Sector Breakdown")

sector_counts = (
    sectors.groupby("broad_sector")
    .size()
    .reset_index(name="Company Count")
)

fig = px.pie(
    sector_counts,
    names="broad_sector",
    values="Company Count",
    hole=0.45,
    title="Companies by Broad Sector"
)

fig.update_layout(
    height=500,
    legend_title="Sector"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown("---")

# ----------------------------------------------------------
# Top 5 Companies by Composite Quality Score
# ----------------------------------------------------------

st.subheader("🏆 Top 5 Companies by Composite Quality Score")

top5 = (
    latest.sort_values(
        "composite_quality_score",
        ascending=False
    )
    .head(5)
)

top5 = top5.merge(
    companies,
    left_on="company_id",
    right_on="id",
    how="left"
)

top5 = top5[
    [
        "company_id",
        "company_name",
        "return_on_equity_pct",
        "debt_to_equity",
        "revenue_cagr_5yr",
        "composite_quality_score"
    ]
]

top5.columns = [
    "Ticker",
    "Company",
    "ROE %",
    "D/E",
    "Revenue CAGR 5Y",
    "Quality Score"
]

st.dataframe(
    top5,
    use_container_width=True,
    hide_index=True
)