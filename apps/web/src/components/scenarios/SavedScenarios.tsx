import { useState } from "react";

import { FREE_SCENARIO_LIMIT, SavedScenario } from "../../lib/storage/localScenarioStore";

type SavedScenariosProps = {
  scenarios: SavedScenario[];
  premiumUnlocked: boolean;
  onSave: (name: string) => void;
  onLoad: (scenario: SavedScenario) => void;
  onDelete: (scenarioId: string) => void;
};

export function SavedScenarios({ scenarios, premiumUnlocked, onSave, onLoad, onDelete }: SavedScenariosProps) {
  const [name, setName] = useState("");
  const saveDisabled = !premiumUnlocked && scenarios.length >= FREE_SCENARIO_LIMIT;

  const handleSave = () => {
    const trimmed = name.trim();
    if (!trimmed) {
      return;
    }

    onSave(trimmed);
    setName("");
  };

  return (
    <section className="saved-scenarios result-card" aria-labelledby="saved-scenarios-heading">
      <h2 id="saved-scenarios-heading">Saved scenarios</h2>
      <p className="resources-disclaimer">Saved only on this device.</p>
      <p className="scenario-note">
        {premiumUnlocked
          ? `${scenarios.length} saved`
          : `${scenarios.length}/${FREE_SCENARIO_LIMIT} saved on free plan`}
      </p>
      <div className="saved-scenarios-form">
        <label htmlFor="saved-scenario-name">
          Scenario name
          <input
            id="saved-scenario-name"
            aria-label="Scenario name"
            value={name}
            onChange={(event) => setName(event.target.value)}
            placeholder="e.g. Higher inflation"
          />
        </label>
        <button type="button" onClick={handleSave} disabled={saveDisabled}>
          Save current scenario
        </button>
      </div>
      {saveDisabled ? <p className="field-error">Free plan limit reached. Premium unlocks unlimited saved scenarios.</p> : null}
      {scenarios.length === 0 ? <p>No saved scenarios yet.</p> : null}
      {scenarios.length > 0 ? (
        <ul className="saved-scenario-list">
          {scenarios.map((scenario) => (
            <li key={scenario.id} className="saved-scenario-item">
              <div>
                <strong>{scenario.name}</strong>
                <p className="scenario-note">Saved {new Date(scenario.savedAtIso).toLocaleString()}</p>
              </div>
              <div className="saved-scenario-actions">
                <button type="button" onClick={() => onLoad(scenario)}>
                  Load
                </button>
                <button type="button" onClick={() => onDelete(scenario.id)}>
                  Delete
                </button>
              </div>
            </li>
          ))}
        </ul>
      ) : null}
    </section>
  );
}
