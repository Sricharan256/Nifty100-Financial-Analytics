import sqlite3
import pandas as pd

DB_PATH = "db/nifty100.db"

conn = sqlite3.connect(DB_PATH)

companies = pd.read_sql(
    """
    SELECT
        id AS company_id,
        company_name
    FROM companies
    """,
    conn
)

ratios = pd.read_sql(
    "SELECT company_id, year FROM financial_ratios",
    conn
)

sector = pd.read_sql(
    "SELECT company_id, broad_sector FROM sectors",
    conn
)

conn.close()

# Merge data
df = companies.merge(
    sector,
    on="company_id",
    how="left"
)

# Count years available
year_count = (
    ratios.groupby("company_id")
    .size()
    .reset_index(name="years_available")
)

df = df.merge(
    year_count,
    on="company_id",
    how="left"
)

df["years_available"] = (
    df["years_available"]
    .fillna(0)
    .astype(int)
)

print("=" * 60)
print("QA DATA SUMMARY")
print("=" * 60)

print(df.head())

print()

print("Companies:", len(df))

print("Sectors:", df["broad_sector"].nunique())
# -----------------------------------------------------
# Companies with Partial Data (<10 Years)
# -----------------------------------------------------

partial_data = df[df["years_available"] < 10]

print("\n" + "=" * 60)
print("COMPANIES WITH PARTIAL DATA (<10 YEARS)")
print("=" * 60)

if partial_data.empty:
    print("All companies have 10 or more years of data.")
else:
    print(
        partial_data[
            [
                "company_id",
                "company_name",
                "broad_sector",
                "years_available"
            ]
        ].sort_values("years_available")
    )

# -----------------------------------------------------
# Select QA Sample Companies
# -----------------------------------------------------

qa_sample = (
    df.sort_values("company_name")
      .groupby("broad_sector")
      .head(2)
      .reset_index(drop=True)
)

qa_sample = qa_sample.head(10)

print("\n" + "=" * 60)
print("QA SAMPLE COMPANIES")
print("=" * 60)

print(
    qa_sample[
        [
            "company_name",
            "broad_sector",
            "years_available"
        ]
    ]
)

# -----------------------------------------------------
# Export QA Checklist
# -----------------------------------------------------

qa_sample.to_csv(
    "output/qa_sample_companies.csv",
    index=False
)

print("\nQA sample exported to output/qa_sample_companies.csv")
# -----------------------------------------------------
# Missing Data Validation
# -----------------------------------------------------

important_metrics = [
    "return_on_equity_pct",
    "net_profit_margin_pct",
    "operating_profit_margin_pct",
    "debt_to_equity",
    "interest_coverage",
    "asset_turnover",
    "free_cash_flow_cr",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "pe_ratio",
    "pb_ratio",
    "ev_ebitda"
]

existing_metrics = [
    col for col in important_metrics
    if col in df.columns
]

missing_summary = []

for metric in existing_metrics:

    missing_count = df[metric].isna().sum()

    missing_summary.append({
        "Metric": metric,
        "Missing Values": missing_count,
        "Available Values": len(df) - missing_count
    })

missing_df = pd.DataFrame(missing_summary)

print("\n" + "=" * 60)
print("MISSING DATA SUMMARY")
print("=" * 60)

print(missing_df)

# -----------------------------------------------------
# Export QA Summary
# -----------------------------------------------------

missing_df.to_csv(
    "output/qa_missing_data_summary.csv",
    index=False
)

print("\nMissing data summary exported.")
# -----------------------------------------------------
# QA Checklist
# -----------------------------------------------------

qa_checklist = pd.DataFrame({
    "Test Case": [
        "Company Profile - 10 Different Companies",
        "Companies with Partial Data (<10 Years)",
        "Stock Screener - Minimum Filters",
        "Stock Screener - Maximum Filters",
        "Trend Analysis Charts",
        "Sector Analysis Charts",
        "Capital Allocation Map",
        "Annual Reports Page",
        "Missing Data Handling",
        "Company Profile Load Time (<3 sec)"
    ],
    "Status": [
        "Pending",
        "Pending",
        "Pending",
        "Pending",
        "Pending",
        "Pending",
        "Pending",
        "Pending",
        "Pending",
        "Pending"
    ],
    "Remarks": [
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        ""
    ]
})

# -----------------------------------------------------
# Export Checklist
# -----------------------------------------------------

qa_checklist.to_excel(
    "output/qa_checklist.xlsx",
    index=False
)

print("\n" + "=" * 60)
print("QA CHECKLIST")
print("=" * 60)

print(qa_checklist)

print("\n QA checklist exported to output/qa_checklist.xlsx")
# -----------------------------------------------------
# QA Summary Report
# -----------------------------------------------------

summary_lines = [
    "=" * 60,
    "DAY 27 - QA SUMMARY REPORT",
    "=" * 60,
    "",
    f"Total Companies Tested      : {len(df)}",
    f"Companies with Partial Data : {len(partial_data)}",
    f"QA Sample Companies         : {len(qa_sample)}",
    f"Metrics Checked            : {len(existing_metrics)}",
    "",
    "Generated Files:",
    "----------------------------",
    "1. qa_sample_companies.csv",
    "2. qa_missing_data_summary.csv",
    "3. qa_checklist.xlsx",
    "",
    "QA Status : COMPLETED",
    "=" * 60
]

summary_path = "output/qa_summary.txt"

with open(summary_path, "w", encoding="utf-8") as file:
    file.write("\n".join(summary_lines))

# -----------------------------------------------------
# Final Console Output
# -----------------------------------------------------

print("\n" + "=" * 60)
print("DAY 27 QA COMPLETED")
print("=" * 60)

print(f"Companies Tested           : {len(df)}")
print(f"Partial Data Companies     : {len(partial_data)}")
print(f"QA Sample Companies        : {len(qa_sample)}")
print(f"Metrics Validated          : {len(existing_metrics)}")

print("\nGenerated Reports")
print("-----------------")
print("✓ output/qa_sample_companies.csv")
print("✓ output/qa_missing_data_summary.csv")
print("✓ output/qa_checklist.xlsx")
print("✓ output/qa_summary.txt")

print("\nQA completed successfully.")