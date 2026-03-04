import { describe, expect, it, vi } from "vitest";

import { createApiClient } from "./client";

describe("createApiClient", () => {
  it("attaches bearer token in Authorization header", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ ok: true })
    });
    vi.stubGlobal("fetch", fetchMock);

    const client = createApiClient("https://api.example.com", async () => "token-123");

    await client.runDeterministic({ input_parameters: {} });

    expect(fetchMock).toHaveBeenCalledTimes(1);
    const [url, options] = fetchMock.mock.calls[0] as [string, RequestInit];
    expect(url).toBe("https://api.example.com/api/v1/deterministic/run");
    expect((options.headers as Record<string, string>).Authorization).toBe("Bearer token-123");
  });

  it("normalizes base URL when it includes extra path segments", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ ok: true })
    });
    vi.stubGlobal("fetch", fetchMock);

    const client = createApiClient("https://api.example.com/health", async () => "token-123");

    await client.runMonteCarlo({ input_parameters: {}, n_sims: 1000, horizon_months: 24 });

    const [url] = fetchMock.mock.calls[0] as [string, RequestInit];
    expect(url).toBe("https://api.example.com/api/v1/montecarlo/run");
  });

  it("throws for missing base URL", () => {
    expect(() => createApiClient("   ", async () => null)).toThrow("Missing VITE_API_BASE_URL");
  });

  it("throws a clear error when auth token is unavailable", async () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);

    const client = createApiClient("https://api.example.com", async () => null);

    await expect(client.runDeterministic({ input_parameters: {} })).rejects.toThrow(
      "No auth token found"
    );
    expect(fetchMock).not.toHaveBeenCalled();
  });
});
