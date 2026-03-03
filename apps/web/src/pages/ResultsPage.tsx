import { useLocation } from "react-router-dom";

export function ResultsPage() {
  const location = useLocation();
  const state = location.state as Record<string, unknown> | null;

  return (
    <main>
      <h1>Results</h1>
      <p>Illustrative simulation results only; not financial advice.</p>
      <pre>{JSON.stringify(state ?? { message: "No results yet." }, null, 2)}</pre>
    </main>
  );
}
