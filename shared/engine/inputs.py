from typing import Literal

from pydantic import BaseModel, Field, model_validator

from shared.engine.fx import SUPPORTED_CURRENCIES, validate_currency


class DeterministicInput(BaseModel):
    household_monthly_net_income_pence: int = Field(
        ..., ge=0, description="Monthly net household income in pence"
    )
    household_monthly_essential_spend_pence: int = Field(
        ..., ge=0, description="Monthly essential spending in pence"
    )
    household_monthly_debt_payments_pence: int = Field(
        ..., ge=0, description="Monthly non-mortgage debt payments in pence"
    )
    cash_savings_pence: int = Field(..., ge=0, description="Total liquid cash savings in pence")
    mortgage_balance_pence: int = Field(
        ..., ge=0, description="Outstanding mortgage balance in pence"
    )
    mortgage_term_months_remaining: int = Field(
        ..., ge=0, description="Remaining mortgage term in months"
    )
    mortgage_rate_bps_current: int = Field(
        ..., ge=0, le=10_000, description="Current mortgage interest rate in basis points"
    )
    mortgage_rate_bps_stress: int = Field(
        ..., ge=0, le=10_000, description="Stressed mortgage interest rate in basis points"
    )
    mortgage_type: Literal["repayment", "interest_only"] = Field(..., description="Mortgage type")
    shock_monthly_income_drop_bps: int = Field(
        ..., ge=0, le=10_000, description="Income shock: percentage drop in basis points"
    )
    inflation_monthly_essentials_increase_bps: int = Field(
        ..., ge=0, le=10_000, description="Monthly essentials inflation increase in basis points"
    )
    household_monthly_net_income_currency: Literal["GBP", "EUR", "USD"] = "GBP"
    household_monthly_essential_spend_currency: Literal["GBP", "EUR", "USD"] = "GBP"
    household_monthly_debt_payments_currency: Literal["GBP", "EUR", "USD"] = "GBP"
    cash_savings_currency: Literal["GBP", "EUR", "USD"] = "GBP"
    mortgage_balance_currency: Literal["GBP", "EUR", "USD"] = "GBP"
    reporting_currency: Literal["GBP", "EUR", "USD"] = "GBP"
    fx_spot_rates: dict[str, float] = Field(
        default_factory=lambda: {"GBP": 1.0, "EUR": 0.86, "USD": 0.78}
    )
    fx_stress_bps: dict[str, int] = Field(default_factory=dict)
    horizon_months: int = Field(default=24, ge=1, description="Projection horizon in months")

    @model_validator(mode="after")
    def validate_mortgage_term(self) -> "DeterministicInput":
        if self.mortgage_balance_pence > 0 and self.mortgage_term_months_remaining <= 0:
            raise ValueError(
                "mortgage_term_months_remaining must be > 0 when mortgage_balance_pence > 0"
            )

        for code in self.fx_spot_rates:
            validate_currency(code)
        for code in self.fx_stress_bps:
            validate_currency(code)

        required = {
            self.household_monthly_net_income_currency,
            self.household_monthly_essential_spend_currency,
            self.household_monthly_debt_payments_currency,
            self.cash_savings_currency,
            self.mortgage_balance_currency,
            self.reporting_currency,
        }

        missing = [code for code in required if code not in self.fx_spot_rates]
        if missing:
            raise ValueError(f"Missing fx_spot_rates for currencies: {', '.join(sorted(missing))}")

        if self.fx_spot_rates.get(self.reporting_currency) != 1.0:
            raise ValueError("fx_spot_rates for reporting_currency must be 1.0")

        for code, shock in self.fx_stress_bps.items():
            if shock < -9_999 or shock > 10_000:
                raise ValueError(f"fx_stress_bps for {code} must be between -9999 and 10000")

        return self


class MonteCarloInput(DeterministicInput):
    num_trials: int = Field(
        default=10_000, ge=100, le=50_000, description="Number of Monte Carlo trials"
    )
    income_shock_std_bps: int = Field(
        default=500, ge=0, le=5_000, description="Std deviation of income shock in basis points"
    )
    rate_shock_std_bps: int = Field(
        default=50,
        ge=0,
        le=1_000,
        description="Std deviation of mortgage rate shock in basis points",
    )
    inflation_shock_std_bps: int = Field(
        default=100,
        ge=0,
        le=2_000,
        description="Std deviation of essentials inflation shock in basis points",
    )
    shock_dynamics: Literal["iid", "ar1"] = Field(default="iid")
    ar1_phi: float = Field(default=0.0, ge=0.0, lt=1.0)
    fx_monthly_vol_bps: dict[str, int] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_montecarlo_fx(self) -> "MonteCarloInput":
        for code, vol in self.fx_monthly_vol_bps.items():
            validate_currency(code)
            if vol < 0 or vol > 5_000:
                raise ValueError(f"fx_monthly_vol_bps for {code} must be between 0 and 5000")
        return self
