import { MonteCarloResponse } from "../../types";

type FanChartProps = {
  data: MonteCarloResponse;
};

function spanPercent(p10: number, p50: number, p90: number): { left: number; middle: number; right: number } {
  const min = Math.min(p10, p50, p90);
  const max = Math.max(p10, p50, p90);
  const width = Math.max(max - min, 1);
  const toPercent = (value: number) => ((value - min) / width) * 100;

  return {
    left: toPercent(p10),
    middle: toPercent(p50),
    right: toPercent(p90)
  };
}

export function FanChart({ data }: FanChartProps) {
  const runway = spanPercent(data.runway_months_p10, data.runway_months_p50, data.runway_months_p90);
  const savings = spanPercent(data.min_savings_p10_pence, data.min_savings_p50_pence, data.min_savings_p90_pence);
  const depletion = spanPercent(data.month_of_depletion_p10, data.month_of_depletion_p50, data.month_of_depletion_p90);

  return (
    <section className="result-card" aria-labelledby="fan-chart-heading">
      <h2 id="fan-chart-heading">Fan chart</h2>
      <p className="scenario-note">Summary percentiles</p>

      <table className="savings-table" aria-label="Monte Carlo summary percentiles">
        <thead>
          <tr>
            <th scope="col">Metric</th>
            <th scope="col">P10</th>
            <th scope="col">P50</th>
            <th scope="col">P90</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Runway (months)</td>
            <td>{data.runway_months_p10.toFixed(1)}</td>
            <td>{data.runway_months_p50.toFixed(1)}</td>
            <td>{data.runway_months_p90.toFixed(1)}</td>
          </tr>
          <tr>
            <td>Min savings (pence)</td>
            <td>{data.min_savings_p10_pence}</td>
            <td>{data.min_savings_p50_pence}</td>
            <td>{data.min_savings_p90_pence}</td>
          </tr>
          <tr>
            <td>Depletion month</td>
            <td>{data.month_of_depletion_p10.toFixed(1)}</td>
            <td>{data.month_of_depletion_p50.toFixed(1)}</td>
            <td>{data.month_of_depletion_p90.toFixed(1)}</td>
          </tr>
        </tbody>
      </table>

      <figure className="fan-band-grid" aria-label="Fan chart placeholder bands">
        <figcaption className="chart-caption">Placeholder percentile bands (P10 to P90) by metric.</figcaption>
        <div className="fan-band-row">
          <span>Runway</span>
          <div className="fan-band-track" aria-hidden="true">
            <div className="fan-band-range" style={{ left: `${runway.left}%`, width: `${Math.max(runway.right - runway.left, 2)}%` }} />
            <div className="fan-band-median" style={{ left: `${runway.middle}%` }} />
          </div>
        </div>
        <div className="fan-band-row">
          <span>Min savings</span>
          <div className="fan-band-track" aria-hidden="true">
            <div className="fan-band-range" style={{ left: `${savings.left}%`, width: `${Math.max(savings.right - savings.left, 2)}%` }} />
            <div className="fan-band-median" style={{ left: `${savings.middle}%` }} />
          </div>
        </div>
        <div className="fan-band-row">
          <span>Depletion</span>
          <div className="fan-band-track" aria-hidden="true">
            <div className="fan-band-range" style={{ left: `${depletion.left}%`, width: `${Math.max(depletion.right - depletion.left, 2)}%` }} />
            <div className="fan-band-median" style={{ left: `${depletion.middle}%` }} />
          </div>
        </div>
      </figure>
    </section>
  );
}
