import os
import sqlite3
import pandas as pd
import numpy as np

# -----------------------------------------------------
# Output Folder
# -----------------------------------------------------

os.makedirs("output", exist_ok=True)

# -----------------------------------------------------
# Database Connection
# -----------------------------------------------------

DB_PATH = "db/nifty100.db"

conn = sqlite3.connect(DB_PATH)

print("=" * 60)
print("DAY 30 - AUTO PROS & CONS GENERATOR")
print("=" * 60)

# -----------------------------------------------------
# Load Companies
# -----------------------------------------------------

companies = pd.read_sql("""
SELECT *
FROM companies
""", conn)
# -----------------------------------------------------
# Load Financial Ratios
# -----------------------------------------------------

ratios = pd.read_sql("""
SELECT *
FROM financial_ratios
""", conn)

# -----------------------------------------------------
# Load Capital Allocation
# -----------------------------------------------------

try:
    capital = pd.read_sql("""
    SELECT *
    FROM capital_allocation
    """, conn)
except:
    capital = pd.DataFrame()

# -----------------------------------------------------
# Load Valuation Data
# -----------------------------------------------------

try:
    valuation = pd.read_sql("""
    SELECT *
    FROM valuation
    """, conn)
except:
    valuation = pd.DataFrame()

# -----------------------------------------------------
# Latest Financial Record
# -----------------------------------------------------

if "year" in ratios.columns:

    ratios["year_num"] = (
        ratios["year"]
        .astype(str)
        .str.extract(r'(\d{4})')
        .astype(float)
    )

    latest_ratios = (
        ratios
        .sort_values("year_num")
        .groupby("company_id")
        .tail(1)
        .reset_index(drop=True)
    )

else:
    latest_ratios = ratios.copy()

# -----------------------------------------------------
# Merge Company Information
# -----------------------------------------------------

latest = latest_ratios.merge(
    companies,
    left_on="company_id",
    right_on="id",
    how="left"
)

print(f"Companies Loaded        : {len(companies)}")
print(f"Financial Ratio Rows    : {len(ratios)}")
print(f"Latest Company Records  : {len(latest)}")

print("\nSample Data")
print("-" * 60)

cols = [
    c for c in [
        "company_name",
        "stock_name",
        "symbol",
        "sector",
        "year"
    ]
    if c in latest.columns
]

print(latest[cols].head())

# -----------------------------------------------------
# Storage for Generated Statements
# -----------------------------------------------------

pros_cons_records = []

print("\nInitialization Complete")
print("Ready to apply financial rules...")
print("=" * 60)
# -----------------------------------------------------
# Helper Functions
# -----------------------------------------------------

def get_value(row, column, default=np.nan):
    """
    Safely fetch a value from a DataFrame row.
    """
    if column in row.index:
        return row[column]
    return default


def is_valid(value):
    """
    Check if a numeric value is available.
    """
    return pd.notna(value)


def confidence_score(metric_value, threshold):
    """
    Calculate confidence score based on distance
    from the rule threshold.
    """

    if pd.isna(metric_value):
        return 0

    diff = abs(metric_value - threshold)

    if diff >= 15:
        return 100
    elif diff >= 10:
        return 90
    elif diff >= 5:
        return 80
    elif diff >= 2:
        return 70
    else:
        return 60


# -----------------------------------------------------
# Add Generated Record
# -----------------------------------------------------

def add_record(company_id,
               company_name,
               category,
               statement,
               confidence):

    pros_cons_records.append({
        "company_id": company_id,
        "company_name": company_name,
        "category": category,
        "statement": statement,
        "confidence": confidence
    })


# -----------------------------------------------------
# Available Financial Columns
# -----------------------------------------------------

print("\nAvailable Financial Ratio Columns")
print("-" * 60)

ratio_columns = sorted(latest.columns.tolist())

for col in ratio_columns:
    print(col)

print("-" * 60)
print(f"Total Columns : {len(ratio_columns)}")


# -----------------------------------------------------
# Rule Engine Initialization
# -----------------------------------------------------

print("\nPreparing Rule Engine...")

for _, row in latest.iterrows():

    company_id = row["company_id"]
    company_name = row["company_name"]

    # Frequently used metrics

    roe = get_value(row, "roe")
    roce = get_value(row, "roce")

    debt_equity = get_value(row, "debt_to_equity")
    npm = get_value(row, "net_profit_margin")
    opm = get_value(row, "operating_profit_margin")

    revenue_cagr = get_value(row, "revenue_cagr_5yr")
    pat_cagr = get_value(row, "pat_cagr_5yr")
    eps_cagr = get_value(row, "eps_cagr_5yr")

print("Rule Engine Ready.")
print("=" * 60)
# -----------------------------------------------------
# Day 30 - Part 4
# Remaining Pro Rules (7-12)
# -----------------------------------------------------

