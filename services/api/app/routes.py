from __future__ import annotations

import asyncio
import secrets
import time

import numpy as np
from fastapi import APIRouter, Depends, HTTPException, status

from shared.engine.deterministic import run_deterministic

from .auth import AuthContext, require_auth
from .models import (
    DeterministicRunRequest,
    DeterministicRunResponse,
    MonteCarloMetrics,
    MonteCarloRunRequest,
    MonteCarloRunResponse,
    PercentileTriplet,
)
from .rate_limit import rate_limiter
from .settings import Settings, get_settings

router = APIRouter()


def _monthly_mortgage_payment(
    balance: float,
    annual_rate_percent: float,
    term_years: float,
    mortgage_type: str,
) -> float:
    if balance <= 0:
        return 0.0

    monthly_rate = annual_rate_percent / 100.0 / 12.0
    n = term_years * 12

    if mortgage_type == "interest_only":
        return balance * monthly_rate

    if monthly_rate == 0.0:
        return balance / n if n > 0 else 0.0

    return balance * (monthly_rate * (1 + monthly_rate) ** n) / ((1 + monthly_rate) ** n - 1)


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


def _assert_limits(payload: MonteCarloRunRequest, settings: Settings) -> None:
    if payload.n_sims > settings.max_monte_carlo_sims:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"n_sims exceeds MAX_MONTE_CARLO_SIMS ({settings.max_monte_carlo_sims})",
        )

    if payload.horizon_months > settings.max_horizon_months:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                f"horizon_months exceeds MAX_HORIZON_MONTHS "
                f"({settings.max_horizon_months})"
            ),
        )


def _apply_rate_limit(auth: AuthContext, settings: Settings) -> None:
    allowed = rate_limiter.allow(auth.subject, settings.rate_limit_rpm)
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded",
        )


def _percentiles(values: np.ndarray) -> PercentileTriplet:
    p10, p50, p90 = np.percentile(values, [10, 50, 90], method="linear")
    return PercentileTriplet(
        p10=float(round(p10, 2)),
        p50=float(round(p50, 2)),
        p90=float(round(p90, 2)),
    )


@router.post("/api/v1/deterministic/run", response_model=DeterministicRunResponse)
async def run_deterministic_route(
    payload: DeterministicRunRequest,
    auth: AuthContext = Depends(require_auth),
    settings: Settings = Depends(get_settings),
) -> DeterministicRunResponse:
    _apply_rate_limit(auth, settings)

    try:
        result = await asyncio.wait_for(
            asyncio.to_thread(run_deterministic, payload.input_parameters),
            timeout=settings.request_timeout_seconds,
        )
    except TimeoutError as exc:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Request timed out",
        ) from exc

    min_savings = (
        payload.input_parameters.cash_savings_gbp
        if result.monthly_cashflow_stress_gbp >= 0
        else max(
            0.0,
            payload.input_parameters.cash_savings_gbp + result.monthly_cashflow_stress_gbp,
        )
    )

    warnings = ["Educational simulation only. Not financial advice."]
    return DeterministicRunResponse(
        runway_months=result.estimated_months_of_runway_stress,
        min_savings=float(round(min_savings, 2)),
        month_by_month=[],
        warnings=warnings,
    )


@router.post("/api/v1/montecarlo/run", response_model=MonteCarloRunResponse)
async def run_montecarlo_route(
    payload: MonteCarloRunRequest,
    auth: AuthContext = Depends(require_auth),
    settings: Settings = Depends(get_settings),
) -> MonteCarloRunResponse:
    _apply_rate_limit(auth, settings)
    _assert_limits(payload, settings)

    async def _run() -> MonteCarloRunResponse:
        start = time.perf_counter()

        p = payload.input_parameters
        n_sims = payload.n_sims
        horizon_months = payload.horizon_months
        seed = payload.seed if payload.seed is not None else secrets.randbelow(2_147_483_647)

        rng = np.random.default_rng(seed)

        income_shock_samples = np.clip(
            rng.normal(
                p.shock_monthly_income_drop_percent,
                p.income_shock_std_percent,
                size=n_sims,
            ),
            0,
            100,
        )
        stress_rate_samples = np.clip(
            rng.normal(p.mortgage_rate_percent_stress, p.rate_shock_std_percent, size=n_sims),
            0,
            100,
        )
        inflation_samples = np.clip(
            rng.normal(
                p.inflation_monthly_essentials_increase_percent,
                p.inflation_shock_std_percent,
                size=n_sims,
            ),
            0,
            100,
        )

        mortgage_payments = np.array(
            [
                _monthly_mortgage_payment(
                    p.mortgage_balance_gbp,
                    float(rate),
                    p.mortgage_term_years_remaining,
                    p.mortgage_type,
                )
                for rate in stress_rate_samples
            ],
            dtype=float,
        )

        stressed_incomes = p.household_monthly_net_income_gbp * (
            1 - income_shock_samples / 100.0
        )
        stressed_essentials = p.household_monthly_essential_spend_gbp * (
            1 + inflation_samples / 100.0
        )

        cashflows = (
            stressed_incomes
            - stressed_essentials
            - p.household_monthly_debt_payments_gbp
            - mortgage_payments
        )

        runway_months = np.where(
            cashflows < 0,
            np.minimum(horizon_months, p.cash_savings_gbp / np.abs(cashflows)),
            float(horizon_months),
        )

        terminal_savings = p.cash_savings_gbp + cashflows * horizon_months
        min_savings = np.clip(
            np.minimum(p.cash_savings_gbp, terminal_savings),
            a_min=0.0,
            a_max=None,
        )
        max_monthly_deficit = np.maximum(0.0, -cashflows)

        metrics = MonteCarloMetrics(
            runway_months=_percentiles(runway_months),
            min_savings=_percentiles(min_savings),
            max_monthly_deficit=_percentiles(max_monthly_deficit),
        )

        runtime_ms = round((time.perf_counter() - start) * 1000.0, 2)

        return MonteCarloRunResponse(
            n_sims=n_sims,
            horizon_months=horizon_months,
            seed=int(seed),
            runtime_ms=runtime_ms,
            metrics=metrics,
        )

    try:
        return await asyncio.wait_for(_run(), timeout=settings.request_timeout_seconds)
    except TimeoutError as exc:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Request timed out",
        ) from exc
