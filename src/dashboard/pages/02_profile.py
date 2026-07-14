import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go

from utils.db import (
    get_companies,
    get_pl,
    get_analysis,
    get_pros_cons,
    get_sectors
)

st.title("🏢 Company Profile")

# -------------------------------------------------------
# Load Data
# -------------------------------------------------------

companies = get_companies()

company_list = sorted(companies["id"].tolist())

selected = st.selectbox(
    "Select Company",
    company_list
)

if not selected:
    st.stop()

company = companies[
    companies["id"] == selected
]

if company.empty:

    st.warning("Ticker not found — please try another.")

    st.stop()

company = company.iloc[0]
# -------------------------------------------------------
# SQLite
# -------------------------------------------------------

conn = sqlite3.connect("db/nifty100.db")

ratios = pd.read_sql(
    """
    SELECT *
    FROM financial_ratios
    WHERE company_id=?
    """,
    conn,
    params=[selected]
)

market = pd.read_sql(
    """
    SELECT *
    FROM market_cap
    WHERE company_id=?
    """,
    conn,
    params=[selected]
)

conn.close()

pl = get_pl(selected)
analysis = get_analysis(selected)
proscons = get_pros_cons(selected)
conn = sqlite3.connect("db/nifty100.db")

sector = pd.read_sql(
    """
    SELECT *
    FROM sectors
    WHERE company_id=?
    """,
    conn,
    params=[selected]
)

conn.close()
if not sector.empty:

    st.write("**Sector:**", sector.iloc[0]["broad_sector"])
    st.write("**Sub Sector:**", sector.iloc[0]["sub_sector"])
# -------------------------------------------------------
# Company Card
# -------------------------------------------------------

st.subheader(company["company_name"])

col1, col2 = st.columns([1,3])

with col1:

    logo = company["company_logo"]

    if pd.notna(logo) and str(logo).strip():

        try:
            st.image(
                logo,
                width=120
            )

        except Exception:

            st.info("Company logo unavailable.")

    else:

        st.info("Company logo unavailable.")

with col2:

    st.write("**Ticker:**", company["id"])

    if not sector.empty:

        st.write(
            "**Sector:**",
            sector.iloc[0]["broad_sector"]
        )

        st.write(
            "**Sub Sector:**",
            sector.iloc[0]["sub_sector"]
        )

    st.write(company["about_company"])

st.markdown("---")

# -------------------------------------------------------
# Latest Data
# -------------------------------------------------------

latest = ratios.iloc[-1]

# latest FCF

fcf = latest["free_cash_flow_cr"]

# latest ROE

roe = latest["return_on_equity_pct"]

# latest DE

de = latest["debt_to_equity"]

# latest margin

npm = latest["net_profit_margin_pct"]

# latest ROCE

roce = company["roce_percentage"]

# CAGR

rev = latest["revenue_cagr_5yr"]

# -------------------------------------------------------
# KPI Tiles
# -------------------------------------------------------

c1,c2,c3 = st.columns(3)

c1.metric(
    "ROE",
    f"{roe:.2f}%"
)

c2.metric(
    "ROCE",
    f"{roce:.2f}%"
)

c3.metric(
    "Net Profit Margin",
    f"{npm:.2f}%"
)

c4,c5,c6 = st.columns(3)

c4.metric(
    "Debt / Equity",
    round(de,2)
)

c5.metric(
    "Revenue CAGR 5Y",
    rev
)

c6.metric(
    "Free Cash Flow",
    round(fcf,2)
)

st.markdown("---")

# -------------------------------------------------------
# Revenue vs Net Profit
# -------------------------------------------------------

st.subheader("Revenue vs Net Profit")

fig = px.bar(
    pl,
    x="year",
    y=[
        "sales",
        "net_profit"
    ],
    barmode="group"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------------------------------------
# ROE ROCE Trend
# -------------------------------------------------------

st.subheader("ROE vs ROCE")

fig = go.Figure()

fig.add_trace(

    go.Scatter(

        x=ratios["year"],

        y=ratios["return_on_equity_pct"],

        mode="lines+markers",

        name="ROE"

    )

)

fig.add_trace(

    go.Scatter(

        x=ratios["year"],

        y=[company["roce_percentage"]]*len(ratios),

        mode="lines",

        name="ROCE"

    )

)

st.plotly_chart(

    fig,

    use_container_width=True

)

# -------------------------------------------------------
# Pros & Cons
# -------------------------------------------------------

st.subheader("Pros & Cons")

if proscons.empty:

    st.info("Pros & Cons are not available for this company.")

else:

    left, right = st.columns(2)

    with left:

        st.success("Pros")

        pros = str(proscons.iloc[0]["pros"])

        if pros.strip():

            for item in pros.split("."):

                if item.strip():

                    st.write(f"✅ {item.strip()}")

        else:

            st.write("No Pros available.")

    with right:

        st.error("Cons")

        cons = str(proscons.iloc[0]["cons"])

        if cons.strip():

            for item in cons.split("."):

                if item.strip():

                    st.write(f"❌ {item.strip()}")

        else:

            st.write("No Cons available.")