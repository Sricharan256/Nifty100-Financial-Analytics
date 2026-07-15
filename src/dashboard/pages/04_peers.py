import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go

from utils.db import (
    get_companies,
    get_peer_groups,
    get_ratios
)

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Peer Comparison",
    layout="wide"
)

st.title("👥 Peer Comparison")

st.markdown("---")

# ---------------------------------------------------------
# Load Data
# ---------------------------------------------------------

companies = get_companies()

conn = sqlite3.connect("db/nifty100.db")

peer_groups = pd.read_sql(
    """
    SELECT *
    FROM peer_groups
    """,
    conn
)

conn.close()

# ---------------------------------------------------------
# Peer Group Selection
# ---------------------------------------------------------

group_names = sorted(
    peer_groups["peer_group_name"].unique()
)

selected_group = st.selectbox(
    "Select Peer Group",
    group_names
)

# ---------------------------------------------------------
# Companies in Selected Group
# ---------------------------------------------------------

group_df = peer_groups[
    peer_groups["peer_group_name"] == selected_group
]

company_list = sorted(
    group_df["company_id"].tolist()
)

selected_company = st.selectbox(
    "Select Company",
    company_list
)

# ---------------------------------------------------------
# Company Information
# ---------------------------------------------------------

company = companies[
    companies["id"] == selected_company
]

if company.empty:

    st.warning("Company not found.")

    st.stop()

company = company.iloc[0]

st.markdown("---")

col1, col2 = st.columns([1,3])

with col1:

    logo = company["company_logo"]

    if pd.notna(logo):

        try:

            st.image(
                logo,
                width=120
            )

        except:

            st.info("Logo unavailable.")

with col2:

    st.subheader(company["company_name"])

    st.write(
        f"**Ticker:** {company['id']}"
    )

    st.write(
        f"**Benchmark Company:** {'Yes' if group_df[group_df['company_id']==selected_company]['is_benchmark'].iloc[0] else 'No'}"
    )

st.markdown("---")

# ---------------------------------------------------------
# Financial Ratios
# ---------------------------------------------------------

ratios = get_ratios(selected_company)

if ratios.empty:

    st.warning("Financial ratios not available.")

    st.stop()

latest = ratios.iloc[-1]

st.success("Peer data loaded successfully.")
# ---------------------------------------------------------
# Prepare Peer Comparison Data
# ---------------------------------------------------------

peer_ratios = []

for ticker in company_list:

    df = get_ratios(ticker)

    if not df.empty:

        peer_ratios.append(df.iloc[-1])

peer_df = pd.DataFrame(peer_ratios)

# ---------------------------------------------------------
# Metrics for Radar Chart
# ---------------------------------------------------------

metrics = [
    "return_on_equity_pct",
    "net_profit_margin_pct",
    "operating_profit_margin_pct",
    "debt_to_equity",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "asset_turnover",
    "free_cash_flow_cr"
]

metric_labels = [
    "ROE",
    "NPM",
    "OPM",
    "D/E",
    "Revenue CAGR",
    "PAT CAGR",
    "Asset Turnover",
    "FCF"
]

# ---------------------------------------------------------
# Selected Company Values
# ---------------------------------------------------------

company_values = []

for metric in metrics:

    value = latest.get(metric, 0)

    if pd.isna(value):

        value = 0

    company_values.append(float(value))

# ---------------------------------------------------------
# Peer Average Values
# ---------------------------------------------------------

peer_average = []

for metric in metrics:

    value = peer_df[metric].fillna(0).mean()

    peer_average.append(float(value))

# Close the radar chart
company_values.append(company_values[0])
peer_average.append(peer_average[0])

labels = metric_labels + [metric_labels[0]]

# ---------------------------------------------------------
# Radar Chart
# ---------------------------------------------------------

st.subheader("📊 Company vs Peer Group")

fig = go.Figure()

fig.add_trace(

    go.Scatterpolar(

        r=company_values,

        theta=labels,

        fill="toself",

        name=selected_company

    )

)

fig.add_trace(

    go.Scatterpolar(

        r=peer_average,

        theta=labels,

        fill="toself",

        name="Peer Average"

    )

)

fig.update_layout(

    polar=dict(

        radialaxis=dict(

            visible=True

        )

    ),

    showlegend=True,

    height=650

)

st.plotly_chart(

    fig,

    use_container_width=True

)

st.markdown("---")
# ---------------------------------------------------------
# KPI Comparison Table
# ---------------------------------------------------------

st.subheader("📋 Peer Comparison Table")

comparison = peer_df.merge(
    companies.rename(columns={"id": "company_id"}),
    on="company_id",
    how="left"
)

comparison = comparison.merge(
    group_df[
        ["company_id", "is_benchmark"]
    ],
    on="company_id",
    how="left"
)

columns = [
    "company_id",
    "company_name",
    "is_benchmark",
    "return_on_equity_pct",
    "net_profit_margin_pct",
    "operating_profit_margin_pct",
    "debt_to_equity",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "free_cash_flow_cr",
    "composite_quality_score"
]

comparison = comparison[columns]

comparison = comparison.rename(
    columns={
        "company_id": "Ticker",
        "company_name": "Company",
        "is_benchmark": "Benchmark",
        "return_on_equity_pct": "ROE %",
        "net_profit_margin_pct": "NPM %",
        "operating_profit_margin_pct": "OPM %",
        "debt_to_equity": "D/E",
        "revenue_cagr_5yr": "Revenue CAGR %",
        "pat_cagr_5yr": "PAT CAGR %",
        "free_cash_flow_cr": "FCF",
        "composite_quality_score": "Quality Score"
    }
)

comparison["Benchmark"] = comparison["Benchmark"].apply(
    lambda x: "⭐ Yes" if x else ""
)

comparison = comparison.sort_values(
    "Quality Score",
    ascending=False
)

st.dataframe(
    comparison,
    use_container_width=True,
    hide_index=True
)

# ---------------------------------------------------------
# Summary
# ---------------------------------------------------------

st.markdown("---")

benchmark_count = (
    comparison["Benchmark"] == "⭐ Yes"
).sum()

st.metric(
    "Companies in Peer Group",
    len(comparison)
)

st.metric(
    "Benchmark Companies",
    benchmark_count
)

st.success("Peer comparison completed successfully.")