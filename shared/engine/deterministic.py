"""
Deterministic stress test engine.

Runway logic:
- If monthly_cashflow < 0: runway = cash_savings / abs(monthly_cashflow)
- If monthly_cashflow >= 0: runway = None  (household is not drawing down savings)
  This is documented as "solvent under stress — no runway consumption modelled".
"""

from shared.engine.inputs import DeterministicInput
from shared.engine.outputs import DISCLAIMER, DeterministicOutput


def _monthly_mortgage_payment(
    balance: float,
    annual_rate_percent: float,
    term_years: float,
    mortgage_type: str,
) -> float:
    """Calculate monthly mortgage payment.

    For repayment mortgages: standard amortisation formula.
    For interest-only: simple monthly interest.
    Returns 0.0 if balance is 0.
    """
    if balance <= 0:
        return 0.0

    monthly_rate = annual_rate_percent / 100.0 / 12.0
    n = term_years * 12

    if mortgage_type == "interest_only":
        return balance * monthly_rate

    # Repayment (amortising)
    if monthly_rate == 0.0:
        return balance / n if n > 0 else 0.0

    return balance * (monthly_rate * (1 + monthly_rate) ** n) / ((1 + monthly_rate) ** n - 1)


def _compute_runway(monthly_cashflow: float, cash_savings: float) -> float | None:
    """Compute months of runway.

    Returns None when cashflow >= 0 (household is not consuming savings).
    Returns cash_savings / abs(monthly_cashflow) when cashflow < 0.
    """
    if monthly_cashflow >= 0:
        return None
    return cash_savings / abs(monthly_cashflow)


def run_deterministic(inputs: DeterministicInput) -> DeterministicOutput:
    """Run deterministic stress test and return outputs."""
    # Base scenario mortgage payment
    mortgage_current = _monthly_mortgage_payment(
        inputs.mortgage_balance_gbp,
        inputs.mortgage_rate_percent_current,
        inputs.mortgage_term_years_remaining,
        inputs.mortgage_type,
    )

    # Stressed mortgage payment
    mortgage_stress = _monthly_mortgage_payment(
        inputs.mortgage_balance_gbp,
        inputs.mortgage_rate_percent_stress,
        inputs.mortgage_term_years_remaining,
        inputs.mortgage_type,
    )

    # Base cashflow
    cashflow_base = (
        inputs.household_monthly_net_income_gbp
        - inputs.household_monthly_essential_spend_gbp
        - inputs.household_monthly_debt_payments_gbp
        - mortgage_current
    )

    # Stressed cashflow
    stressed_income = inputs.household_monthly_net_income_gbp * (
        1 - inputs.shock_monthly_income_drop_percent / 100.0
    )
    stressed_essentials = inputs.household_monthly_essential_spend_gbp * (
        1 + inputs.inflation_monthly_essentials_increase_percent / 100.0
    )
    cashflow_stress = (
        stressed_income
        - stressed_essentials
        - inputs.household_monthly_debt_payments_gbp
        - mortgage_stress
    )

    runway_base = _compute_runway(cashflow_base, inputs.cash_savings_gbp)
    runway_stress = _compute_runway(cashflow_stress, inputs.cash_savings_gbp)

    # Build summary
    if cashflow_stress >= 0:
        stress_summary = "Under stress, the household remains cash-flow positive."
    else:
        months = f"{runway_stress:.1f}" if runway_stress is not None else "unknown"
        stress_summary = (
            f"Under stress, monthly cashflow is negative (£{cashflow_stress:,.2f}). "
            f"Estimated savings runway: {months} months."
        )

    summary = (
        f"Base monthly cashflow: £{cashflow_base:,.2f}. "
        f"Stressed monthly cashflow: £{cashflow_stress:,.2f}. "
        f"{stress_summary}"
    )

    return DeterministicOutput(
        monthly_cashflow_base_gbp=round(cashflow_base, 2),
        monthly_cashflow_stress_gbp=round(cashflow_stress, 2),
        estimated_months_of_runway_base=round(runway_base, 2) if runway_base is not None else None,
        estimated_months_of_runway_stress=(
            round(runway_stress, 2) if runway_stress is not None else None
        ),
        mortgage_payment_current_gbp=round(mortgage_current, 2),
        mortgage_payment_stress_gbp=round(mortgage_stress, 2),
        summary=summary,
        disclaimer=DISCLAIMER,
    )