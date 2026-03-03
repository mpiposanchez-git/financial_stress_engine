from pydantic import BaseModel

DISCLAIMER = (
    "EDUCATIONAL SIMULATION ONLY. This output is not financial advice, investment advice, "
    "or a product recommendation. Results are illustrative estimates based on the inputs you "
    "provided and simplified modelling assumptions. Always consult a qualified financial adviser "
    "before making financial decisions. Past performance and modelled scenarios are not reliable "
    "indicators of future results."
)


class DeterministicOutput(BaseModel):
    monthly_cashflow_base_gbp: float
    monthly_cashflow_stress_gbp: float
    estimated_months_of_runway_base: float | None
    estimated_months_of_runway_stress: float | None
    mortgage_payment_current_gbp: float
    mortgage_payment_stress_gbp: float
    summary: str
    disclaimer: str = DISCLAIMER


class MonteCarloOutput(BaseModel):
    p10_monthly_cashflow_gbp: float
    p50_monthly_cashflow_gbp: float
    p90_monthly_cashflow_gbp: float
    p10_runway_months: float | None
    p50_runway_months: float | None
    p90_runway_months: float | None
    probability_negative_cashflow: float
    probability_runway_lt_3_months: float
    num_trials: int
    disclaimer: str = DISCLAIMER
