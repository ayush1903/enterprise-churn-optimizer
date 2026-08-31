"""Unit tests for the RiskScore heuristic in eda_and_cleaning.calculate_risk.

Run with: pytest tests/test_calculate_risk.py -v
"""
import sys
import os
import pandas as pd
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "02_Data_Analytics"))

from eda_and_cleaning import calculate_risk  # noqa: E402


def make_row(contract="Two year", payment="Mailed check", tenure=36, internet="DSL"):
    return pd.Series({
        "Contract": contract,
        "PaymentMethod": payment,
        "tenure": tenure,
        "InternetService": internet,
    })


class TestContractComponent:
    def test_month_to_month_adds_40(self):
        row = make_row(contract="Month-to-month", payment="Mailed check", tenure=36, internet="DSL")
        assert calculate_risk(row) == 40

    def test_one_year_adds_15(self):
        row = make_row(contract="One year", payment="Mailed check", tenure=36, internet="DSL")
        assert calculate_risk(row) == 15

    def test_two_year_adds_nothing(self):
        row = make_row(contract="Two year", payment="Mailed check", tenure=36, internet="DSL")
        assert calculate_risk(row) == 0


class TestPaymentComponent:
    def test_electronic_check_adds_25(self):
        row = make_row(contract="Two year", payment="Electronic check", tenure=36, internet="DSL")
        assert calculate_risk(row) == 25

    def test_other_payment_methods_add_nothing(self):
        for method in ["Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"]:
            row = make_row(contract="Two year", payment=method, tenure=36, internet="DSL")
            assert calculate_risk(row) == 0


class TestTenureComponent:
    def test_tenure_at_or_under_12_adds_25(self):
        row = make_row(tenure=12)
        assert calculate_risk(row) == 25

    def test_tenure_zero_adds_25(self):
        row = make_row(tenure=0)
        assert calculate_risk(row) == 25

    def test_tenure_13_to_24_adds_10(self):
        row = make_row(tenure=24)
        assert calculate_risk(row) == 10
        row = make_row(tenure=13)
        assert calculate_risk(row) == 10

    def test_tenure_over_24_adds_nothing(self):
        row = make_row(tenure=25)
        assert calculate_risk(row) == 0


class TestInternetServiceComponent:
    def test_fiber_optic_adds_10(self):
        row = make_row(internet="Fiber optic")
        assert calculate_risk(row) == 10

    def test_other_internet_adds_nothing(self):
        for service in ["DSL", "No"]:
            row = make_row(internet=service)
            assert calculate_risk(row) == 0


class TestCombinedScoresAndCap:
    def test_worst_case_customer_hits_cap_of_100(self):
        row = make_row(
            contract="Month-to-month",
            payment="Electronic check",
            tenure=1,
            internet="Fiber optic",
        )
        # 40 + 25 + 25 + 10 = 100, at the cap boundary
        assert calculate_risk(row) == 100

    def test_best_case_customer_scores_zero(self):
        row = make_row(
            contract="Two year",
            payment="Bank transfer (automatic)",
            tenure=60,
            internet="DSL",
        )
        assert calculate_risk(row) == 0

    def test_mixed_profile_sums_correctly(self):
        # Month-to-month (40) + electronic check (25) + tenure 24 (10) + DSL (0) = 75
        row = make_row(
            contract="Month-to-month",
            payment="Electronic check",
            tenure=24,
            internet="DSL",
        )
        assert calculate_risk(row) == 75


class TestRiskTierBinning:
    """Verify the RiskScore -> RiskTier bins used in run_data_pipeline stay aligned
    with calculate_risk's output range."""

    @pytest.mark.parametrize("score,expected_tier", [
        (0, "Low Risk"),
        (39, "Low Risk"),
        (40, "Medium Risk"),
        (69, "Medium Risk"),
        (70, "High Risk"),
        (100, "High Risk"),
    ])
    def test_tier_boundaries(self, score, expected_tier):
        tier = pd.cut(
            pd.Series([score]),
            bins=[-1, 39, 69, 100],
            labels=["Low Risk", "Medium Risk", "High Risk"],
        )[0]
        assert tier == expected_tier
