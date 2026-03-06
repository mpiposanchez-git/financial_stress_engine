import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { ScenarioTabs } from "./ScenarioTabs";

describe("ScenarioTabs", () => {
  it("allows selecting and cloning premium scenarios", () => {
    const onSelect = vi.fn();
    const onCloneFromBase = vi.fn();

    render(
      <ScenarioTabs
        activeScenario="a"
        premiumUnlocked={true}
        scenarioHasDraft={{ base: true, a: false, b: false, c: false }}
        onSelect={onSelect}
        onCloneFromBase={onCloneFromBase}
      />
    );

    fireEvent.click(screen.getByRole("tab", { name: "B" }));
    expect(onSelect).toHaveBeenCalledWith("b");

    fireEvent.click(screen.getByRole("button", { name: "Clone Base into A" }));
    expect(onCloneFromBase).toHaveBeenCalledWith("a");
  });

  it("disables non-base tabs when premium is locked", () => {
    render(
      <ScenarioTabs
        activeScenario="base"
        premiumUnlocked={false}
        scenarioHasDraft={{ base: true, a: false, b: false, c: false }}
        onSelect={vi.fn()}
        onCloneFromBase={vi.fn()}
      />
    );

    expect(screen.getByRole("tab", { name: "A (Premium)" })).toBeDisabled();
    expect(screen.getByText("Premium unlock required for scenarios A/B/C.")).toBeInTheDocument();
  });
});
