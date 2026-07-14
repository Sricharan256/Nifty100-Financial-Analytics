"""
Sprint 4 - Day 22

Shared Database Utility
"""

import sqlite3
import pandas as pd
import streamlit as st

DB_PATH = "db/nifty100.db"


# ---------------------------------------------------------
# SQLite Connection
# ---------------------------------------------------------

def get_connection():

    return sqlite3.connect(DB_PATH)


# ---------------------------------------------------------
# Companies
# ---------------------------------------------------------

@st.cache_data(ttl=600)
def get_companies():

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT
            id,
            company_name,
            company_logo,
            about_company,
            website,
            nse_profile,
            bse_profile,
            face_value,
            book_value,
            roce_percentage,
            roe_percentage
        FROM companies
        ORDER BY company_name
        """,
        conn
    )

    conn.close()

    return df


# ---------------------------------------------------------
# Financial Ratios
# ---------------------------------------------------------

def get_ratios(ticker=None, year=None):

    conn = get_connection()

    sql = "SELECT * FROM financial_ratios"
    params = []

    if ticker is not None:
        sql += " WHERE company_id=?"
        params.append(ticker)

        if year is not None:
            sql += " AND year=?"
            params.append(year)

    elif year is not None:
        sql += " WHERE year=?"
        params.append(year)

    sql += " ORDER BY company_id, year"

    df = pd.read_sql(
        sql,
        conn,
        params=params
    )

    conn.close()

    return df
# ---------------------------------------------------------
# Load All Financial Ratios
# ---------------------------------------------------------
@st.cache_data(ttl=600)
def get_all_ratios():

    conn = get_connection()

    df = pd.read_sql(

        """
        SELECT *
        FROM financial_ratios
        """,

        conn

    )

    conn.close()

    return df
# ---------------------------------------------------------
# Profit & Loss
# ---------------------------------------------------------

@st.cache_data(ttl=600)
def get_pl(ticker):

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM profit_loss
        WHERE company_id=?
        ORDER BY year
        """,
        conn,
        params=[ticker]
    )

    conn.close()

    return df


# ---------------------------------------------------------
# Balance Sheet
# ---------------------------------------------------------

@st.cache_data(ttl=600)
def get_bs(ticker):

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM balance_sheet
        WHERE company_id=?
        ORDER BY year
        """,
        conn,
        params=[ticker]
    )

    conn.close()

    return df


# ---------------------------------------------------------
# Cash Flow
# ---------------------------------------------------------

@st.cache_data(ttl=600)
def get_cf(ticker):

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM cash_flow
        WHERE company_id=?
        ORDER BY year
        """,
        conn,
        params=[ticker]
    )

    conn.close()

    return df


# ---------------------------------------------------------
# Sectors
# ---------------------------------------------------------

@st.cache_data(ttl=600)
def get_sectors():

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT DISTINCT
            broad_sector
        FROM sectors
        ORDER BY broad_sector
        """,
        conn
    )

    conn.close()

    return df


# ---------------------------------------------------------
# Sector Details
# ---------------------------------------------------------

@st.cache_data(ttl=600)
def get_sector_companies(sector):

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM sectors
        WHERE broad_sector=?
        """,
        conn,
        params=[sector]
    )

    conn.close()

    return df


# ---------------------------------------------------------
# Peer Groups
# ---------------------------------------------------------

@st.cache_data(ttl=600)
def get_peer_groups():

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT DISTINCT
            peer_group_name
        FROM peer_groups
        ORDER BY peer_group_name
        """,
        conn
    )

    conn.close()

    return df


# ---------------------------------------------------------
# Peer Companies
# ---------------------------------------------------------

@st.cache_data(ttl=600)
def get_peers(group_name):

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM peer_percentiles
        WHERE peer_group_name=?
        """,
        conn,
        params=[group_name]
    )

    conn.close()

    return df


# ---------------------------------------------------------
# Market Valuation
# ---------------------------------------------------------

@st.cache_data(ttl=600)
def get_valuation(ticker):

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM market_cap
        WHERE company_id=?
        ORDER BY year
        """,
        conn,
        params=[ticker]
    )

    conn.close()

    return df


# ---------------------------------------------------------
# Analysis
# ---------------------------------------------------------

@st.cache_data(ttl=600)
def get_analysis(ticker):

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM analysis
        WHERE company_id=?
        """,
        conn,
        params=[ticker]
    )

    conn.close()

    return df


# ---------------------------------------------------------
# Pros & Cons
# ---------------------------------------------------------

@st.cache_data(ttl=600)
def get_pros_cons(ticker):

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM pros_cons
        WHERE company_id=?
        """,
        conn,
        params=[ticker]
    )

    conn.close()

    return df


# ---------------------------------------------------------
# Annual Reports
# ---------------------------------------------------------

@st.cache_data(ttl=600)
def get_reports(ticker):

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM documents
        WHERE company_id=?
        ORDER BY Year DESC
        """,
        conn,
        params=[ticker]
    )

    conn.close()

    return df
