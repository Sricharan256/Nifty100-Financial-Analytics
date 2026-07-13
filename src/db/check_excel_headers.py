import pandas as pd

files = [
    "companies.xlsx",
    "sectors.xlsx",
    "peer_groups.xlsx",
    "market_cap.xlsx"
]

for file in files:

    print("=" * 80)
    print(file)
    print("=" * 80)

    df = pd.read_excel(f"data/raw/{file}")

    print(df.columns.tolist())

    print()

    print(df.head())

    print("\n")