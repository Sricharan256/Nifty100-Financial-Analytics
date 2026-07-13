"""
export_presets.py

Sprint 3 - Day 16

Exports all preset screeners to Excel.
"""

import os
import pandas as pd

from src.screener.presets import get_presets


OUTPUT_FILE = "output/screener_output.xlsx"


def export_to_excel():

    os.makedirs("output", exist_ok=True)

    presets = get_presets()

    with pd.ExcelWriter(
        OUTPUT_FILE,
        engine="openpyxl"
    ) as writer:

        for sheet_name, df in presets.items():

            export_columns = [
                "company_id",
                "year",
                "return_on_equity_pct",
                "debt_to_equity",
                "free_cash_flow_cr",
                "asset_turnover",
                "net_profit_margin_pct",
                "operating_profit_margin_pct",
                "interest_coverage",
                "earnings_per_share",
                "book_value_per_share",
                "dividend_payout_ratio_pct",
                "total_debt_cr",
                "cash_from_operations_cr",
                "composite_quality_score"
            ]

            columns = [
                col for col in export_columns
                if col in df.columns
            ]

            df = df[columns]

            df.to_excel(
                writer,
                sheet_name=sheet_name[:31],
                index=False
            )

    print("=" * 60)
    print("SPRINT 3 - DAY 16")
    print("=" * 60)
    print(f"Excel Report Generated Successfully")
    print(f"Location : {OUTPUT_FILE}")


if __name__ == "__main__":
    export_to_excel()   