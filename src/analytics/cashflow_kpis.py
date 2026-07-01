"""
cashflow_kpis.py

Implements Cash Flow KPIs and Capital Allocation analysis.
"""

# -----------------------------------------------------
# Free Cash Flow
# -----------------------------------------------------

def free_cash_flow(operating_activity, investing_activity):
    """
    Calculate Free Cash Flow (FCF).

    Formula:
        FCF = Operating Activity + Investing Activity

    Returns:
        float | None
    """

    if operating_activity is None or investing_activity is None:
        return None

    return operating_activity + investing_activity


# -----------------------------------------------------
# CFO Quality Score
# -----------------------------------------------------

def cfo_quality_score(cfo, pat):
    """
    Calculate CFO Quality Score.

    Formula:
        CFO / PAT

    Returns:
        tuple (ratio, quality)
    """

    if cfo is None or pat is None:
        return None

    if pat == 0:
        return None

    ratio = round(cfo / pat, 2)

    if ratio > 1.0:
        quality = "High Quality"

    elif ratio >= 0.5:
        quality = "Moderate"

    else:
        quality = "Accrual Risk"

    return ratio, quality


# -----------------------------------------------------
# CapEx Intensity
# -----------------------------------------------------

def capex_intensity(investing_activity, sales):
    """
    Calculate CapEx Intensity.

    Formula:
        abs(Investing Activity) / Sales × 100

    Returns:
        tuple (ratio, category)
    """

    if investing_activity is None or sales is None:
        return None

    if sales == 0:
        return None

    ratio = round(abs(investing_activity) / sales * 100, 2)

    if ratio < 3:
        category = "Asset Light"

    elif ratio <= 8:
        category = "Moderate"

    else:
        category = "Capital Intensive"

    return ratio, category


# -----------------------------------------------------
# FCF Conversion Rate
# -----------------------------------------------------

def fcf_conversion_rate(fcf, operating_profit):
    """
    Calculate FCF Conversion Rate.

    Formula:
        FCF / Operating Profit × 100

    Returns:
        float | None
    """

    if fcf is None or operating_profit is None:
        return None

    if operating_profit == 0:
        return None

    return round((fcf / operating_profit) * 100, 2)


# -----------------------------------------------------
# Capital Allocation Pattern
# -----------------------------------------------------

def capital_allocation_pattern(cfo, cfi, cff, cfo_pat_ratio=None):
    """
    Classify Capital Allocation Pattern.

    Pattern Labels

    (+,-,-) = Reinvestor
    (+,-,-) with CFO/PAT > 1 = Shareholder Returns
    (+,+,-) = Liquidating Assets
    (-,+,+) = Distress Signal
    (-,-,+) = Growth Funded by Debt
    (+,+,+) = Cash Accumulator
    (-,-,-) = Pre-Revenue
    (+,-,+) = Mixed
    """

    sign = (
        cfo > 0,
        cfi > 0,
        cff > 0
    )

    if sign == (True, False, False):

        if cfo_pat_ratio is not None and cfo_pat_ratio > 1:
            return "Shareholder Returns"

        return "Reinvestor"

    elif sign == (True, True, False):
        return "Liquidating Assets"

    elif sign == (False, True, True):
        return "Distress Signal"

    elif sign == (False, False, True):
        return "Growth Funded by Debt"

    elif sign == (True, True, True):
        return "Cash Accumulator"

    elif sign == (False, False, False):
        return "Pre-Revenue"

    elif sign == (True, False, True):
        return "Mixed"

    return "Unknown"


# -----------------------------------------------------
# Demo
# -----------------------------------------------------

if __name__ == "__main__":

    print("=" * 60)
    print("DAY 11 - CASH FLOW KPI ENGINE")
    print("=" * 60)

    # -------------------------
    # Free Cash Flow
    # -------------------------

    print("\nFree Cash Flow")
    print("-" * 40)

    fcf = free_cash_flow(2500, -900)

    print("Operating Activity :", 2500)
    print("Investing Activity :", -900)
    print("Free Cash Flow     :", fcf)

    # -------------------------
    # CFO Quality
    # -------------------------

    print("\nCFO Quality Score")
    print("-" * 40)

    result = cfo_quality_score(1800, 1500)

    print("CFO :", 1800)
    print("PAT :", 1500)
    print("Result :", result)

    # -------------------------
    # CapEx Intensity
    # -------------------------

    print("\nCapEx Intensity")
    print("-" * 40)

    result = capex_intensity(-600, 10000)

    print("Investing Activity :", -600)
    print("Sales              :", 10000)
    print("Result             :", result)

    # -------------------------
    # FCF Conversion
    # -------------------------

    print("\nFCF Conversion Rate")
    print("-" * 40)

    result = fcf_conversion_rate(fcf, 2000)

    print("FCF               :", fcf)
    print("Operating Profit  :", 2000)
    print("Conversion (%)    :", result)

    # -------------------------
    # Capital Allocation
    # -------------------------

    print("\nCapital Allocation Pattern")
    print("-" * 40)

    pattern = capital_allocation_pattern(
        cfo=2500,
        cfi=-900,
        cff=-500,
        cfo_pat_ratio=1.2
    )

    print("Pattern :", pattern)

    print("\nDay 11 Cash Flow KPI Engine Completed Successfully.")