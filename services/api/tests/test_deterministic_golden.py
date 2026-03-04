from __future__ import annotations

from shared.engine.deterministic import run_deterministic
from shared.engine.inputs import DeterministicInput


def test_deterministic_savings_path_golden() -> None:
    inputs = DeterministicInput(
        household_monthly_net_income_pence=100_000,
        household_monthly_essential_spend_pence=120_000,
        household_monthly_debt_payments_pence=10_000,
        cash_savings_pence=100_000,
        mortgage_balance_pence=0,
        mortgage_term_months_remaining=0,
        mortgage_rate_bps_current=450,
        mortgage_rate_bps_stress=600,
        mortgage_type="repayment",
        shock_monthly_income_drop_bps=0,
        inflation_monthly_essentials_increase_bps=0,
        horizon_months=5,
    )

    output = run_deterministic(inputs)

    expected_path = [100_000, 70_000, 40_000, 10_000, 0, 0]
    expected_formatted = ["£1,000.00", "£700.00", "£400.00", "£100.00", "£0.00", "£0.00"]

    assert output.savings_path_pence == expected_path
    assert output.savings_path_formatted == expected_formatted
    assert output.min_savings_pence == 0
    assert output.min_savings_formatted == "£0.00"
    assert output.month_of_depletion == 4
    assert output.runway_months == 3.33


def test_deterministic_two_currency_reporting_golden() -> None:
    inputs = DeterministicInput(
        household_monthly_net_income_pence=200_000,
        household_monthly_essential_spend_pence=100_000,
        household_monthly_debt_payments_pence=20_000,
        cash_savings_pence=500_000,
        mortgage_balance_pence=0,
        mortgage_term_months_remaining=0,
        mortgage_rate_bps_current=450,
        mortgage_rate_bps_stress=600,
        mortgage_type="repayment",
        shock_monthly_income_drop_bps=1_000,
        inflation_monthly_essentials_increase_bps=500,
        household_monthly_net_income_currency="EUR",
        household_monthly_essential_spend_currency="USD",
        household_monthly_debt_payments_currency="GBP",
        cash_savings_currency="EUR",
        mortgage_balance_currency="USD",
        reporting_currency="GBP",
        fx_spot_rates={"GBP": 1.0, "EUR": 0.86, "USD": 0.78},
        fx_stress_bps={"EUR": 1000, "USD": -500, "GBP": 0},
        horizon_months=3,
    )

    output = run_deterministic(inputs)

    assert output.reporting_currency == "GBP"
    assert output.fx_spot_rates_used["EUR"] == 0.86
    assert output.fx_stressed_rates_used["EUR"] == 0.946
    assert output.fx_stressed_rates_used["USD"] == 0.741

    assert output.monthly_cashflow_base_pence == 74_000
    assert output.monthly_cashflow_stress_pence == 72_475
    assert output.monthly_cashflow_base_formatted == "£740.00"
    assert output.monthly_cashflow_stress_formatted == "£724.75"

    assert output.savings_path_pence == [473_000, 545_475, 617_950, 690_425]
    assert output.min_savings_pence == 473_000
    assert output.min_savings_formatted == "£4,730.00"
    assert output.month_of_depletion is None
    assert output.runway_months is None
