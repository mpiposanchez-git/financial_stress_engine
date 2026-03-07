import { render, screen, within } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { FanChart } from "./FanChart";

describe("FanChart", () => {
  it("renders summary percentile headings and values", () => {
    render(
      <FanChart
        data={{
          n_sims: 1000,
          horizon_months: 24,
          seed: 42,
          runtime_ms: 10.5,
          runway_months_p10: 5.5,
          runway_months_p50: 8.5,
          runway_months_p90: 12.5,
          min_savings_p10_pence: 10000,
          min_savings_p50_pence: 20000,
          min_savings_p90_pence: 35000,
          month_of_depletion_p10: 7,
          month_of_depletion_p50: 11,
          month_of_depletion_p90: 17,
          metrics: {
            runway_months: { p10: 5.5, p50: 8.5, p90: 12.5 },
            min_savings: {
              p10_pence: 10000,
              p10_formatted: "GBP 100.00",
              p50_pence: 20000,
              p50_formatted: "GBP 200.00",
              p90_pence: 35000,
              p90_formatted: "GBP 350.00"
            },
            month_of_depletion: { p10: 7, p50: 11, p90: 17 }
          }
        }}
      />
    );

    expect(screen.getByRole("heading", { name: "Fan chart" })).toBeInTheDocument();
    expect(screen.getByText("Summary percentiles")).toBeInTheDocument();

    const table = screen.getByRole("table", { name: "Monte Carlo summary percentiles" });
    const ui = within(table);
    expect(ui.getByRole("columnheader", { name: "P10" })).toBeInTheDocument();
    expect(ui.getByRole("columnheader", { name: "P50" })).toBeInTheDocument();
    expect(ui.getByRole("columnheader", { name: "P90" })).toBeInTheDocument();
    expect(ui.getByRole("cell", { name: "8.5" })).toBeInTheDocument();
    expect(ui.getByRole("cell", { name: "20000" })).toBeInTheDocument();

    expect(screen.getByLabelText("Fan chart placeholder bands")).toBeInTheDocument();
  });
});
