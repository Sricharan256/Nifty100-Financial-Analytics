import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

query = """
SELECT *
FROM financial_ratios
LIMIT 5
"""

df = pd.read_sql(query, conn)

print("=" * 60)
print("FINANCIAL RATIOS DEMO")
print("=" * 60)

print(df)

conn.close()