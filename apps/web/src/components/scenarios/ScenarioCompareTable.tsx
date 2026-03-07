import { CompareScenarioResult } from "../../types";

type ScenarioCompareTableProps = {
  scenarios: CompareScenarioResult[];
};

function formatRunway(value: number | null): string {
  if (value === null) {
    return "Solvent";
  }

  return value.toFixed(1);
}

function formatDepletionMonth(value: number | null): string {
  if (value === null) {
    return "Not depleted";
  }

  return `${value}`;
}

export function ScenarioCompareTable({ scenarios }: ScenarioCompareTableProps) {
  return (
    <section className="result-card" aria-labelledby="scenario-compare-heading">
      <h2 id="scenario-compare-heading">Scenario comparison</h2>
      <table className="savings-table" aria-label="Scenario comparison table">
        <thead>
          <tr>
            <th scope="col">Scenario</th>
            <th scope="col">Runway (months)</th>
            <th scope="col">Depletion month</th>
            <th scope="col">Min savings</th>
            <th scope="col">Stressed cashflow</th>
            <th scope="col">Stressed mortgage payment</th>
          </tr>
        </thead>
        <tbody>
          {scenarios.map((scenario) => (
            <tr key={scenario.name}>
              <td>{scenario.name}</td>
              <td>{formatRunway(scenario.runway_months)}</td>
              <td>{formatDepletionMonth(scenario.month_of_depletion)}</td>
              <td>
                {scenario.min_savings_formatted} ({scenario.min_savings_pence} pence)
              </td>
              <td>
                {scenario.monthly_cashflow_stress_formatted} ({scenario.monthly_cashflow_stress_pence} pence)
              </td>
              <td>
                {scenario.mortgage_payment_stress_formatted} ({scenario.mortgage_payment_stress_pence} pence)
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
