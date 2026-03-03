"""Tests for the deterministic stress test engine."""

from app.engines.deterministic import _compute_runway, _monthly_mortgage_payment, run_deterministic
from app.models.inputs import DeterministicInput

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
)


def make_input(**overrides) -> DeterministicInput:
    data = {**BASE_INPUTS, **overrides}
    return DeterministicInput(**data)


class TestMortgagePayment:
    def test_interest_only(self):
        payment = _monthly_mortgage_payment(200000, 5.0, 20, "interest_only")
        expected = 200000 * (5.0 / 100 / 12)
        assert abs(payment - expected) < 0.01

    def test_repayment_positive(self):
        payment = _monthly_mortgage_payment(200000, 5.0, 25, "repayment")
        assert payment > 0

    def test_zero_balance_returns_zero(self):
        assert _monthly_mortgage_payment(0, 5.0, 25, "repayment") == 0.0
        assert _monthly_mortgage_payment(0, 5.0, 25, "interest_only") == 0.0

    def test_zero_rate_repayment(self):
        payment = _monthly_mortgage_payment(120000, 0.0, 10, "repayment")
        assert abs(payment - 1000.0) < 0.01

    def test_repayment_greater_than_interest_only(self):
        repayment = _monthly_mortgage_payment(200000, 4.5, 25, "repayment")
        interest_only = _monthly_mortgage_payment(200000, 4.5, 25, "interest_only")
        assert repayment > interest_only


class TestComputeRunway:
    def test_negative_cashflow_returns_runway(self):
        runway = _compute_runway(-500, 10000)
        assert abs(runway - 20.0) < 0.01

    def test_zero_cashflow_returns_none(self):
        assert _compute_runway(0, 10000) is None

    def test_positive_cashflow_returns_none(self):
        assert _compute_runway(100, 10000) is None

    def test_zero_savings_zero_cashflow(self):
        assert _compute_runway(0, 0) is None

    def test_zero_savings_negative_cashflow(self):
        runway = _compute_runway(-100, 0)
        assert runway == 0.0


class TestRunDeterministic:
    def test_base_output_structure(self):
        result = run_deterministic(make_input())
        assert result.monthly_cashflow_base_gbp is not None
        assert result.monthly_cashflow_stress_gbp is not None
        assert result.disclaimer != ""
        assert "EDUCATIONAL SIMULATION ONLY" in result.disclaimer

    def test_stress_cashflow_less_than_base(self):
        result = run_deterministic(make_input())
        assert result.monthly_cashflow_stress_gbp < result.monthly_cashflow_base_gbp

    def test_stressed_mortgage_greater(self):
        result = run_deterministic(make_input())
        assert result.mortgage_payment_stress_gbp > result.mortgage_payment_current_gbp

    def test_zero_income(self):
        result = run_deterministic(make_input(household_monthly_net_income_gbp=0))
        assert result.monthly_cashflow_base_gbp < 0
        assert result.estimated_months_of_runway_base is not None

    def test_zero_savings_negative_cashflow(self):
        result = run_deterministic(
            make_input(
                cash_savings_gbp=0,
                household_monthly_net_income_gbp=0,
            )
        )
        assert result.estimated_months_of_runway_base == 0.0

    def test_positive_cashflow_no_runway(self):
        result = run_deterministic(
            make_input(
                household_monthly_net_income_gbp=10000,
                household_monthly_essential_spend_gbp=1000,
                household_monthly_debt_payments_gbp=0,
                mortgage_balance_gbp=0,
                mortgage_term_years_remaining=0,
                shock_monthly_income_drop_percent=0,
                inflation_monthly_essentials_increase_percent=0,
            )
        )
        assert result.estimated_months_of_runway_base is None
        assert result.estimated_months_of_runway_stress is None

    def test_extreme_rate_shock(self):
        result = run_deterministic(make_input(mortgage_rate_percent_stress=20.0))
        assert result.monthly_cashflow_stress_gbp < result.monthly_cashflow_base_gbp

    def test_interest_only(self):
        result = run_deterministic(make_input(mortgage_type="interest_only"))
        assert result.mortgage_payment_current_gbp > 0
        assert result.mortgage_payment_stress_gbp > result.mortgage_payment_current_gbp

    def test_no_mortgage(self):
        result = run_deterministic(
            make_input(mortgage_balance_gbp=0, mortgage_term_years_remaining=0)
        )
        assert result.mortgage_payment_current_gbp == 0.0
        assert result.mortgage_payment_stress_gbp == 0.0

    def test_summary_contains_cashflow(self):
        result = run_deterministic(make_input())
        assert "cashflow" in result.summary.lower()
