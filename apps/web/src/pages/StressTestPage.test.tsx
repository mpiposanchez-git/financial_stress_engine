import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { StressTestPage } from "./StressTestPage";

const {
  mockNavigate,
  mockRunDeterministic,
  mockGetDefaults,
  mockGetToken,
  deterministicResponse
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

  return {
    mockNavigate: vi.fn(),
    mockRunDeterministic: vi.fn().mockResolvedValue(deterministic),
    mockGetDefaults: vi.fn().mockResolvedValue({
      bank_rate_bps: 525,
      cpih_12m_bps: 310,
      fx_spot_rates: { EUR: 0.91, USD: 0.83 },
      energy_reference_values: { annual_bill_gbp: 1738 },
      fetched_at: { boe_bank_rate: "2026-03-06T00:00:00Z" }
    }),
    mockGetToken: vi.fn(),
    deterministicResponse: deterministic
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
    getDefaults: mockGetDefaults,
    runDeterministic: mockRunDeterministic,
    runMonteCarlo: vi.fn()
  })
}));

describe("StressTestPage", () => {
  beforeEach(() => {
    window.localStorage.clear();
    mockGetDefaults.mockClear();
  });

  it("prefills defaults and allows manual override", async () => {
    render(
      <MemoryRouter>
        <StressTestPage />
      </MemoryRouter>
    );

    await waitFor(() => {
      expect(mockGetDefaults).toHaveBeenCalledTimes(1);
      expect(screen.getByLabelText("FX spot EUR to reporting")).toHaveValue(0.91);
      expect(screen.getByLabelText("Use defaults")).toBeChecked();
    });

    const eurInput = screen.getByLabelText("FX spot EUR to reporting");
    fireEvent.change(eurInput, { target: { value: "0.95" } });
    expect(eurInput).toHaveValue(0.95);
  });

  it("supports wizard step navigation", () => {
    const { container } = render(
      <MemoryRouter>
        <StressTestPage />
      </MemoryRouter>
    );
    const ui = within(container);

    expect(ui.getByRole("tab", { name: "Base" })).toHaveAttribute("aria-selected", "true");
    expect(ui.getByRole("tab", { name: "A (Premium)" })).toBeDisabled();

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

  it("navigates to results with deterministic state", async () => {
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
      expect(mockNavigate).toHaveBeenCalledWith("/results", {
        state: expect.objectContaining({
          deterministic: deterministicResponse,
          premiumUnlocked: false,
          inputParameters: expect.objectContaining({
            reporting_currency: "GBP",
            mortgage_type: "repayment"
          })
        })
      });
    });
  });

  it("shows saved-scenarios local device warning", () => {
    const { container } = render(
      <MemoryRouter>
        <StressTestPage />
      </MemoryRouter>
    );
    const ui = within(container);

    expect(ui.getByText("Saved only on this device.")).toBeInTheDocument();
    expect(ui.getByText(/Premium unlock required to split essentials/i)).toBeInTheDocument();
  });
});
