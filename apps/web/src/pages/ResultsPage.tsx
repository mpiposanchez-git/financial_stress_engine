import { useLocation } from "react-router-dom";

import { ResultsRouteState } from "../types";

export function ResultsPage() {
  const location = useLocation();
  const state = location.state as ResultsRouteState | null;

  if (!state) {
    return (
      <main>
        <h1>Results</h1>
        <p>Illustrative simulation results only; not financial advice.</p>
        <p>No results yet.</p>
      </main>
    );
  }

  return (
    <main>
      <h1>Results</h1>
      <p>Illustrative simulation results only; not financial advice.</p>
      <h2>Deterministic</h2>
      <p>Runway months: {state.deterministic.runway_months ?? "Solvent"}</p>
      <p>
        Minimum savings: {state.deterministic.min_savings_formatted} ({state.deterministic.min_savings_pence} pence)
      </p>

      <h2>Monte Carlo</h2>
      <p>Runway p50: {state.montecarlo.metrics.runway_months.p50} months</p>
      <p>
        Min savings p50: {state.montecarlo.metrics.min_savings.p50_formatted} ({state.montecarlo.metrics.min_savings.p50_pence} pence)
      </p>
      <p>
        Month of depletion p50: {state.montecarlo.metrics.month_of_depletion.p50}
      </p>
    </main>
  );
}
