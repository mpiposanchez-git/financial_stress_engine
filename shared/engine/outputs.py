from pydantic import BaseModel, Field

DISCLAIMER = (
    "EDUCATIONAL SIMULATION ONLY. This output is not financial advice, investment advice, "
    "or a product recommendation. Results are illustrative estimates based on the inputs you "
    "provided and simplified modelling assumptions. Always consult a qualified financial adviser "
    "before making financial decisions. Past performance and modelled scenarios are not reliable "
    "indicators of future results."
)


class DeterministicOutput(BaseModel):
    reporting_currency: str
    fx_spot_rates_used: dict[str, float]
    fx_stressed_rates_used: dict[str, float]
    fx_stress_bps: dict[str, int]
    monthly_cashflow_base_pence: int
    monthly_cashflow_base_formatted: str
    monthly_cashflow_stress_pence: int
    monthly_cashflow_stress_formatted: str
    estimated_months_of_runway_base: float | None
    estimated_months_of_runway_stress: float | None
    mortgage_payment_current_pence: int
    mortgage_payment_current_formatted: str
    mortgage_payment_stress_pence: int
    mortgage_payment_stress_formatted: str
    savings_path_pence: list[int] = Field(
        ..., description="Savings path including month 0 (initial) through horizon month"
    )
    savings_path_formatted: list[str] = Field(
        ..., description="Formatted savings path values aligned with savings_path_pence"
    )
    min_savings_pence: int
    min_savings_formatted: str
    month_of_depletion: int | None
    runway_months: float | None
    summary: str
    disclaimer: str = DISCLAIMER
