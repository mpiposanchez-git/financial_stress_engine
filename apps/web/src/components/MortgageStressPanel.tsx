type MortgageStressPanelProps = {
  currentPaymentPence: number;
  currentPaymentFormatted: string;
  stressPaymentPence: number;
  stressPaymentFormatted: string;
};

function formatDeltaPence(value: number): string {
  const sign = value >= 0 ? "+" : "-";
  return `${sign}${Math.abs(value)}p`;
}

export function MortgageStressPanel({
  currentPaymentPence,
  currentPaymentFormatted,
  stressPaymentPence,
  stressPaymentFormatted
}: MortgageStressPanelProps) {
  const deltaPence = stressPaymentPence - currentPaymentPence;
  const direction = deltaPence > 0 ? "higher" : deltaPence < 0 ? "lower" : "unchanged";

  return (
    <section className="result-card" aria-labelledby="mortgage-stress-heading">
      <h2 id="mortgage-stress-heading">Mortgage stress impact</h2>
      <p>
        Current monthly payment: {currentPaymentFormatted} ({currentPaymentPence} pence)
      </p>
      <p>
        Stressed monthly payment: {stressPaymentFormatted} ({stressPaymentPence} pence)
      </p>
      <p>
        Delta under stress: {formatDeltaPence(deltaPence)} ({direction} than current).
      </p>
      <p className="chart-summary">
        This comparison shows how monthly mortgage cash outflow changes under the selected stress assumptions. It is a
        descriptive model output and not a recommendation.
      </p>
    </section>
  );
}
