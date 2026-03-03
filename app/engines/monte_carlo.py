"""
Monte Carlo probabilistic stress test engine.

Models uncertainty in:
- Income shock severity (normally distributed around the deterministic shock)
- Mortgage rate change magnitude (normally distributed around the deterministic stress rate)
- Essentials inflation increase (normally distributed around the deterministic value)

Safe upper bound on trials: 50,000 (enforced by Pydantic validator in MonteCarloInput).
"""

from __future__ import annotations

import numpy as np

from app.engines.deterministic import _monthly_mortgage_payment
from app.models.inputs import MonteCarloInput
from app.models.outputs import DISCLAIMER, MonteCarloOutput


def run_monte_carlo(inputs: MonteCarloInput) -> MonteCarloOutput:
    """Run Monte Carlo simulation and return P10/P50/P90 outputs."""
    rng = np.random.default_rng()

    n = inputs.num_trials

    # Sample stochastic inputs
    income_shock_samples = np.clip(
        rng.normal(
            loc=inputs.shock_monthly_income_drop_percent,
            scale=inputs.income_shock_std_percent,
            size=n,
        ),
        0,
        100,
    )

    stress_rate_samples = np.clip(
        rng.normal(
            loc=inputs.mortgage_rate_percent_stress,
            scale=inputs.rate_shock_std_percent,
            size=n,
        ),
        0,
        100,
    )

    inflation_samples = np.clip(
        rng.normal(
            loc=inputs.inflation_monthly_essentials_increase_percent,
            scale=inputs.inflation_shock_std_percent,
            size=n,
        ),
        0,
        100,
    )

    # Compute mortgage payments for all trials (vectorised via numpy)
    mortgage_payments = np.array(
        [
            _monthly_mortgage_payment(
                inputs.mortgage_balance_gbp,
                rate,
                inputs.mortgage_term_years_remaining,
                inputs.mortgage_type,
            )
            for rate in stress_rate_samples
        ]
    )

    stressed_incomes = inputs.household_monthly_net_income_gbp * (1 - income_shock_samples / 100.0)
    stressed_essentials = inputs.household_monthly_essential_spend_gbp * (
        1 + inflation_samples / 100.0
    )

    cashflows = (
        stressed_incomes
        - stressed_essentials
        - inputs.household_monthly_debt_payments_gbp
        - mortgage_payments
    )

    # Runway: per-trial
    runways = np.where(
        cashflows < 0,
        inputs.cash_savings_gbp / np.abs(cashflows),
        np.nan,
    )

    # Percentiles
    p10_cf, p50_cf, p90_cf = np.percentile(cashflows, [10, 50, 90])

    # Runway percentiles — only over trials where runway is finite (i.e. cashflow < 0)
    finite_runways = runways[np.isfinite(runways)]
    if len(finite_runways) > 0:
        p10_r, p50_r, p90_r = np.percentile(finite_runways, [10, 50, 90])
    else:
        p10_r = p50_r = p90_r = None

    prob_negative = float(np.mean(cashflows < 0))
    prob_lt_3 = float(np.mean(runways < 3) if len(finite_runways) > 0 else 0.0)

    return MonteCarloOutput(
        p10_monthly_cashflow_gbp=round(float(p10_cf), 2),
        p50_monthly_cashflow_gbp=round(float(p50_cf), 2),
        p90_monthly_cashflow_gbp=round(float(p90_cf), 2),
        p10_runway_months=round(float(p10_r), 2) if p10_r is not None else None,
        p50_runway_months=round(float(p50_r), 2) if p50_r is not None else None,
        p90_runway_months=round(float(p90_r), 2) if p90_r is not None else None,
        probability_negative_cashflow=round(prob_negative, 4),
        probability_runway_lt_3_months=round(prob_lt_3, 4),
        num_trials=n,
        disclaimer=DISCLAIMER,
    )
