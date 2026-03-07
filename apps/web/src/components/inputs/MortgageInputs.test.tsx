import { fireEvent, render, within } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { MortgageInputs } from "./MortgageInputs";

describe("MortgageInputs", () => {
  it("renders mortgage fields", () => {
    const { container } = render(
      <MortgageInputs
        balance={250000}
        balanceCurrency="GBP"
        mortgageType="repayment"
        termYearsRemaining={25}
        currentRatePercent={4.5}
        stressRatePercent={6}
        onBalanceChange={vi.fn()}
        onBalanceCurrencyChange={vi.fn()}
        onMortgageTypeChange={vi.fn()}
        onTermYearsRemainingChange={vi.fn()}
        onCurrentRatePercentChange={vi.fn()}
        onStressRatePercentChange={vi.fn()}
      />
    );
    const ui = within(container);

    expect(ui.getByLabelText("Mortgage balance amount")).toBeInTheDocument();
    expect(ui.getByRole("combobox", { name: "Mortgage type" })).toBeInTheDocument();
    expect(ui.getByLabelText("Mortgage term remaining (years)")).toBeInTheDocument();
    expect(ui.getByLabelText("Current mortgage rate (%)")).toBeInTheDocument();
    expect(ui.getByLabelText("Stressed mortgage rate (%)")).toBeInTheDocument();
  });

  it("shows validation messages for missing term and negative rates", () => {
    const onTermYearsRemainingChange = vi.fn();
    const onCurrentRatePercentChange = vi.fn();
    const onStressRatePercentChange = vi.fn();

    const { container } = render(
      <MortgageInputs
        balance={150000}
        balanceCurrency="GBP"
        mortgageType="repayment"
        termYearsRemaining={0}
        currentRatePercent={-0.2}
        stressRatePercent={-1}
        onBalanceChange={vi.fn()}
        onBalanceCurrencyChange={vi.fn()}
        onMortgageTypeChange={vi.fn()}
        onTermYearsRemainingChange={onTermYearsRemainingChange}
        onCurrentRatePercentChange={onCurrentRatePercentChange}
        onStressRatePercentChange={onStressRatePercentChange}
      />
    );
    const ui = within(container);

    expect(ui.getByText("Term is required when mortgage balance is above zero.")).toBeInTheDocument();
    expect(ui.getByText("Current mortgage rate must be 0% or higher.")).toBeInTheDocument();
    expect(ui.getByText("Stressed mortgage rate must be 0% or higher.")).toBeInTheDocument();

    fireEvent.change(ui.getByLabelText("Mortgage term remaining (years)"), { target: { value: "20" } });
    fireEvent.change(ui.getByLabelText("Current mortgage rate (%)"), { target: { value: "2.1" } });
    fireEvent.change(ui.getByLabelText("Stressed mortgage rate (%)"), { target: { value: "5.2" } });

    expect(onTermYearsRemainingChange).toHaveBeenCalledWith(20);
    expect(onCurrentRatePercentChange).toHaveBeenCalledWith(2.1);
    expect(onStressRatePercentChange).toHaveBeenCalledWith(5.2);
  });
});
