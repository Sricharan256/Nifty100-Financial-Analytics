"""
leverage.py

Calculates leverage ratios for financial analysis.
"""


def debt_to_equity(total_debt, shareholders_equity):
    """
    Calculate Debt-to-Equity Ratio.
    """
    if total_debt is None or shareholders_equity is None:
        return None

    if shareholders_equity <= 0:
        return None

    return round(total_debt / shareholders_equity, 2)


def interest_coverage(profit_before_tax, interest_expense):
    """
    Calculate Interest Coverage Ratio.

    Formula:
        EBIT = Profit Before Tax + Interest Expense
        Interest Coverage Ratio = EBIT / Interest Expense
    """

    # Missing values
    if profit_before_tax is None or interest_expense is None:
        return None

    # Prevent division by zero
    if interest_expense == 0:
        return None

    # Calculate EBIT
    ebit = profit_before_tax + interest_expense

    return round(ebit / interest_expense, 2)


if __name__ == "__main__":

    print("=" * 50)
    print("LEVERAGE RATIO ENGINE")
    print("=" * 50)

    # -------------------------------
    # Debt to Equity
    # -------------------------------

    print("\nDebt-to-Equity Ratio")
    print("-" * 30)

    print("Test 1 :", debt_to_equity(2500, 5000))
    print("Test 2 :", debt_to_equity(1000, 500))
    print("Test 3 :", debt_to_equity(1000, 0))
    print("Test 4 :", debt_to_equity(1000, -500))
    print("Test 5 :", debt_to_equity(None, 500))

    # -------------------------------
    # Interest Coverage Ratio
    # -------------------------------

    print("\nInterest Coverage Ratio")
    print("-" * 30)

    print("Test 1 :", interest_coverage(1200, 200))
    print("Test 2 :", interest_coverage(500, 100))
    print("Test 3 :", interest_coverage(1000, 0))
    print("Test 4 :", interest_coverage(None, 200))