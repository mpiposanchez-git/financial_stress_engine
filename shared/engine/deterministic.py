"""
Deterministic stress test engine.

Runway logic:
- If monthly_cashflow_pence < 0: runway = cash_savings_pence / abs(monthly_cashflow_pence)
- If monthly_cashflow_pence >= 0: runway = None (household is not drawing down savings)
  This is documented as "solvent under stress — no runway consumption modelled".
"""

from decimal import Decimal

from shared.engine.fx import (
    convert_minor_units,
    currency_symbol,
    get_spot_rate_to_reporting,
    stressed_rate,
    validate_currency,
)
from shared.engine.inflation_categories import (
    categories_total_pence,
    stressed_categories_total_pence,
)
from shared.engine.inputs import DeterministicInput
from shared.engine.money import (
    apply_bps,
    format_currency_from_pence,
    round_half_up_decimal,
)
from shared.engine.mortgage import mortgage_payment_interest_only, mortgage_payment_repayment
from shared.engine.outputs import DISCLAIMER, DeterministicOutput
from shared.engine.savings_path import compute_savings_path, min_savings, month_of_depletion
from shared.engine.schedules import resolve_schedule_levels


def _monthly_mortgage_payment(
    balance_pence: int,
    annual_rate_bps: int,
    term_months: int,
    mortgage_type: str,
) -> int:
    """Calculate monthly mortgage payment.

    For repayment mortgages: standard amortisation formula.
    For interest-only: simple monthly interest.
    Returns 0 if balance is 0.
    """
    if balance_pence <= 0:
        return 0

    if mortgage_type == "interest_only":
        return mortgage_payment_interest_only(balance_pence, annual_rate_bps)

    return mortgage_payment_repayment(balance_pence, annual_rate_bps, term_months)


def _compute_runway(monthly_cashflow_pence: int, cash_savings_pence: int) -> Decimal | None:
    """Compute months of runway.

    Returns None when cashflow >= 0 (household is not consuming savings).
    Returns cash_savings / abs(monthly_cashflow) when cashflow < 0.
    """
    if monthly_cashflow_pence >= 0:
        return None
    return Decimal(cash_savings_pence) / Decimal(abs(monthly_cashflow_pence))


def _convert_to_reporting(
    amount_pence: int,
    source_currency: str,
    fx_rates: dict[str, Decimal],
) -> int:
    rate = fx_rates[validate_currency(source_currency)]
    return convert_minor_units(amount_pence, rate)


