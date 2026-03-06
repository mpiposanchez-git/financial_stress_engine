from __future__ import annotations

from pydantic import BaseModel, Field

from shared.engine.inputs import (
    DebtItem,
    DeterministicInput,
    EssentialsCategory,
    MonteCarloInput,
)
from shared.engine.money import gbp_to_pence, percent_to_bps, years_to_months


class EssentialsCategoryInputParameters(BaseModel):
    monthly_spend_gbp: float = Field(..., ge=0)
    inflation_bps: int = Field(..., ge=0, le=10_000)


class DeterministicInputParameters(BaseModel):
    household_monthly_net_income_gbp: float = Field(..., ge=0)
    household_monthly_essential_spend_gbp: float = Field(..., ge=0)
    household_monthly_debt_payments_gbp: float = Field(..., ge=0)
    cash_savings_gbp: float = Field(..., ge=0)
    mortgage_balance_gbp: float = Field(..., ge=0)
    mortgage_term_years_remaining: float = Field(..., ge=0)
    mortgage_rate_percent_current: float = Field(..., ge=0, le=100)
    mortgage_rate_percent_stress: float = Field(..., ge=0, le=100)
    mortgage_type: str = Field(...)
    shock_monthly_income_drop_percent: float = Field(..., ge=0, le=100)
    inflation_monthly_essentials_increase_percent: float = Field(..., ge=0, le=100)
    household_monthly_net_income_currency: str = Field(default="GBP")
    household_monthly_essential_spend_currency: str = Field(default="GBP")
    household_monthly_debt_payments_currency: str = Field(default="GBP")
    cash_savings_currency: str = Field(default="GBP")
    mortgage_balance_currency: str = Field(default="GBP")
    reporting_currency: str = Field(default="GBP")
    fx_spot_rates: dict[str, float] = Field(
        default_factory=lambda: {"GBP": 1.0, "EUR": 0.86, "USD": 0.78}
    )
    fx_stress_bps: dict[str, int] = Field(default_factory=dict)
    essentials_categories: dict[str, EssentialsCategoryInputParameters] | None = None
    debts: list[DebtItem] | None = None

    def to_engine_input(self, horizon_months: int = 24) -> DeterministicInput:
        return DeterministicInput(
            household_monthly_net_income_pence=gbp_to_pence(self.household_monthly_net_income_gbp),
            household_monthly_essential_spend_pence=gbp_to_pence(
                self.household_monthly_essential_spend_gbp
            ),
            household_monthly_debt_payments_pence=gbp_to_pence(
                self.household_monthly_debt_payments_gbp
            ),
            cash_savings_pence=gbp_to_pence(self.cash_savings_gbp),
            mortgage_balance_pence=gbp_to_pence(self.mortgage_balance_gbp),
            mortgage_term_months_remaining=years_to_months(self.mortgage_term_years_remaining),
            mortgage_rate_bps_current=percent_to_bps(self.mortgage_rate_percent_current),
            mortgage_rate_bps_stress=percent_to_bps(self.mortgage_rate_percent_stress),
            mortgage_type=self.mortgage_type,
            shock_monthly_income_drop_bps=percent_to_bps(self.shock_monthly_income_drop_percent),
            inflation_monthly_essentials_increase_bps=percent_to_bps(
                self.inflation_monthly_essentials_increase_percent
            ),
            household_monthly_net_income_currency=self.household_monthly_net_income_currency,
            household_monthly_essential_spend_currency=self.household_monthly_essential_spend_currency,
            household_monthly_debt_payments_currency=self.household_monthly_debt_payments_currency,
            cash_savings_currency=self.cash_savings_currency,
            mortgage_balance_currency=self.mortgage_balance_currency,
            reporting_currency=self.reporting_currency,
            fx_spot_rates=self.fx_spot_rates,
            fx_stress_bps=self.fx_stress_bps,
            debts=self.debts,
            essentials_categories=(
                {
                    name: EssentialsCategory(
                        monthly_spend_pence=gbp_to_pence(category.monthly_spend_gbp),
                        inflation_bps=category.inflation_bps,
                    )
                    for name, category in self.essentials_categories.items()
                }
                if self.essentials_categories is not None
                else None
            ),
            horizon_months=horizon_months,
        )


class MonteCarloInputParameters(DeterministicInputParameters):
    income_shock_std_percent: float = Field(default=5.0, ge=0, le=50)
    rate_shock_std_percent: float = Field(default=0.5, ge=0, le=10)
    inflation_shock_std_percent: float = Field(default=1.0, ge=0, le=20)
    shock_dynamics: str = Field(default="iid")
    ar1_phi: float = Field(default=0.0, ge=0.0, lt=1.0)
    fx_monthly_vol_bps: dict[str, int] = Field(default_factory=dict)

    def to_engine_input(self) -> MonteCarloInput:
        base = super().to_engine_input()
        return MonteCarloInput(
            **base.model_dump(),
            income_shock_std_bps=percent_to_bps(self.income_shock_std_percent),
            rate_shock_std_bps=percent_to_bps(self.rate_shock_std_percent),
            inflation_shock_std_bps=percent_to_bps(self.inflation_shock_std_percent),
            shock_dynamics=self.shock_dynamics,
            ar1_phi=self.ar1_phi,
            fx_monthly_vol_bps=self.fx_monthly_vol_bps,
        )


