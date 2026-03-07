import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { EmergencyFundCard } from "./EmergencyFundCard";

describe("EmergencyFundCard", () => {
  it("computes and renders months of essentials covered", () => {
    render(
      <EmergencyFundCard
        minSavingsPence={90000}
        monthlyEssentialsSpendPence={30000}
        monthlyDebtPaymentsPence={5000}
      />
    );

    expect(screen.getByRole("heading", { name: "Emergency fund adequacy" })).toBeInTheDocument();
    expect(screen.getByText("Minimum modeled savings: 90000 pence")).toBeInTheDocument();
    expect(screen.getByText("Baseline monthly outgoings used: 35000 pence")).toBeInTheDocument();
    expect(screen.getByText("Months of essentials covered: 2.57")).toBeInTheDocument();
  });
});
