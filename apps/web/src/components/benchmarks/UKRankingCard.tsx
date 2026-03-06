import { PercentileDisclosure } from "./PercentileDisclosure";
import { UkPercentileResponse } from "../../types";

type UKRankingCardProps = {
  ranking: UkPercentileResponse | null;
  loading: boolean;
  error: string | null;
};

export function UKRankingCard({ ranking, loading, error }: UKRankingCardProps) {
  if (loading) {
    return (
      <section className="result-card" aria-label="UK ranking loading">
        <h2>UK income ranking</h2>
        <p>Loading premium percentile ranking...</p>
      </section>
    );
  }

  if (error) {
    return (
      <section className="result-card" aria-label="UK ranking error">
        <h2>UK income ranking</h2>
        <p>{error}</p>
      </section>
    );
  }

  if (!ranking) {
    return (
      <section className="result-card" aria-label="UK ranking unavailable">
        <h2>UK income ranking</h2>
        <p>Ranking unavailable for this run.</p>
      </section>
    );
  }

  return (
    <>
      <section className="result-card" aria-label="UK ranking card">
        <h2>UK income ranking</h2>
        <p>Percentile bucket: P{ranking.percentile_bucket}</p>
        <p>Reference year: {ranking.year_label}</p>
      </section>
      <PercentileDisclosure />
    </>
  );
}
