from __future__ import annotations

import math
import time
from dataclasses import dataclass

import numpy as np

from .fx import get_spot_rate_to_reporting, stressed_rate, validate_currency
from .inputs import MonteCarloInput
from .mortgage import mortgage_payment_interest_only, mortgage_payment_repayment
from .schedules import resolve_schedule_levels
from .shock_process import generate_shock_paths, round_half_up_int_array


@dataclass(frozen=True)
class PercentileTriplet:
    p10: float
    p50: float
    p90: float


@dataclass(frozen=True)
class MoneyPercentileTriplet:
    p10_pence: int
    p50_pence: int
    p90_pence: int


@dataclass(frozen=True)
class MonteCarloResult:
    n_sims: int
    horizon_months: int
    seed: int
    runtime_ms: float
    runway_months: PercentileTriplet
    min_savings: MoneyPercentileTriplet
    month_of_depletion: PercentileTriplet


def _round_half_up_float(value: float, places: int = 2) -> float:
    factor = 10**places
    return math.floor(value * factor + 0.5) / factor


def _percentiles_float(values: np.ndarray) -> PercentileTriplet:
    p10, p50, p90 = np.percentile(values, [10, 50, 90], method="linear")
    return PercentileTriplet(
        p10=_round_half_up_float(float(p10), 2),
        p50=_round_half_up_float(float(p50), 2),
        p90=_round_half_up_float(float(p90), 2),
    )


def _percentiles_int(values: np.ndarray) -> MoneyPercentileTriplet:
    p10, p50, p90 = np.percentile(values, [10, 50, 90], method="linear")
    return MoneyPercentileTriplet(
        p10_pence=int(math.floor(float(p10) + 0.5)),
        p50_pence=int(math.floor(float(p50) + 0.5)),
        p90_pence=int(math.floor(float(p90) + 0.5)),
    )


def _monthly_mortgage_payment_from_bps(
    balance_pence: int,
    annual_rate_bps: np.ndarray,
    term_months: int,
    mortgage_type: str,
) -> np.ndarray:
    if balance_pence <= 0:
        return np.zeros_like(annual_rate_bps, dtype=np.int64)

    if mortgage_type == "interest_only":
        return np.fromiter(
            (mortgage_payment_interest_only(balance_pence, int(rate)) for rate in annual_rate_bps),
            dtype=np.int64,
            count=annual_rate_bps.size,
        )

    return np.fromiter(
        (
            mortgage_payment_repayment(balance_pence, int(rate), term_months)
            for rate in annual_rate_bps
        ),
        dtype=np.int64,
        count=annual_rate_bps.size,
    )


def _build_fx_paths(
    rng: np.random.Generator,
    inputs: MonteCarloInput,
    n_sims: int,
    horizon_months: int,
) -> dict[str, np.ndarray]:
    paths: dict[str, np.ndarray] = {}

    for code in inputs.fx_spot_rates:
        currency = validate_currency(code)
        if currency == inputs.reporting_currency:
            paths[currency] = np.ones((n_sims, horizon_months), dtype=np.float64)
            continue

        vol_bps = int(inputs.fx_monthly_vol_bps.get(currency, 0))
        stress_bps = int(inputs.fx_stress_bps.get(currency, 0))
        base_rate = float(get_spot_rate_to_reporting(currency, inputs.fx_spot_rates))

        stressed_start = float(
            stressed_rate(get_spot_rate_to_reporting(currency, inputs.fx_spot_rates), stress_bps)
        )
        if vol_bps == 0:
            paths[currency] = np.full((n_sims, horizon_months), stressed_start, dtype=np.float64)
            continue

        sigma = vol_bps / 10_000.0
        eps = rng.normal(0.0, sigma, size=(n_sims, horizon_months))
        if inputs.shock_dynamics == "ar1":
            returns = np.zeros((n_sims, horizon_months), dtype=np.float64)
            returns[:, 0] = eps[:, 0]
            for month in range(1, horizon_months):
                returns[:, month] = inputs.ar1_phi * returns[:, month - 1] + eps[:, month]
        else:
            returns = eps

        series = np.zeros((n_sims, horizon_months), dtype=np.float64)
        series[:, 0] = stressed_start * np.exp(returns[:, 0])
        for month in range(1, horizon_months):
            series[:, month] = series[:, month - 1] * np.exp(returns[:, month])
        paths[currency] = series

        if base_rate <= 0:
            raise ValueError(f"Invalid FX rate for {currency}")

    return paths


