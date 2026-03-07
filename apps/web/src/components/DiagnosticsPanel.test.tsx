import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { DiagnosticsPanel } from "./DiagnosticsPanel";
import type { InputParameters } from "../types";

function makeInput(overrides: Partial<InputParameters> = {}): InputParameters {
  return {
    household_monthly_net_income_gbp: 4000,
    household_monthly_essential_spend_gbp: 1500,
    household_monthly_debt_payments_gbp: 200,
    cash_savings_gbp: 10000,
    mortgage_balance_gbp: 250000,
    mortgage_term_years_remaining: 25,
    mortgage_rate_percent_current: 4.5,
    mortgage_rate_percent_stress: 6,
    mortgage_type: "repayment",
    shock_monthly_income_drop_percent: 10,
    inflation_monthly_essentials_increase_percent: 5,
    household_monthly_net_income_currency: "GBP",
    household_monthly_essential_spend_currency: "GBP",
    household_monthly_debt_payments_currency: "GBP",
    cash_savings_currency: "GBP",
    mortgage_balance_currency: "GBP",
    reporting_currency: "GBP",
    fx_spot_rates: { GBP: 1, EUR: 0.86, USD: 0.78 },
    fx_stress_bps: { GBP: 0, EUR: 0, USD: 0 },
    income_shock_std_percent: 5,
    rate_shock_std_percent: 0.5,
    inflation_shock_std_percent: 1,
    ...overrides
  };
}

describe("DiagnosticsPanel", () => {
  it("shows warning when essentials exceed income", () => {
    render(
      <DiagnosticsPanel
        input={makeInput({
          household_monthly_net_income_gbp: 1800,
          household_monthly_essential_spend_gbp: 2100
        })}
      />
    );

    expect(screen.getByText("Warning:", { exact: false })).toBeInTheDocument();
    expect(screen.getByText("Essentials spending is above net income.")).toBeInTheDocument();
    expect(screen.getByText("Why this matters")).toHaveAttribute(
      "title",
      "A persistent monthly shortfall can reduce savings runway faster under stress."
    );
  });

  it("shows warning when savings are zero and monthly balance is negative", () => {
    render(
      <DiagnosticsPanel
        input={makeInput({
          household_monthly_net_income_gbp: 1500,
          household_monthly_essential_spend_gbp: 1600,
          household_monthly_debt_payments_gbp: 200,
          cash_savings_gbp: 0
        })}
      />
    );

    expect(screen.getByText("Savings are zero while monthly balance is negative.")).toBeInTheDocument();
  });

  it("shows error when reporting currency FX spot is not 1.0", () => {
    render(
      <DiagnosticsPanel
        input={makeInput({
          reporting_currency: "GBP",
          fx_spot_rates: { GBP: 0.95, EUR: 0.86, USD: 0.78 }
        })}
      />
    );

    expect(screen.getByText("Error:", { exact: false })).toBeInTheDocument();
    expect(screen.getByText("FX spot for reporting currency (GBP) must be 1.0.")).toBeInTheDocument();
  });
});
