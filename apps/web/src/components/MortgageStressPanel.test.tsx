import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { MortgageStressPanel } from "./MortgageStressPanel";

describe("MortgageStressPanel", () => {
  it("renders current, stressed, and delta payment with plain-English explanation", () => {
    render(
      <MortgageStressPanel
        currentPaymentPence={120000}
        currentPaymentFormatted="£1,200.00"
        stressPaymentPence={150000}
        stressPaymentFormatted="£1,500.00"
      />
    );

    expect(screen.getByRole("heading", { name: "Mortgage stress impact" })).toBeInTheDocument();
    expect(screen.getByText("Current monthly payment: £1,200.00 (120000 pence)")).toBeInTheDocument();
    expect(screen.getByText("Stressed monthly payment: £1,500.00 (150000 pence)")).toBeInTheDocument();
    expect(screen.getByText("Delta under stress: +30000p (higher than current).")).toBeInTheDocument();
    expect(screen.getByText(/descriptive model output and not a recommendation/i)).toBeInTheDocument();
  });
});
