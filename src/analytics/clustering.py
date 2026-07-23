import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# =====================================================
# Configuration
# =====================================================

DB_PATH = "db/nifty100.db"

OUTPUT_DIR = "output"
REPORT_DIR = "reports"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

# =====================================================
# Connect Database
# =====================================================

conn = sqlite3.connect(DB_PATH)

# =====================================================
# Load Latest Financial Data
# =====================================================

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
    fr.composite_quality_score

FROM companies c

LEFT JOIN sectors s
ON c.id = s.company_id

LEFT JOIN financial_ratios fr
ON c.id = fr.company_id
"""

df = pd.read_sql(query, conn)

print(f"Rows Loaded : {len(df)}")

# =====================================================
# Latest Year per Company
# =====================================================

df["year"] = pd.to_numeric(df["year"], errors="coerce")

df = (
    df.sort_values("year")
      .groupby("id")
      .tail(1)
      .reset_index(drop=True)
)

print(f"Companies : {len(df)}")

# =====================================================
# Features
# =====================================================

features = [

    "return_on_equity_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "operating_profit_margin_pct",
    "composite_quality_score"

]

cluster_df = df[
    [
        "id",
        "company_name",
        "broad_sector"
    ] + features
].copy()

# =====================================================
# Convert Numeric
# =====================================================

for col in features:

    cluster_df[col] = pd.to_numeric(
        cluster_df[col],
        errors="coerce"
    )

# =====================================================
# Fill Missing Values
# Sector Median
# =====================================================

for col in features:

    cluster_df[col] = (

        cluster_df
        .groupby("broad_sector")[col]
        .transform(

            lambda x: x.fillna(x.median())

        )

    )

# Global Median

for col in features:

    cluster_df[col] = cluster_df[col].fillna(

        cluster_df[col].median()

    )

print("\nMissing Values")

print(cluster_df[features].isna().sum())

# =====================================================
# Standard Scaling
# =====================================================

scaler = StandardScaler()

X = scaler.fit_transform(cluster_df[features])

print("\nScaling Completed")

# =====================================================
# Elbow Plot
# =====================================================

inertia = []

for k in range(2, 11):

    model = KMeans(

        n_clusters=k,
        random_state=42,
        n_init=10

    )

    model.fit(X)

    inertia.append(model.inertia_)

plt.figure(figsize=(8,5))

plt.plot(

    range(2,11),
    inertia,
    marker="o"

)

plt.title("KMeans Elbow Plot")

plt.xlabel("Number of Clusters")

plt.ylabel("Inertia")

plt.grid(True)

plt.savefig(

    os.path.join(REPORT_DIR,"elbow_plot.png"),

    dpi=300,

    bbox_inches="tight"

)

plt.close()

print("Elbow Plot Saved")

# =====================================================
# Final Clustering
# =====================================================

kmeans = KMeans(

    n_clusters=5,
    random_state=42,
    n_init=10

)

cluster_df["cluster_id"] = kmeans.fit_predict(X)

# =====================================================
# Distance From Centroid
# =====================================================

dist = kmeans.transform(X)

cluster_df["distance_from_centroid"] = [

    dist[i][cluster_df.iloc[i]["cluster_id"]]

    for i in range(len(cluster_df))

]

# =====================================================
# Cluster Names
# =====================================================

cluster_names = {

    0: "High-Quality Compounders",

    1: "Defensive Dividend Payers",

    2: "Value Cyclicals",

    3: "Emerging Growth",

    4: "Distressed / Turnaround"

}

cluster_df["cluster_name"] = (

    cluster_df["cluster_id"]

    .map(cluster_names)

)

# =====================================================
# Export CSV
# =====================================================

output = cluster_df[
    [

        "id",
        "company_name",
        "cluster_id",
        "cluster_name",
        "distance_from_centroid"

    ]
].rename(

    columns={

        "id":"company_id"

    }

)

csv_path = os.path.join(

    OUTPUT_DIR,

    "cluster_labels.csv"

)

output.to_csv(

    csv_path,

    index=False

)

print("\nCluster Distribution")

print(

    output["cluster_name"].value_counts()

)

print("\nSaved :", csv_path)

print("Saved : reports/elbow_plot.png")

conn.close()

print("\nDay 36 Completed Successfully.")