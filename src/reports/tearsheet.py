"""
tearsheet.py

Sprint 5 – Day 33
Company PDF Tearsheet
"""
import pandas as pd
import os
import sqlite3
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.graphics import renderPDF
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Table,
    TableStyle
)

# -----------------------------------------------------
# Output Folder
# -----------------------------------------------------

os.makedirs("output/tearsheets", exist_ok=True)

# -----------------------------------------------------
# Database
# -----------------------------------------------------

DB_PATH = "db/nifty100.db"

conn = sqlite3.connect(DB_PATH)

# -----------------------------------------------------
# Styles
# -----------------------------------------------------

styles = getSampleStyleSheet()

title_style = styles["Heading1"]
title_style.alignment = TA_CENTER

heading_style = styles["Heading2"]

normal_style = styles["BodyText"]

# -----------------------------------------------------
# Header
# -----------------------------------------------------

def create_header(company_name, ticker):
    table = Table(
        [[f"{company_name} ({ticker})"]],
        colWidths=[500]
    )

    table.setStyle(TableStyle([

        ("BACKGROUND", (0,0), (-1,-1), colors.navy),

        ("TEXTCOLOR",(0,0),(-1,-1),colors.white),

        ("ALIGN",(0,0),(-1,-1),"CENTER"),

        ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold"),

        ("FONTSIZE",(0,0),(-1,-1),18),

        ("BOTTOMPADDING",(0,0),(-1,-1),12)

    ]))

    return table

# -----------------------------------------------------
# KPI Tiles
# -----------------------------------------------------

def create_kpi_table(company, revenue, ratios):

    latest_pl = revenue.iloc[-1]
    latest_ratio = ratios.iloc[-1]

    data = [

        [
            f"Revenue\n₹ {latest_pl['sales']:.2f} Cr",
            f"Net Profit\n₹ {latest_pl['net_profit']:.2f} Cr",
            f"ROE\n{latest_ratio['return_on_equity_pct']:.2f}%"
        ],

        [
            f"ROCE\n{company['roce_percentage']:.2f}%",
            f"EPS\n₹ {latest_pl['eps']:.2f}",
            f"Book Value\n₹ {company['book_value']:.2f}"
        ]

    ]

    table = Table(
        data,
        colWidths=[160,160,160]
    )

    table.setStyle(TableStyle([

        ("GRID",(0,0),(-1,-1),1,colors.grey),

        ("BACKGROUND",(0,0),(-1,-1),colors.whitesmoke),

        ("ALIGN",(0,0),(-1,-1),"CENTER"),

        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),

        ("WORDWRAP",(0,0),(-1,-1),True),

        ("BOTTOMPADDING",(0,0),(-1,-1),10),

        ("TOPPADDING",(0,0),(-1,-1),10)

    ]))

    return table

# -----------------------------------------------------
# Placeholder Section
# -----------------------------------------------------

def placeholder(title):

    t = Table(
        [[title]],
        colWidths=[500],
        rowHeights=[180]
    )

    t.setStyle(TableStyle([

        ("GRID",(0,0),(-1,-1),1,colors.grey),

        ("ALIGN",(0,0),(-1,-1),"CENTER"),

        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),

        ("BACKGROUND",(0,0),(-1,-1),colors.beige),

        ("WORDWRAP",(0,0),(-1,-1),True)

    ]))

    return t
# -----------------------------------------------------
# Load Company Data
# -----------------------------------------------------

def load_company_data(ticker):

    company = pd.read_sql(
        """
        SELECT *
        FROM companies
        WHERE id = ?
        """,
        conn,
        params=[ticker]
    )

    if company.empty:
        raise ValueError(f"{ticker} not found.")

    company = company.iloc[0]

    revenue = pd.read_sql(
        """
        SELECT year,
               sales,
               net_profit,
               operating_profit,
               eps
        FROM profit_loss
        WHERE company_id=?
        ORDER BY year
        """,
        conn,
        params=[ticker]
    )

    ratios = pd.read_sql(
        """
        SELECT year,
               return_on_equity_pct,
               debt_to_equity,
               free_cash_flow_cr
        FROM financial_ratios
        WHERE company_id=?
        ORDER BY year
        """,
        conn,
        params=[ticker]
    )

    balance = pd.read_sql(
        """
        SELECT *
        FROM balance_sheet
        WHERE company_id=?
        ORDER BY year
        """,
        conn,
        params=[ticker]
    )

    cashflow = pd.read_sql(
        """
        SELECT *
        FROM cash_flow
        WHERE company_id=?
        ORDER BY year
        """,
        conn,
        params=[ticker]
    )

    pros_cons = pd.read_sql(
        """
        SELECT *
        FROM pros_cons
        WHERE company_id=?
        """,
        conn,
        params=[ticker]
    )
    print("\nPros & Cons Columns")

    return {
        "company": company,
        "revenue": revenue,
        "ratios": ratios,
        "balance": balance,
        "cashflow": cashflow,
        "pros_cons": pros_cons
    }
