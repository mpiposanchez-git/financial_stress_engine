import { useLocation } from "react-router-dom";

import { PercentileDisclosure } from "../components/benchmarks/PercentileDisclosure";
import { EmergencyFundCard } from "../components/EmergencyFundCard";
import { SavingsPathChart } from "../components/charts/SavingsPathChart";
import { MortgageStressPanel } from "../components/MortgageStressPanel";
import { ResultsRouteState } from "../types";

type PercentileChartProps = {
  title: string;
  p10: number;
  p50: number;
  p90: number;
  formatter?: (value: number) => string;
};

function PercentileChart({ title, p10, p50, p90, formatter }: PercentileChartProps) {
  const min = Math.min(p10, p50, p90);
  const max = Math.max(p10, p50, p90);
  const span = Math.max(max - min, 1);
  const toPercent = (value: number): number => ((value - min) / span) * 100;
  const format = formatter ?? ((value: number) => `${value}`);
  const headingId = `chart-${title.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "")}`;

  return (
    <figure className="result-card" aria-labelledby={headingId}>
      <h3 id={headingId}>{title}</h3>
      <div className="percentile-track" aria-hidden="true">
        <div
          className="percentile-band"
          style={{ left: `${toPercent(p10)}%`, width: `${Math.max(toPercent(p90) - toPercent(p10), 2)}%` }}
        />
        <div className="percentile-marker p10" style={{ left: `${toPercent(p10)}%` }}>
          <span>P10</span>
        </div>
        <div className="percentile-marker p50" style={{ left: `${toPercent(p50)}%` }}>
          <span>P50</span>
        </div>
        <div className="percentile-marker p90" style={{ left: `${toPercent(p90)}%` }}>
          <span>P90</span>
        </div>
      </div>
      <figcaption className="percentile-values">
        P10: {format(p10)} | P50: {format(p50)} | P90: {format(p90)}
      </figcaption>
      <p className="chart-summary">
        Summary: central estimate at P50 is {format(p50)}, with an approximate spread of {format(p10)} to {format(p90)}.
      </p>
    </figure>
  );
}

export function ResultsPage() {
  const location = useLocation();
  const state = location.state as ResultsRouteState | null;
  const hasMonteCarlo = Boolean(state?.montecarlo);

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

      {hasMonteCarlo ? (
        <section className="summary-grid">
          <PercentileDisclosure />
          <PercentileChart
            title="Runway distribution (months)"
            p10={state.montecarlo!.metrics.runway_months.p10}
            p50={state.montecarlo!.metrics.runway_months.p50}
            p90={state.montecarlo!.metrics.runway_months.p90}
            formatter={(value) => `${value.toFixed(1)}m`}
          />
          <PercentileChart
            title="Minimum savings distribution (pence)"
            p10={state.montecarlo!.metrics.min_savings.p10_pence}
            p50={state.montecarlo!.metrics.min_savings.p50_pence}
            p90={state.montecarlo!.metrics.min_savings.p90_pence}
            formatter={(value) => `${Math.round(value)}p`}
          />
          <PercentileChart
            title="Depletion month distribution"
            p10={state.montecarlo!.metrics.month_of_depletion.p10}
            p50={state.montecarlo!.metrics.month_of_depletion.p50}
            p90={state.montecarlo!.metrics.month_of_depletion.p90}
            formatter={(value) => `${value.toFixed(1)}m`}
          />
        </section>
      ) : null}

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
