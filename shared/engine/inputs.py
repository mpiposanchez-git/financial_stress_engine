from typing import Literal

from pydantic import BaseModel, Field, model_validator


class DeterministicInput(BaseModel):
    household_monthly_net_income_gbp: float = Field(
        ..., ge=0, description="Monthly net household income in GBP"
    )
    household_monthly_essential_spend_gbp: float = Field(
        ..., ge=0, description="Monthly essential spending in GBP"
    )
    household_monthly_debt_payments_gbp: float = Field(
        ..., ge=0, description="Monthly non-mortgage debt payments in GBP"
    )
    cash_savings_gbp: float = Field(..., ge=0, description="Total liquid cash savings in GBP")
    mortgage_balance_gbp: float = Field(
        ..., ge=0, description="Outstanding mortgage balance in GBP"
    )
    mortgage_term_years_remaining: float = Field(
        ..., ge=0, description="Remaining mortgage term in years"
    )
    mortgage_rate_percent_current: float = Field(
        ..., ge=0, le=100, description="Current mortgage interest rate (%)"
    )
    mortgage_rate_percent_stress: float = Field(
        ..., ge=0, le=100, description="Stressed mortgage interest rate (%)"
    )
    mortgage_type: Literal["repayment", "interest_only"] = Field(..., description="Mortgage type")
    shock_monthly_income_drop_percent: float = Field(
        ..., ge=0, le=100, description="Income shock: percentage drop (%)"
    )
    inflation_monthly_essentials_increase_percent: float = Field(
        ..., ge=0, le=100, description="Monthly essentials inflation increase (%)"
    )

    @model_validator(mode="after")
    def validate_mortgage_term(self) -> "DeterministicInput":
        if self.mortgage_balance_gbp > 0 and self.mortgage_term_years_remaining <= 0:
            raise ValueError(
                "mortgage_term_years_remaining must be > 0 when mortgage_balance_gbp > 0"
            )
        return self


class MonteCarloInput(DeterministicInput):
    num_trials: int = Field(
        default=10_000, ge=100, le=50_000, description="Number of Monte Carlo trials"
    )
    income_shock_std_percent: float = Field(
        default=5.0, ge=0, le=50, description="Std deviation of income shock (%)"
    )
    rate_shock_std_percent: float = Field(
        default=0.5, ge=0, le=10, description="Std deviation of mortgage rate shock (%)"
    )
    inflation_shock_std_percent: float = Field(
        default=1.0, ge=0, le=20, description="Std deviation of essentials inflation shock (%)"
    )