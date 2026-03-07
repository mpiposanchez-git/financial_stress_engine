import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { MoneyInput } from "./MoneyInput";

describe("MoneyInput", () => {
  it("renders amount and currency controls with accessibility descriptors", () => {
    const onAmountChange = vi.fn();
    const onCurrencyChange = vi.fn();

    render(
      <MoneyInput
        idPrefix="income"
        label="Income"
        amount={4000}
        currency="GBP"
        onAmountChange={onAmountChange}
        onCurrencyChange={onCurrencyChange}
        ariaDescribedBy="form-error"
      />
    );

    expect(screen.getByLabelText("Income amount")).toHaveAttribute("aria-describedby", "form-error");
    expect(screen.getByRole("combobox", { name: "Income currency" })).toHaveAttribute(
      "aria-describedby",
      "form-error"
    );
  });

  it("emits value updates for amount and currency", () => {
    const onAmountChange = vi.fn();
    const onCurrencyChange = vi.fn();

    render(
      <MoneyInput
        idPrefix="essentials"
        label="Essentials"
        amount={1500}
        currency="GBP"
        onAmountChange={onAmountChange}
        onCurrencyChange={onCurrencyChange}
      />
    );

    fireEvent.change(screen.getByLabelText("Essentials amount"), { target: { value: "1800" } });
    fireEvent.change(screen.getByRole("combobox", { name: "Essentials currency" }), { target: { value: "EUR" } });

    expect(onAmountChange).toHaveBeenCalledWith(1800);
    expect(onCurrencyChange).toHaveBeenCalledWith("EUR");
  });
});
