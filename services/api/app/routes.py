from __future__ import annotations

import asyncio
import secrets
import time

from fastapi import APIRouter, Depends, Header, HTTPException, Response, status

from shared.engine.deterministic import run_deterministic
from shared.engine.money import format_currency_from_pence
from shared.engine.montecarlo import run_montecarlo
from shared.engine.reports.pdf_report import generate_pdf_report
from shared.engine.sensitivity import compute_sensitivity

from .auth import AuthContext, require_auth
from .benchmarks.percentile import compute_uk_income_percentile
from .benchmarks.reference_values import get_uk_reference_values
from .data_cache import DATA_CACHE
from .data_registry import DATA_REGISTRY
from .entitlements import is_premium, require_premium
from .models import (
    CompareRunRequest,
    CompareRunResponse,
    CompareScenarioResult,
    DataDefaultsResponse,
    DeterministicRunRequest,
    DeterministicRunResponse,
    MoneyPercentileTriplet,
    MonteCarloMetrics,
    MonteCarloRunRequest,
    MonteCarloRunResponse,
    PdfReportRequest,
    RunwayPercentileTriplet,
    SensitivityDriverImpact,
    SensitivityRunRequest,
    SensitivityRunResponse,
    UkPercentileRequest,
    UkPercentileResponse,
    UkReferenceValuesResponse,
)
from .rate_limit import rate_limiter
from .settings import Settings, get_settings
from .telemetry import get_telemetry_snapshot, record_deterministic_run, record_montecarlo_run

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/api/v1/data/registry")
def data_registry() -> dict[str, list[dict[str, object]]]:
    return {"datasets": [entry.model_dump() for entry in DATA_REGISTRY]}


@router.get("/api/v1/data/defaults", response_model=DataDefaultsResponse)
def data_defaults() -> DataDefaultsResponse:
    bank_rate_entry = DATA_CACHE.get("boe_bank_rate")
    cpih_entry = DATA_CACHE.get("ons_cpih_12m")
    fx_entry = DATA_CACHE.get("boe_fx_spot")
    ofgem_entry = DATA_CACHE.get("ofgem_price_cap")

    bank_rate_bps = 450
    if bank_rate_entry and isinstance(bank_rate_entry.value, dict):
        rate_percent = bank_rate_entry.value.get("rate_percent")
        if isinstance(rate_percent, (int, float)):
            bank_rate_bps = int(round(float(rate_percent) * 100))

    cpih_12m_bps = 500
    if cpih_entry and isinstance(cpih_entry.value, dict):
        annual_rate_percent = cpih_entry.value.get("annual_rate_percent")
        if isinstance(annual_rate_percent, (int, float)):
            cpih_12m_bps = int(round(float(annual_rate_percent) * 100))

    eur = 0.86
    usd = 0.78
    if fx_entry and isinstance(fx_entry.value, dict):
        eur_value = fx_entry.value.get("eur")
        usd_value = fx_entry.value.get("usd")
        if isinstance(eur_value, (int, float)):
            eur = float(eur_value)
        if isinstance(usd_value, (int, float)):
            usd = float(usd_value)

    energy_reference_values: dict[str, float] | None = None
    if ofgem_entry and isinstance(ofgem_entry.value, dict):
        annual_bill_gbp = ofgem_entry.value.get("annual_bill_gbp")
        if isinstance(annual_bill_gbp, (int, float)):
            energy_reference_values = {"annual_bill_gbp": float(annual_bill_gbp)}

    return DataDefaultsResponse(
        bank_rate_bps=bank_rate_bps,
        cpih_12m_bps=cpih_12m_bps,
        fx_spot_rates={"EUR": eur, "USD": usd},
        energy_reference_values=energy_reference_values,
        fetched_at={
            "boe_bank_rate": bank_rate_entry.meta.fetched_at_utc if bank_rate_entry else None,
            "ons_cpih_12m": cpih_entry.meta.fetched_at_utc if cpih_entry else None,
            "boe_fx_spot": fx_entry.meta.fetched_at_utc if fx_entry else None,
            "ofgem_price_cap": ofgem_entry.meta.fetched_at_utc if ofgem_entry else None,
        },
    )


@router.get("/api/v1/benchmarks/uk/reference", response_model=UkReferenceValuesResponse)
def uk_reference_values() -> UkReferenceValuesResponse:
    return UkReferenceValuesResponse.model_validate(get_uk_reference_values())


@router.post("/api/v1/benchmarks/uk/percentile", response_model=UkPercentileResponse)
def uk_income_percentile(
    payload: UkPercentileRequest,
    auth: AuthContext = Depends(require_premium),
) -> UkPercentileResponse:
    _ = auth
    result = compute_uk_income_percentile(
        annual_net_income_reporting_currency=payload.annual_net_income_reporting_currency,
        reporting_currency=payload.reporting_currency,
    )
    return UkPercentileResponse.model_validate(result)


