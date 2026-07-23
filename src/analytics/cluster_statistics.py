import os
import sqlite3
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from scipy.stats import zscore

# =====================================================
# Configuration
# =====================================================

DB_PATH = "db/nifty100.db"

OUTPUT_DIR = "output"
REPORT_DIR = "reports"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

conn = sqlite3.connect(DB_PATH)
query = """
SELECT

    c.id,
    c.company_name,
    s.broad_sector,

    fr.year,
    fr.return_on_equity_pct,
    fr.debt_to_equity,
    fr.free_cash_flow_cr,
    fr.operating_profit_margin_pct,
    fr.composite_quality_score,
    fr.net_profit_margin_pct,
    fr.asset_turnover,
    fr.interest_coverage,
    fr.book_value_per_share,
    fr.earnings_per_share

FROM companies c

LEFT JOIN sectors s
ON c.id = s.company_id

LEFT JOIN financial_ratios fr
ON c.id = fr.company_id
"""

df = pd.read_sql(query, conn)

print("Rows Loaded :", len(df))
df["year"] = pd.to_numeric(df["year"], errors="coerce")

df = (
    df.sort_values("year")
      .groupby("id")
      .tail(1)
      .reset_index(drop=True)
)

print("Companies :", len(df))
clusters = pd.read_csv(
    "output/cluster_labels.csv"
)

df = df.merge(

    clusters[["company_id", "cluster_id", "cluster_name"]],

    left_on="id",
    right_on="company_id",
    how="left"

)

print(df.head())
# =====================================================
# Cluster Profiling
# =====================================================

profile_features = [
    "return_on_equity_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "operating_profit_margin_pct",
    "composite_quality_score"
]

print("\n==============================")
print("Cluster Mean Statistics")
print("==============================")

cluster_mean = (
    df.groupby("cluster_name")[profile_features]
      .mean()
      .round(2)
)

print(cluster_mean)

print("\n==============================")
print("Cluster Median Statistics")
print("==============================")

cluster_median = (
    df.groupby("cluster_name")[profile_features]
      .median()
      .round(2)
)

print(cluster_median)

# =====================================================
# Correlation Heatmap
# =====================================================

corr_features = [

    "return_on_equity_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "operating_profit_margin_pct",
    "composite_quality_score",
    "net_profit_margin_pct",
    "asset_turnover",
    "interest_coverage",
    "book_value_per_share",
    "earnings_per_share"

]

corr_df = df[corr_features].apply(
    pd.to_numeric,
    errors="coerce"
)

corr = corr_df.corr(method="pearson")

plt.figure(figsize=(10,8))

sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title("Correlation Heatmap")

plt.tight_layout()

plt.savefig(
    os.path.join(
        REPORT_DIR,
        "correlation_heatmap.png"
    ),
    dpi=300
)

plt.close()

print("\nSaved : reports/correlation_heatmap.png")

# =====================================================
# Outlier Detection
# =====================================================

outliers = []

for sector, group in df.groupby("broad_sector"):

    numeric = group[profile_features].apply(
        pd.to_numeric,
        errors="coerce"
    )

    z = numeric.apply(
        lambda x: (x - x.mean()) / x.std(ddof=0)
    )

    for idx in z.index:

        for col in profile_features:

            value = z.loc[idx, col]

            if pd.notna(value) and abs(value) > 3:

                outliers.append({

                    "company_id": group.loc[idx, "id"],
                    "company_name": group.loc[idx, "company_name"],
                    "sector": sector,
                    "metric": col,
                    "z_score": round(value,2)

                })

outlier_df = pd.DataFrame(outliers)

outlier_df.to_csv(

    os.path.join(
        OUTPUT_DIR,
        "outlier_report.csv"
    ),

    index=False

)

print("Saved : output/outlier_report.csv")

# =====================================================
# Portfolio Statistics
# =====================================================

stats = []

for col in corr_features:

    series = pd.to_numeric(
        df[col],
        errors="coerce"
    ).dropna()

    stats.append({

        "KPI": col,
        "P10": series.quantile(0.10),
        "P25": series.quantile(0.25),
        "P50": series.quantile(0.50),
        "P75": series.quantile(0.75),
        "P90": series.quantile(0.90),
        "Mean": series.mean(),
        "Std": series.std()

    })

portfolio_stats = pd.DataFrame(stats)

portfolio_stats = portfolio_stats.round(2)

portfolio_stats.to_csv(

    os.path.join(
        OUTPUT_DIR,
        "portfolio_stats.csv"
    ),

    index=False

)

print("Saved : output/portfolio_stats.csv")

print("\nDay 37 Completed Successfully.")

conn.close()