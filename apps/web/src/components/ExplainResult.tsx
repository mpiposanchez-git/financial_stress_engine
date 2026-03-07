import { GlossaryTooltip } from "./GlossaryTooltip";

type ExplainResultProps = {
  runwayMonths: number | null;
  minSavingsFormatted: string;
  cashflowBaseFormatted: string;
  cashflowStressFormatted: string;
  hasMonteCarlo: boolean;
};

export function ExplainResult({
  runwayMonths,
  minSavingsFormatted,
  cashflowBaseFormatted,
  cashflowStressFormatted,
  hasMonteCarlo
}: ExplainResultProps) {
  const runwayText = runwayMonths === null ? "no modeled depletion within the horizon" : `${runwayMonths.toFixed(1)} months`;

  return (
    <section className="result-card" aria-labelledby="explain-result-heading">
      <h2 id="explain-result-heading">Explain the result</h2>
      <p>
        The modeled <GlossaryTooltip term="runway" definition="Estimated months until savings are depleted under model assumptions." />
        {" "}is {runwayText}, driven by the gap between baseline cashflow ({cashflowBaseFormatted}) and stressed cashflow ({cashflowStressFormatted}).
      </p>
      <p>
        The lowest modeled savings level is {minSavingsFormatted}, which provides context for the
        {" "}<GlossaryTooltip term="minimum savings" definition="The lowest savings point reached in the modeled horizon." /> value.
      </p>
      <p>
        {hasMonteCarlo
          ? "Monte Carlo percentile outputs add dispersion context around the deterministic path."
          : "Monte Carlo distribution context is unavailable for this run, so interpretation uses deterministic outputs only."}
      </p>
    </section>
  );
}
