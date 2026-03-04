from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP


def _to_decimal(value: Decimal | int | float | str) -> Decimal:
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))


def round_half_up_int(value: Decimal | int | float | str) -> int:
    return int(_to_decimal(value).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def round_half_up_decimal(value: Decimal | int | float | str, places: int) -> Decimal:
    exponent = Decimal("1").scaleb(-places)
    return _to_decimal(value).quantize(exponent, rounding=ROUND_HALF_UP)


def gbp_to_pence(amount_gbp: Decimal | int | float | str) -> int:
    return round_half_up_int(_to_decimal(amount_gbp) * Decimal("100"))


def percent_to_bps(percent: Decimal | int | float | str) -> int:
    return round_half_up_int(_to_decimal(percent) * Decimal("100"))


def years_to_months(years: Decimal | int | float | str) -> int:
    return round_half_up_int(_to_decimal(years) * Decimal("12"))


def divide_round_half_up(numerator: int, denominator: int) -> int:
    if denominator <= 0:
        raise ValueError("denominator must be > 0")

    sign = -1 if numerator < 0 else 1
    quotient = (abs(numerator) + denominator // 2) // denominator
    return sign * quotient


def apply_bps(amount: int, bps: int) -> int:
    return divide_round_half_up(amount * bps, 10_000)


def pence_to_gbp_decimal(pence: int) -> Decimal:
    return Decimal(pence) / Decimal("100")


def format_currency_from_pence(pence: int, symbol: str = "£") -> str:
    sign = "-" if pence < 0 else ""
    absolute = abs(pence)
    pounds = absolute // 100
    pennies = absolute % 100
    return f"{sign}{symbol}{pounds:,}.{pennies:02d}"
