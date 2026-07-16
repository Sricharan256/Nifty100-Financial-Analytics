import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

from utils.db import (
    get_companies,
    get_ratios,
    get_market_cap
)

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Sector Analysis",
    layout="wide"
)

st.title("🏭 Sector Analysis")

st.markdown("---")

# ---------------------------------------------------------
# Load Data
# ---------------------------------------------------------

companies = get_companies().rename(
    columns={"id": "company_id"}
)

ratios = get_ratios()

market = get_market_cap()

# ---------------------------------------------------------
# Load Sector Table
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
# Latest Year
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

df = df.loc[:, ~df.columns.duplicated()]

# ---------------------------------------------------------
# Sector Dropdown
# ---------------------------------------------------------

sector_list = sorted(
    df["broad_sector"].dropna().unique()
)

selected_sector = st.selectbox(
    "Select Sector",
    sector_list
)

sector_df = df[
    df["broad_sector"] == selected_sector
]

st.success(
    f"{len(sector_df)} companies found in {selected_sector}"
)
# ---------------------------------------------------------
# Revenue Data
# ---------------------------------------------------------

conn = sqlite3.connect("db/nifty100.db")

pl = pd.read_sql(
    """
    SELECT
        company_id,
        year,
        sales
    FROM profit_loss
    """,
    conn
)

conn.close()

pl["year_num"] = (
    pl["year"]
    .astype(str)
    .str.extract(r"(\d{4})", expand=False)
)

pl = pl.dropna(subset=["year_num"])

pl["year_num"] = pl["year_num"].astype(int)

latest_pl_year = pl["year_num"].max()

pl = pl[
    pl["year_num"] == latest_pl_year
]

# ---------------------------------------------------------
# Merge Revenue
# ---------------------------------------------------------

sector_df = sector_df.merge(

    pl[
        [
            "company_id",
            "sales"
        ]
    ],

    on="company_id",

    how="left"

)

sector_df["sales"] = sector_df["sales"].fillna(0)

# ---------------------------------------------------------
# Bubble Chart
# ---------------------------------------------------------

st.markdown("---")

st.subheader("📊 Sector Bubble Chart")

fig = px.scatter(

    sector_df,

    x="sales",

    y="return_on_equity_pct",

    size="market_cap_crore",

    color="sub_sector",

    hover_name="company_name",

    hover_data=[
        "company_id",
        "pe_ratio",
        "pb_ratio"
    ],

    size_max=60,

    title=f"{selected_sector} Companies"

)

fig.update_layout(

    xaxis_title="Revenue (₹ Cr)",

    yaxis_title="ROE (%)",

    height=650

)

st.plotly_chart(

    fig,

    use_container_width=True

)
# ---------------------------------------------------------
# Sector Median KPI Chart
# ---------------------------------------------------------

st.markdown("---")

st.subheader("📊 Sector Median KPI")

kpi_columns = [
    "return_on_equity_pct",
    "net_profit_margin_pct",
    "operating_profit_margin_pct",
    "debt_to_equity",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "pe_ratio",
    "pb_ratio"
]

median_values = (
    sector_df[kpi_columns]
    .median(numeric_only=True)
    .reset_index()
)

median_values.columns = ["Metric", "Median"]

metric_names = {
    "return_on_equity_pct": "ROE",
    "net_profit_margin_pct": "Net Profit Margin",
    "operating_profit_margin_pct": "OPM",
    "debt_to_equity": "Debt/Equity",
    "revenue_cagr_5yr": "Revenue CAGR",
    "pat_cagr_5yr": "PAT CAGR",
    "pe_ratio": "P/E",
    "pb_ratio": "P/B"
}

median_values["Metric"] = median_values["Metric"].map(metric_names)

fig = px.bar(
    median_values,
    x="Metric",
    y="Median",
    text="Median",
    title=f"{selected_sector} Median Financial KPIs"
)

fig.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside"
)

fig.update_layout(
    height=550,
    xaxis_title="Financial Metrics",
    yaxis_title="Median Value"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
# ---------------------------------------------------------
# Company Count
# ---------------------------------------------------------

st.info(

    f"Bubble chart shows {len(sector_df)} companies."

)