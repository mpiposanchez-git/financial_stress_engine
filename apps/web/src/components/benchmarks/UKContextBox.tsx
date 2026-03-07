import { UkReferenceValuesResponse } from "../../types";

type UKContextBoxProps = {
  reference: UkReferenceValuesResponse | null;
  loading: boolean;
  error: string | null;
};

export function UKContextBox({ reference, loading, error }: UKContextBoxProps) {
  if (loading) {
    return (
      <section className="result-card" aria-label="UK context loading">
        <h2>UK context</h2>
        <p>Loading UK benchmark context...</p>
      </section>
    );
  }

  if (error) {
    return (
      <section className="result-card" aria-label="UK context error">
        <h2>UK context</h2>
        <p>{error}</p>
      </section>
    );
  }

  if (!reference) {
    return (
      <section className="result-card" aria-label="UK context unavailable">
        <h2>UK context</h2>
        <p>UK benchmark context unavailable.</p>
      </section>
    );
  }

  return (
    <section className="result-card" aria-label="UK context box">
      <h2>UK context</h2>
      <p>
        Median BHC income ({reference.income_median_bhc.year_label}): GBP {reference.income_median_bhc.amount_gbp.toLocaleString()}
      </p>
      <p>
        Source: <a href={reference.provenance.source_url}>{reference.provenance.source_url}</a>
      </p>
    </section>
  );
}
