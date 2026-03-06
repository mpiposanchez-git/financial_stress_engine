import { render, screen, within } from "@testing-library/react";
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
    expect(screen.getByRole("heading", { name: "Mortgage stress impact" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Emergency fund adequacy" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Explain the result" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Assumptions and limits" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Official resources" })).toBeInTheDocument();
    expect(screen.getByText("runway")).toHaveAttribute(
      "title",
      "Estimated months until savings are depleted under model assumptions."
    );
    expect(screen.getByText(/Delta under stress: \+30000p \(higher than current\)\./)).toBeInTheDocument();
    expect(screen.getByText(/P10: 6.5m \| P50: 9.5m \| P90: 14.2m/)).toBeInTheDocument();
    expect(
      screen.getByText(/Summary: central estimate at P50 is 9.5m, with an approximate spread of 6.5m to 14.2m\./)
    ).toBeInTheDocument();
    expect(
      screen.getByText(/Summary: starts at 123456 pence, ends at 120000 pence, and ranges between 120000 and 123456 pence\./)
    ).toBeInTheDocument();
    expect(
      screen.getByText(/Approximate benchmark only\. Percentile ranking uses the UK HBAI BHC definition and depends on year and definitions\./)
    ).toBeInTheDocument();
    expect(screen.getByText(/It is not advice and not a measure of worth\./)).toBeInTheDocument();
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

  it("renders deterministic-only results when montecarlo state is absent", () => {
    const state = {
      deterministic: {
        reporting_currency: "GBP",
        fx_spot_rates_used: { GBP: 1, EUR: 0.86, USD: 0.78 },
        fx_stressed_rates_used: { GBP: 1, EUR: 0.86, USD: 0.78 },
        fx_stress_bps: { GBP: 0, EUR: 0, USD: 0 },
        monthly_cashflow_base_pence: 90000,
        monthly_cashflow_base_formatted: "£900.00",
        monthly_cashflow_stress_pence: 40000,
        monthly_cashflow_stress_formatted: "£400.00",
        mortgage_payment_current_pence: 120000,
        mortgage_payment_current_formatted: "£1,200.00",
        mortgage_payment_stress_pence: 150000,
        mortgage_payment_stress_formatted: "£1,500.00",
        runway_months: 9.2,
        savings_path_pence: [90000, 87000],
        savings_path_formatted: ["£900.00", "£870.00"],
        min_savings_pence: 87000,
        min_savings_formatted: "£870.00",
        month_of_depletion: null,
        warnings: []
      }
    };

    const { container } = render(
      <MemoryRouter initialEntries={[{ pathname: "/results", state }]}> 
        <Routes>
          <Route path="/results" element={<ResultsPage />} />
        </Routes>
      </MemoryRouter>
    );
    const ui = within(container);

    expect(ui.getByText(/Minimum savings: £870.00 \(87000 pence\)/)).toBeInTheDocument();
    expect(ui.getByText("Monte Carlo results unavailable for this run.")).toBeInTheDocument();
    expect(ui.queryByRole("heading", { name: "Runway distribution (months)" })).not.toBeInTheDocument();
  });

  it("renders scenario comparison table for premium users", () => {
    const state = {
      premiumUnlocked: true,
      deterministic: {
        reporting_currency: "GBP",
        fx_spot_rates_used: { GBP: 1, EUR: 0.86, USD: 0.78 },
        fx_stressed_rates_used: { GBP: 1, EUR: 0.86, USD: 0.78 },
        fx_stress_bps: { GBP: 0, EUR: 0, USD: 0 },
        monthly_cashflow_base_pence: 90000,
        monthly_cashflow_base_formatted: "£900.00",
        monthly_cashflow_stress_pence: 40000,
        monthly_cashflow_stress_formatted: "£400.00",
        mortgage_payment_current_pence: 120000,
        mortgage_payment_current_formatted: "£1,200.00",
        mortgage_payment_stress_pence: 150000,
        mortgage_payment_stress_formatted: "£1,500.00",
        runway_months: 9.2,
        savings_path_pence: [90000, 87000],
        savings_path_formatted: ["£900.00", "£870.00"],
        min_savings_pence: 87000,
        min_savings_formatted: "£870.00",
        month_of_depletion: null,
        warnings: []
      },
      compare: {
        scenarios: [
          {
            name: "Base",
            reporting_currency: "GBP",
            runway_months: 11.2,
            month_of_depletion: 17,
            min_savings_pence: 110000,
            min_savings_formatted: "GBP 1,100.00",
            monthly_cashflow_stress_pence: -10000,
            monthly_cashflow_stress_formatted: "GBP -100.00",
            mortgage_payment_stress_pence: 145000,
            mortgage_payment_stress_formatted: "GBP 1,450.00",
            warnings: []
          },
          {
            name: "A",
            reporting_currency: "GBP",
            runway_months: null,
            month_of_depletion: null,
            min_savings_pence: 250000,
            min_savings_formatted: "GBP 2,500.00",
            monthly_cashflow_stress_pence: 5000,
            monthly_cashflow_stress_formatted: "GBP 50.00",
            mortgage_payment_stress_pence: 135000,
            mortgage_payment_stress_formatted: "GBP 1,350.00",
            warnings: []
          }
        ]
      }
    };

    render(
      <MemoryRouter initialEntries={[{ pathname: "/results", state }]}> 
        <Routes>
          <Route path="/results" element={<ResultsPage />} />
        </Routes>
      </MemoryRouter>
    );

    expect(screen.getByRole("heading", { name: "Scenario comparison" })).toBeInTheDocument();
    const table = screen.getByRole("table", { name: "Scenario comparison table" });
    const ui = within(table);
    expect(ui.getByRole("columnheader", { name: "Runway (months)" })).toBeInTheDocument();
    expect(ui.getByRole("cell", { name: "Base" })).toBeInTheDocument();
    expect(ui.getByRole("cell", { name: "11.2" })).toBeInTheDocument();
    expect(ui.getByRole("cell", { name: "A" })).toBeInTheDocument();
    expect(ui.getByRole("cell", { name: "Solvent" })).toBeInTheDocument();
  });

  it("shows premium lock message when compare data exists but premium is locked", () => {
    const state = {
      premiumUnlocked: false,
      deterministic: {
        reporting_currency: "GBP",
        fx_spot_rates_used: { GBP: 1, EUR: 0.86, USD: 0.78 },
        fx_stressed_rates_used: { GBP: 1, EUR: 0.86, USD: 0.78 },
        fx_stress_bps: { GBP: 0, EUR: 0, USD: 0 },
        monthly_cashflow_base_pence: 90000,
        monthly_cashflow_base_formatted: "£900.00",
        monthly_cashflow_stress_pence: 40000,
        monthly_cashflow_stress_formatted: "£400.00",
        mortgage_payment_current_pence: 120000,
        mortgage_payment_current_formatted: "£1,200.00",
        mortgage_payment_stress_pence: 150000,
        mortgage_payment_stress_formatted: "£1,500.00",
        runway_months: 9.2,
        savings_path_pence: [90000, 87000],
        savings_path_formatted: ["£900.00", "£870.00"],
        min_savings_pence: 87000,
        min_savings_formatted: "£870.00",
        month_of_depletion: null,
        warnings: []
      },
      compare: {
        scenarios: [
          {
            name: "Base",
            reporting_currency: "GBP",
            runway_months: 11.2,
            month_of_depletion: 17,
            min_savings_pence: 110000,
            min_savings_formatted: "GBP 1,100.00",
            monthly_cashflow_stress_pence: -10000,
            monthly_cashflow_stress_formatted: "GBP -100.00",
            mortgage_payment_stress_pence: 145000,
            mortgage_payment_stress_formatted: "GBP 1,450.00",
            warnings: []
          }
        ]
      }
    };

    const { container } = render(
      <MemoryRouter initialEntries={[{ pathname: "/results", state }]}> 
        <Routes>
          <Route path="/results" element={<ResultsPage />} />
        </Routes>
      </MemoryRouter>
    );
    const ui = within(container);

    expect(ui.getByText("Premium unlock required to view side-by-side scenario comparison.")).toBeInTheDocument();
    expect(ui.queryByRole("table", { name: "Scenario comparison table" })).not.toBeInTheDocument();
  });
});
