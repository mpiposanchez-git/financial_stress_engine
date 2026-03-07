import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { AssumptionsPanel } from "./AssumptionsPanel";

describe("AssumptionsPanel", () => {
  it("renders horizon, precision, rounding, cap lock, and timestamp placeholder", () => {
    render(
      <AssumptionsPanel
        horizonMonths={24}
        monteCarloSimulationCap={1000}
        premiumUnlocked={false}
        dataTimestamp="Not provided"
      />
    );

    expect(screen.getByRole("heading", { name: "Assumptions and limits" })).toBeInTheDocument();
    expect(screen.getByText("Model horizon: 24 months")).toBeInTheDocument();
    expect(screen.getByText(/Monetary precision: integer pence outputs/)).toBeInTheDocument();
    expect(screen.getByText(/Rate precision: stress\/rate inputs represented using bps-compatible assumptions\./)).toBeInTheDocument();
    expect(screen.getByText(/Rounding policy: round half up/)).toBeInTheDocument();
    expect(screen.getByText(/Monte Carlo cap: 1,000 simulations per run \(locked unless premium\)\./)).toBeInTheDocument();
    expect(screen.getByText("Data timestamp placeholder: Not provided")).toBeInTheDocument();
  });
});
