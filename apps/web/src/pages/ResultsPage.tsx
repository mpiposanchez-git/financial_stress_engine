import { useEffect, useMemo, useState } from "react";
import { useLocation } from "react-router-dom";

import { createApiClient } from "../api/client";
import { useAuthState } from "../auth/useAuthState";
import { AssumptionsPanel } from "../components/AssumptionsPanel";
import { UKContextBox } from "../components/benchmarks/UKContextBox";
import { UKRankingCard } from "../components/benchmarks/UKRankingCard";
import { EmergencyFundCard } from "../components/EmergencyFundCard";
import { ExplainResult } from "../components/ExplainResult";
import { FanChart } from "../components/charts/FanChart";
import { SavingsPathChart } from "../components/charts/SavingsPathChart";
import { TornadoChart } from "../components/charts/TornadoChart";
import { MortgageStressPanel } from "../components/MortgageStressPanel";
import { OfficialResources } from "../components/OfficialResources";
import { PdfDownloadButton } from "../components/PdfDownloadButton";
import { ScenarioCompareTable } from "../components/scenarios/ScenarioCompareTable";
import { buildExportBundle, downloadJsonBundle, formatJsonExportFilename } from "../lib/exportJson";
import { ResultsRouteState, SensitivityDriverImpact, UkPercentileResponse, UkReferenceValuesResponse } from "../types";

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
  const [ukReference, setUkReference] = useState<UkReferenceValuesResponse | null>(null);
  const [ukReferenceLoading, setUkReferenceLoading] = useState(false);
  const [ukReferenceError, setUkReferenceError] = useState<string | null>(null);
  const [ukRanking, setUkRanking] = useState<UkPercentileResponse | null>(null);
  const [ukRankingLoading, setUkRankingLoading] = useState(false);
  const [ukRankingError, setUkRankingError] = useState<string | null>(null);
  const [pdfLoading, setPdfLoading] = useState(false);
  const [pdfError, setPdfError] = useState<string | null>(null);

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

  useEffect(() => {
    let cancelled = false;

    const loadReference = async () => {
      setUkReferenceLoading(true);
      setUkReferenceError(null);
      try {
        const response = await api.getUkReferenceValues();
        if (!cancelled) {
          setUkReference(response);
        }
      } catch (error) {
        if (!cancelled) {
          setUkReferenceError(error instanceof Error ? error.message : "UK reference request failed");
        }
      } finally {
        if (!cancelled) {
          setUkReferenceLoading(false);
        }
      }
    };

    void loadReference();
    return () => {
      cancelled = true;
    };
  }, [api]);

  useEffect(() => {
    let cancelled = false;

    if (!premiumUnlocked || !inputParameters) {
      setUkRanking(null);
      setUkRankingLoading(false);
      setUkRankingError(null);
      return () => {
        cancelled = true;
      };
    }

    const loadRanking = async () => {
      setUkRankingLoading(true);
      setUkRankingError(null);
      try {
        const response = await api.getUkPercentile({
          annual_net_income_reporting_currency: inputParameters.household_monthly_net_income_gbp * 12,
          reporting_currency: inputParameters.reporting_currency,
        });
        if (!cancelled) {
          setUkRanking(response);
        }
      } catch (error) {
        if (!cancelled) {
          setUkRankingError(error instanceof Error ? error.message : "UK percentile request failed");
        }
      } finally {
        if (!cancelled) {
          setUkRankingLoading(false);
        }
      }
    };

    void loadRanking();
    return () => {
      cancelled = true;
    };
  }, [api, premiumUnlocked, inputParameters]);

  if (!state) {
    return (
      <main>
        <h1>Results</h1>
        <p>Illustrative simulation results only; not financial advice.</p>
        <p>No results yet.</p>
      </main>
    );
  }

  const onDownloadPdf = async () => {
    setPdfLoading(true);
    setPdfError(null);
    try {
      const pdfBlob = await api.downloadPdfReport({
        inputs: (inputParameters ?? {}) as Record<string, unknown>,
        outputs: {
          deterministic: state.deterministic,
          montecarlo: state.montecarlo ?? null,
          sensitivity: sensitivityImpacts ?? null,
        },
        disclaimers: ["Educational simulation only.", "Not financial advice."],
        provenance: {
          reference_fetched_at_utc: ukReference?.provenance.fetched_at_utc ?? null,
          reference_source_url: ukReference?.provenance.source_url ?? null,
        },
        app_version: "0.1.1",
      });

      const objectUrl = URL.createObjectURL(pdfBlob);
      const link = document.createElement("a");
      link.href = objectUrl;
      link.download = "stress-report.pdf";
      document.body.appendChild(link);
      link.click();
      link.remove();
      URL.revokeObjectURL(objectUrl);
    } catch (error) {
      setPdfError(error instanceof Error ? error.message : "PDF export failed");
    } finally {
      setPdfLoading(false);
    }
  };

  const onDownloadJson = () => {
    const bundle = buildExportBundle({
      inputParameters,
      deterministic: state.deterministic,
      montecarlo: state.montecarlo,
      sensitivityImpacts,
      premiumUnlocked,
      provenance: {
        data_reference_fetched_at_utc: ukReference?.provenance.fetched_at_utc ?? null,
        data_reference_source_url: ukReference?.provenance.source_url ?? null,
      },
      appVersion: "0.1.1",
      modelVersion: "deterministic-v1",
    });

    const filename = formatJsonExportFilename(state.deterministic.reporting_currency);
    downloadJsonBundle(bundle, filename);
  };

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

      <UKContextBox reference={ukReference} loading={ukReferenceLoading} error={ukReferenceError} />
      {premiumUnlocked ? (
        <UKRankingCard ranking={ukRanking} loading={ukRankingLoading} error={ukRankingError} />
      ) : (
        <section className="result-card" aria-label="UK ranking locked">
          <h2>UK income ranking</h2>
          <p>Premium unlock required to view UK percentile ranking.</p>
        </section>
      )}

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

      <section className="result-card" aria-label="JSON export">
        <h2>JSON export</h2>
        <button type="button" onClick={onDownloadJson}>
          Download JSON bundle
        </button>
      </section>

      {premiumUnlocked ? (
        <PdfDownloadButton onDownload={onDownloadPdf} loading={pdfLoading} />
      ) : (
        <section className="result-card" aria-label="PDF export locked">
          <h2>PDF report export</h2>
          <p>Premium unlock required to download PDF report.</p>
        </section>
      )}

      {pdfError ? (
        <section className="result-card" aria-label="PDF export error">
          <h2>PDF report export</h2>
          <p>{pdfError}</p>
        </section>
      ) : null}

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
