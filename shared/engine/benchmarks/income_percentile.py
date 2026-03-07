from __future__ import annotations


def compute_percentile_bucket(annual_income_gbp: float, decile_thresholds_gbp: list[float]) -> int:
    if len(decile_thresholds_gbp) != 9:
        raise ValueError("decile_thresholds_gbp must contain exactly 9 values")

    for threshold in decile_thresholds_gbp:
        if threshold < 0:
            raise ValueError("decile thresholds must be non-negative")

    if annual_income_gbp < 0:
        raise ValueError("annual_income_gbp must be non-negative")

    for idx, threshold in enumerate(decile_thresholds_gbp):
        if annual_income_gbp <= threshold:
            return (idx + 1) * 10

    return 90
