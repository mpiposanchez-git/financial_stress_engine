from __future__ import annotations

from pydantic import BaseModel, Field

from shared.engine.inputs import DeterministicInput


class MonteCarloInputParameters(DeterministicInput):
    income_shock_std_percent: float = Field(default=5.0, ge=0, le=50)
    rate_shock_std_percent: float = Field(default=0.5, ge=0, le=10)
    inflation_shock_std_percent: float = Field(default=1.0, ge=0, le=20)


class DeterministicRunRequest(BaseModel):
    input_parameters: DeterministicInput


class DeterministicRunResponse(BaseModel):
    runway_months: float | None
    min_savings: float
    month_by_month: list[float]
    warnings: list[str]


class PercentileTriplet(BaseModel):
    p10: float
    p50: float
    p90: float


class MonteCarloMetrics(BaseModel):
    runway_months: PercentileTriplet
    min_savings: PercentileTriplet
    max_monthly_deficit: PercentileTriplet


class MonteCarloRunRequest(BaseModel):
    input_parameters: MonteCarloInputParameters
    n_sims: int = Field(default=2000, ge=1)
    horizon_months: int = Field(default=24, ge=1)
    seed: int | None = None


class MonteCarloRunResponse(BaseModel):
    n_sims: int
    horizon_months: int
    seed: int
    runtime_ms: float
    metrics: MonteCarloMetrics
