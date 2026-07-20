import os
import sqlite3
import pandas as pd

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)

# ------------------------------------
# Configuration
# ------------------------------------

DB_PATH = "db/nifty100.db"

REPORT_DIR = "reports/portfolio"

os.makedirs(REPORT_DIR, exist_ok=True)

conn = sqlite3.connect(DB_PATH)

styles = getSampleStyleSheet()

title_style = styles["Heading1"]
heading_style = styles["Heading2"]
normal_style = styles["BodyText"]

# ------------------------------------
# Load Companies
# ------------------------------------

companies = pd.read_sql("""
SELECT
    c.id,
    c.company_name,
    s.broad_sector
FROM companies c

LEFT JOIN sectors s
ON c.id=s.company_id

ORDER BY c.id
""", conn)

print("Companies Loaded :", len(companies))
def latest_ratios(company_id):

    query = """
    SELECT *
    FROM financial_ratios
    WHERE company_id=?
    ORDER BY year DESC
    LIMIT 1
    """

    return pd.read_sql(
        query,
        conn,
        params=[company_id]
    )
def trend_arrow(values):

    values = pd.to_numeric(
        values,
        errors="coerce"
    ).dropna()

    if len(values) < 2:
        return "→"

    latest = values.iloc[0]
    previous = values.iloc[1]

    if previous == 0:
        return "→"

    change = ((latest - previous) / abs(previous)) * 100

    if change > 2:
        return "↑"

    elif change < -2:
        return "↓"

    else:
        return "→"
# ------------------------------------
# Build Portfolio Summary PDF
# ------------------------------------

pdf = SimpleDocTemplate(
    "reports/portfolio/portfolio_summary.pdf"
)

story = []

for _, company in companies.iterrows():

    ratios = latest_ratios(company["id"])

    story.append(
        Paragraph(
            company["company_name"],
            title_style
        )
    )

    story.append(
        Paragraph(
            f"<b>Ticker:</b> {company['id']}",
            normal_style
        )
    )

    story.append(
        Paragraph(
            f"<b>Sector:</b> {company['broad_sector']}",
            normal_style
        )
    )

    story.append(Spacer(1,12))

    if ratios.empty:

        story.append(
            Paragraph(
                "No financial ratio data available.",
                normal_style
            )
        )

        story.append(PageBreak())

        continue

    ratio_history = pd.read_sql(
        """
        SELECT *
        FROM financial_ratios
        WHERE company_id=?
        ORDER BY year DESC
        LIMIT 2
        """,
        conn,
        params=[company["id"]]
    )

    metrics = [

        ("ROE (%)", "return_on_equity_pct"),

        ("Debt / Equity", "debt_to_equity"),

        ("Free Cash Flow (Cr)", "free_cash_flow_cr"),

        ("EPS", "earnings_per_share"),

        ("Book Value", "book_value_per_share"),

        ("Quality Score", "composite_quality_score")

    ]

    for title, column in metrics:

        value = ratios.iloc[0][column]

        arrow = trend_arrow(
            ratio_history[column]
        )

        story.append(
            Paragraph(
                f"<b>{title}</b> : {value} {arrow}",
                normal_style
            )
        )

    story.append(PageBreak())

pdf.build(story)

conn.close()

print()
print("Portfolio Summary Generated Successfully")
print("Location : reports/portfolio/portfolio_summary.pdf")