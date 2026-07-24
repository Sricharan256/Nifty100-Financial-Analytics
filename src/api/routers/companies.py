from fastapi import APIRouter
from src.api.database import get_connection
import pandas as pd
import numpy as np

router = APIRouter()


@router.get("/companies")
def get_companies():

    conn = get_connection()

    query = """
    SELECT
        c.id,
        c.company_name,
        s.broad_sector
    FROM companies c
    LEFT JOIN sectors s
    ON c.id = s.company_id
    ORDER BY c.company_name
"""

    df = pd.read_sql(query, conn)

    conn.close()

    return df.to_dict(orient="records")
@router.get("/companies/{ticker}")
def get_company(ticker: str):

    conn = get_connection()

    query = """
SELECT

    c.*,
    s.broad_sector,
    s.sub_sector,

    fr.return_on_equity_pct,
    fr.debt_to_equity,
    fr.operating_profit_margin_pct,
    fr.free_cash_flow_cr,
    fr.composite_quality_score,
    fr.earnings_per_share,
    fr.book_value_per_share

FROM companies c

LEFT JOIN sectors s
ON c.id = s.company_id

LEFT JOIN financial_ratios fr
ON c.id = fr.company_id

WHERE c.id = ?

ORDER BY fr.year DESC

LIMIT 1
"""

    df = pd.read_sql(
        query,
        conn,
        params=[ticker]
    )

    conn.close()

    if df.empty:

        return {
            "error": "Ticker not found"
        }

    return df.iloc[0].to_dict()
@router.get("/companies/{ticker}/pl")
def company_profit_loss(ticker: str):

    conn = get_connection()

    query = """
    SELECT p.*

    FROM profit_loss p

    JOIN companies c
        ON p.company_id = c.id

    WHERE c.id = ?

    ORDER BY p.year
    """

    df = pd.read_sql(
    query,
    conn,
    params=[ticker]
)

    conn.close()

# Replace NaN with None so JSON can serialize it
    df = df.where(pd.notnull(df), None)

    import numpy as np

# Convert dataframe to object dtype first
    f = df.astype(object)

# Replace NaN with None
    df = df.replace({np.nan: None})

    return df.to_dict(orient="records")
@router.get("/companies/{ticker}/bs")
def company_balance_sheet(ticker: str):

    conn = get_connection()

    query = """
    SELECT b.*

    FROM balance_sheet b

    JOIN companies c
        ON b.company_id = c.id

    WHERE c.id = ?

    ORDER BY b.year
    """

    df = pd.read_sql(query, conn, params=[ticker])

    conn.close()

    df = df.astype(object)
    df = df.replace({np.nan: None})

    return df.to_dict(orient="records")
@router.get("/companies/{ticker}/cashflow")
def company_cashflow(ticker: str):

    conn = get_connection()

    query = """
    SELECT cf.*

    FROM cash_flow cf

    JOIN companies c
        ON cf.company_id = c.id

    WHERE c.id = ?

    ORDER BY cf.year
    """

    df = pd.read_sql(query, conn, params=[ticker])

    conn.close()

    df = df.astype(object)
    df = df.replace({np.nan: None})

    return df.to_dict(orient="records")
@router.get("/companies/{ticker}/ratios")
def company_ratios(ticker: str):

    conn = get_connection()

    query = """
    SELECT fr.*

    FROM financial_ratios fr

    JOIN companies c
        ON fr.company_id = c.id

    WHERE c.id = ?

    ORDER BY fr.year
    """

    df = pd.read_sql(query, conn, params=[ticker])

    conn.close()

    df = df.astype(object)
    df = df.replace({np.nan: None})

    return df.to_dict(orient="records")
from fastapi.responses import FileResponse
import os


@router.get("/companies/{ticker}/tearsheet")
def company_tearsheet(ticker: str):

    pdf_path = os.path.join(
        "reports",
        "tearsheets",
        f"{ticker}.pdf"
    )

    if not os.path.exists(pdf_path):
        return {"error": "Tearsheet not found"}

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=f"{ticker}.pdf"
    )