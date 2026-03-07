type EmergencyFundCardProps = {
  minSavingsPence: number;
  monthlyEssentialsSpendPence: number;
  monthlyDebtPaymentsPence?: number;
};

function toMonthsCovered(minSavingsPence: number, monthlyBurnPence: number): number | null {
  if (monthlyBurnPence <= 0) {
    return null;
  }
  return minSavingsPence / monthlyBurnPence;
}

export function EmergencyFundCard({
  minSavingsPence,
  monthlyEssentialsSpendPence,
  monthlyDebtPaymentsPence = 0
}: EmergencyFundCardProps) {
  const baselineMonthlyOutgoings = monthlyEssentialsSpendPence + monthlyDebtPaymentsPence;
  const monthsCovered = toMonthsCovered(minSavingsPence, baselineMonthlyOutgoings);

  return (
    <section className="result-card" aria-labelledby="emergency-fund-heading">
      <h2 id="emergency-fund-heading">Emergency fund adequacy</h2>
      <p>Minimum modeled savings: {minSavingsPence} pence</p>
      <p>Baseline monthly outgoings used: {baselineMonthlyOutgoings} pence</p>
      <p>
        Months of essentials covered: {monthsCovered === null ? "Not defined" : monthsCovered.toFixed(2)}
      </p>
      <p className="chart-summary">
        This ratio estimates how many months baseline outgoings could be covered by the modeled low-point savings level.
      </p>
    </section>
  );
}
