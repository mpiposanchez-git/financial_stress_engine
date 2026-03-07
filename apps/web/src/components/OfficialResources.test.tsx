import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { OfficialResources } from "./OfficialResources";

describe("OfficialResources", () => {
  it("renders MoneyHelper and Citizens Advice links with information-only disclaimer", () => {
    render(<OfficialResources />);

    expect(screen.getByRole("heading", { name: "Official resources" })).toBeInTheDocument();
    expect(screen.getByText(/Information only: these links provide general guidance/)).toBeInTheDocument();

    const moneyHelperLink = screen.getByRole("link", { name: "MoneyHelper" });
    const citizensAdviceLink = screen.getByRole("link", { name: "Citizens Advice" });

    expect(moneyHelperLink).toHaveAttribute("href", "https://www.moneyhelper.org.uk/");
    expect(citizensAdviceLink).toHaveAttribute("href", "https://www.citizensadvice.org.uk/");
  });
});
