import streamlit as st
import pandas as pd

from utils.db import (
    get_companies,
    get_ratios
)

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Trend Analysis",
    layout="wide"
)

st.title("📈 Trend Analysis")

st.markdown("---")

# ---------------------------------------------------------
# Load Companies
# ---------------------------------------------------------

companies = get_companies()

company_names = companies["company_name"].tolist()

selected_company = st.selectbox(
    "Select Company",
    company_names
)

company_id = companies.loc[
    companies["company_name"] == selected_company,
    "id"
].iloc[0]

# ---------------------------------------------------------
# Load Financial Ratios
# ---------------------------------------------------------

ratios = get_ratios(company_id)

if ratios.empty:

    st.warning("Financial data not available.")

    st.stop()

# ---------------------------------------------------------
# Prepare Year
# ---------------------------------------------------------

ratios["year_num"] = (
    ratios["year"]
    .astype(str)
    .str.extract(r"(\d{4})")
    .astype(int)
)

ratios = ratios.sort_values(
    "year_num"
)

# ---------------------------------------------------------
# Available Metrics
# ---------------------------------------------------------

metrics = {
    "ROE": "return_on_equity_pct",
    "Net Profit Margin": "net_profit_margin_pct",
    "Operating Profit Margin": "operating_profit_margin_pct",
    "Debt / Equity": "debt_to_equity",
    "Interest Coverage": "interest_coverage",
    "Free Cash Flow": "free_cash_flow_cr",
    "Revenue CAGR (5Y)": "revenue_cagr_5yr",
    "PAT CAGR (5Y)": "pat_cagr_5yr",
    "EPS CAGR (5Y)": "eps_cagr_5yr",
    "Asset Turnover": "asset_turnover"
}

selected_metrics = st.multiselect(
    "Select up to 3 metrics",
    list(metrics.keys()),
    default=["ROE"],
    max_selections=3
)

if len(selected_metrics) == 0:

    st.info("Please select at least one metric.")

    st.stop()

st.markdown("---")

st.subheader(selected_company)

st.write("Selected Metrics")

for metric in selected_metrics:

    st.write("•", metric)
# ---------------------------------------------------------
# Trend Analysis Chart
# ---------------------------------------------------------

import plotly.graph_objects as go

st.markdown("---")

st.subheader("📈 10-Year Trend Analysis")

fig = go.Figure()

for metric_name in selected_metrics:

    column = metrics[metric_name]

    fig.add_trace(

        go.Scatter(

            x=ratios["year_num"],

            y=ratios[column],

            mode="lines+markers+text",

            name=metric_name,

            text=[
                ""
                if i == 0
                else f"{((curr-prev)/prev*100):.1f}%"
                if prev not in [0, None] and pd.notna(prev)
                else ""
                for i, (curr, prev) in enumerate(
                    zip(
                        ratios[column],
                        ratios[column].shift(1)
                    )
                )
            ],

            textposition="top center",

            hovertemplate=
                "<b>Year:</b> %{x}<br>"
                "<b>Value:</b> %{y:.2f}"
                "<extra></extra>"

        )

    )

fig.update_layout(

    title="Financial Metric Trends",

    xaxis_title="Year",

    yaxis_title="Metric Value",

    hovermode="x unified",

    legend_title="Metrics",

    height=650

)

st.plotly_chart(

    fig,

    use_container_width=True

)

# ---------------------------------------------------------
# Data Table
# ---------------------------------------------------------

st.markdown("---")

st.subheader("Trend Data")

table_columns = ["year_num"]

for metric_name in selected_metrics:

    table_columns.append(
        metrics[metric_name]
    )

table = ratios[
    table_columns
].copy()

rename_dict = {

    "year_num": "Year"

}

for metric_name in selected_metrics:

    rename_dict[
        metrics[metric_name]
    ] = metric_name

table.rename(

    columns=rename_dict,

    inplace=True

)

st.dataframe(

    table,

    use_container_width=True,

    hide_index=True

)

# ---------------------------------------------------------
# Download CSV
# ---------------------------------------------------------

csv = table.to_csv(

    index=False

).encode("utf-8")

st.download_button(

    "📥 Download Trend Data",

    csv,

    file_name=f"{company_id}_trend_analysis.csv",

    mime="text/csv"

)