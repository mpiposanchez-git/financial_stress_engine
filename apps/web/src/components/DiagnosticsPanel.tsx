import type { InputParameters } from "../types";

type DiagnosticSeverity = "warning" | "error";

type DiagnosticItem = {
  id: string;
  severity: DiagnosticSeverity;
  message: string;
  whyThisMatters: string;
};

type DiagnosticsPanelProps = {
  input: InputParameters;
};

export function buildDiagnostics(input: InputParameters): DiagnosticItem[] {
  const items: DiagnosticItem[] = [];

  if (input.household_monthly_essential_spend_gbp > input.household_monthly_net_income_gbp) {
    items.push({
      id: "essentials-over-income",
      severity: "warning",
      message: "Essentials spending is above net income.",
      whyThisMatters: "A persistent monthly shortfall can reduce savings runway faster under stress."
    });
  }

  const monthlyBalance =
    input.household_monthly_net_income_gbp -
    input.household_monthly_essential_spend_gbp -
    input.household_monthly_debt_payments_gbp;
  if (input.cash_savings_gbp === 0 && monthlyBalance < 0) {
    items.push({
      id: "zero-savings-deficit",
      severity: "warning",
      message: "Savings are zero while monthly balance is negative.",
      whyThisMatters: "A deficit with no buffer can make outcomes highly sensitive to even small shocks."
    });
  }

  const reportingSpot = input.fx_spot_rates[input.reporting_currency];
  if (reportingSpot !== 1) {
    items.push({
      id: "reporting-fx-not-one",
      severity: "error",
      message: `FX spot for reporting currency (${input.reporting_currency}) must be 1.0.`,
      whyThisMatters: "Reporting-currency conversion anchors all amounts and should stay fixed at 1.0."
    });
  }

  return items;
}

export function DiagnosticsPanel({ input }: DiagnosticsPanelProps) {
  const diagnostics = buildDiagnostics(input);

  return (
    <section className="diagnostics-panel" aria-live="polite" aria-label="Input diagnostics">
      <h2>Input diagnostics</h2>
      {diagnostics.length === 0 ? (
        <p>No diagnostics detected.</p>
      ) : (
        <ul className="diagnostics-list">
          {diagnostics.map((item) => (
            <li key={item.id} className={`diagnostic-item diagnostic-${item.severity}`}>
              <strong>{item.severity === "error" ? "Error" : "Warning"}:</strong> {item.message}{" "}
              <abbr className="diagnostic-help" title={item.whyThisMatters}>
                Why this matters
              </abbr>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