class DeterministicRunRequest(BaseModel):
    input_parameters: DeterministicInputParameters
    horizon_months: int = Field(default=24, ge=1)


class DataDefaultsResponse(BaseModel):
    bank_rate_bps: int
    cpih_12m_bps: int
    fx_spot_rates: dict[str, float]
    energy_reference_values: dict[str, float] | None = None
    fetched_at: dict[str, str | None]


class IncomeMedianBhc(BaseModel):
    year_label: str
    amount_gbp: float


class ReferenceProvenance(BaseModel):
    dataset_key: str
    source_url: str
    fetched_at_utc: str | None
    sha256: str | None
    status: str


class UkReferenceValuesResponse(BaseModel):
    income_median_bhc: IncomeMedianBhc
    income_deciles_bhc_gbp: list[float] | None = None
    provenance: ReferenceProvenance


class UkPercentileRequest(BaseModel):
    annual_net_income_reporting_currency: float = Field(..., ge=0)
    reporting_currency: str = Field(default="GBP", min_length=3, max_length=3)


class UkPercentileResponse(BaseModel):
    percentile_bucket: int
    year_label: str
    reporting_currency: str
    thresholds_gbp: list[float]
    caveats: list[str]


class PdfReportRequest(BaseModel):
    inputs: dict[str, object]
    outputs: dict[str, object]
    disclaimers: list[str] = Field(default_factory=list)
    provenance: dict[str, object] = Field(default_factory=dict)
    app_version: str = Field(default="0.1.1", min_length=1)


class DeterministicRunResponse(BaseModel):
    reporting_currency: str
    fx_spot_rates_used: dict[str, float]
    fx_stressed_rates_used: dict[str, float]
    fx_stress_bps: dict[str, int]
    monthly_cashflow_base_pence: int
    monthly_cashflow_base_formatted: str
    monthly_cashflow_stress_pence: int
    monthly_cashflow_stress_formatted: str
    mortgage_payment_current_pence: int
    mortgage_payment_current_formatted: str
    mortgage_payment_stress_pence: int
    mortgage_payment_stress_formatted: str
    runway_months: float | None
    savings_path_pence: list[int]
    savings_path_formatted: list[str]
    debt_balance_path_pence: list[int] | None = None
    min_savings_pence: int
    min_savings_formatted: str
    month_of_depletion: int | None
    warnings: list[str]


class RunwayPercentileTriplet(BaseModel):
    p10: float
    p50: float
    p90: float


class MoneyPercentileTriplet(BaseModel):
    p10_pence: int
    p10_formatted: str
    p50_pence: int
    p50_formatted: str
    p90_pence: int
    p90_formatted: str


class MonteCarloMetrics(BaseModel):
    runway_months: RunwayPercentileTriplet
    min_savings: MoneyPercentileTriplet
    month_of_depletion: RunwayPercentileTriplet


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
    runway_months_p10: float
    runway_months_p50: float
    runway_months_p90: float
    min_savings_p10_pence: int
    min_savings_p50_pence: int
    min_savings_p90_pence: int
    month_of_depletion_p10: float
    month_of_depletion_p50: float
    month_of_depletion_p90: float
    metrics: MonteCarloMetrics


class CompareScenarioRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=64)
    input_parameters: DeterministicInputParameters
    horizon_months: int = Field(default=24, ge=1)


class CompareRunRequest(BaseModel):
    scenarios: list[CompareScenarioRequest] = Field(..., min_length=1, max_length=4)


class CompareScenarioResult(BaseModel):
    name: str
    reporting_currency: str
    runway_months: float | None
    month_of_depletion: int | None
    min_savings_pence: int
    min_savings_formatted: str
    monthly_cashflow_stress_pence: int
    monthly_cashflow_stress_formatted: str
    mortgage_payment_stress_pence: int
    mortgage_payment_stress_formatted: str
    warnings: list[str]


class CompareRunResponse(BaseModel):
    scenarios: list[CompareScenarioResult]


class SensitivityRunRequest(BaseModel):
    input_parameters: DeterministicInputParameters
    horizon_months: int = Field(default=24, ge=1)
    delta_bps: int = Field(default=100, ge=0, le=10_000)


class SensitivityDriverImpact(BaseModel):
    driver: str
    delta_bps: int
    base_runway_months: float | None
    perturbed_runway_months: float | None
    runway_months_impact: float | None
    base_min_savings_pence: int
    perturbed_min_savings_pence: int
    min_savings_impact_pence: int


class SensitivityRunResponse(BaseModel):
    impacts: list[SensitivityDriverImpact]
