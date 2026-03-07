import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { UKRankingCard } from "./UKRankingCard";

describe("UKRankingCard", () => {
  it("renders percentile bucket and disclosure for premium ranking", () => {
    render(
      <UKRankingCard
        loading={false}
        error={null}
        ranking={{
          percentile_bucket: 70,
          year_label: "FY2024",
          reporting_currency: "GBP",
          thresholds_gbp: [12000, 15500, 19000, 23000, 28000, 34000, 42000, 55000, 80000],
          caveats: ["indicative"],
        }}
      />
    );

    expect(screen.getByRole("heading", { name: "UK income ranking" })).toBeInTheDocument();
    expect(screen.getByText("Percentile bucket: P70")).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Percentile ranking disclosure" })).toBeInTheDocument();
  });
});
