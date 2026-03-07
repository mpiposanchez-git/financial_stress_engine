import { render, screen, within } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { ScenarioCompareTable } from "./ScenarioCompareTable";

describe("ScenarioCompareTable", () => {
  it("renders comparison headers and scenario rows", () => {
    render(
      <ScenarioCompareTable
        scenarios={[
          {
            name: "Base",
            reporting_currency: "GBP",
            runway_months: 10.25,
            month_of_depletion: 14,
            min_savings_pence: 120000,
            min_savings_formatted: "GBP 1,200.00",
            monthly_cashflow_stress_pence: -20000,
            monthly_cashflow_stress_formatted: "GBP -200.00",
            mortgage_payment_stress_pence: 150000,
            mortgage_payment_stress_formatted: "GBP 1,500.00",
            warnings: []
          },
          {
            name: "A",
            reporting_currency: "GBP",
            runway_months: null,
            month_of_depletion: null,
            min_savings_pence: 450000,
            min_savings_formatted: "GBP 4,500.00",
            monthly_cashflow_stress_pence: 5000,
            monthly_cashflow_stress_formatted: "GBP 50.00",
            mortgage_payment_stress_pence: 130000,
            mortgage_payment_stress_formatted: "GBP 1,300.00",
            warnings: ["Illustrative only"]
          }
        ]}
      />
    );

    const table = screen.getByRole("table", { name: "Scenario comparison table" });
    const ui = within(table);

    expect(ui.getByRole("columnheader", { name: "Scenario" })).toBeInTheDocument();
    expect(ui.getByRole("columnheader", { name: "Runway (months)" })).toBeInTheDocument();
    expect(ui.getByRole("columnheader", { name: "Depletion month" })).toBeInTheDocument();
    expect(ui.getByRole("columnheader", { name: "Min savings" })).toBeInTheDocument();
    expect(ui.getByRole("columnheader", { name: "Stressed cashflow" })).toBeInTheDocument();
    expect(ui.getByRole("columnheader", { name: "Stressed mortgage payment" })).toBeInTheDocument();

    expect(ui.getByRole("cell", { name: "Base" })).toBeInTheDocument();
    expect(ui.getByRole("cell", { name: "10.3" })).toBeInTheDocument();
    expect(ui.getByRole("cell", { name: "14" })).toBeInTheDocument();
    expect(ui.getByRole("cell", { name: "GBP 1,200.00 (120000 pence)" })).toBeInTheDocument();

    expect(ui.getByRole("cell", { name: "A" })).toBeInTheDocument();
    expect(ui.getByRole("cell", { name: "Solvent" })).toBeInTheDocument();
    expect(ui.getByRole("cell", { name: "Not depleted" })).toBeInTheDocument();
  });
});
