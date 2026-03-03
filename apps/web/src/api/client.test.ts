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
    const [, options] = fetchMock.mock.calls[0] as [string, RequestInit];
    expect((options.headers as Record<string, string>).Authorization).toBe("Bearer token-123");
  });
});
