from __future__ import annotations

from shared.engine.inputs import MonteCarloInput, ShockSchedule
from shared.engine.montecarlo import run_montecarlo


def _base_input() -> MonteCarloInput:
    return MonteCarloInput(
        household_monthly_net_income_pence=400_000,
        household_monthly_essential_spend_pence=170_000,
        household_monthly_debt_payments_pence=30_000,
        cash_savings_pence=1_000_000,
        mortgage_balance_pence=20_000_000,
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
        income_shock_std_bps=500,
        rate_shock_std_bps=50,
        inflation_shock_std_bps=100,
        shock_dynamics="ar1",
        ar1_phi=0.5,
        fx_monthly_vol_bps={"EUR": 50, "USD": 50},
    )


def test_montecarlo_scheduled_means_reproducible_with_fixed_seed() -> None:
    scheduled = _base_input().model_copy(
        update={
            "income_shock_schedule": ShockSchedule(kind="ramp", level_bps=2_000, end_month=6),
            "inflation_shock_schedule": ShockSchedule(
                kind="stepped",
                points=[(1, 300), (4, 700), (8, 900)],
            ),
            "mortgage_rate_stress_schedule": ShockSchedule(kind="step", level_bps=700),
        },
        deep=True,
    )

    first = run_montecarlo(scheduled, n_sims=300, horizon_months=12, seed=123456)
    second = run_montecarlo(scheduled, n_sims=300, horizon_months=12, seed=123456)

    assert first.seed == second.seed
    assert first.n_sims == second.n_sims
    assert first.horizon_months == second.horizon_months
    assert first.runway_months == second.runway_months
    assert first.min_savings == second.min_savings
    assert first.month_of_depletion == second.month_of_depletion


def test_montecarlo_schedule_changes_distribution_when_sigma_zero() -> None:
    unscheduled = _base_input().model_copy(
        update={
            "income_shock_std_bps": 0,
            "rate_shock_std_bps": 0,
            "inflation_shock_std_bps": 0,
            "fx_monthly_vol_bps": {"EUR": 0, "USD": 0},
            "shock_dynamics": "iid",
            "ar1_phi": 0.0,
        },
        deep=True,
    )
    scheduled = unscheduled.model_copy(
        update={
            "income_shock_schedule": ShockSchedule(kind="step", level_bps=2_000),
        },
        deep=True,
    )

    baseline = run_montecarlo(unscheduled, n_sims=200, horizon_months=12, seed=42)
    with_schedule = run_montecarlo(scheduled, n_sims=200, horizon_months=12, seed=42)

    assert baseline != with_schedule
    assert with_schedule.min_savings.p50_pence <= baseline.min_savings.p50_pence
