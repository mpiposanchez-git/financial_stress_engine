from __future__ import annotations

from shared.engine.deterministic import run_deterministic
from shared.engine.inputs import DeterministicInput, ShockSchedule


def _base_input() -> DeterministicInput:
    return DeterministicInput(
        household_monthly_net_income_pence=100_000,
        household_monthly_essential_spend_pence=100_000,
        household_monthly_debt_payments_pence=0,
        cash_savings_pence=100_000,
        mortgage_balance_pence=0,
        mortgage_term_months_remaining=0,
        mortgage_rate_bps_current=300,
        mortgage_rate_bps_stress=300,
        mortgage_type="repayment",
        shock_monthly_income_drop_bps=0,
        inflation_monthly_essentials_increase_bps=0,
        horizon_months=4,
    )


def test_step_schedule_applies_constant_income_shock() -> None:
    inputs = _base_input().model_copy(
        update={
            "income_shock_schedule": ShockSchedule(kind="step", level_bps=1_000),
        },
        deep=True,
    )

    output = run_deterministic(inputs)

    assert output.monthly_cashflow_stress_pence == -10_000
    assert output.savings_path_pence == [100_000, 90_000, 80_000, 70_000, 60_000]


def test_ramp_schedule_applies_linear_inflation_change() -> None:
    inputs = _base_input().model_copy(
        update={
            "inflation_shock_schedule": ShockSchedule(kind="ramp", level_bps=2_000, end_month=4),
        },
        deep=True,
    )

    output = run_deterministic(inputs)

    # Month 1 is unchanged; months 2-4 gradually increase inflation drag.
    assert output.monthly_cashflow_stress_pence == 0
    assert output.savings_path_pence == [100_000, 100_000, 93_330, 80_000, 60_000]


def test_stepped_schedule_applies_mortgage_rate_changes_by_month() -> None:
    inputs = _base_input().model_copy(
        update={
            "household_monthly_essential_spend_pence": 70_000,
            "mortgage_balance_pence": 3_000_000,
            "mortgage_term_months_remaining": 120,
            "mortgage_rate_bps_stress": 300,
            "mortgage_rate_stress_schedule": ShockSchedule(
                kind="stepped",
                points=[(1, 300), (3, 900)],
            ),
        },
        deep=True,
    )

    output = run_deterministic(inputs)

    monthly_deltas = [
        output.savings_path_pence[idx + 1] - output.savings_path_pence[idx]
        for idx in range(len(output.savings_path_pence) - 1)
    ]

    # Cashflow after the month-3 rate jump should be weaker than month 2.
    assert monthly_deltas[2] < monthly_deltas[1]
