type ScenarioId = "base" | "a" | "b" | "c";

type ScenarioTabsProps = {
  activeScenario: ScenarioId;
  premiumUnlocked: boolean;
  scenarioHasDraft: Record<ScenarioId, boolean>;
  onSelect: (scenario: ScenarioId) => void;
  onCloneFromBase: (scenario: Exclude<ScenarioId, "base">) => void;
};

const scenarioOrder: ScenarioId[] = ["base", "a", "b", "c"];

function toLabel(id: ScenarioId): string {
  return id === "base" ? "Base" : id.toUpperCase();
}

export function ScenarioTabs({
  activeScenario,
  premiumUnlocked,
  scenarioHasDraft,
  onSelect,
  onCloneFromBase
}: ScenarioTabsProps) {
  return (
    <section className="scenario-tabs" aria-label="Scenario tabs">
      <div className="scenario-tab-row" role="tablist" aria-label="Scenario selection">
        {scenarioOrder.map((id) => {
          const locked = id !== "base" && !premiumUnlocked;
          const label = locked ? `${toLabel(id)} (Premium)` : toLabel(id);

          return (
            <button
              key={id}
              type="button"
              role="tab"
              aria-selected={activeScenario === id}
              className={`scenario-tab ${activeScenario === id ? "scenario-tab-active" : ""}`}
              onClick={() => onSelect(id)}
              disabled={locked}
            >
              {label}
            </button>
          );
        })}
      </div>

      {!premiumUnlocked ? <p className="scenario-note">Premium unlock required for scenarios A/B/C.</p> : null}

      {premiumUnlocked && activeScenario !== "base" && !scenarioHasDraft[activeScenario] ? (
        <div className="scenario-clone-card">
          <p>This scenario is empty. Clone Base to start editing.</p>
          <button type="button" onClick={() => onCloneFromBase(activeScenario)}>
            Clone Base into {toLabel(activeScenario)}
          </button>
        </div>
      ) : null}
    </section>
  );
}