@router.post("/api/v1/reports/pdf")
def create_pdf_report(
    payload: PdfReportRequest,
    auth: AuthContext = Depends(require_premium),
) -> Response:
    _ = auth
    pdf_bytes = generate_pdf_report(
        inputs=payload.inputs,
        outputs=payload.outputs,
        disclaimers=payload.disclaimers,
        provenance=payload.provenance,
        app_version=payload.app_version,
    )
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="stress-report.pdf"'},
    )


@router.get("/api/v1/me")
def me(auth: AuthContext = Depends(require_auth)) -> dict[str, str | bool]:
    return {"subject": auth.subject, "is_premium": is_premium(auth)}


@router.get("/api/v1/admin/telemetry")
def admin_telemetry(
    x_admin_metrics_token: str | None = Header(default=None, alias="X-Admin-Metrics-Token"),
    settings: Settings = Depends(get_settings),
) -> dict[str, dict[str, int] | int]:
    if not settings.admin_metrics_token or x_admin_metrics_token != settings.admin_metrics_token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return get_telemetry_snapshot()


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
    started = time.perf_counter()
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
    response = DeterministicRunResponse(
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
        debt_balance_path_pence=result.debt_balance_path_pence,
        min_savings_pence=result.min_savings_pence,
        min_savings_formatted=result.min_savings_formatted,
        month_of_depletion=result.month_of_depletion,
        warnings=warnings,
    )
    record_deterministic_run((time.perf_counter() - started) * 1000.0)
    return response


@router.post("/api/v1/compare/run", response_model=CompareRunResponse)
async def run_compare_route(
    payload: CompareRunRequest,
    auth: AuthContext = Depends(require_premium),
    settings: Settings = Depends(get_settings),
) -> CompareRunResponse:
    _apply_rate_limit(auth, settings)

    async def _run() -> CompareRunResponse:
        results: list[CompareScenarioResult] = []
        for scenario in payload.scenarios:
            engine_input = scenario.input_parameters.to_engine_input(scenario.horizon_months)
            deterministic = await asyncio.to_thread(run_deterministic, engine_input)
            results.append(
                CompareScenarioResult(
                    name=scenario.name,
                    reporting_currency=deterministic.reporting_currency,
                    runway_months=deterministic.runway_months,
                    month_of_depletion=deterministic.month_of_depletion,
                    min_savings_pence=deterministic.min_savings_pence,
                    min_savings_formatted=deterministic.min_savings_formatted,
                    monthly_cashflow_stress_pence=deterministic.monthly_cashflow_stress_pence,
                    monthly_cashflow_stress_formatted=deterministic.monthly_cashflow_stress_formatted,
                    mortgage_payment_stress_pence=deterministic.mortgage_payment_stress_pence,
                    mortgage_payment_stress_formatted=deterministic.mortgage_payment_stress_formatted,
                    warnings=["Educational simulation only. Not financial advice."],
                )
            )

        return CompareRunResponse(scenarios=results)

    try:
        return await asyncio.wait_for(_run(), timeout=settings.request_timeout_seconds)
    except TimeoutError as exc:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Request timed out",
        ) from exc


@router.post("/api/v1/sensitivity/run", response_model=SensitivityRunResponse)
async def run_sensitivity_route(
    payload: SensitivityRunRequest,
    auth: AuthContext = Depends(require_premium),
    settings: Settings = Depends(get_settings),
) -> SensitivityRunResponse:
    _apply_rate_limit(auth, settings)

    async def _run() -> SensitivityRunResponse:
        engine_input = payload.input_parameters.to_engine_input(payload.horizon_months)
        impacts = await asyncio.to_thread(
            compute_sensitivity,
            engine_input,
            payload.delta_bps,
        )
        return SensitivityRunResponse(
            impacts=[SensitivityDriverImpact(**item.model_dump()) for item in impacts]
        )

    try:
        return await asyncio.wait_for(_run(), timeout=settings.request_timeout_seconds)
    except TimeoutError as exc:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Request timed out",
        ) from exc


@router.post("/api/v1/montecarlo/run", response_model=MonteCarloRunResponse)
async def run_montecarlo_route(
    payload: MonteCarloRunRequest,
    auth: AuthContext = Depends(require_premium),
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

        response = MonteCarloRunResponse(
            n_sims=result.n_sims,
            horizon_months=result.horizon_months,
            seed=result.seed,
            runtime_ms=result.runtime_ms,
            runway_months_p10=result.runway_months.p10,
            runway_months_p50=result.runway_months.p50,
            runway_months_p90=result.runway_months.p90,
            min_savings_p10_pence=result.min_savings.p10_pence,
            min_savings_p50_pence=result.min_savings.p50_pence,
            min_savings_p90_pence=result.min_savings.p90_pence,
            month_of_depletion_p10=result.month_of_depletion.p10,
            month_of_depletion_p50=result.month_of_depletion.p50,
            month_of_depletion_p90=result.month_of_depletion.p90,
            metrics=metrics,
        )
        record_montecarlo_run(result.runtime_ms)
        return response

    try:
        return await asyncio.wait_for(_run(), timeout=settings.request_timeout_seconds)
    except TimeoutError as exc:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Request timed out",
        ) from exc
