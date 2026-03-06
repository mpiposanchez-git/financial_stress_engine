import { describe, expect, it } from "vitest";

import { buildDeterministicPayload } from "./buildPayload";
import type { InputParameters } from "../types";

const input: InputParameters = {
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
  reporting_currency: "EUR",
  fx_spot_rates: { GBP: 1.17, EUR: 0.84, USD: 0.78 },
  fx_stress_bps: { USD: 45 },
  income_shock_std_percent: 5,
  rate_shock_std_percent: 0.5,
  inflation_shock_std_percent: 1
};

describe("buildDeterministicPayload", () => {
  it("normalizes reporting currency FX spot to 1 and fills missing FX stress keys", () => {
    const payload = buildDeterministicPayload(input);

    expect(payload.input_parameters.fx_spot_rates.EUR).toBe(1);
    expect(payload.input_parameters.fx_spot_rates.GBP).toBe(1.17);
    expect(payload.input_parameters.fx_stress_bps).toEqual({ GBP: 0, EUR: 0, USD: 45 });
  });
});
