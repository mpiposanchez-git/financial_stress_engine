from __future__ import annotations

import asyncio
import secrets

from fastapi import APIRouter, Depends, HTTPException, status

from shared.engine.deterministic import run_deterministic
from shared.engine.money import format_currency_from_pence
from shared.engine.montecarlo import run_montecarlo

from .auth import AuthContext, require_auth
from .models import (
    DeterministicRunRequest,
    DeterministicRunResponse,
    MoneyPercentileTriplet,
    MonteCarloMetrics,
    MonteCarloRunRequest,
    MonteCarloRunResponse,
    RunwayPercentileTriplet,
)
from .rate_limit import rate_limiter
from .settings import Settings, get_settings

router = APIRouter()


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
            detail=(f"horizon_months exceeds MAX_HORIZON_MONTHS ({settings.max_horizon_months})"),
        )


def _apply_rate_limit(auth: AuthContext, settings: Settings) -> None:
    allowed = rate_limiter.allow(auth.subject, settings.rate_limit_rpm)
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded",
        )


@router.post("/api/v1/deterministic/run", response_model=DeterministicRunResponse)
async def run_deterministic_route(
    payload: DeterministicRunRequest,
    auth: AuthContext = Depends(require_auth),
    settings: Settings = Depends(get_settings),
) -> DeterministicRunResponse:
    _apply_rate_limit(auth, settings)
    engine_input = payload.input_parameters.to_engine_input(payload.horizon_months)

    try:
        result = await asyncio.wait_for(
            asyncio.to_thread(run_deterministic, engine_input),
            timeout=settings.request_timeout_seconds,
        )
    except TimeoutError as exc:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Request timed out",
        ) from exc

    warnings = ["Educational simulation only. Not financial advice."]
    return DeterministicRunResponse(
        reporting_currency=result.reporting_currency,
        fx_spot_rates_used=result.fx_spot_rates_used,
        fx_stressed_rates_used=result.fx_stressed_rates_used,
        fx_stress_bps=result.fx_stress_bps,
        monthly_cashflow_base_pence=result.monthly_cashflow_base_pence,
        monthly_cashflow_base_formatted=result.monthly_cashflow_base_formatted,
        monthly_cashflow_stress_pence=result.monthly_cashflow_stress_pence,
        monthly_cashflow_stress_formatted=result.monthly_cashflow_stress_formatted,
        mortgage_payment_current_pence=result.mortgage_payment_current_pence,
        mortgage_payment_current_formatted=result.mortgage_payment_current_formatted,
        mortgage_payment_stress_pence=result.mortgage_payment_stress_pence,
        mortgage_payment_stress_formatted=result.mortgage_payment_stress_formatted,
        runway_months=result.runway_months,
        savings_path_pence=result.savings_path_pence,
        savings_path_formatted=result.savings_path_formatted,
        min_savings_pence=result.min_savings_pence,
        min_savings_formatted=result.min_savings_formatted,
        month_of_depletion=result.month_of_depletion,
        month_by_month=result.savings_path_pence,
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
        engine_input = payload.input_parameters.to_engine_input()
        seed = payload.seed if payload.seed is not None else secrets.randbelow(2_147_483_647)
        result = await asyncio.to_thread(
            run_montecarlo,
            engine_input,
            payload.n_sims,
            payload.horizon_months,
            int(seed),
        )

        metrics = MonteCarloMetrics(
            runway_months=RunwayPercentileTriplet(
                p10=result.runway_months.p10,
                p50=result.runway_months.p50,
                p90=result.runway_months.p90,
            ),
            min_savings=MoneyPercentileTriplet(
                p10_pence=result.min_savings.p10_pence,
                p10_formatted=format_currency_from_pence(result.min_savings.p10_pence),
                p50_pence=result.min_savings.p50_pence,
                p50_formatted=format_currency_from_pence(result.min_savings.p50_pence),
                p90_pence=result.min_savings.p90_pence,
                p90_formatted=format_currency_from_pence(result.min_savings.p90_pence),
            ),
            month_of_depletion=RunwayPercentileTriplet(
                p10=result.month_of_depletion.p10,
                p50=result.month_of_depletion.p50,
                p90=result.month_of_depletion.p90,
            ),
        )

        return MonteCarloRunResponse(
            n_sims=result.n_sims,
            horizon_months=result.horizon_months,
            seed=result.seed,
            runtime_ms=result.runtime_ms,
            metrics=metrics,
        )

    try:
        return await asyncio.wait_for(_run(), timeout=settings.request_timeout_seconds)
    except TimeoutError as exc:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Request timed out",
        ) from exc
