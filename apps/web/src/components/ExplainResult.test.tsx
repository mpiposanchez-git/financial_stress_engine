import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { ExplainResult } from "./ExplainResult";

describe("ExplainResult", () => {
  it("renders narrative with key glossary tooltips", () => {
    render(
      <ExplainResult
        runwayMonths={7.25}
        minSavingsFormatted="£1,250.00"
        cashflowBaseFormatted="£1,000.00"
        cashflowStressFormatted="£500.00"
        hasMonteCarlo={true}
      />
    );

    expect(screen.getByRole("heading", { name: "Explain the result" })).toBeInTheDocument();
    expect(screen.getByText("runway")).toHaveAttribute(
      "title",
      "Estimated months until savings are depleted under model assumptions."
    );
    expect(screen.getByText("minimum savings")).toHaveAttribute(
      "title",
      "The lowest savings point reached in the modeled horizon."
    );
    expect(screen.getByText(/Monte Carlo percentile outputs add dispersion context/)).toBeInTheDocument();
  });
});
