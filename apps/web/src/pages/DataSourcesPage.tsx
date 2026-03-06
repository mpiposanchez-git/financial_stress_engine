import { useEffect, useMemo, useState } from "react";

type DataSourceItem = {
  key: string;
  name: string;
  provider: string;
  url: string;
  refresh_cadence: string;
  license_note: string;
  verification_steps: string[];
};

type DataRegistryResponse = {
  datasets: DataSourceItem[];
};

export function DataSourcesPage() {
  const [datasets, setDatasets] = useState<DataSourceItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const apiBaseUrl = useMemo(() => import.meta.env.VITE_API_BASE_URL as string, []);

  useEffect(() => {
    let cancelled = false;

    const loadRegistry = async () => {
      setLoading(true);
      setError(null);

      try {
        const response = await fetch(`${apiBaseUrl}/api/v1/data/registry`);
        if (!response.ok) {
          throw new Error(`Request failed with status ${response.status}`);
        }

        const payload = (await response.json()) as DataRegistryResponse;
        if (!cancelled) {
          setDatasets(payload.datasets ?? []);
        }
      } catch (loadError) {
        if (!cancelled) {
          const message = loadError instanceof Error ? loadError.message : "Failed to load data registry";
          setError(message);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    };

    void loadRegistry();

    return () => {
      cancelled = true;
    };
  }, [apiBaseUrl]);

  return (
    <main>
      <h1>Data Sources</h1>
      <p>Transparency view of external datasets used for benchmark assumptions.</p>

      {loading ? <p>Loading data registry...</p> : null}
      {error ? (
        <p role="alert">Unable to load data registry: {error}</p>
      ) : null}

      {!loading && !error ? (
        <section aria-label="Data registry list">
          {datasets.map((dataset) => (
            <article key={dataset.key} className="result-card">
              <h2>{dataset.name}</h2>
              <p>
                <strong>Provider:</strong> {dataset.provider}
              </p>
              <p>
                <strong>Refresh cadence:</strong> {dataset.refresh_cadence}
              </p>
              <p>
                <strong>License:</strong> {dataset.license_note}
              </p>
              <p>
                <a href={dataset.url} target="_blank" rel="noreferrer">
                  {dataset.url}
                </a>
              </p>
              <h3>Verification steps</h3>
              <ol>
                {dataset.verification_steps.map((step) => (
                  <li key={step}>{step}</li>
                ))}
              </ol>
            </article>
          ))}
        </section>
      ) : null}
    </main>
  );
}
