import { render, screen, within } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { TornadoChart } from "./TornadoChart";

describe("TornadoChart", () => {
  it("renders ranked bars and summary text", () => {
    render(
      <TornadoChart
        impacts={[
          {
            driver: "mortgage_rate_stress_bps",
            delta_bps: 100,
            base_runway_months: 10.2,
            perturbed_runway_months: 9.4,
            runway_months_impact: -0.8,
            base_min_savings_pence: 250000,
            perturbed_min_savings_pence: 190000,
            min_savings_impact_pence: -60000
          },
          {
            driver: "income_shock_bps",
            delta_bps: 100,
            base_runway_months: 10.2,
            perturbed_runway_months: 9.9,
            runway_months_impact: -0.3,
            base_min_savings_pence: 250000,
            perturbed_min_savings_pence: 220000,
            min_savings_impact_pence: -30000
          }
        ]}
      />
    );

    expect(screen.getByRole("heading", { name: "Tornado sensitivity chart" })).toBeInTheDocument();
    expect(screen.getByLabelText("Ranked sensitivity bars")).toBeInTheDocument();
    expect(screen.getByText("Mortgage Rate Stress")).toBeInTheDocument();
    expect(screen.getByText("Income Shock")).toBeInTheDocument();
    expect(screen.getByText("Top sensitivity driver: Mortgage Rate Stress (-60000p impact on minimum savings)."))
      .toBeInTheDocument();

    const list = screen.getByRole("list");
    const ui = within(list);
    expect(ui.getAllByRole("listitem")).toHaveLength(2);
  });
});
