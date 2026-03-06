import { SensitivityDriverImpact } from "../../types";

type TornadoChartProps = {
  impacts: SensitivityDriverImpact[];
};

function prettyDriverName(driver: string): string {
  return driver
    .replace(/_bps$/u, "")
    .replace(/_/gu, " ")
    .replace(/\b\w/gu, (char) => char.toUpperCase());
}

export function TornadoChart({ impacts }: TornadoChartProps) {
  const maxAbsImpact = Math.max(...impacts.map((item) => Math.abs(item.min_savings_impact_pence)), 1);
  const topImpact = impacts[0];

  return (
    <section className="result-card" aria-labelledby="tornado-chart-heading">
      <h2 id="tornado-chart-heading">Tornado sensitivity chart</h2>
      <figure aria-label="Ranked sensitivity bars">
        <figcaption className="chart-caption">
          Ranked impact bars by absolute change in minimum savings after one-factor perturbation.
        </figcaption>
        <div className="tornado-list" role="list">
          {impacts.map((impact) => {
            const widthPercent = (Math.abs(impact.min_savings_impact_pence) / maxAbsImpact) * 100;
            const positive = impact.min_savings_impact_pence >= 0;

            return (
              <div key={impact.driver} className="tornado-item" role="listitem">
                <div className="tornado-label-row">
                  <span>{prettyDriverName(impact.driver)}</span>
                  <span>
                    {impact.min_savings_impact_pence > 0 ? "+" : ""}
                    {impact.min_savings_impact_pence}p
                  </span>
                </div>
                <div className="tornado-track" aria-hidden="true">
                  <div
                    className={`tornado-bar ${positive ? "tornado-bar-positive" : "tornado-bar-negative"}`}
                    style={{ width: `${Math.max(widthPercent, 3)}%` }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </figure>
      {topImpact ? (
        <p className="chart-summary">
          Top sensitivity driver: {prettyDriverName(topImpact.driver)} ({topImpact.min_savings_impact_pence > 0 ? "+" : ""}
          {topImpact.min_savings_impact_pence}p impact on minimum savings).
        </p>
      ) : null}
    </section>
  );
}
