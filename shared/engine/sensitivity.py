from __future__ import annotations

from collections.abc import Callable

from pydantic import BaseModel

from shared.engine.deterministic import run_deterministic
from shared.engine.inputs import DeterministicInput


class SensitivityImpact(BaseModel):
    driver: str
    delta_bps: int
    base_runway_months: float | None
    perturbed_runway_months: float | None
    runway_months_impact: float | None
    base_min_savings_pence: int
    perturbed_min_savings_pence: int
    min_savings_impact_pence: int


def _clamp(value: int, minimum: int, maximum: int) -> int:
    return max(minimum, min(maximum, value))


def _impact_value(item: SensitivityImpact) -> int:
    # Rank by absolute savings impact to keep ordering deterministic even when runway is None.
    return abs(item.min_savings_impact_pence)


def _run_impact(
    base_input: DeterministicInput,
    base_result,
    driver: str,
    delta_bps: int,
    updater: Callable[[DeterministicInput], DeterministicInput],
) -> SensitivityImpact:
    perturbed_input = updater(base_input)
    perturbed_result = run_deterministic(perturbed_input)

    runway_impact: float | None
    if base_result.runway_months is None or perturbed_result.runway_months is None:
        runway_impact = None
    else:
        runway_impact = round(perturbed_result.runway_months - base_result.runway_months, 4)

    return SensitivityImpact(
        driver=driver,
        delta_bps=delta_bps,
        base_runway_months=base_result.runway_months,
        perturbed_runway_months=perturbed_result.runway_months,
        runway_months_impact=runway_impact,
        base_min_savings_pence=base_result.min_savings_pence,
        perturbed_min_savings_pence=perturbed_result.min_savings_pence,
        min_savings_impact_pence=perturbed_result.min_savings_pence
        - base_result.min_savings_pence,
    )


def compute_sensitivity(
    inputs: DeterministicInput,
    delta_bps: int = 100,
) -> list[SensitivityImpact]:
    """Compute deterministic one-factor sensitivity impacts.

    Each driver is perturbed upward by ``delta_bps`` while holding other values constant.
    Returned impacts are ranked by absolute min-savings impact (descending).
    """
    if delta_bps < 0:
        raise ValueError("delta_bps must be >= 0")

    base_input = inputs.model_copy(deep=True)
    base_result = run_deterministic(base_input)

    def with_income_shock(value: DeterministicInput) -> DeterministicInput:
        return value.model_copy(
            update={
                "shock_monthly_income_drop_bps": _clamp(
                    value.shock_monthly_income_drop_bps + delta_bps,
                    0,
                    10_000,
                )
            },
            deep=True,
        )

    def with_inflation_shock(value: DeterministicInput) -> DeterministicInput:
        return value.model_copy(
            update={
                "inflation_monthly_essentials_increase_bps": _clamp(
                    value.inflation_monthly_essentials_increase_bps + delta_bps,
                    0,
                    10_000,
                )
            },
            deep=True,
        )

    def with_mortgage_rate_stress(value: DeterministicInput) -> DeterministicInput:
        return value.model_copy(
            update={
                "mortgage_rate_bps_stress": _clamp(
                    value.mortgage_rate_bps_stress + delta_bps,
                    0,
                    10_000,
                )
            },
            deep=True,
        )

    def with_fx_stress(value: DeterministicInput) -> DeterministicInput:
        next_fx_stress = dict(value.fx_stress_bps)
        for code in value.fx_spot_rates:
            if code == value.reporting_currency:
                continue
            current = int(next_fx_stress.get(code, 0))
            next_fx_stress[code] = _clamp(current + delta_bps, -9_999, 10_000)

        return value.model_copy(update={"fx_stress_bps": next_fx_stress}, deep=True)

    perturbations: list[tuple[str, Callable[[DeterministicInput], DeterministicInput]]] = [
        ("income_shock_bps", with_income_shock),
        ("inflation_shock_bps", with_inflation_shock),
        ("mortgage_rate_stress_bps", with_mortgage_rate_stress),
        ("fx_stress_bps", with_fx_stress),
    ]

    impacts = [
        _run_impact(base_input, base_result, name, delta_bps, updater)
        for name, updater in perturbations
    ]

    return sorted(impacts, key=lambda item: (-_impact_value(item), item.driver))
