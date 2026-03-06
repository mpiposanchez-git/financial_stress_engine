import { InputParameters } from "../../types";

export const FREE_SCENARIO_LIMIT = 2;
const STORAGE_KEY = "fse.savedScenarios.v1";

export type SavedScenario = {
  id: string;
  name: string;
  savedAtIso: string;
  input: InputParameters;
};

export type SaveScenarioResult =
  | { ok: true; scenarios: SavedScenario[] }
  | { ok: false; reason: "limit"; scenarios: SavedScenario[] };

function cloneInput(input: InputParameters): InputParameters {
  return {
    ...input,
    fx_spot_rates: { ...input.fx_spot_rates },
    fx_stress_bps: { ...input.fx_stress_bps }
  };
}

function isSavedScenario(value: unknown): value is SavedScenario {
  if (!value || typeof value !== "object") {
    return false;
  }

  const candidate = value as Partial<SavedScenario>;
  return (
    typeof candidate.id === "string" &&
    typeof candidate.name === "string" &&
    typeof candidate.savedAtIso === "string" &&
    typeof candidate.input === "object" &&
    candidate.input !== null
  );
}

export function getSavedScenarios(): SavedScenario[] {
  const raw = window.localStorage.getItem(STORAGE_KEY);
  if (!raw) {
    return [];
  }

  try {
    const parsed = JSON.parse(raw) as unknown;
    if (!Array.isArray(parsed)) {
      return [];
    }

    return parsed.filter(isSavedScenario).map((scenario) => ({
      ...scenario,
      input: cloneInput(scenario.input)
    }));
  } catch {
    return [];
  }
}

function persistSavedScenarios(scenarios: SavedScenario[]): void {
  window.localStorage.setItem(STORAGE_KEY, JSON.stringify(scenarios));
}

export function saveScenario(options: {
  name: string;
  input: InputParameters;
  premiumUnlocked: boolean;
}): SaveScenarioResult {
  const existing = getSavedScenarios();
  if (!options.premiumUnlocked && existing.length >= FREE_SCENARIO_LIMIT) {
    return { ok: false, reason: "limit", scenarios: existing };
  }

  const savedScenario: SavedScenario = {
    id: `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
    name: options.name.trim(),
    savedAtIso: new Date().toISOString(),
    input: cloneInput(options.input)
  };

  const updated = [savedScenario, ...existing];
  persistSavedScenarios(updated);
  return { ok: true, scenarios: updated };
}

export function deleteScenario(id: string): SavedScenario[] {
  const updated = getSavedScenarios().filter((scenario) => scenario.id !== id);
  persistSavedScenarios(updated);
  return updated;
}