# -----------------------------------------------------
# Revenue / Net Profit Chart
# -----------------------------------------------------

def revenue_profit_chart(revenue):

    revenue = revenue.copy()

    revenue["year"] = revenue["year"].astype(str)

    years = revenue["year"].tolist()

    sales = revenue["sales"].fillna(0).tolist()

    profit = revenue["net_profit"].fillna(0).tolist()

    drawing = Drawing(500, 220)

    chart = VerticalBarChart()

    chart.x = 40
    chart.y = 30

    chart.width = 420
    chart.height = 150

    chart.data = [sales, profit]

    chart.categoryAxis.categoryNames = years

    chart.valueAxis.valueMin = 0

    chart.bars[0].fillColor = colors.darkblue
    chart.bars[1].fillColor = colors.green

    drawing.add(chart)

    return drawing
# -----------------------------------------------------
# ROE / ROCE Chart
# -----------------------------------------------------

def roe_roce_chart(ratios, latest_roce):

    ratios = ratios.copy()

    ratios["year"] = ratios["year"].astype(str)

    years = ratios["year"].tolist()

    roe = ratios["return_on_equity_pct"].fillna(0).tolist()

    roce = [latest_roce] * len(years)

    drawing = Drawing(500, 220)

    chart = HorizontalLineChart()

    chart.x = 40
    chart.y = 35

    chart.width = 420
    chart.height = 140

    chart.data = [roe, roce]

    chart.categoryAxis.categoryNames = years

    chart.lines[0].strokeColor = colors.blue
    chart.lines[0].symbol = makeMarker("Circle")

    chart.lines[1].strokeColor = colors.red
    chart.lines[1].symbol = makeMarker("Square")

    drawing.add(chart)

    return drawing
# -----------------------------------------------------
# Balance Sheet Composition
# -----------------------------------------------------

def balance_sheet_chart(balance):

    balance = balance.copy()

    balance["year"] = balance["year"].astype(str)

    balance["equity"] = (
        balance["equity_capital"].fillna(0)
        + balance["reserves"].fillna(0)
    )

    years = balance["year"].tolist()

    equity = balance["equity"].tolist()
    borrowings = balance["borrowings"].fillna(0).tolist()
    other = balance["other_liabilities"].fillna(0).tolist()

    drawing = Drawing(500, 230)

    chart = VerticalBarChart()

    chart.x = 45
    chart.y = 35

    chart.width = 420
    chart.height = 160

    chart.data = [
        equity,
        borrowings,
        other
    ]

    chart.categoryAxis.categoryNames = years

    chart.valueAxis.valueMin = 0

    chart.bars[0].fillColor = colors.darkgreen
    chart.bars[1].fillColor = colors.orange
    chart.bars[2].fillColor = colors.red

    drawing.add(chart)

    return drawing
# -----------------------------------------------------
# Cash Flow Chart
# -----------------------------------------------------

def cashflow_chart(cashflow):

    cf = cashflow.copy()

    # Keep only the latest record
    cf["year_num"] = (
        cf["year"]
        .astype(str)
        .str.extract(r"(\d{4})")
        .astype(float)
    )

    cf = cf.sort_values("year_num").iloc[-1]

    values = [
        cf["operating_activity"],
        cf["investing_activity"],
        cf["financing_activity"],
        cf["net_cash_flow"]
    ]

    drawing = Drawing(500, 220)

    chart = VerticalBarChart()

    chart.x = 45
    chart.y = 35

    chart.width = 400
    chart.height = 150

    chart.data = [values]

    chart.categoryAxis.categoryNames = [
        "CFO",
        "CFI",
        "CFF",
        "Net Cash"
    ]

    chart.valueAxis.valueMin = min(0, min(values))

    chart.bars[0].fillColor = colors.darkblue

    drawing.add(chart)

    return drawing
