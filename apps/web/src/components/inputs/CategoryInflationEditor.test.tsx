import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { CategoryInflationEditor } from "./CategoryInflationEditor";

describe("CategoryInflationEditor", () => {
  it("renders locked teaser when premium is unavailable", () => {
    render(
      <CategoryInflationEditor
        premiumUnlocked={false}
        enabled={false}
        value={{}}
        onEnabledChange={vi.fn()}
        onChange={vi.fn()}
      />
    );

    expect(screen.getByRole("heading", { name: "Category inflation (Premium)" })).toBeInTheDocument();
    expect(screen.getByText(/Premium unlock required to split essentials/i)).toBeInTheDocument();
    expect(screen.queryByLabelText("Use category inflation")).not.toBeInTheDocument();
  });

  it("renders category inputs when enabled and emits changes", () => {
    const onEnabledChange = vi.fn();
    const onChange = vi.fn();

    render(
      <CategoryInflationEditor
        premiumUnlocked={true}
        enabled={true}
        value={{
          food: { monthly_spend_gbp: 100, inflation_bps: 500 },
          energy: { monthly_spend_gbp: 50, inflation_bps: 800 },
          housing: { monthly_spend_gbp: 400, inflation_bps: 200 },
          transport: { monthly_spend_gbp: 120, inflation_bps: 300 }
        }}
        onEnabledChange={onEnabledChange}
        onChange={onChange}
      />
    );

    fireEvent.change(screen.getByLabelText("Food monthly spend (GBP)"), {
      target: { value: "130" }
    });
    expect(onChange).toHaveBeenCalled();

    fireEvent.change(screen.getByLabelText("Energy inflation (bps)"), {
      target: { value: "950" }
    });
    expect(onChange).toHaveBeenCalledTimes(2);

    fireEvent.click(screen.getByLabelText("Use category inflation"));
    expect(onEnabledChange).toHaveBeenCalledWith(false);
  });
});
