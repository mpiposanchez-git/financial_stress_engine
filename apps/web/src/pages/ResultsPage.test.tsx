import { render, screen } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it } from "vitest";

import { ResultsPage } from "./ResultsPage";

describe("ResultsPage", () => {
  it("renders formatted and pence money fields from route state", () => {
    const state = {
      deterministic: {
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
        savings_path_pence: [123456, 120000],
        savings_path_formatted: ["£1,234.56", "£1,200.00"],
        min_savings_pence: 123456,
        min_savings_formatted: "£1,234.56",
        month_of_depletion: null,
        month_by_month: [],
        warnings: ["Educational simulation only. Not financial advice."]
      },
      montecarlo: {
        n_sims: 1000,
        horizon_months: 24,
        seed: 42,
        runtime_ms: 12.34,
        metrics: {
          runway_months: { p10: 6.5, p50: 9.5, p90: 14.2 },
          min_savings: {
            p10_pence: 10000,
            p10_formatted: "£100.00",
            p50_pence: 222222,
            p50_formatted: "£2,222.22",
            p90_pence: 500000,
            p90_formatted: "£5,000.00"
          },
          month_of_depletion: { p10: 8, p50: 13, p90: 25 }
        }
      }
    };

    render(
      <MemoryRouter initialEntries={[{ pathname: "/results", state }]}> 
        <Routes>
          <Route path="/results" element={<ResultsPage />} />
        </Routes>
      </MemoryRouter>
    );

    expect(screen.getByText(/Minimum savings: £1,234.56 \(123456 pence\)/)).toBeInTheDocument();
    expect(
      screen.getByText(/Min savings p50: £2,222.22 \(222222 pence\)/)
    ).toBeInTheDocument();
    expect(screen.getByText(/Month of depletion p50: 13/)).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Runway distribution (months)" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Deterministic savings path" })).toBeInTheDocument();
  });

  it("shows fallback message when no route state is present", () => {
    render(
      <MemoryRouter initialEntries={["/results"]}>
        <Routes>
          <Route path="/results" element={<ResultsPage />} />
        </Routes>
      </MemoryRouter>
    );

    expect(screen.getByText("No results yet.")).toBeInTheDocument();
  });
});
