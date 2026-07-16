import streamlit as st
import pandas as pd

from utils.db import (
    get_companies,
    get_reports
)

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Annual Reports",
    layout="wide"
)

st.title("📄 Annual Reports")

st.markdown("---")

# ---------------------------------------------------------
# Load Companies
# ---------------------------------------------------------

companies = get_companies()

company_names = sorted(
    companies["company_name"].tolist()
)

selected_company = st.selectbox(
    "Select Company",
    company_names
)

company_id = companies.loc[
    companies["company_name"] == selected_company,
    "id"
].iloc[0]

# ---------------------------------------------------------
# Load Reports
# ---------------------------------------------------------

reports = get_reports(company_id)

if reports.empty:

    st.warning("No annual reports available.")

    st.stop()

# ---------------------------------------------------------
# Sort Reports
# ---------------------------------------------------------

reports["Year"] = pd.to_numeric(
    reports["Year"],
    errors="coerce"
)

reports = reports.sort_values(
    "Year",
    ascending=False
)

st.success(
    f"{len(reports)} reports found."
)

st.markdown("---")

# ---------------------------------------------------------
# Annual Reports
# ---------------------------------------------------------

st.markdown("---")

st.subheader("📚 Available Annual Reports")

for _, row in reports.iterrows():

    year = int(row["Year"])

    report_url = str(row["Annual_Report"])

    col1, col2 = st.columns([1, 5])

    with col1:

        st.write(f"**{year}**")

    with col2:

        if (
            report_url
            and report_url != "nan"
            and report_url.startswith("http")
        ):

            st.markdown(
                f"[📄 Open Annual Report]({report_url})"
            )

        else:

            st.error("🔴 Report Unavailable")