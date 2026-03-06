from __future__ import annotations

from shared.engine.inputs import DeterministicInput
from shared.engine.sensitivity import compute_sensitivity


def _base_input() -> DeterministicInput:
    return DeterministicInput(
        household_monthly_net_income_pence=300_000,
        household_monthly_essential_spend_pence=180_000,
        household_monthly_debt_payments_pence=40_000,
        cash_savings_pence=600_000,
        mortgage_balance_pence=15_000_000,
        mortgage_term_months_remaining=300,
        mortgage_rate_bps_current=450,
        mortgage_rate_bps_stress=600,
        mortgage_type="repayment",
        shock_monthly_income_drop_bps=1_000,
        inflation_monthly_essentials_increase_bps=500,
        household_monthly_net_income_currency="GBP",
        household_monthly_essential_spend_currency="GBP",
        household_monthly_debt_payments_currency="GBP",
        cash_savings_currency="GBP",
        mortgage_balance_currency="GBP",
        reporting_currency="GBP",
        fx_spot_rates={"GBP": 1.0, "EUR": 0.86, "USD": 0.78},
        fx_stress_bps={"GBP": 0, "EUR": 0, "USD": 0},
        horizon_months=12,
    )


def test_compute_sensitivity_returns_ranked_driver_impacts() -> None:
    impacts = compute_sensitivity(_base_input(), delta_bps=100)

    assert len(impacts) == 4
    assert {item.driver for item in impacts} == {
        "income_shock_bps",
        "inflation_shock_bps",
        "mortgage_rate_stress_bps",
        "fx_stress_bps",
    }

    abs_impacts = [abs(item.min_savings_impact_pence) for item in impacts]
    assert abs_impacts == sorted(abs_impacts, reverse=True)
    assert any(
        item.min_savings_impact_pence != 0
        or (item.runway_months_impact is not None and item.runway_months_impact != 0)
        for item in impacts
    )


def test_compute_sensitivity_is_deterministic_for_same_input() -> None:
    first = compute_sensitivity(_base_input(), delta_bps=100)
    second = compute_sensitivity(_base_input(), delta_bps=100)

    assert [item.model_dump() for item in first] == [item.model_dump() for item in second]
