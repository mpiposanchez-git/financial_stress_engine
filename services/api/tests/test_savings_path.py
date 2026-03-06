from __future__ import annotations

import pytest

from shared.engine.savings_path import compute_savings_path, min_savings, month_of_depletion


def test_compute_savings_path_hand_computed() -> None:
    # month0=10,000 -> +2,000 -> -4,000 -> -4,000 floor at zero
    path = compute_savings_path(10_000, [2_000, -4_000, -4_000])
    assert path == [10_000, 12_000, 8_000, 4_000]


def test_compute_savings_path_floors_at_zero() -> None:
    path = compute_savings_path(5_000, [-3_000, -3_000, 1_000])
    assert path == [5_000, 2_000, 0, 1_000]


def test_month_of_depletion_returns_first_zero_index() -> None:
    assert month_of_depletion([5_000, 2_000, 0, 0]) == 2
    assert month_of_depletion([5_000, 2_000, 1_000]) is None


def test_min_savings_from_path() -> None:
    assert min_savings([5_000, 2_000, 0, 1_000]) == 0


def test_min_savings_rejects_empty_path() -> None:
    with pytest.raises(ValueError, match="path must not be empty"):
        min_savings([])
