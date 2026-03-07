from __future__ import annotations

from shared.engine.deterministic import run_deterministic
from shared.engine.inputs import DebtItem, DeterministicInput


def _base_input() -> DeterministicInput:
    return DeterministicInput(
        household_monthly_net_income_pence=0,
        household_monthly_essential_spend_pence=0,
        household_monthly_debt_payments_pence=0,
        cash_savings_pence=0,
        mortgage_balance_pence=0,
        mortgage_term_months_remaining=0,
        mortgage_rate_bps_current=0,
        mortgage_rate_bps_stress=0,
        mortgage_type="repayment",
        shock_monthly_income_drop_bps=0,
        inflation_monthly_essentials_increase_bps=0,
        horizon_months=3,
    )


def test_debt_schedule_pays_down_to_zero() -> None:
    inputs = _base_input().model_copy(
        update={
            "household_monthly_net_income_pence": 10_000,
            "horizon_months": 4,
            "debts": [
                DebtItem(balance_pence=10_000, apr_bps=0, min_payment_pence=3_000),
            ],
        },
        deep=True,
    )

    output = run_deterministic(inputs)

    assert output.debt_balance_path_pence == [10_000, 7_000, 4_000, 1_000, 0]
    assert output.monthly_cashflow_stress_pence == 7_000


def test_debt_schedule_accrues_interest_before_payment() -> None:
    inputs = _base_input().model_copy(
        update={
            "debts": [
                DebtItem(balance_pence=120_000, apr_bps=1_200, min_payment_pence=1_000),
            ],
            "horizon_months": 3,
        },
        deep=True,
    )

    output = run_deterministic(inputs)

    assert output.debt_balance_path_pence == [120_000, 120_200, 120_402, 120_606]
    assert output.monthly_cashflow_stress_pence == -1_000
