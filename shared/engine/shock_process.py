from __future__ import annotations

import numpy as np


def round_half_up_int_array(values: np.ndarray) -> np.ndarray:
    return np.floor(values + 0.5).astype(np.int64)


def generate_shock_paths(
    rng: np.random.Generator,
    mean_bps: int,
    std_bps: int,
    n_sims: int,
    horizon_months: int,
    dynamics: str,
    ar1_phi: float,
    clip_low: int,
    clip_high: int,
) -> np.ndarray:
    """Generate monthly bps shock paths under IID or AR(1) dynamics."""
    if std_bps == 0:
        values = np.full((n_sims, horizon_months), mean_bps, dtype=np.int64)
        return np.clip(values, clip_low, clip_high)

    eps = rng.normal(0.0, std_bps, size=(n_sims, horizon_months))
    paths = np.zeros((n_sims, horizon_months), dtype=np.float64)

    if dynamics == "ar1":
        paths[:, 0] = mean_bps + eps[:, 0]
        for month in range(1, horizon_months):
            paths[:, month] = mean_bps + ar1_phi * (paths[:, month - 1] - mean_bps) + eps[:, month]
    else:
        paths = mean_bps + eps

    rounded = round_half_up_int_array(paths)
    return np.clip(rounded, clip_low, clip_high)
