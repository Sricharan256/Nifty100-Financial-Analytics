import os
import re
import sqlite3

import pandas as pd

# -----------------------------------------------------
# Create Output Folder
# -----------------------------------------------------

os.makedirs("output", exist_ok=True)

# -----------------------------------------------------
# Connect to SQLite Database
# -----------------------------------------------------

DB_PATH = "db/nifty100.db"

conn = sqlite3.connect(DB_PATH)

# -----------------------------------------------------
# Load Analysis Table
# -----------------------------------------------------

analysis = pd.read_sql(
    """
    SELECT *
    FROM analysis
    """,
    conn
)

# -----------------------------------------------------
# Load Financial Ratios
# (Used later for cross-validation)
# -----------------------------------------------------

ratios = pd.read_sql(
    """
    SELECT
        company_id,
        year,
        revenue_cagr_5yr,
        pat_cagr_5yr,
        eps_cagr_5yr
    FROM financial_ratios
    """,
    conn
)

# -----------------------------------------------------
# Load Companies
# -----------------------------------------------------

companies = pd.read_sql(
    """
    SELECT
        id AS company_id,
        company_name
    FROM companies
    """,
    conn
)

# -----------------------------------------------------
# Display Summary
# -----------------------------------------------------

print("=" * 60)
print("DAY 29 - NLP ANALYSIS PARSER")
print("=" * 60)

print(f"Companies Loaded : {len(companies)}")
print(f"Analysis Rows    : {len(analysis)}")
print(f"Ratio Rows       : {len(ratios)}")
print("=" * 60)

# -----------------------------------------------------
# Target Fields for Parsing
# -----------------------------------------------------

TARGET_FIELDS = [
    "compounded_sales_growth",
    "compounded_profit_growth",
    "stock_price_cagr",
    "roe"
]

print("\nTarget Fields:")

for field in TARGET_FIELDS:
    print(f"✓ {field}")
# -----------------------------------------------------
# Regex Pattern
# Example:
# "10 Years: 21%"
# "5 Year : 18.4%"
# -----------------------------------------------------

PATTERN = re.compile(r"(\d+)\s*Years?:?\s*([\d.]+)%", re.IGNORECASE)


# -----------------------------------------------------
# Parse Function
# -----------------------------------------------------

def parse_metric(text):
    """
    Extract:
        Period (Years)
        Percentage Value

    Example:
        "10 Years: 21%"
        ->
        (10, 21.0)

    Returns None if pattern not found.
    """

    if pd.isna(text):
        return None

    text = str(text).strip()

    match = PATTERN.search(text)

    if not match:
        return None

    period = int(match.group(1))
    value = float(match.group(2))

    return period, value


# -----------------------------------------------------
# Quick Parser Test
# -----------------------------------------------------

print("\nRegex Parser Test")
print("-" * 40)

samples = [
    "10 Years: 21%",
    "5 Years: 18.4%",
    "3 Year: 12%",
    "Invalid Text"
]

for sample in samples:

    result = parse_metric(sample)

    if result:
        print(
            f"{sample:<25} -> "
            f"Period={result[0]}, "
            f"Value={result[1]}"
        )
    else:
        print(f"{sample:<25} -> No Match")
# -----------------------------------------------------
# Parse Analysis Fields
# -----------------------------------------------------

parsed_records = []
failed_records = []

print("\nParsing Analysis Text...")
print("-" * 50)

for _, row in analysis.iterrows():

    company_id = row["company_id"]

    for metric in TARGET_FIELDS:

        text = row.get(metric)

        result = parse_metric(text)

        if result:

            period, value = result

            parsed_records.append({
                "company_id": company_id,
                "metric_type": metric,
                "period_years": period,
                "value_pct": value
            })

        else:

            failed_records.append({
                "company_id": company_id,
                "metric_type": metric,
                "original_text": text
            })

# -----------------------------------------------------
# Create DataFrames
# -----------------------------------------------------

parsed_df = pd.DataFrame(parsed_records)

failed_df = pd.DataFrame(failed_records)

# -----------------------------------------------------
# Save Parsed Output
# -----------------------------------------------------

parsed_df.to_csv(
    "output/analysis_parsed.csv",
    index=False
)

failed_df.to_csv(
    "output/parse_failures.csv",
    index=False
)