print("\nApplying Additional Pro Rules...")
print("-" * 60)

for _, row in latest.iterrows():

    company_id = row["company_id"]
    company_name = row["company_name"]

    npm = get_value(row, "net_profit_margin_pct")
    opm = get_value(row, "operating_profit_margin_pct")
    debt = get_value(row, "debt_to_equity")
    interest = get_value(row, "interest_coverage")
    fcf = get_value(row, "free_cash_flow_cr")
    composite = get_value(row, "composite_quality_score")

    # -------------------------------------------------
    # Rule 7
    # -------------------------------------------------
    if is_valid(npm) and npm >= 15:
        add_record(
            company_id,
            company_name,
            "Pro",
            "Healthy Net Profit Margin indicates strong profitability.",
            confidence_score(npm, 15)
        )

    # -------------------------------------------------
    # Rule 8
    # -------------------------------------------------
    if is_valid(opm) and opm >= 20:
        add_record(
            company_id,
            company_name,
            "Pro",
            "Strong Operating Profit Margin reflects operational efficiency.",
            confidence_score(opm, 20)
        )

    # -------------------------------------------------
    # Rule 9
    # -------------------------------------------------
    if is_valid(interest) and interest >= 5:
        add_record(
            company_id,
            company_name,
            "Pro",
            "Comfortable interest coverage reduces financial risk.",
            confidence_score(interest, 5)
        )

    # -------------------------------------------------
    # Rule 10
    # -------------------------------------------------
    if is_valid(fcf) and fcf > 0:
        add_record(
            company_id,
            company_name,
            "Pro",
            "Positive Free Cash Flow supports future growth.",
            confidence_score(fcf, 0)
        )

    # -------------------------------------------------
    # Rule 11
    # -------------------------------------------------
    if is_valid(debt) and debt <= 1:
        add_record(
            company_id,
            company_name,
            "Pro",
            "Debt levels remain under control.",
            confidence_score(1 - debt, 0)
        )

    # -------------------------------------------------
    # Rule 12
    # -------------------------------------------------
    if is_valid(composite) and composite >= 70:
        add_record(
            company_id,
            company_name,
            "Pro",
            "High Composite Quality Score indicates strong overall fundamentals.",
            confidence_score(composite, 70)
        )

print(f"\nTotal Pro Statements Generated : {len(pros_cons_records)}")

if len(pros_cons_records) > 0:
    sample_df = pd.DataFrame(pros_cons_records)
    print("\nSample Generated Pros")
    print("-" * 60)
    print(sample_df.head(15))
# -----------------------------------------------------
# Day 30 - Part 5
# Con Rules (1-6)
# -----------------------------------------------------

print("\nApplying Con Rules...")
print("-" * 60)

for _, row in latest.iterrows():

    company_id = row["company_id"]
    company_name = row["company_name"]

    roe = get_value(row, "return_on_equity_pct")
    roce = get_value(row, "roce_percentage")
    debt = get_value(row, "debt_to_equity")
    revenue_cagr = get_value(row, "revenue_cagr_5yr")
    pat_cagr = get_value(row, "pat_cagr_5yr")
    eps_cagr = get_value(row, "eps_cagr_5yr")

    # -------------------------------------------------
    # Rule 1
    # -------------------------------------------------
    if is_valid(roe) and roe < 10:
        add_record(
            company_id,
            company_name,
            "Con",
            "Low Return on Equity indicates weaker shareholder returns.",
            confidence_score(10 - roe, 0)
        )

    # -------------------------------------------------
    # Rule 2
    # -------------------------------------------------
    if is_valid(roce) and roce < 10:
        add_record(
            company_id,
            company_name,
            "Con",
            "Low ROCE suggests inefficient capital utilization.",
            confidence_score(10 - roce, 0)
        )

    # -------------------------------------------------
    # Rule 3
    # -------------------------------------------------
    if is_valid(debt) and debt > 2:
        add_record(
            company_id,
            company_name,
            "Con",
            "High Debt-to-Equity increases financial risk.",
            confidence_score(debt, 2)
        )

    # -------------------------------------------------
    # Rule 4
    # -------------------------------------------------
    if is_valid(revenue_cagr) and revenue_cagr < 10:
        add_record(
            company_id,
            company_name,
            "Con",
            "Weak long-term revenue growth.",
            confidence_score(10 - revenue_cagr, 0)
        )

    # -------------------------------------------------
    # Rule 5
    # -------------------------------------------------
    if is_valid(pat_cagr) and pat_cagr < 10:
        add_record(
            company_id,
            company_name,
            "Con",
            "Profit growth has remained below expectations.",
            confidence_score(10 - pat_cagr, 0)
        )

    # -------------------------------------------------
    # Rule 6
    # -------------------------------------------------
    if is_valid(eps_cagr) and eps_cagr < 10:
        add_record(
            company_id,
            company_name,
            "Con",
            "EPS growth has been relatively weak.",
            confidence_score(10 - eps_cagr, 0)
        )

