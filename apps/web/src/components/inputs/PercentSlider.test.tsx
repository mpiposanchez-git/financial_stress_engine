import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { PercentSlider } from "./PercentSlider";

describe("PercentSlider", () => {
  it("shows percent and bps display for percent values", () => {
    render(
      <PercentSlider
        id="income-shock"
        label="Income shock"
        value={10}
        min={0}
        max={50}
        onChange={vi.fn()}
      />
    );

    expect(screen.getByText("10.00% (1000 bps)")).toBeInTheDocument();
  });

  it("shows percent and bps display for bps values", () => {
    render(
      <PercentSlider
        id="fx-stress-eur-slider"
        label="FX stress EUR"
        value={125}
        min={-500}
        max={500}
        valueKind="bps"
        onChange={vi.fn()}
      />
    );

    expect(screen.getByText("1.25% (125 bps)")).toBeInTheDocument();
  });

  it("emits slider value changes", () => {
    const onChange = vi.fn();

    render(
      <PercentSlider
        id="inflation-shock"
        label="Inflation shock"
        value={5}
        min={0}
        max={25}
        onChange={onChange}
      />
    );

    fireEvent.change(screen.getByRole("slider", { name: "Inflation shock" }), { target: { value: "7.5" } });

    expect(onChange).toHaveBeenCalledWith(7.5);
  });
});
