import { useEffect, useMemo, useState } from "react";
import { useLocation } from "react-router-dom";

import { createApiClient } from "../api/client";
import { useAuthState } from "../auth/useAuthState";
import { AssumptionsPanel } from "../components/AssumptionsPanel";
import { EmergencyFundCard } from "../components/EmergencyFundCard";
import { ExplainResult } from "../components/ExplainResult";
import { FanChart } from "../components/charts/FanChart";
import { SavingsPathChart } from "../components/charts/SavingsPathChart";
import { TornadoChart } from "../components/charts/TornadoChart";
import { MortgageStressPanel } from "../components/MortgageStressPanel";
import { OfficialResources } from "../components/OfficialResources";
import { ScenarioCompareTable } from "../components/scenarios/ScenarioCompareTable";
import { SensitivityDriverImpact, ResultsRouteState } from "../types";

export function ResultsPage() {
  const location = useLocation();
  const state = location.state as ResultsRouteState | null;
  const inputParameters = state?.inputParameters;
  const hasMonteCarlo = Boolean(state?.montecarlo);
  const premiumUnlocked = Boolean(state?.premiumUnlocked);
  const { getToken } = useAuthState();
  const [sensitivityImpacts, setSensitivityImpacts] = useState<SensitivityDriverImpact[] | null>(null);
  const [sensitivityLoading, setSensitivityLoading] = useState(false);
  const [sensitivityError, setSensitivityError] = useState<string | null>(null);

  const api = useMemo(() => {
    const baseUrl = import.meta.env.VITE_API_BASE_URL as string;
    return createApiClient(baseUrl, getToken);
  }, [getToken]);

  useEffect(() => {
    let cancelled = false;

    if (!premiumUnlocked || !inputParameters) {
      setSensitivityImpacts(null);
      setSensitivityLoading(false);
      setSensitivityError(null);
      return () => {
        cancelled = true;
      };
    }

    const loadSensitivity = async () => {
      setSensitivityLoading(true);
      setSensitivityError(null);
      try {
        const response = await api.runSensitivity({
          input_parameters: inputParameters,
          horizon_months: state.montecarlo?.horizon_months ?? 24,
          delta_bps: 100
        });
        if (!cancelled) {
          setSensitivityImpacts(response.impacts);
        }
      } catch (error) {
        if (!cancelled) {
          setSensitivityError(error instanceof Error ? error.message : "Sensitivity request failed");
        }
      } finally {
        if (!cancelled) {
          setSensitivityLoading(false);
        }
      }
    };

    void loadSensitivity();
    return () => {
      cancelled = true;
    };
  }, [api, premiumUnlocked, inputParameters, state?.montecarlo?.horizon_months]);

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
    <main className="page-shell">
      <h1>Results</h1>
      <p>Illustrative simulation results only; not financial advice.</p>
      <section className="summary-grid">
        <article className="result-card">
          <h2>Deterministic</h2>
          <p>Runway months: {state.deterministic.runway_months ?? "Solvent"}</p>
          <p>
            Minimum savings: {state.deterministic.min_savings_formatted} ({state.deterministic.min_savings_pence} pence)
          </p>
        </article>
        {hasMonteCarlo ? (
          <article className="result-card">
            <h2>Monte Carlo</h2>
            <p>Simulations: {state.montecarlo?.n_sims}</p>
            <p>Runtime: {state.montecarlo?.runtime_ms.toFixed(2)} ms</p>
            <p>
              Min savings p50: {state.montecarlo?.metrics.min_savings.p50_formatted} ({state.montecarlo?.metrics.min_savings.p50_pence} pence)
            </p>
            <p>Month of depletion p50: {state.montecarlo?.metrics.month_of_depletion.p50}</p>
          </article>
        ) : (
          <article className="result-card">
            <h2>Monte Carlo</h2>
            <p>Monte Carlo results unavailable for this run.</p>
          </article>
        )}
      </section>

      {state.compare ? (
        premiumUnlocked ? (
          <ScenarioCompareTable scenarios={state.compare.scenarios} />
        ) : (
          <section className="result-card" aria-label="Scenario comparison locked">
            <h2>Scenario comparison</h2>
            <p>Premium unlock required to view side-by-side scenario comparison.</p>
          </section>
        )
      ) : null}

      {hasMonteCarlo ? (
        premiumUnlocked ? (
          <FanChart data={state.montecarlo!} />
        ) : (
          <section className="result-card" aria-label="Fan chart locked">
            <h2>Fan chart</h2>
            <p>Premium unlock required to view summary percentile fan chart.</p>
          </section>
        )
      ) : null}

      {premiumUnlocked ? (
        inputParameters ? (
          sensitivityLoading ? (
            <section className="result-card" aria-label="Sensitivity loading">
              <h2>Tornado sensitivity chart</h2>
              <p>Loading sensitivity analysis...</p>
            </section>
          ) : sensitivityError ? (
            <section className="result-card" aria-label="Sensitivity error">
              <h2>Tornado sensitivity chart</h2>
              <p>{sensitivityError}</p>
            </section>
          ) : sensitivityImpacts && sensitivityImpacts.length > 0 ? (
            <TornadoChart impacts={sensitivityImpacts} />
          ) : null
        ) : (
          <section className="result-card" aria-label="Sensitivity unavailable">
            <h2>Tornado sensitivity chart</h2>
            <p>Sensitivity input unavailable for this run.</p>
          </section>
        )
      ) : (
        <section className="result-card" aria-label="Tornado chart locked">
          <h2>Tornado sensitivity chart</h2>
          <p>Premium unlock required to view tornado sensitivity chart.</p>
        </section>
      )}

      <SavingsPathChart
        values={state.deterministic.savings_path_pence}
        formattedValues={state.deterministic.savings_path_formatted}
      />

      <MortgageStressPanel
        currentPaymentPence={state.deterministic.mortgage_payment_current_pence}
        currentPaymentFormatted={state.deterministic.mortgage_payment_current_formatted}
        stressPaymentPence={state.deterministic.mortgage_payment_stress_pence}
        stressPaymentFormatted={state.deterministic.mortgage_payment_stress_formatted}
      />

      <EmergencyFundCard
        minSavingsPence={state.deterministic.min_savings_pence}
        monthlyEssentialsSpendPence={state.deterministic.monthly_cashflow_base_pence < 0 ? 0 : state.deterministic.monthly_cashflow_base_pence}
      />

      <ExplainResult
        runwayMonths={state.deterministic.runway_months}
        minSavingsFormatted={state.deterministic.min_savings_formatted}
        cashflowBaseFormatted={state.deterministic.monthly_cashflow_base_formatted}
        cashflowStressFormatted={state.deterministic.monthly_cashflow_stress_formatted}
        hasMonteCarlo={hasMonteCarlo}
      />

      <AssumptionsPanel
        horizonMonths={state.montecarlo?.horizon_months}
        monteCarloSimulationCap={1000}
        premiumUnlocked={false}
        dataTimestamp="Not provided"
      />

      <OfficialResources />

      {state.deterministic.warnings.length > 0 ? (
        <section className="result-card">
          <h2>Warnings</h2>
          {state.deterministic.warnings.map((warning) => (
            <p key={warning}>{warning}</p>
          ))}
        </section>
      ) : null}
    </main>
  );
}
