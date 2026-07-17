import os
import sqlite3
import pandas as pd

# -----------------------------------------------------
# Paths
# -----------------------------------------------------

DB_PATH = "db/nifty100.db"

OUTPUT_DIR = "output"

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

# -----------------------------------------------------
# Database
# -----------------------------------------------------

conn = sqlite3.connect(DB_PATH)

companies = pd.read_sql(
    "SELECT * FROM companies",
    conn
)

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

market = pd.read_sql(
    "SELECT * FROM market_cap",
    conn
)

sector = pd.read_sql(
    "SELECT * FROM sectors",
    conn
)

conn.close()

# -----------------------------------------------------
# Prepare Ratios
# -----------------------------------------------------

ratios["year_num"] = (

    ratios["year"]

    .astype(str)

    .str.extract(r"(\d{4})", expand=False)

)

ratios = ratios.dropna(
    subset=["year_num"]
)

ratios["year_num"] = ratios["year_num"].astype(int)

ratios = (

    ratios

    .sort_values("year_num")

    .groupby("company_id", as_index=False)

    .tail(1)

)

# -----------------------------------------------------
# Latest Market Cap
# -----------------------------------------------------

market = (

    market

    .sort_values("year")

    .groupby("company_id", as_index=False)

    .tail(1)

)

# -----------------------------------------------------
# Merge
# -----------------------------------------------------

companies = companies.rename(
    columns={
        "id": "company_id"
    }
)

df = ratios.merge(

    companies,

    on="company_id",

    how="left"

)

df = df.merge(

    sector[
        [
            "company_id",
            "broad_sector"
        ]
    ],

    on="company_id",

    how="left"

)

df = df.merge(

    market,

    on="company_id",

    how="left"

)

df = df.loc[
    :,
    ~df.columns.duplicated()
]

print()

print("Companies Loaded :", len(df))

print(df.head())
# -----------------------------------------------------
# Numeric Columns
# -----------------------------------------------------

numeric_cols = [
    "free_cash_flow_cr",
    "market_cap_crore",
    "pe_ratio",
    "pb_ratio",
    "ev_ebitda"
]

for col in numeric_cols:

    if col in df.columns:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

# Fill missing values
existing_cols = [col for col in numeric_cols if col in df.columns]

df[existing_cols] = df[existing_cols].fillna(0)

# -----------------------------------------------------
# FCF Yield (%)
# FCF / Market Cap × 100
# -----------------------------------------------------

df["FCF_yield_pct"] = 0.0

mask = df["market_cap_crore"] > 0

df.loc[mask, "FCF_yield_pct"] = (

    df.loc[mask, "free_cash_flow_cr"]

    / df.loc[mask, "market_cap_crore"]

    * 100

)

# -----------------------------------------------------
# Sector Median PE
# -----------------------------------------------------

sector_median = (

    df

    .groupby("broad_sector")["pe_ratio"]

    .median()

    .reset_index()

    .rename(
        columns={
            "pe_ratio": "5yr_median_PE"
        }
    )

)

df = df.merge(

    sector_median,

    on="broad_sector",

    how="left"

)

# -----------------------------------------------------
# PE vs Sector Median (%)
# -----------------------------------------------------

df["PE_vs_sector_median_pct"] = 0.0

mask = df["5yr_median_PE"] > 0

df.loc[mask, "PE_vs_sector_median_pct"] = (

    (
        df.loc[mask, "pe_ratio"]

        - df.loc[mask, "5yr_median_PE"]
    )

    /

    df.loc[mask, "5yr_median_PE"]

    * 100

)

# -----------------------------------------------------
# Valuation Flag
# -----------------------------------------------------

def valuation_flag(row):

    pe = row["pe_ratio"]

    median = row["5yr_median_PE"]

    if median <= 0:

        return "Fair"

    if pe > median * 1.5:

        return "Caution"

    elif pe < median * 0.7:

        return "Discount"

    else:

        return "Fair"


df["flag"] = df.apply(
    valuation_flag,
    axis=1
)

# -----------------------------------------------------
# Preview
# -----------------------------------------------------

print()

print(df[
    [
        "company_name",
        "broad_sector",
        "pe_ratio",
        "5yr_median_PE",
        "FCF_yield_pct",
        "PE_vs_sector_median_pct",
        "flag"
    ]
].head())
# -----------------------------------------------------
# Valuation Summary
# -----------------------------------------------------

summary = df[
    [
        "company_id",
        "company_name",
        "broad_sector",
        "pe_ratio",
        "pb_ratio",
        "ev_ebitda",
        "FCF_yield_pct",
        "5yr_median_PE",
        "PE_vs_sector_median_pct",
        "flag"
    ]
].copy()

summary = summary.rename(
    columns={
        "broad_sector": "sector",
        "pe_ratio": "P/E",
        "pb_ratio": "P/B",
        "ev_ebitda": "EV/EBITDA"
    }
)

# -----------------------------------------------------
# Save Excel
# -----------------------------------------------------

summary.to_excel(
    "output/valuation_summary.xlsx",
    index=False
)

print()

print("✅ valuation_summary.xlsx created")

# -----------------------------------------------------
# Save Flags CSV
# -----------------------------------------------------

flags = summary[
    summary["flag"].isin(
        [
            "Caution",
            "Discount"
        ]
    )
]

flags.to_csv(
    "output/valuation_flags.csv",
    index=False
)

print("✅ valuation_flags.csv created")

print()

print("Total Companies :", len(summary))

print("Flagged Companies :", len(flags))