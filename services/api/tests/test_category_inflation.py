from __future__ import annotations

from shared.engine.deterministic import run_deterministic
from shared.engine.inputs import DeterministicInput, EssentialsCategory


def _base_input() -> DeterministicInput:
    return DeterministicInput(
        household_monthly_net_income_pence=200_000,
        household_monthly_essential_spend_pence=100_000,
        household_monthly_debt_payments_pence=10_000,
        cash_savings_pence=500_000,
        mortgage_balance_pence=0,
        mortgage_term_months_remaining=0,
        mortgage_rate_bps_current=450,
        mortgage_rate_bps_stress=600,
        mortgage_type="repayment",
        shock_monthly_income_drop_bps=0,
        inflation_monthly_essentials_increase_bps=500,
        horizon_months=3,
    )


def test_single_category_matches_single_bucket_when_equivalent() -> None:
    bucket = _base_input()
    category = _base_input().model_copy(
        update={
            "essentials_categories": {
                "all": EssentialsCategory(
                    monthly_spend_pence=100_000,
                    inflation_bps=500,
                )
            }
        },
        deep=True,
    )

    bucket_result = run_deterministic(bucket)
    category_result = run_deterministic(category)

    assert (
        category_result.monthly_cashflow_base_pence
        == bucket_result.monthly_cashflow_base_pence
    )
    assert (
        category_result.monthly_cashflow_stress_pence
        == bucket_result.monthly_cashflow_stress_pence
    )
    assert category_result.savings_path_pence == bucket_result.savings_path_pence
    assert category_result.min_savings_pence == bucket_result.min_savings_pence
    assert category_result.runway_months == bucket_result.runway_months


def test_category_totals_override_single_bucket_and_use_per_category_inflation() -> None:
    category = _base_input().model_copy(
        update={
            "household_monthly_essential_spend_pence": 1,
            "essentials_categories": {
                "food": EssentialsCategory(monthly_spend_pence=100_000, inflation_bps=0),
                "energy": EssentialsCategory(monthly_spend_pence=100_000, inflation_bps=2_000),
            },
        },
        deep=True,
    )

    category_result = run_deterministic(category)

    # Base uses category sum (200,000), not single-bucket field (1).
    assert category_result.monthly_cashflow_base_pence == -10_000

    # Stressed essentials = 100,000 + 120,000 = 220,000.
    assert category_result.monthly_cashflow_stress_pence == -30_000
