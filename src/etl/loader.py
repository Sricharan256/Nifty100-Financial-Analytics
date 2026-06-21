"""
loader.py

Loads Excel files and applies normalization.
"""

from pathlib import Path

import pandas as pd

from src.etl.normaliser import normalize_year, normalize_ticker


DATA_PATH = Path("data/raw")


def load_excel(file_name):

    file_path = DATA_PATH / file_name

    try:

        df = pd.read_excel(file_path, header=1)
        print(f"\nLoaded : {file_name}")
        print(f"Rows   : {len(df)}")
        print(f"Cols   : {len(df.columns)}")

        # Normalize Year column
        if "Year" in df.columns:
            df["Year"] = df["Year"].apply(normalize_year)

        # Normalize Ticker column
        if "Ticker" in df.columns:
            df["Ticker"] = df["Ticker"].apply(normalize_ticker)

        print("Normalization completed successfully.")

        return df

    except FileNotFoundError:

        print(f"{file_name} not found.")

    except Exception as e:

        print(e)


if __name__ == "__main__":

    files = [
        "companies.xlsx",
        "profitandloss.xlsx",
        "balancesheet.xlsx",
        "cashflow.xlsx",
        "stock_prices.xlsx",
        "analysis.xlsx",
        "documents.xlsx",
        "financial_ratios.xlsx",
        "peer_groups.xlsx",
        "prosandcons.xlsx",
        "sectors.xlsx",
        "shareholding.xlsx"
    ]

    for file in files:
        print(f"\n{'=' * 50}")
        print(f"Loading {file}")
        print(f"{'=' * 50}")

        load_excel(file)