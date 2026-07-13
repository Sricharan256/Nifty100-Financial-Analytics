import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

tables = [
    "sectors",
    "peer_groups",
    "market_cap",
    "analysis",
    "pros_cons",
    "documents"
]

for table in tables:
    print("\n" + "=" * 70)
    print(table.upper())
    print("=" * 70)

    print(pd.read_sql(f"PRAGMA table_info({table})", conn))

conn.close()