"""
Sprint 3 - Day 17

P10/P90 Winsorization Normalization
"""

import pandas as pd


def winsorize(df, columns):
    """
    Cap values between 10th and 90th percentile.
    """

    df = df.copy()

    for col in columns:

        if col not in df.columns:
            continue

        series = df[col].fillna(0)

        p10 = series.quantile(0.10)
        p90 = series.quantile(0.90)

        df[col] = series.clip(lower=p10, upper=p90)

    return df


def min_max_scale(df, columns):
    """
    Scale values between 0 and 100.
    """

    df = df.copy()

    for col in columns:

        if col not in df.columns:
            continue

        minimum = df[col].min()
        maximum = df[col].max()

        if maximum == minimum:

            df[col + "_score"] = 50

        else:

            df[col + "_score"] = (
                (df[col] - minimum)
                / (maximum - minimum)
            ) * 100

    return df


if __name__ == "__main__":

    import sqlite3

    conn = sqlite3.connect("db/nifty100.db")

    df = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn
    )

    conn.close()

    metrics = [
        "return_on_equity_pct",
        "net_profit_margin_pct",
        "debt_to_equity",
        "free_cash_flow_cr",
        "asset_turnover",
        "interest_coverage"
    ]

    df = winsorize(df, metrics)

    df = min_max_scale(df, metrics)

    print(df.head())