def _convert_array_to_reporting(amount_pence: np.ndarray, fx_rate_path: np.ndarray) -> np.ndarray:
    return round_half_up_int_array(amount_pence.astype(np.float64) * fx_rate_path)


def run_montecarlo(
    inputs: MonteCarloInput,
    n_sims: int,
    horizon_months: int,
    seed: int,
) -> MonteCarloResult:
    start = time.perf_counter()
    rng = np.random.default_rng(seed)

    income_mu = np.array(
        resolve_schedule_levels(
            inputs.shock_monthly_income_drop_bps,
            horizon_months,
            inputs.income_shock_schedule,
        ),
        dtype=np.int64,
    )
    inflation_mu = np.array(
        resolve_schedule_levels(
            inputs.inflation_monthly_essentials_increase_bps,
            horizon_months,
            inputs.inflation_shock_schedule,
        ),
        dtype=np.int64,
    )
    rate_mu = np.array(
        resolve_schedule_levels(
            inputs.mortgage_rate_bps_stress,
            horizon_months,
            inputs.mortgage_rate_stress_schedule,
        ),
        dtype=np.int64,
    )

    income_drop = generate_shock_paths(
        rng,
        income_mu,
        inputs.income_shock_std_bps,
        n_sims,
        horizon_months,
        inputs.shock_dynamics,
        inputs.ar1_phi,
        0,
        10_000,
    )
    inflation = generate_shock_paths(
        rng,
        inflation_mu,
        inputs.inflation_shock_std_bps,
        n_sims,
        horizon_months,
        inputs.shock_dynamics,
        inputs.ar1_phi,
        0,
        10_000,
    )
    rate_bps = generate_shock_paths(
        rng,
        rate_mu,
        inputs.rate_shock_std_bps,
        n_sims,
        horizon_months,
        inputs.shock_dynamics,
        inputs.ar1_phi,
        0,
        10_000,
    )

    fx_paths = _build_fx_paths(rng, inputs, n_sims, horizon_months)

    savings = np.full(n_sims, inputs.cash_savings_pence, dtype=np.int64)
    savings = _convert_array_to_reporting(
        savings,
        fx_paths[inputs.cash_savings_currency][:, 0],
    )
    min_savings = savings.copy()
    month_of_depletion = np.zeros(n_sims, dtype=np.int64)

    for month in range(horizon_months):
        income_source = (
            inputs.household_monthly_net_income_pence * (10_000 - income_drop[:, month]) + 5_000
        ) // 10_000
        essentials_source = (
            inputs.household_monthly_essential_spend_pence * (10_000 + inflation[:, month]) + 5_000
        ) // 10_000

        debt_source = np.full(n_sims, inputs.household_monthly_debt_payments_pence, dtype=np.int64)
        mortgage_source = _monthly_mortgage_payment_from_bps(
            inputs.mortgage_balance_pence,
            rate_bps[:, month],
            inputs.mortgage_term_months_remaining,
            inputs.mortgage_type,
        )

        income_reporting = _convert_array_to_reporting(
            income_source,
            fx_paths[inputs.household_monthly_net_income_currency][:, month],
        )
        essentials_reporting = _convert_array_to_reporting(
            essentials_source,
            fx_paths[inputs.household_monthly_essential_spend_currency][:, month],
        )
        debt_reporting = _convert_array_to_reporting(
            debt_source,
            fx_paths[inputs.household_monthly_debt_payments_currency][:, month],
        )
        mortgage_reporting = _convert_array_to_reporting(
            mortgage_source,
            fx_paths[inputs.mortgage_balance_currency][:, month],
        )

        cashflow = income_reporting - essentials_reporting - debt_reporting - mortgage_reporting
        savings = np.maximum(0, savings + cashflow)
        min_savings = np.minimum(min_savings, savings)

        newly_depleted = (month_of_depletion == 0) & (savings == 0)
        month_of_depletion[newly_depleted] = month + 1

    depletion_for_percentiles = np.where(
        month_of_depletion > 0, month_of_depletion, horizon_months + 1
    )
    runway = depletion_for_percentiles.astype(np.float64)

    runtime_ms = _round_half_up_float((time.perf_counter() - start) * 1000.0, 2)

    return MonteCarloResult(
        n_sims=n_sims,
        horizon_months=horizon_months,
        seed=seed,
        runtime_ms=runtime_ms,
        runway_months=_percentiles_float(runway),
        min_savings=_percentiles_int(min_savings),
        month_of_depletion=_percentiles_float(depletion_for_percentiles.astype(np.float64)),
    )
