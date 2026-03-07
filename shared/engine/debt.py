from __future__ import annotations

from shared.engine.money import divide_round_half_up


def _monthly_interest_pence(balance_pence: int, apr_bps: int) -> int:
    # APR bps is annual; convert to monthly by dividing by 12.
    return divide_round_half_up(balance_pence * apr_bps, 120_000)


def amortize_debts(
    balances_pence: list[int],
    apr_bps: list[int],
    min_payments_pence: list[int],
    horizon_months: int,
) -> tuple[list[int], list[int]]:
    """Return (payment_series, aggregate_balance_path) for debt amortisation."""
    if not (len(balances_pence) == len(apr_bps) == len(min_payments_pence)):
        raise ValueError("debt vectors must have equal length")

    balances = list(balances_pence)
    aggregate_path = [sum(balances)]
    payment_series: list[int] = []

    for _month in range(horizon_months):
        month_payment_total = 0
        next_balances: list[int] = []

        for balance, apr, min_payment in zip(balances, apr_bps, min_payments_pence, strict=True):
            if balance <= 0:
                next_balances.append(0)
                continue

            accrued = balance + _monthly_interest_pence(balance, apr)
            payment = min(min_payment, accrued)
            next_balance = accrued - payment

            month_payment_total += payment
            next_balances.append(next_balance)

        payment_series.append(month_payment_total)
        balances = next_balances
        aggregate_path.append(sum(balances))

    return payment_series, aggregate_path
