from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol

from shared.engine.money import apply_bps


class CategoryLike(Protocol):
    monthly_spend_pence: int
    inflation_bps: int


def categories_total_pence(categories: Mapping[str, CategoryLike]) -> int:
    return sum(category.monthly_spend_pence for category in categories.values())


def stressed_categories_total_pence(categories: Mapping[str, CategoryLike]) -> int:
    return sum(
        apply_bps(category.monthly_spend_pence, 10_000 + category.inflation_bps)
        for category in categories.values()
    )
