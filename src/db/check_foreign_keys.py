import sqlite3

conn = sqlite3.connect("db/nifty100.db")
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_key_check;")
rows = cursor.fetchall()

if rows:
    print("Foreign key issues found:")
    for row in rows:
        print(row)
else:
    print("No foreign key issues found.")

conn.close()