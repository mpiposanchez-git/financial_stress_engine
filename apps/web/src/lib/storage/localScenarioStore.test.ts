import { beforeEach, describe, expect, it } from "vitest";

import { FREE_SCENARIO_LIMIT, getSavedScenarios, saveScenario } from "./localScenarioStore";
import { InputParameters } from "../../types";

const baseInput: InputParameters = {
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
};

describe("localScenarioStore", () => {
  beforeEach(() => {
    window.localStorage.clear();
  });

  it("enforces free save limit", () => {
    const first = saveScenario({ name: "Base", input: baseInput, premiumUnlocked: false });
    const second = saveScenario({ name: "A", input: baseInput, premiumUnlocked: false });
    const third = saveScenario({ name: "B", input: baseInput, premiumUnlocked: false });

    expect(first.ok).toBe(true);
    expect(second.ok).toBe(true);
    expect(third.ok).toBe(false);
    if (!third.ok) {
      expect(third.reason).toBe("limit");
    }
    expect(getSavedScenarios()).toHaveLength(FREE_SCENARIO_LIMIT);
  });

  it("allows unlimited saves for premium", () => {
    for (let index = 0; index < FREE_SCENARIO_LIMIT + 2; index += 1) {
      const result = saveScenario({
        name: `Scenario ${index + 1}`,
        input: baseInput,
        premiumUnlocked: true
      });
      expect(result.ok).toBe(true);
    }

    expect(getSavedScenarios().length).toBe(FREE_SCENARIO_LIMIT + 2);
  });
});
