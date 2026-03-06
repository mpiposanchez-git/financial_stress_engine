type AssumptionsPanelProps = {
  horizonMonths?: number;
  monteCarloSimulationCap: number;
  premiumUnlocked: boolean;
  dataTimestamp?: string;
};

export function AssumptionsPanel({
  horizonMonths,
  monteCarloSimulationCap,
  premiumUnlocked,
  dataTimestamp = "Not provided"
}: AssumptionsPanelProps) {
  const horizonDisplay = typeof horizonMonths === "number" ? `${horizonMonths} months` : "Not provided";

  return (
    <section className="result-card" aria-labelledby="assumptions-heading">
      <h2 id="assumptions-heading">Assumptions and limits</h2>
      <ul className="assumptions-list">
        <li>Model horizon: {horizonDisplay}</li>
        <li>Monetary precision: integer pence outputs and display formatting for readability.</li>
        <li>Rate precision: stress/rate inputs represented using bps-compatible assumptions.</li>
        <li>Rounding policy: round half up for deterministic reporting values.</li>
        <li>
          Monte Carlo cap: {monteCarloSimulationCap.toLocaleString()} simulations per run
          {premiumUnlocked ? " (premium unlocked)." : " (locked unless premium)."}
        </li>
        <li>Data timestamp placeholder: {dataTimestamp}</li>
      </ul>
    </section>
  );
}
