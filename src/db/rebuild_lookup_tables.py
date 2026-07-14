import sqlite3
import pandas as pd

DB = "db/nifty100.db"

conn = sqlite3.connect(DB)

# -------------------------------------------------------
# Helper Function
# -------------------------------------------------------

def rebuild_table(excel_file, table_name):

    print(f"\nRebuilding {table_name}...")

    df = pd.read_excel(
        excel_file
    )

    df.to_sql(
        table_name,
        conn,
        if_exists="replace",
        index=False
    )

    print("Done.")

# -------------------------------------------------------
# Rebuild Tables
# -------------------------------------------------------

rebuild_table(
    "data/raw/sectors.xlsx",
    "sectors"
)

rebuild_table(
    "data/raw/peer_groups.xlsx",
    "peer_groups"
)

rebuild_table(
    "data/raw/market_cap.xlsx",
    "market_cap"
)

conn.close()

print("\nDatabase Updated Successfully.")