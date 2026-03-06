from __future__ import annotations

import pytest

from shared.engine.mortgage import mortgage_payment_interest_only, mortgage_payment_repayment


def test_interest_only_known_value() -> None:
    # 250,000.00 at 4.5% annual => 937.50 monthly
    assert mortgage_payment_interest_only(25_000_000, 450) == 93_750


def test_interest_only_zero_balance_is_zero() -> None:
    assert mortgage_payment_interest_only(0, 450) == 0


def test_repayment_known_value() -> None:
    # Verified against amortization formula with round-half-up.
    assert mortgage_payment_repayment(25_000_000, 450, 300) == 138_958


def test_repayment_zero_rate_divides_evenly() -> None:
    assert mortgage_payment_repayment(12_000, 0, 12) == 1_000


def test_repayment_zero_balance_is_zero() -> None:
    assert mortgage_payment_repayment(0, 600, 360) == 0


def test_repayment_invalid_term_raises() -> None:
    with pytest.raises(ValueError, match="term_months must be > 0"):
        mortgage_payment_repayment(10_000, 400, 0)


def test_negative_rate_raises() -> None:
    with pytest.raises(ValueError, match="annual_rate_bps must be >= 0"):
        mortgage_payment_interest_only(10_000, -1)
