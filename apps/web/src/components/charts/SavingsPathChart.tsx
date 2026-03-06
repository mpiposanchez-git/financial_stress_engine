type SavingsPathChartProps = {
  values: number[];
  formattedValues?: string[];
};

export function SavingsPathChart({ values, formattedValues = [] }: SavingsPathChartProps) {
  if (values.length < 2) {
    return <p>Savings path chart unavailable.</p>;
  }

  const width = 440;
  const height = 180;
  const padding = 16;
  const min = Math.min(...values);
  const max = Math.max(...values);
  const span = Math.max(max - min, 1);

  const points = values
    .map((value, index) => {
      const x = padding + (index / (values.length - 1)) * (width - padding * 2);
      const y = height - padding - ((value - min) / span) * (height - padding * 2);
      return `${x.toFixed(2)},${y.toFixed(2)}`;
    })
    .join(" ");

  return (
    <figure className="result-card" aria-labelledby="deterministic-savings-heading">
      <h3 id="deterministic-savings-heading">Deterministic savings path</h3>
      <svg
        className="savings-chart"
        viewBox={`0 0 ${width} ${height}`}
        role="img"
        aria-label="Deterministic month-by-month savings path"
      >
        <line x1={padding} y1={padding} x2={padding} y2={height - padding} className="chart-axis" />
        <line x1={padding} y1={height - padding} x2={width - padding} y2={height - padding} className="chart-axis" />
        <polyline points={points} className="chart-line" />
      </svg>
      <figcaption className="chart-caption">
        Low point: {min} pence | High point: {max} pence
      </figcaption>
      <p className="chart-summary">
        Summary: starts at {values[0]} pence, ends at {values[values.length - 1]} pence, and ranges between {min} and {max} pence.
      </p>
      <table className="savings-table" aria-label="Deterministic savings path table">
        <thead>
          <tr>
            <th scope="col">Month</th>
            <th scope="col">Savings (pence)</th>
            <th scope="col">Savings (formatted)</th>
          </tr>
        </thead>
        <tbody>
          {values.map((value, index) => (
            <tr key={`month-${index + 1}`}>
              <th scope="row">{index + 1}</th>
              <td>{value}</td>
              <td>{formattedValues[index] ?? "-"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </figure>
  );
}
