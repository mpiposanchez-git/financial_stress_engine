from __future__ import annotations

from shared.engine.money import (
    apply_bps,
    divide_round_half_up,
    format_currency_from_pence,
    gbp_to_pence,
    percent_to_bps,
    years_to_months,
)


def test_gbp_to_pence_round_half_up() -> None:
    assert gbp_to_pence(1.234) == 123
    assert gbp_to_pence(1.235) == 124
    assert gbp_to_pence("1000.005") == 100_001


def test_percent_to_bps_round_half_up() -> None:
    assert percent_to_bps(4.125) == 413
    assert percent_to_bps(6.0) == 600
    assert percent_to_bps("0.005") == 1


def test_years_to_months_round_half_up() -> None:
    assert years_to_months(25) == 300
    assert years_to_months(1.49) == 18
    assert years_to_months(1.5) == 18


def test_divide_round_half_up_and_apply_bps() -> None:
    assert divide_round_half_up(10_001, 100) == 100
    assert divide_round_half_up(10_050, 100) == 101
    assert apply_bps(100_005, 2_500) == 25_001


def test_currency_formatting_from_pence() -> None:
    assert format_currency_from_pence(0) == "£0.00"
    assert format_currency_from_pence(123_456) == "£1,234.56"
    assert format_currency_from_pence(-501) == "-£5.01"