# -----------------------------------------------------
# Pros & Cons
# -----------------------------------------------------

def pros_cons_table(df):

    pros = []
    cons = []

    if not df.empty:

        for _, row in df.iterrows():

            if pd.notna(row["pros"]) and str(row["pros"]).strip():
                pros.append("• " + str(row["pros"]))

            if pd.notna(row["cons"]) and str(row["cons"]).strip():
                cons.append("• " + str(row["cons"]))

    if len(pros) == 0:
        pros.append("No Pros Available")

    if len(cons) == 0:
        cons.append("No Cons Available")

    left = Paragraph(
        "<br/>".join(pros),
        normal_style
    )

    right = Paragraph(
        "<font color='red'>" +
        "<br/>".join(cons) +
        "</font>",
        normal_style
    )

    table = Table(
        [
            ["Pros", "Cons"],
            [left, right]
        ],
        colWidths=[240, 240]
    )

    table.setStyle(TableStyle([

        ("GRID", (0,0), (-1,-1), 1, colors.grey),

        ("BACKGROUND", (0,0), (0,0), colors.lightgreen),
        ("BACKGROUND", (1,0), (1,0), colors.pink),

        ("TEXTCOLOR", (0,0), (-1,0), colors.black),

        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),

        ("VALIGN", (0,0), (-1,-1), "TOP"),

        ("WORDWRAP", (0,0), (-1,-1), True),

        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING", (0,0), (-1,-1), 8)

    ]))

    return table
# -----------------------------------------------------
# Capital Allocation Badge
# -----------------------------------------------------

def allocation_badge():

    badge = Table(
        [["Capital Allocation : Balanced"]],
        colWidths=[250]
    )

    badge.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(-1,-1),colors.darkgreen),
        ("TEXTCOLOR",(0,0),(-1,-1),colors.white),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),
        ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold"),
        ("BOTTOMPADDING",(0,0),(-1,-1),8)

    ]))

    return badge
# -----------------------------------------------------
# Build PDF
# -----------------------------------------------------

def build_tearsheet(company_name, ticker):

    data = load_company_data(ticker)

    company = data["company"]
    latest_roce = company["roce_percentage"]
    revenue = data["revenue"]
    ratios = data["ratios"]
    balance = data["balance"]
    cashflow = data["cashflow"]
    pros_cons = data["pros_cons"]

    pdf_path = f"output/tearsheets/{ticker}.pdf"

    doc = SimpleDocTemplate(pdf_path)

    story = []

    # -----------------------
    # PAGE 1
    # -----------------------

    story.append(create_header(company_name, ticker))

    story.append(Spacer(1,15))

    story.append(
    create_kpi_table(
        company,
        revenue,
        ratios
    )
)

    story.append(Spacer(1,20))

    story.append(
    revenue_profit_chart(revenue)
)

    story.append(Spacer(1,20))

    story.append(
    roe_roce_chart(
        ratios,
        latest_roce
    )
)

    # -----------------------
    # PAGE 2
    # -----------------------

    story.append(PageBreak())

    story.append(create_header(company_name, ticker))

    story.append(Spacer(1,15))

    story.append(
    balance_sheet_chart(balance)
)

    story.append(Spacer(1,15))

    story.append(
    cashflow_chart(cashflow)
)

    story.append(Spacer(1,15))

    story.append(
    pros_cons_table(pros_cons)
)
    story.append(Spacer(1,10))
    story.append(allocation_badge())
    print("\nLoaded Data")
    print("-" * 60)
    print("Revenue Records :", len(revenue))
    print("Ratio Records   :", len(ratios))
    print("Balance Records :", len(balance))
    print("Cashflow Records:", len(cashflow))
    print("Pros/Cons       :", len(pros_cons))

    doc.build(story)

    print(f"Generated : {pdf_path}")

# -----------------------------------------------------
# Test
# -----------------------------------------------------

test_companies = [

    ("Tata Consultancy Services", "TCS"),
    ("HDFC Bank", "HDFCBANK"),
    ("Reliance Industries", "RELIANCE"),
    ("Sun Pharmaceutical Industries", "SUNPHARMA"),
    ("Tata Steel", "TATASTEEL")

]

for company_name, ticker in test_companies:

    build_tearsheet(
        company_name,
        ticker
    )

conn.close()
