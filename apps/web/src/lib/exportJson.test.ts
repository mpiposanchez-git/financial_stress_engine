import { describe, expect, it } from "vitest";

import { buildExportBundle, formatJsonExportFilename } from "./exportJson";

const deterministic = {
  reporting_currency: "GBP",
  fx_spot_rates_used: { GBP: 1, EUR: 0.86, USD: 0.78 },
  fx_stressed_rates_used: { GBP: 1, EUR: 0.86, USD: 0.78 },
  fx_stress_bps: { GBP: 0, EUR: 0, USD: 0 },
  monthly_cashflow_base_pence: 100000,
  monthly_cashflow_base_formatted: "£1,000.00",
  monthly_cashflow_stress_pence: 50000,
  monthly_cashflow_stress_formatted: "£500.00",
  mortgage_payment_current_pence: 120000,
  mortgage_payment_current_formatted: "£1,200.00",
  mortgage_payment_stress_pence: 150000,
  mortgage_payment_stress_formatted: "£1,500.00",
  runway_months: 12.5,
  savings_path_pence: [120000, 110000],
  savings_path_formatted: ["£1,200.00", "£1,100.00"],
  min_savings_pence: 110000,
  min_savings_formatted: "£1,100.00",
  month_of_depletion: null,
  warnings: [],
};

describe("exportJson", () => {
  it("formats filename with UTC date and reporting currency", () => {
    const date = new Date("2026-03-06T13:14:15Z");
    expect(formatJsonExportFilename("GBP", date)).toBe("stress-export-2026-03-06-GBP.json");
  });

  it("builds required export keys and premium-gated sections", () => {
    const bundle = buildExportBundle({
      inputParameters: null,
      deterministic: deterministic as never,
      montecarlo: null,
      sensitivityImpacts: null,
      premiumUnlocked: false,
      provenance: { data_timestamp: "2026-03-06T00:00:00Z" },
      appVersion: "0.1.1",
      modelVersion: "deterministic-v1",
    });

    expect(Object.keys(bundle)).toEqual([
      "input_payload",
      "deterministic_outputs",
      "montecarlo_outputs",
      "sensitivity_outputs",
      "provenance",
      "versions",
    ]);
    expect(bundle.montecarlo_outputs).toBeNull();
    expect(bundle.sensitivity_outputs).toBeNull();
    expect((bundle.versions as Record<string, string>).app_version).toBe("0.1.1");
  });
});
