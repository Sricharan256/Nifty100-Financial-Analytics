"""
efficiency.py

Calculates efficiency ratios for financial analysis.
"""


def asset_turnover(sales, total_assets):
    """
    Calculate Asset Turnover Ratio.

    Formula:
        Asset Turnover = Sales / Total Assets

    Parameters
    ----------
    sales : float
        Total sales or revenue.

    total_assets : float
        Total assets of the company.

    Returns
    -------
    float | None
    """

    # Missing values
    if sales is None or total_assets is None:
        return None

    # Prevent division by zero
    if total_assets == 0:
        return None


    # Negative assets are invalid
    if total_assets < 0:
        return None

    return round(sales / total_assets, 2)


if __name__ == "__main__":

    print("=" * 50)
    print("ASSET TURNOVER RATIO")
    print("=" * 50)

    # Test Case 1
    print("\nTest Case 1")
    print("Sales :", 10000)
    print("Assets :", 5000)
    print("Asset Turnover :", asset_turnover(10000, 5000))

    # Test Case 2
    print("\nTest Case 2")
    print("Sales :", 5000)
    print("Assets :", 2500)
    print("Asset Turnover :", asset_turnover(5000, 2500))

    # Test Case 3
    print("\nTest Case 3 (Zero Assets)")
    print("Asset Turnover :", asset_turnover(10000, 0))

    # Test Case 4
    print("\nTest Case 4 (Negative Assets)")
    print("Asset Turnover :", asset_turnover(10000, -5000))

    # Test Case 5
    print("\nTest Case 5 (Missing Values)")
    print("Asset Turnover :", asset_turnover(None, 5000))