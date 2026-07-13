"""
Sprint 4 - Day 22

Main Streamlit Application
"""

import streamlit as st


# -----------------------------------------------------
# Page Configuration
# -----------------------------------------------------

st.set_page_config(

    page_title="Nifty 100 Analytics",

    layout="wide",

    initial_sidebar_state="expanded"

)

# -----------------------------------------------------
# Sidebar
# -----------------------------------------------------

st.sidebar.title("Nifty 100 Analytics")

page = st.sidebar.radio(

    "Navigation",

    [

        "Home",

        "Company Profile",

        "Screener",

        "Peer Comparison",

        "Trend Analysis",

        "Sector Analysis",

        "Capital Allocation",

        "Annual Reports"

    ]

)

# -----------------------------------------------------
# Dashboard Title
# -----------------------------------------------------

st.title("📈 Nifty 100 Financial Intelligence Platform")

st.markdown("---")

# -----------------------------------------------------
# Placeholder Pages
# -----------------------------------------------------

if page == "Home":

    st.header("Home")

    st.info("Home screen will be implemented on Day 23.")

elif page == "Company Profile":

    st.header("Company Profile")

    st.info("Company Profile screen will be implemented on Day 23.")

elif page == "Screener":

    st.header("Financial Screener")

    st.info("Screener screen will be implemented on Day 24.")

elif page == "Peer Comparison":

    st.header("Peer Comparison")

    st.info("Peer Comparison screen will be implemented on Day 24.")

elif page == "Trend Analysis":

    st.header("Trend Analysis")

    st.info("Trend Analysis screen will be implemented on Day 25.")

elif page == "Sector Analysis":

    st.header("Sector Analysis")

    st.info("Sector Analysis screen will be implemented on Day 25.")

elif page == "Capital Allocation":

    st.header("Capital Allocation")

    st.info("Capital Allocation screen will be implemented on Day 25.")

elif page == "Annual Reports":

    st.header("Annual Reports")

    st.info("Annual Reports screen will be implemented on Day 25.")