# -----------------------------------------------------
# Summary
# -----------------------------------------------------

print("\nParsing Summary")
print("-" * 50)

print(f"Parsed Records  : {len(parsed_df)}")
print(f"Failed Records  : {len(failed_df)}")

print("\nSample Parsed Data")

if not parsed_df.empty:
    print(parsed_df.head(10))
else:
    print("No records parsed.")

print("\nFiles Generated")
print("-----------------------------")
print("✓ output/analysis_parsed.csv")
print("✓ output/parse_failures.csv")
# -----------------------------------------------------
# Cross Validation with Ratio Engine
# -----------------------------------------------------

print("\nCross Validating Parsed CAGR Values...")
print("-" * 60)

# Latest financial ratio for each company
ratios["year_num"] = (
    ratios["year"]
    .astype(str)
    .str.extract(r"(\d{4})")
    .astype(float)
)

latest_ratios = (
    ratios.sort_values("year_num")
          .groupby("company_id", as_index=False)
          .tail(1)
)

# Mapping between parsed metric and ratio engine column
metric_mapping = {
    "compounded_sales_growth": "revenue_cagr_5yr",
    "compounded_profit_growth": "pat_cagr_5yr",
    "stock_price_cagr": None,     # No matching ratio
    "roe": None                   # ROE is not CAGR
}

validation_records = []

for _, row in parsed_df.iterrows():

    metric = row["metric_type"]

    # Skip metrics without comparison column
    if metric_mapping[metric] is None:
        continue

    company_id = row["company_id"]

    ratio_row = latest_ratios[
        latest_ratios["company_id"] == company_id
    ]

    if ratio_row.empty:
        continue

    ratio_value = ratio_row.iloc[0][metric_mapping[metric]]

    if pd.isna(ratio_value):
        continue

    parsed_value = row["value_pct"]

    difference = abs(parsed_value - ratio_value)

    validation_records.append({
        "company_id": company_id,
        "metric_type": metric,
        "parsed_value_pct": round(parsed_value, 2),
        "ratio_engine_pct": round(ratio_value, 2),
        "difference_pct": round(difference, 2),
        "manual_review": difference > 5
    })

# -----------------------------------------------------
# Validation Report
# -----------------------------------------------------
validation_df = pd.DataFrame(validation_records)

if validation_df.empty:

    print("No matching records found for CAGR validation.")

    validation_df = pd.DataFrame(columns=[
        "company_id",
        "metric_type",
        "parsed_value_pct",
        "ratio_engine_pct",
        "difference_pct",
        "manual_review"
    ])

review_df = validation_df[
    validation_df["manual_review"] == True
]

validation_df.to_csv(
    "output/cagr_validation_review.csv",
    index=False
)
print(f"Validated Records : {len(validation_df)}")
print(f"Manual Review     : {len(review_df)}")

if not review_df.empty:

    print("\nTop Divergences")
    print(review_df.head(10))

print("\nGenerated File")
print("------------------------")
print("✓ output/cagr_validation_review.csv")
# -----------------------------------------------------
# Day 29 Final Summary
# -----------------------------------------------------

print("\n" + "=" * 60)
print("DAY 29 - NLP ANALYSIS PARSER COMPLETED")
print("=" * 60)

print(f"Companies Loaded        : {len(companies)}")
print(f"Analysis Records        : {len(analysis)}")
print(f"Parsed Records          : {len(parsed_df)}")
print(f"Parse Failures          : {len(failed_df)}")

if 'validation_df' in globals():
    print(f"CAGR Validations        : {len(validation_df)}")

    if 'review_df' in globals():
        print(f"Manual Review Required  : {len(review_df)}")
else:
    print("CAGR Validation         : Skipped")

print("\nGenerated Files")
print("-" * 60)
print("✓ output/analysis_parsed.csv")
print("✓ output/parse_failures.csv")

if os.path.exists("output/cagr_validation_review.csv"):
    print("✓ output/cagr_validation_review.csv")

print("\nOverall Status")

if len(parsed_df) > 0:
    print("✓ NLP parser executed successfully.")
else:
    print("⚠ No records were parsed. Please verify the analysis table format.")

print("=" * 60)

# -----------------------------------------------------
# Close Database Connection
# -----------------------------------------------------

conn.close()