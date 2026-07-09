import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

df = pd.read_sql("""
SELECT *
FROM peer_percentiles
WHERE peer_group_name = 'IT Services'
ORDER BY percentile_rank DESC
""", conn)

print("IT Services Peer Rankings")
print(df.head())

conn.close()
conn = sqlite3.connect("db/nifty100.db")

cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM financial_ratios")
print("financial_ratios :", cursor.fetchone()[0])

cursor.execute("SELECT COUNT(*) FROM peer_percentiles")
print("peer_percentiles :", cursor.fetchone()[0])

conn.close()    