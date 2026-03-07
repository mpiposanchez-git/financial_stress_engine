import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { UKContextBox } from "./UKContextBox";

describe("UKContextBox", () => {
  it("renders median and source when reference is available", () => {
    render(
      <UKContextBox
        loading={false}
        error={null}
        reference={{
          income_median_bhc: { year_label: "FY2024", amount_gbp: 35000 },
          income_deciles_bhc_gbp: null,
          provenance: {
            dataset_key: "dwp_hbai_zip_raw",
            source_url: "https://example.test/hbai",
            fetched_at_utc: "2026-03-06T00:00:00Z",
            sha256: "abc",
            status: "placeholder",
          },
        }}
      />
    );

    expect(screen.getByRole("heading", { name: "UK context" })).toBeInTheDocument();
    expect(screen.getByText(/Median BHC income \(FY2024\): GBP 35,000/)).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "https://example.test/hbai" })).toBeInTheDocument();
  });
});
