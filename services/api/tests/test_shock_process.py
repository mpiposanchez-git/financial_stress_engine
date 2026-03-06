from __future__ import annotations

import numpy as np

from shared.engine.shock_process import generate_shock_paths


def test_generate_shock_paths_reproducible_iid() -> None:
    seed = 24680
    rng_a = np.random.default_rng(seed)
    rng_b = np.random.default_rng(seed)

    a = generate_shock_paths(
        rng_a,
        mean_bps=500,
        std_bps=120,
        n_sims=8,
        horizon_months=10,
        dynamics="iid",
        ar1_phi=0.0,
        clip_low=0,
        clip_high=10_000,
    )
    b = generate_shock_paths(
        rng_b,
        mean_bps=500,
        std_bps=120,
        n_sims=8,
        horizon_months=10,
        dynamics="iid",
        ar1_phi=0.0,
        clip_low=0,
        clip_high=10_000,
    )

    assert np.array_equal(a, b)


def test_generate_shock_paths_reproducible_ar1() -> None:
    seed = 13579
    rng_a = np.random.default_rng(seed)
    rng_b = np.random.default_rng(seed)

    a = generate_shock_paths(
        rng_a,
        mean_bps=600,
        std_bps=80,
        n_sims=6,
        horizon_months=12,
        dynamics="ar1",
        ar1_phi=0.6,
        clip_low=0,
        clip_high=10_000,
    )
    b = generate_shock_paths(
        rng_b,
        mean_bps=600,
        std_bps=80,
        n_sims=6,
        horizon_months=12,
        dynamics="ar1",
        ar1_phi=0.6,
        clip_low=0,
        clip_high=10_000,
    )

    assert np.array_equal(a, b)


def test_generate_shock_paths_zero_std_collapses_to_mean() -> None:
    rng = np.random.default_rng(11)
    values = generate_shock_paths(
        rng,
        mean_bps=750,
        std_bps=0,
        n_sims=5,
        horizon_months=7,
        dynamics="iid",
        ar1_phi=0.0,
        clip_low=0,
        clip_high=10_000,
    )

    assert values.shape == (5, 7)
    assert np.all(values == 750)


def test_generate_shock_paths_respects_clipping_bounds() -> None:
    rng = np.random.default_rng(99)
    values = generate_shock_paths(
        rng,
        mean_bps=5_000,
        std_bps=20_000,
        n_sims=40,
        horizon_months=4,
        dynamics="iid",
        ar1_phi=0.0,
        clip_low=0,
        clip_high=10_000,
    )

    assert int(values.min()) >= 0
    assert int(values.max()) <= 10_000
