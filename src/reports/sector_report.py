import os
import sqlite3
import pandas as pd

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

# ------------------------------------
# Configuration
# ------------------------------------

DB_PATH = "db/nifty100.db"
REPORT_DIR = "reports/sector"

os.makedirs(REPORT_DIR, exist_ok=True)

conn = sqlite3.connect(DB_PATH)

styles = getSampleStyleSheet()

title_style = styles["Heading1"]
heading_style = styles["Heading2"]
normal_style = styles["BodyText"]

# ------------------------------------
# Load Data
# ------------------------------------

sector_df = pd.read_sql(
    """
    SELECT
        s.broad_sector,
        c.id,
        c.company_name,

        fr.return_on_equity_pct,
        fr.debt_to_equity,
        fr.free_cash_flow_cr,

        mc.market_cap_crore,
        mc.dividend_yield_pct,

        fr.dividend_payout_ratio_pct,
        fr.revenue_cagr_5yr,
        fr.pat_cagr_5yr

    FROM sectors s

    JOIN companies c
        ON s.company_id = c.id

    LEFT JOIN financial_ratios fr
        ON c.id = fr.company_id

    LEFT JOIN market_cap mc
        ON c.id = mc.company_id

    ORDER BY s.broad_sector, c.company_name
    """,
    conn
)

print("Rows Loaded :", len(sector_df))
print("Sectors :", sector_df["broad_sector"].nunique())


# ------------------------------------
# Sector Summary
# ------------------------------------

def sector_summary(df):

    numeric_cols = [
        "return_on_equity_pct",
        "debt_to_equity",
        "free_cash_flow_cr",
        "market_cap_crore",
        "dividend_payout_ratio_pct",
        "dividend_yield_pct"
    ]

    summary = (
        df[numeric_cols]
        .apply(pd.to_numeric, errors="coerce")
        .median()
        .round(2)
    )

    return summary


# ------------------------------------
# Generate Sector Reports
# ------------------------------------

for sector in sorted(sector_df["broad_sector"].dropna().unique()):

    sector_data = sector_df[
        sector_df["broad_sector"] == sector
    ]

    filename = sector.replace("/", "-").replace(" ", "_")

    pdf = SimpleDocTemplate(
        f"{REPORT_DIR}/{filename}_report.pdf"
    )

    story = []

    story.append(
        Paragraph(
            f"{sector} Sector Report",
            title_style
        )
    )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            "<b>Median Sector KPIs</b>",
            heading_style
        )
    )

    summary = sector_summary(sector_data)

    summary_table = [["Metric", "Median Value"]]

    for metric, value in summary.items():

        summary_table.append([
            metric,
            str(value)
        ])

    table = Table(
        summary_table,
        colWidths=[250, 150]
    )

    table.setStyle(TableStyle([

        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),

        ("BACKGROUND", (0,0), (-1,0), colors.lightblue),

        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),

        ("ALIGN", (1,1), (-1,-1), "CENTER"),

        ("BOTTOMPADDING", (0,0), (-1,0), 8)

    ]))

    story.append(table)

    story.append(Spacer(1,20))

    story.append(
        Paragraph(
            "<b>Companies in Sector</b>",
            heading_style
        )
    )

    company_table = [[

        "Company",
        "ROE",
        "Debt/Equity",
        "FCF",
        "Market Cap",
        "Revenue CAGR",
        "PAT CAGR",
        "Dividend Payout",
        "Dividend Yield"

    ]]

    for _, row in sector_data.iterrows():

        company_table.append([

            row["company_name"],

            row["return_on_equity_pct"],

            row["debt_to_equity"],

            row["free_cash_flow_cr"],

            row["market_cap_crore"],

            row["revenue_cagr_5yr"],

            row["pat_cagr_5yr"],

            row["dividend_payout_ratio_pct"],

            row["dividend_yield_pct"]

        ])

    company_tbl = Table(company_table)

    company_tbl.setStyle(TableStyle([

        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),

        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),

        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),

        ("FONTSIZE", (0,0), (-1,-1), 8),

        ("BOTTOMPADDING", (0,0), (-1,0), 6),

        ("WORDWRAP", (0,0), (-1,-1), True)

    ]))

    story.append(company_tbl)

    pdf.build(story)

    print(f"Generated : {sector}")

conn.close()

print("\nAll sector reports generated successfully.")