print(f"\nTotal Statements Generated : {len(pros_cons_records)}")

sample_df = pd.DataFrame(pros_cons_records)

print("\nSample Output")
print("-" * 60)
print(sample_df.tail(15))
# -----------------------------------------------------
# Day 30 - Part 6
# Remaining Con Rules (7-12)
# -----------------------------------------------------

print("\nApplying Additional Con Rules...")
print("-" * 60)

for _, row in latest.iterrows():

    company_id = row["company_id"]
    company_name = row["company_name"]

    npm = get_value(row, "net_profit_margin_pct")
    opm = get_value(row, "operating_profit_margin_pct")
    interest = get_value(row, "interest_coverage")
    fcf = get_value(row, "free_cash_flow_cr")
    composite = get_value(row, "composite_quality_score")
    debt = get_value(row, "debt_to_equity")

    # -------------------------------------------------
    # Rule 7
    # -------------------------------------------------
    if is_valid(npm) and npm < 8:
        add_record(
            company_id,
            company_name,
            "Con",
            "Low Net Profit Margin indicates weak profitability.",
            confidence_score(8 - npm, 0)
        )

    # -------------------------------------------------
    # Rule 8
    # -------------------------------------------------
    if is_valid(opm) and opm < 10:
        add_record(
            company_id,
            company_name,
            "Con",
            "Low Operating Profit Margin indicates poor operating efficiency.",
            confidence_score(10 - opm, 0)
        )

    # -------------------------------------------------
    # Rule 9
    # -------------------------------------------------
    if is_valid(interest) and interest < 2:
        add_record(
            company_id,
            company_name,
            "Con",
            "Low interest coverage may increase financial risk.",
            confidence_score(2 - interest, 0)
        )

    # -------------------------------------------------
    # Rule 10
    # -------------------------------------------------
    if is_valid(fcf) and fcf < 0:
        add_record(
            company_id,
            company_name,
            "Con",
            "Negative Free Cash Flow may impact future growth.",
            confidence_score(abs(fcf), 0)
        )

    # -------------------------------------------------
    # Rule 11
    # -------------------------------------------------
    if is_valid(composite) and composite < 40:
        add_record(
            company_id,
            company_name,
            "Con",
            "Low Composite Quality Score indicates weak overall fundamentals.",
            confidence_score(40 - composite, 0)
        )

    # -------------------------------------------------
    # Rule 12
    # -------------------------------------------------
    if is_valid(debt) and debt > 3:
        add_record(
            company_id,
            company_name,
            "Con",
            "Very high leverage increases long-term financial risk.",
            confidence_score(debt, 3)
        )

print(f"\nTotal Statements After Part 6 : {len(pros_cons_records)}")

sample_df = pd.DataFrame(pros_cons_records)

print("\nLatest Generated Statements")
print("-" * 60)
print(sample_df.tail(15))
# -----------------------------------------------------
# Day 30 - Part 7
# Export Results & Summary
# -----------------------------------------------------

print("\nGenerating Final Output...")
print("-" * 60)

pros_cons_df = pd.DataFrame(pros_cons_records)

# Remove duplicate statements
pros_cons_df = pros_cons_df.drop_duplicates(
    subset=["company_id", "category", "statement"]
)

# Sort output
pros_cons_df = pros_cons_df.sort_values(
    ["company_name", "category"]
).reset_index(drop=True)

# Export CSV
output_file = "output/pros_cons_generated.csv"
pros_cons_df.to_csv(output_file, index=False)

# -----------------------------------------------------
# Validation
# -----------------------------------------------------

validation = (
    pros_cons_df.groupby(["company_name", "category"])
    .size()
    .unstack(fill_value=0)
)

print("\nValidation Summary")
print("-" * 60)

companies_with_pro = (
    validation["Pro"].gt(0).sum()
    if "Pro" in validation.columns else 0
)

companies_with_con = (
    validation["Con"].gt(0).sum()
    if "Con" in validation.columns else 0
)

print(f"Companies with Pro : {companies_with_pro}")
print(f"Companies with Con : {companies_with_con}")

# -----------------------------------------------------
# Overall Summary
# -----------------------------------------------------

print("\nOverall Summary")
print("-" * 60)

print(f"Total Companies           : {len(companies)}")
print(f"Total Statements          : {len(pros_cons_df)}")
print(f"Total Pros               : {(pros_cons_df['category']=='Pro').sum()}")
print(f"Total Cons               : {(pros_cons_df['category']=='Con').sum()}")

print(f"\nOutput File")
print(f"✓ {output_file}")

print("\nSample Output")
print("-" * 60)
print(pros_cons_df.head(15))

print("\n" + "=" * 60)
print("DAY 30 - AUTO PROS & CONS GENERATOR COMPLETED")
print("=" * 60)

conn.close()