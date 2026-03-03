"""Tests for the Monte Carlo probabilistic engine."""

import pytest

from app.engines.monte_carlo import run_monte_carlo
from app.models.inputs import MonteCarloInput

BASE_INPUTS = dict(
    household_monthly_net_income_gbp=3500.0,
    household_monthly_essential_spend_gbp=1800.0,
    household_monthly_debt_payments_gbp=200.0,
    cash_savings_gbp=10000.0,
    mortgage_balance_gbp=200000.0,
    mortgage_term_years_remaining=22.0,
    mortgage_rate_percent_current=4.5,
    mortgage_rate_percent_stress=6.5,
    mortgage_type="repayment",
    shock_monthly_income_drop_percent=20.0,
    inflation_monthly_essentials_increase_percent=5.0,
    num_trials=1000,  # smaller for test speed
)


def make_input(**overrides) -> MonteCarloInput:
    data = {**BASE_INPUTS, **overrides}
    return MonteCarloInput(**data)


class TestMonteCarloOutput:
    def test_output_structure(self):
        result = run_monte_carlo(make_input())
        assert result.num_trials == 1000
        assert result.p10_monthly_cashflow_gbp <= result.p50_monthly_cashflow_gbp
        assert result.p50_monthly_cashflow_gbp <= result.p90_monthly_cashflow_gbp

    def test_probabilities_bounded(self):
        result = run_monte_carlo(make_input())
        assert 0.0 <= result.probability_negative_cashflow <= 1.0
        assert 0.0 <= result.probability_runway_lt_3_months <= 1.0

    def test_disclaimer_present(self):
        result = run_monte_carlo(make_input())
        assert "EDUCATIONAL SIMULATION ONLY" in result.disclaimer

    def test_certain_negative_cashflow(self):
        """With zero income, cashflow must always be negative."""
        result = run_monte_carlo(
            make_input(
                household_monthly_net_income_gbp=0,
                shock_monthly_income_drop_percent=0,
                income_shock_std_percent=0,
            )
        )
        assert result.probability_negative_cashflow == 1.0

    def test_certain_positive_cashflow(self):
        """With huge income and zero costs/shocks, cashflow must always be positive."""
        result = run_monte_carlo(
            make_input(
                household_monthly_net_income_gbp=1_000_000,
                household_monthly_essential_spend_gbp=100,
                household_monthly_debt_payments_gbp=0,
                mortgage_balance_gbp=0,
                mortgage_term_years_remaining=0,
                shock_monthly_income_drop_percent=0,
                inflation_monthly_essentials_increase_percent=0,
                income_shock_std_percent=0,
                rate_shock_std_percent=0,
                inflation_shock_std_percent=0,
            )
        )
        assert result.probability_negative_cashflow == 0.0

    def test_trial_count_respected(self):
        result = run_monte_carlo(make_input(num_trials=500))
        assert result.num_trials == 500

    def test_max_trials_enforced_by_pydantic(self):
        with pytest.raises(Exception):
            MonteCarloInput(**{**BASE_INPUTS, "num_trials": 100_000})

    def test_runway_none_when_all_positive(self):
        result = run_monte_carlo(
            make_input(
                household_monthly_net_income_gbp=1_000_000,
                household_monthly_essential_spend_gbp=100,
                household_monthly_debt_payments_gbp=0,
                mortgage_balance_gbp=0,
                mortgage_term_years_remaining=0,
                shock_monthly_income_drop_percent=0,
                inflation_monthly_essentials_increase_percent=0,
                income_shock_std_percent=0,
                rate_shock_std_percent=0,
                inflation_shock_std_percent=0,
            )
        )
        assert result.p10_runway_months is None
        assert result.p50_runway_months is None
        assert result.p90_runway_months is None
