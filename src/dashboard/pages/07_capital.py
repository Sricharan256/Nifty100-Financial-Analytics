import streamlit as st
import pandas as pd
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
    page_title="Capital Allocation Map",
    layout="wide"
)

st.title("💰 Capital Allocation Map")

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
# Prepare Ratios
# ---------------------------------------------------------

ratios["year_num"] = (
    ratios["year"]
    .astype(str)
    .str.extract(r"(\d{4})", expand=False)
)

ratios = ratios.dropna(subset=["year_num"])

ratios["year_num"] = ratios["year_num"].astype(int)

# Latest record for each company
ratios = (
    ratios
    .sort_values("year_num")
    .groupby("company_id", as_index=False)
    .tail(1)
)

# ---------------------------------------------------------
# Prepare Market Cap
# ---------------------------------------------------------

market["year"] = pd.to_numeric(
    market["year"],
    errors="coerce"
)

market = market.dropna(subset=["year"])

market["year"] = market["year"].astype(int)

market = (
    market
    .sort_values("year")
    .groupby("company_id", as_index=False)
    .tail(1)
)

# ---------------------------------------------------------
# Merge Tables
# ---------------------------------------------------------

df = ratios.merge(
    companies,
    on="company_id",
    how="left"
)

df = df.merge(
    market[
        [
            "company_id",
            "market_cap_crore",
            "pe_ratio",
            "pb_ratio",
            "dividend_yield_pct"
        ]
    ],
    on="company_id",
    how="left"
)

# Remove duplicate columns
df = df.loc[:, ~df.columns.duplicated()]

# ---------------------------------------------------------
# Fill Missing Values
# ---------------------------------------------------------

numeric_cols = df.select_dtypes(include="number").columns

df[numeric_cols] = df[numeric_cols].fillna(0)

# Remove rows with missing company names
df = df.dropna(subset=["company_name"])

df = df[
    df["company_name"].astype(str).str.strip() != ""
]

st.success(
    f"{len(df)} companies loaded successfully."
)

st.markdown("---")
# ---------------------------------------------------------
# Clean Numeric Columns
# ---------------------------------------------------------

numeric_cols = [
    "return_on_equity_pct",
    "debt_to_equity",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "free_cash_flow_cr",
    "capex_cr",
    "dividend_payout_ratio_pct",
    "market_cap_crore"
]

for col in numeric_cols:

    if col in df.columns:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        ).fillna(0)

# ---------------------------------------------------------
# Capital Allocation Classification
# ---------------------------------------------------------

def classify_company(row):

    roe = row["return_on_equity_pct"]
    de = row["debt_to_equity"]
    revenue = row["revenue_cagr_5yr"]
    pat = row["pat_cagr_5yr"]
    fcf = row["free_cash_flow_cr"]
    capex = row["capex_cr"]
    payout = row["dividend_payout_ratio_pct"]

    if de == 0:
        return "Debt Free"

    elif roe >= 20 and revenue >= 15:
        return "Compounder"

    elif revenue >= 20 and pat >= 20:
        return "Growth"

    elif payout >= 40:
        return "Dividend"

    elif capex >= df["capex_cr"].median():
        return "High Capex"

    elif pat < 0:
        return "Turnaround"

    elif roe >= 15 and fcf > 0:
        return "Efficient"

    else:
        return "Value"

df["capital_pattern"] = df.apply(
    classify_company,
    axis=1
)

# ---------------------------------------------------------
# Remove Invalid Rows
# ---------------------------------------------------------

df = df.dropna(
    subset=[
        "company_name",
        "capital_pattern"
    ]
)

df = df[
    df["company_name"].astype(str).str.strip() != ""
]

# ---------------------------------------------------------
# Treemap
# ---------------------------------------------------------

st.subheader("🌳 Capital Allocation Treemap")

fig = px.treemap(

    df,

    path=[
        px.Constant("Capital Allocation"),
        "capital_pattern",
        "company_name"
    ],

    values="market_cap_crore",

    color="capital_pattern",

    hover_name="company_name",

    hover_data={
        "company_id": True,
        "return_on_equity_pct": True,
        "debt_to_equity": True,
        "revenue_cagr_5yr": True,
        "market_cap_crore": True
    }

)

fig.update_layout(

    height=750,

    margin=dict(
        t=40,
        l=20,
        r=20,
        b=20
    )

)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------------
# Pattern Summary
# ---------------------------------------------------------

summary = (

    df.groupby("capital_pattern")

      .agg(

          Companies=("company_id", "count"),

          Avg_ROE=("return_on_equity_pct", "mean"),

          Avg_Revenue_CAGR=("revenue_cagr_5yr", "mean")

      )

      .reset_index()

      .sort_values(

          "Companies",

          ascending=False

      )

)

st.markdown("---")

st.subheader("📊 Capital Allocation Summary")

st.dataframe(

    summary,

    use_container_width=True,

    hide_index=True

)
# ---------------------------------------------------------
# Pattern Filter
# ---------------------------------------------------------

st.markdown("---")

st.subheader("📋 Companies by Capital Allocation Pattern")

pattern_list = sorted(
    df["capital_pattern"].unique()
)

selected_pattern = st.selectbox(
    "Select Capital Allocation Pattern",
    pattern_list
)

pattern_df = df[
    df["capital_pattern"] == selected_pattern
].copy()

st.success(
    f"{len(pattern_df)} companies found in '{selected_pattern}'"
)

# ---------------------------------------------------------
# Display Table
# ---------------------------------------------------------

display_cols = [
    "company_id",
    "company_name",
    "return_on_equity_pct",
    "debt_to_equity",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "free_cash_flow_cr",
    "market_cap_crore",
    "pe_ratio",
    "pb_ratio",
    "dividend_yield_pct"
]

display_cols = [
    col
    for col in display_cols
    if col in pattern_df.columns
]

result = pattern_df[
    display_cols
].copy()

result = result.rename(
    columns={
        "company_id": "Ticker",
        "company_name": "Company",
        "return_on_equity_pct": "ROE %",
        "debt_to_equity": "Debt/Equity",
        "revenue_cagr_5yr": "Revenue CAGR %",
        "pat_cagr_5yr": "PAT CAGR %",
        "free_cash_flow_cr": "Free Cash Flow",
        "market_cap_crore": "Market Cap (₹ Cr)",
        "pe_ratio": "P/E",
        "pb_ratio": "P/B",
        "dividend_yield_pct": "Dividend Yield %"
    }
)

if "ROE %" in result.columns:
    result = result.sort_values(
        "ROE %",
        ascending=False
    )

st.dataframe(
    result,
    use_container_width=True,
    hide_index=True
)

# ---------------------------------------------------------
# Download CSV
# ---------------------------------------------------------

csv = result.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="📥 Download Company List",
    data=csv,
    file_name=f"{selected_pattern.lower().replace(' ','_')}_companies.csv",
    mime="text/csv"
)

# ---------------------------------------------------------
# Pattern Statistics
# ---------------------------------------------------------

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Companies",
        len(result)
    )

with col2:
    if "ROE %" in result.columns:
        st.metric(
            "Average ROE",
            f"{result['ROE %'].mean():.2f}%"
        )

with col3:
    if "Market Cap (₹ Cr)" in result.columns:
        st.metric(
            "Average Market Cap",
            f"{result['Market Cap (₹ Cr)'].mean():,.0f}"
        )

st.success("✅ Capital Allocation Map completed successfully.")