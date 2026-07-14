"""
Sprint 4 - Day 23

Nifty 100 Financial Analytics Dashboard
Main Entry Point
"""

import streamlit as st

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Nifty 100 Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Dashboard Header
# ---------------------------------------------------------

st.title("📈 Nifty 100 Financial Analytics Platform")

st.markdown(
    """
    Welcome to the **Nifty 100 Financial Analytics Dashboard**.

    Use the **sidebar** to navigate between the dashboard screens.
    """
)

st.markdown("---")

# ---------------------------------------------------------
# Home Information
# ---------------------------------------------------------

st.subheader("Dashboard Modules")

col1, col2 = st.columns(2)

with col1:

    st.success("🏠 Home Dashboard")

    st.success("🏢 Company Profile")

    st.success("📊 Financial Screener")

    st.success("👥 Peer Comparison")

with col2:

    st.success("📈 Trend Analysis")

    st.success("🏭 Sector Analysis")

    st.success("💰 Capital Allocation")

    st.success("📄 Annual Reports")

st.markdown("---")

st.info(
    "Select a page from the left sidebar to begin exploring the dashboard."
)