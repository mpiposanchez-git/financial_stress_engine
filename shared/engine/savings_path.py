from __future__ import annotations


def compute_savings_path(s0_pence: int, cashflows_pence: list[int]) -> list[int]:
    """Compute month-by-month savings path with a zero floor."""
    path = [s0_pence]
    current = s0_pence
    for cashflow in cashflows_pence:
        current = max(0, current + cashflow)
        path.append(current)
    return path


def month_of_depletion(path: list[int]) -> int | None:
    """Return first month index where savings reaches zero, if any."""
    for idx, value in enumerate(path):
        if value == 0:
            return idx
    return None


def min_savings(path: list[int]) -> int:
    """Return minimum savings observed in the path."""
    if not path:
        raise ValueError("path must not be empty")
    return min(path)
