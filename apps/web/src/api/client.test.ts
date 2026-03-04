import { describe, expect, it, vi } from "vitest";

import { createApiClient } from "./client";
import type { InputParameters } from "../types";

const inputParameters: InputParameters = {
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

describe("createApiClient", () => {
  it("attaches bearer token in Authorization header", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ ok: true })
    });
    vi.stubGlobal("fetch", fetchMock);

    const client = createApiClient("https://api.example.com", async () => "token-123");

    await client.runDeterministic({ input_parameters: inputParameters });

    expect(fetchMock).toHaveBeenCalledTimes(1);
    const [, options] = fetchMock.mock.calls[0] as [string, RequestInit];
    expect((options.headers as Record<string, string>).Authorization).toBe("Bearer token-123");
  });
});
