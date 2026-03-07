import { render, screen, within } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { SavingsPathChart } from "./SavingsPathChart";

describe("SavingsPathChart", () => {
  it("renders figcaption and summary text", () => {
    render(
      <SavingsPathChart values={[123456, 120000, 118000]} formattedValues={["£1,234.56", "£1,200.00", "£1,180.00"]} />
    );

    expect(screen.getByText("Low point: 118000 pence | High point: 123456 pence")).toBeInTheDocument();
    expect(
      screen.getByText("Summary: starts at 123456 pence, ends at 118000 pence, and ranges between 118000 and 123456 pence.")
    ).toBeInTheDocument();
  });

  it("renders an accessible month-by-month table", () => {
    const { container } = render(<SavingsPathChart values={[1000, 900]} formattedValues={["£10.00", "£9.00"]} />);
    const ui = within(container);

    expect(ui.getByRole("table", { name: "Deterministic savings path table" })).toBeInTheDocument();
    expect(ui.getByRole("columnheader", { name: "Month" })).toBeInTheDocument();
    expect(ui.getByText("£9.00")).toBeInTheDocument();
  });
});
