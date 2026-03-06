import { render, screen, waitFor, within } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { ResultsPage } from "./ResultsPage";

const { mockGetToken, mockRunSensitivity, mockGetUkReferenceValues, mockGetUkPercentile } = vi.hoisted(() => ({
  mockGetToken: vi.fn(),
  mockRunSensitivity: vi.fn().mockResolvedValue({
    impacts: [
      {
        driver: "mortgage_rate_stress_bps",
        delta_bps: 100,
        base_runway_months: 10.2,
        perturbed_runway_months: 9.4,
        runway_months_impact: -0.8,
        base_min_savings_pence: 250000,
        perturbed_min_savings_pence: 190000,
        min_savings_impact_pence: -60000
      }
    ]
  }),
  mockGetUkReferenceValues: vi.fn().mockResolvedValue({
    income_median_bhc: { year_label: "FY2024", amount_gbp: 35000 },
    income_deciles_bhc_gbp: null,
    provenance: {
      dataset_key: "dwp_hbai_zip_raw",
      source_url: "https://example.test/hbai",
      fetched_at_utc: "2026-03-06T00:00:00Z",
      sha256: "abc",
      status: "placeholder",
    },
  }),
  mockGetUkPercentile: vi.fn().mockResolvedValue({
    percentile_bucket: 70,
    year_label: "FY2024",
    reporting_currency: "GBP",
    thresholds_gbp: [12000, 15500, 19000, 23000, 28000, 34000, 42000, 55000, 80000],
    caveats: ["indicative"],
  }),
}));

vi.mock("../auth/useAuthState", () => ({
  useAuthState: () => ({
    isLoaded: true,
    isSignedIn: true,
    getToken: mockGetToken
  })
}));

vi.mock("../api/client", () => ({
  createApiClient: () => ({
    runDeterministic: vi.fn(),
    runMonteCarlo: vi.fn(),
    runSensitivity: mockRunSensitivity,
    getUkReferenceValues: mockGetUkReferenceValues,
    getUkPercentile: mockGetUkPercentile,
  })
}));

const inputParameters = {
  household_monthly_net_income_gbp: 4000,
  household_monthly_essential_spend_gbp: 1500,
  household_monthly_debt_payments_gbp: 200,
  cash_savings_gbp: 10000,
  mortgage_balance_gbp: 250000,
  mortgage_term_years_remaining: 25,
  mortgage_rate_percent_current: 4.5,
  mortgage_rate_percent_stress: 6,
  mortgage_type: "repayment" as const,
  shock_monthly_income_drop_percent: 10,
  inflation_monthly_essentials_increase_percent: 5,
  household_monthly_net_income_currency: "GBP" as const,
  household_monthly_essential_spend_currency: "GBP" as const,
  household_monthly_debt_payments_currency: "GBP" as const,
  cash_savings_currency: "GBP" as const,
  mortgage_balance_currency: "GBP" as const,
  reporting_currency: "GBP" as const,
  fx_spot_rates: { GBP: 1, EUR: 0.86, USD: 0.78 },
  fx_stress_bps: { GBP: 0, EUR: 0, USD: 0 },
  income_shock_std_percent: 5,
  rate_shock_std_percent: 0.5,
  inflation_shock_std_percent: 1
};

describe("ResultsPage", () => {
  beforeEach(() => {
    mockRunSensitivity.mockClear();
    mockGetUkReferenceValues.mockClear();
    mockGetUkPercentile.mockClear();
  });

  it("renders formatted and pence money fields from route state", () => {
    const state = {
      premiumUnlocked: true,
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
        runway_months_p10: 6.5,
        runway_months_p50: 9.5,
        runway_months_p90: 14.2,
        min_savings_p10_pence: 10000,
        min_savings_p50_pence: 222222,
        min_savings_p90_pence: 500000,
        month_of_depletion_p10: 8,
        month_of_depletion_p50: 13,
        month_of_depletion_p90: 25,
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
    expect(screen.getByRole("heading", { name: "Fan chart" })).toBeInTheDocument();
    expect(screen.getByText("Summary percentiles")).toBeInTheDocument();
    expect(screen.getByRole("table", { name: "Monte Carlo summary percentiles" })).toBeInTheDocument();
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
    expect(
      screen.getByText(/Summary: starts at 123456 pence, ends at 120000 pence, and ranges between 120000 and 123456 pence\./)
    ).toBeInTheDocument();
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
    expect(ui.queryByRole("heading", { name: "Fan chart" })).not.toBeInTheDocument();
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

  it("shows fan chart locked card when montecarlo is present but premium is locked", () => {
    const state = {
      premiumUnlocked: false,
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
        warnings: []
      },
      montecarlo: {
        n_sims: 1000,
        horizon_months: 24,
        seed: 42,
        runtime_ms: 12.34,
        runway_months_p10: 6.5,
        runway_months_p50: 9.5,
        runway_months_p90: 14.2,
        min_savings_p10_pence: 10000,
        min_savings_p50_pence: 222222,
        min_savings_p90_pence: 500000,
        month_of_depletion_p10: 8,
        month_of_depletion_p50: 13,
        month_of_depletion_p90: 25,
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

    const { container } = render(
      <MemoryRouter initialEntries={[{ pathname: "/results", state }]}> 
        <Routes>
          <Route path="/results" element={<ResultsPage />} />
        </Routes>
      </MemoryRouter>
    );
    const ui = within(container);

    expect(ui.getByText("Premium unlock required to view summary percentile fan chart.")).toBeInTheDocument();
    expect(ui.queryByRole("table", { name: "Monte Carlo summary percentiles" })).not.toBeInTheDocument();
  });

  it("fetches and renders tornado sensitivity chart for premium runs", async () => {
    const state = {
      premiumUnlocked: true,
      inputParameters,
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

    await waitFor(() => {
      expect(mockRunSensitivity).toHaveBeenCalledTimes(1);
      expect(ui.getByRole("heading", { name: "Tornado sensitivity chart" })).toBeInTheDocument();
      expect(ui.getByText(/Top sensitivity driver:/)).toBeInTheDocument();
    });
  });

  it("shows tornado locked card for non-premium", () => {
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

    expect(ui.getByText("Premium unlock required to view tornado sensitivity chart.")).toBeInTheDocument();
  });
});
