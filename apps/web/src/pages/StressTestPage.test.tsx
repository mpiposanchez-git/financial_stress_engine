import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";

import { StressTestPage } from "./StressTestPage";

const {
  mockNavigate,
  mockRunDeterministic,
  mockRunMonteCarlo,
  mockGetToken,
  deterministicResponse,
  monteCarloResponse
} = vi.hoisted(() => {
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
    runway_months: 7.25,
    savings_path_pence: [125000, 175000],
    savings_path_formatted: ["£1,250.00", "£1,750.00"],
    min_savings_pence: 125000,
    min_savings_formatted: "£1,250.00",
    month_of_depletion: null,
    warnings: ["Educational simulation only. Not financial advice."]
  };

  const montecarlo = {
    n_sims: 1000,
    horizon_months: 24,
    seed: 123,
    runtime_ms: 12.5,
    metrics: {
      runway_months: { p10: 3.1, p50: 6.9, p90: 12.4 },
      min_savings: {
        p10_pence: 1000,
        p10_formatted: "£10.00",
        p50_pence: 2000,
        p50_formatted: "£20.00",
        p90_pence: 3000,
        p90_formatted: "£30.00"
      },
      month_of_depletion: { p10: 8.0, p50: 11.0, p90: 25.0 }
    }
  };

  return {
    mockNavigate: vi.fn(),
    mockRunDeterministic: vi.fn().mockResolvedValue(deterministic),
    mockRunMonteCarlo: vi.fn().mockResolvedValue(montecarlo),
    mockGetToken: vi.fn(),
    deterministicResponse: deterministic,
    monteCarloResponse: montecarlo
  };
});

vi.mock("react-router-dom", async () => {
  const actual = await vi.importActual<typeof import("react-router-dom")>("react-router-dom");
  return {
    ...actual,
    useNavigate: () => mockNavigate
  };
});

vi.mock("../auth/useAuthState", () => ({
  useAuthState: () => ({
    isLoaded: true,
    isSignedIn: true,
    getToken: mockGetToken
  })
}));

vi.mock("../api/client", () => ({
  createApiClient: () => ({
    runDeterministic: mockRunDeterministic,
    runMonteCarlo: mockRunMonteCarlo
  })
}));

describe("StressTestPage", () => {
  it("supports wizard step navigation", () => {
    const { container } = render(
      <MemoryRouter>
        <StressTestPage />
      </MemoryRouter>
    );
    const ui = within(container);

    expect(ui.getByText("Step 1 of 3")).toBeInTheDocument();
    expect(ui.getByRole("heading", { name: "Currencies and FX spots" })).toBeInTheDocument();

    fireEvent.click(ui.getByRole("button", { name: "Next" }));
    expect(ui.getByText("Step 2 of 3")).toBeInTheDocument();
    expect(ui.getByRole("heading", { name: "Mortgage inputs" })).toBeInTheDocument();

    fireEvent.click(ui.getByRole("button", { name: "Next" }));
    expect(ui.getByText("Step 3 of 3")).toBeInTheDocument();
    expect(ui.getByRole("heading", { name: "FX stress and review" })).toBeInTheDocument();

    fireEvent.click(ui.getByRole("button", { name: "Back" }));
    expect(ui.getByText("Step 2 of 3")).toBeInTheDocument();
  });

  it("provides explicit labels and error descriptors for form controls", () => {
    const { container } = render(
      <MemoryRouter>
        <StressTestPage />
      </MemoryRouter>
    );
    const ui = within(container);

    const reportingCurrency = ui.getByRole("combobox", { name: "Reporting currency" });
    const incomeCurrency = ui.getByRole("combobox", { name: "Income currency" });
    const fxSpotEur = ui.getByLabelText("FX spot EUR to reporting");

    expect(reportingCurrency).toHaveAttribute("aria-describedby", "stress-form-error");
    expect(incomeCurrency).toHaveAttribute("aria-describedby", "stress-form-error");
    expect(fxSpotEur).toHaveAttribute("aria-describedby", "stress-form-error");
    expect(ui.getByRole("alert")).toHaveAttribute("id", "stress-form-error");
  });

  it("navigates to results with deterministic and montecarlo state", async () => {
    const { container } = render(
      <MemoryRouter>
        <StressTestPage />
      </MemoryRouter>
    );
    const ui = within(container);

    fireEvent.click(ui.getByRole("button", { name: "Next" }));
    fireEvent.click(ui.getByRole("button", { name: "Next" }));
    fireEvent.click(ui.getByRole("button", { name: "Run simulation" }));

    await waitFor(() => {
      expect(mockRunDeterministic).toHaveBeenCalledTimes(1);
      expect(mockRunMonteCarlo).toHaveBeenCalledTimes(1);
      expect(mockNavigate).toHaveBeenCalledWith("/results", {
        state: {
          deterministic: deterministicResponse,
          montecarlo: monteCarloResponse
        }
      });
    });
  });
});
