"""
test_cashflow_kpis.py

Unit tests for Cash Flow KPIs.
"""

import unittest

from src.analytics.cashflow_kpis import (
    free_cash_flow,
    cfo_quality_score,
    capex_intensity,
    fcf_conversion_rate,
    capital_allocation_pattern
)


class TestCashFlowKPIs(unittest.TestCase):

    # -------------------------------------------------
    # Free Cash Flow Tests
    # -------------------------------------------------

    def test_free_cash_flow(self):
        self.assertEqual(
            free_cash_flow(2500, -900),
            1600
        )

    def test_negative_free_cash_flow(self):
        self.assertEqual(
            free_cash_flow(500, -1000),
            -500
        )

    def test_free_cash_flow_none(self):
        self.assertIsNone(
            free_cash_flow(None, -900)
        )

    # -------------------------------------------------
    # CFO Quality Score Tests
    # -------------------------------------------------

    def test_high_quality(self):
        self.assertEqual(
            cfo_quality_score(1800, 1500),
            (1.2, "High Quality")
        )

    def test_moderate_quality(self):
        self.assertEqual(
            cfo_quality_score(700, 1000),
            (0.7, "Moderate")
        )

    def test_accrual_risk(self):
        self.assertEqual(
            cfo_quality_score(200, 1000),
            (0.2, "Accrual Risk")
        )

    def test_pat_zero(self):
        self.assertIsNone(
            cfo_quality_score(1000, 0)
        )

    # -------------------------------------------------
    # CapEx Intensity Tests
    # -------------------------------------------------

    def test_asset_light(self):
        self.assertEqual(
            capex_intensity(-150, 10000),
            (1.5, "Asset Light")
        )

    def test_moderate(self):
        self.assertEqual(
            capex_intensity(-600, 10000),
            (6.0, "Moderate")
        )

    def test_capital_intensive(self):
        self.assertEqual(
            capex_intensity(-1500, 10000),
            (15.0, "Capital Intensive")
        )

    def test_sales_zero(self):
        self.assertIsNone(
            capex_intensity(-500, 0)
        )

    # -------------------------------------------------
    # FCF Conversion Tests
    # -------------------------------------------------

    def test_fcf_conversion(self):
        self.assertEqual(
            fcf_conversion_rate(1600, 2000),
            80.0
        )

    def test_fcf_conversion_zero_profit(self):
        self.assertIsNone(
            fcf_conversion_rate(1600, 0)
        )

    # -------------------------------------------------
    # Capital Allocation Pattern Tests
    # -------------------------------------------------

    def test_shareholder_returns(self):
        self.assertEqual(
            capital_allocation_pattern(
                2500,
                -900,
                -500,
                1.2
            ),
            "Shareholder Returns"
        )

    def test_reinvestor(self):
        self.assertEqual(
            capital_allocation_pattern(
                2500,
                -900,
                -500,
                0.8
            ),
            "Reinvestor"
        )

    def test_liquidating_assets(self):
        self.assertEqual(
            capital_allocation_pattern(
                1000,
                500,
                -300
            ),
            "Liquidating Assets"
        )

    def test_distress_signal(self):
        self.assertEqual(
            capital_allocation_pattern(
                -100,
                500,
                300
            ),
            "Distress Signal"
        )

    def test_growth_funded_by_debt(self):
        self.assertEqual(
            capital_allocation_pattern(
                -100,
                -500,
                300
            ),
            "Growth Funded by Debt"
        )

    def test_cash_accumulator(self):
        self.assertEqual(
            capital_allocation_pattern(
                500,
                300,
                200
            ),
            "Cash Accumulator"
        )

    def test_pre_revenue(self):
        self.assertEqual(
            capital_allocation_pattern(
                -500,
                -300,
                -200
            ),
            "Pre-Revenue"
        )

    def test_mixed(self):
        self.assertEqual(
            capital_allocation_pattern(
                500,
                -300,
                200
            ),
            "Mixed"
        )


if __name__ == "__main__":
    unittest.main()