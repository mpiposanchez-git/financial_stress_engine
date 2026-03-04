from __future__ import annotations

from decimal import Decimal
from typing import Literal

from .money import round_half_up_int

CurrencyCode = Literal["GBP", "EUR", "USD"]
SUPPORTED_CURRENCIES: set[str] = {"GBP", "EUR", "USD"}

_CURRENCY_SYMBOLS: dict[str, str] = {
    "GBP": "£",
    "EUR": "€",
    "USD": "$",
}


def validate_currency(code: str) -> str:
    upper = code.upper()
    if upper not in SUPPORTED_CURRENCIES:
        raise ValueError(f"Unsupported currency '{code}'. Supported: GBP, EUR, USD")
    return upper


def currency_symbol(code: str) -> str:
    return _CURRENCY_SYMBOLS[validate_currency(code)]


def get_spot_rate_to_reporting(source_currency: str, fx_spot_rates: dict[str, float]) -> Decimal:
    source = validate_currency(source_currency)
    if source not in fx_spot_rates:
        raise ValueError(f"Missing FX spot rate for currency '{source}'")
    rate = Decimal(str(fx_spot_rates[source]))
    if rate <= 0:
        raise ValueError(f"FX spot rate for '{source}' must be > 0")
    return rate


def stressed_rate(spot_rate: Decimal, shock_bps: int) -> Decimal:
    multiplier = Decimal("1") + (Decimal(shock_bps) / Decimal("10000"))
    stressed = spot_rate * multiplier
    if stressed <= 0:
        raise ValueError("Stressed FX rate must be > 0")
    return stressed


def convert_minor_units(amount_minor: int, rate_to_reporting: Decimal) -> int:
    return round_half_up_int(Decimal(amount_minor) * rate_to_reporting)
