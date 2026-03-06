from __future__ import annotations

from decimal import Decimal

from .money import divide_round_half_up, round_half_up_int


def mortgage_payment_interest_only(balance_pence: int, annual_rate_bps: int) -> int:
    """Return monthly interest-only mortgage payment in pence."""
    if balance_pence <= 0:
        return 0
    if annual_rate_bps < 0:
        raise ValueError("annual_rate_bps must be >= 0")
    return divide_round_half_up(balance_pence * annual_rate_bps, 120_000)


def mortgage_payment_repayment(balance_pence: int, annual_rate_bps: int, term_months: int) -> int:
    """Return monthly repayment mortgage payment in pence."""
    if balance_pence <= 0:
        return 0
    if annual_rate_bps < 0:
        raise ValueError("annual_rate_bps must be >= 0")
    if term_months <= 0:
        raise ValueError("term_months must be > 0 when balance_pence > 0")

    if annual_rate_bps == 0:
        return divide_round_half_up(balance_pence, term_months)

    principal = Decimal(balance_pence)
    monthly_rate = Decimal(annual_rate_bps) / Decimal(120_000)
    factor = (Decimal("1") + monthly_rate) ** term_months
    payment = principal * (monthly_rate * factor) / (factor - Decimal("1"))
    return round_half_up_int(payment)
