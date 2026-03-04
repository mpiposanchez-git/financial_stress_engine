from __future__ import annotations

from decimal import Decimal

from shared.engine.fx import convert_minor_units, currency_symbol, stressed_rate


def test_convert_minor_units_round_half_up() -> None:
    assert convert_minor_units(10_000, Decimal("0.865")) == 8_650
    assert convert_minor_units(101, Decimal("0.5")) == 51


def test_stressed_rate_applies_bps() -> None:
    assert stressed_rate(Decimal("0.8000"), 500) == Decimal("0.84000")
    assert stressed_rate(Decimal("1.0000"), -1000) == Decimal("0.90000")


def test_currency_symbol_lookup() -> None:
    assert currency_symbol("GBP") == "£"
    assert currency_symbol("EUR") == "€"
    assert currency_symbol("USD") == "$"
