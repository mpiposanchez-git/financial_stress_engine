import { fireEvent, render, screen, within } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { SavedScenarios } from "./SavedScenarios";

describe("SavedScenarios", () => {
  it("shows device-only warning and free-plan limit message", () => {
    render(
      <SavedScenarios
        scenarios={[
          {
            id: "1",
            name: "Base",
            savedAtIso: "2026-03-06T00:00:00.000Z",
            input: {
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
              inflation_shock_std_percent: 1
            }
          },
          {
            id: "2",
            name: "Scenario A",
            savedAtIso: "2026-03-06T01:00:00.000Z",
            input: {
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
              inflation_shock_std_percent: 1
            }
          }
        ]}
        premiumUnlocked={false}
        onSave={vi.fn()}
        onLoad={vi.fn()}
        onDelete={vi.fn()}
      />
    );

    expect(screen.getByText("Saved only on this device.")).toBeInTheDocument();
    expect(screen.getByText("2/2 saved on free plan")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Save current scenario" })).toBeDisabled();
    expect(screen.getByText("Free plan limit reached. Premium unlocks unlimited saved scenarios.")).toBeInTheDocument();
  });

  it("invokes save and load handlers", () => {
    const onSave = vi.fn();
    const onLoad = vi.fn();

    const { container } = render(
      <SavedScenarios
        scenarios={[
          {
            id: "1",
            name: "Base",
            savedAtIso: "2026-03-06T00:00:00.000Z",
            input: {
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
              inflation_shock_std_percent: 1
            }
          }
        ]}
        premiumUnlocked={true}
        onSave={onSave}
        onLoad={onLoad}
        onDelete={vi.fn()}
      />
    );
    const ui = within(container);

    fireEvent.change(ui.getByRole("textbox", { name: "Scenario name" }), {
      target: { value: "Inflation stress" }
    });
    fireEvent.click(ui.getByRole("button", { name: "Save current scenario" }));
    expect(onSave).toHaveBeenCalledWith("Inflation stress");

    fireEvent.click(ui.getByRole("button", { name: "Load" }));
    expect(onLoad).toHaveBeenCalledTimes(1);
  });
});
