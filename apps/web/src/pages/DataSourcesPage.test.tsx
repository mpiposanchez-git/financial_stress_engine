import { render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { DataSourcesPage } from "./DataSourcesPage";

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("DataSourcesPage", () => {
  it("renders dataset names and URLs from registry API", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        json: async () => ({
          datasets: [
            {
              key: "boe_bank_rate",
              name: "Bank of England Bank Rate",
              provider: "Bank of England",
              url: "https://www.bankofengland.co.uk/boeapps/database/Bank-Rate.asp",
              refresh_cadence: "Daily",
              license_note: "Source terms apply",
              verification_steps: ["Check date", "Check value"]
            },
            {
              key: "ons_cpih_12m",
              name: "ONS CPIH 12-Month Rate",
              provider: "Office for National Statistics",
              url: "https://www.ons.gov.uk/economy/inflationandpriceindices",
              refresh_cadence: "Monthly",
              license_note: "OGL",
              verification_steps: ["Check month"]
            }
          ]
        })
      })
    );

    render(<DataSourcesPage />);

    await waitFor(() => {
      expect(screen.getByRole("heading", { name: "Bank of England Bank Rate" })).toBeInTheDocument();
      expect(screen.getByRole("heading", { name: "ONS CPIH 12-Month Rate" })).toBeInTheDocument();
    });

    expect(
      screen.getByRole("link", {
        name: "https://www.bankofengland.co.uk/boeapps/database/Bank-Rate.asp"
      })
    ).toBeInTheDocument();
    expect(
      screen.getByRole("link", {
        name: "https://www.ons.gov.uk/economy/inflationandpriceindices"
      })
    ).toBeInTheDocument();
  });
});