def run_deterministic(inputs: DeterministicInput) -> DeterministicOutput:
    """Run deterministic stress test and return outputs."""
    reporting_currency = validate_currency(inputs.reporting_currency)
    symbol = currency_symbol(reporting_currency)

    fx_spot_rates_used: dict[str, Decimal] = {
        code: get_spot_rate_to_reporting(code, inputs.fx_spot_rates)
        for code in sorted(inputs.fx_spot_rates.keys())
    }
    fx_stress_bps_used: dict[str, int] = {
        code: int(inputs.fx_stress_bps.get(code, 0)) for code in sorted(fx_spot_rates_used.keys())
    }
    fx_stressed_rates_used: dict[str, Decimal] = {
        code: stressed_rate(spot, fx_stress_bps_used.get(code, 0))
        for code, spot in fx_spot_rates_used.items()
    }

    # Base scenario mortgage payment
    mortgage_current_source = _monthly_mortgage_payment(
        inputs.mortgage_balance_pence,
        inputs.mortgage_rate_bps_current,
        inputs.mortgage_term_months_remaining,
        inputs.mortgage_type,
    )
    mortgage_current = _convert_to_reporting(
        mortgage_current_source,
        inputs.mortgage_balance_currency,
        fx_spot_rates_used,
    )

    income_shock_levels = resolve_schedule_levels(
        inputs.shock_monthly_income_drop_bps,
        inputs.horizon_months,
        inputs.income_shock_schedule,
    )
    inflation_levels = resolve_schedule_levels(
        inputs.inflation_monthly_essentials_increase_bps,
        inputs.horizon_months,
        inputs.inflation_shock_schedule,
    )
    mortgage_rate_levels = resolve_schedule_levels(
        inputs.mortgage_rate_bps_stress,
        inputs.horizon_months,
        inputs.mortgage_rate_stress_schedule,
    )

    income_base = _convert_to_reporting(
        inputs.household_monthly_net_income_pence,
        inputs.household_monthly_net_income_currency,
        fx_spot_rates_used,
    )
    essentials_base_source = (
        categories_total_pence(inputs.essentials_categories)
        if inputs.essentials_categories
        else inputs.household_monthly_essential_spend_pence
    )
    essentials_base = _convert_to_reporting(
        essentials_base_source,
        inputs.household_monthly_essential_spend_currency,
        fx_spot_rates_used,
    )
    debt_base = _convert_to_reporting(
        inputs.household_monthly_debt_payments_pence,
        inputs.household_monthly_debt_payments_currency,
        fx_spot_rates_used,
    )
    cash_savings_base = _convert_to_reporting(
        inputs.cash_savings_pence,
        inputs.cash_savings_currency,
        fx_spot_rates_used,
    )

    # Base cashflow
    cashflow_base = income_base - essentials_base - debt_base - mortgage_current

    stressed_debt = _convert_to_reporting(
        inputs.household_monthly_debt_payments_pence,
        inputs.household_monthly_debt_payments_currency,
        fx_stressed_rates_used,
    )
    cash_savings_stress = _convert_to_reporting(
        inputs.cash_savings_pence,
        inputs.cash_savings_currency,
        fx_stressed_rates_used,
    )

    cashflow_stress_series: list[int] = []
    mortgage_stress_series: list[int] = []

    for month_idx in range(inputs.horizon_months):
        stressed_income_source = apply_bps(
            inputs.household_monthly_net_income_pence,
            10_000 - income_shock_levels[month_idx],
        )
        if inputs.essentials_categories:
            stressed_essentials_source = stressed_categories_total_pence(
                inputs.essentials_categories
            )
        else:
            stressed_essentials_source = apply_bps(
                inputs.household_monthly_essential_spend_pence,
                10_000 + inflation_levels[month_idx],
            )
        stressed_income = _convert_to_reporting(
            stressed_income_source,
            inputs.household_monthly_net_income_currency,
            fx_stressed_rates_used,
        )
        stressed_essentials = _convert_to_reporting(
            stressed_essentials_source,
            inputs.household_monthly_essential_spend_currency,
            fx_stressed_rates_used,
        )

        mortgage_stress_source = _monthly_mortgage_payment(
            inputs.mortgage_balance_pence,
            mortgage_rate_levels[month_idx],
            inputs.mortgage_term_months_remaining,
            inputs.mortgage_type,
        )
        mortgage_stress = _convert_to_reporting(
            mortgage_stress_source,
            inputs.mortgage_balance_currency,
            fx_stressed_rates_used,
        )
        mortgage_stress_series.append(mortgage_stress)

        cashflow_stress_series.append(
            stressed_income - stressed_essentials - stressed_debt - mortgage_stress
        )

    cashflow_stress = cashflow_stress_series[0]
    mortgage_stress = mortgage_stress_series[0]

    runway_base = _compute_runway(cashflow_base, cash_savings_base)
    runway_stress = _compute_runway(cashflow_stress, cash_savings_stress)
    savings_path_pence = compute_savings_path(
        cash_savings_stress,
        cashflow_stress_series,
    )
    min_savings_pence = min_savings(savings_path_pence)
    depletion_month = month_of_depletion(savings_path_pence)

    # Build summary
    if cashflow_stress >= 0:
        stress_summary = "Under stress, the household remains cash-flow positive."
    else:
        months = (
            f"{round_half_up_decimal(runway_stress, 1):.1f}"
            if runway_stress is not None
            else "unknown"
        )
        stress_summary = (
            "Under stress, monthly cashflow is negative "
            f"({format_currency_from_pence(cashflow_stress, symbol=symbol)}). "
            f"Estimated savings runway: {months} months."
        )

    summary = (
        f"Base monthly cashflow: {format_currency_from_pence(cashflow_base, symbol=symbol)}. "
        f"Stressed monthly cashflow: {format_currency_from_pence(cashflow_stress, symbol=symbol)}. "
        f"{stress_summary}"
    )

    return DeterministicOutput(
        reporting_currency=reporting_currency,
        fx_spot_rates_used={k: float(v) for k, v in fx_spot_rates_used.items()},
        fx_stressed_rates_used={k: float(v) for k, v in fx_stressed_rates_used.items()},
        fx_stress_bps=fx_stress_bps_used,
        monthly_cashflow_base_pence=cashflow_base,
        monthly_cashflow_base_formatted=format_currency_from_pence(cashflow_base, symbol=symbol),
        monthly_cashflow_stress_pence=cashflow_stress,
        monthly_cashflow_stress_formatted=format_currency_from_pence(
            cashflow_stress, symbol=symbol
        ),
        estimated_months_of_runway_base=(
            float(round_half_up_decimal(runway_base, 2)) if runway_base is not None else None
        ),
        estimated_months_of_runway_stress=(
            float(round_half_up_decimal(runway_stress, 2)) if runway_stress is not None else None
        ),
        mortgage_payment_current_pence=mortgage_current,
        mortgage_payment_current_formatted=format_currency_from_pence(
            mortgage_current, symbol=symbol
        ),
        mortgage_payment_stress_pence=mortgage_stress,
        mortgage_payment_stress_formatted=format_currency_from_pence(
            mortgage_stress, symbol=symbol
        ),
        savings_path_pence=savings_path_pence,
        savings_path_formatted=[
            format_currency_from_pence(value, symbol=symbol) for value in savings_path_pence
        ],
        min_savings_pence=min_savings_pence,
        min_savings_formatted=format_currency_from_pence(min_savings_pence, symbol=symbol),
        month_of_depletion=depletion_month,
        runway_months=(
            float(round_half_up_decimal(runway_stress, 2)) if runway_stress is not None else None
        ),
        summary=summary,
        disclaimer=DISCLAIMER,
    )
