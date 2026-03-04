import type { DeterministicRequest, MonteCarloRequest } from "../types";

type TokenProvider = () => Promise<string | null>;

function normalizeBaseUrl(baseUrl: string): string {
  const trimmed = baseUrl.trim();
  if (!trimmed) {
    throw new Error("Missing VITE_API_BASE_URL");
  }

  const parsed = new URL(trimmed);
  parsed.pathname = "/";
  parsed.search = "";
  parsed.hash = "";
  return parsed.toString();
}

export function createApiClient(baseUrl: string, getToken: TokenProvider) {
  const normalizedBaseUrl = normalizeBaseUrl(baseUrl);

  const postJson = async <T>(path: string, payload: unknown): Promise<T> => {
    const token = await getToken();
    if (!token) {
      throw new Error("No auth token found. Please sign out and sign in again.");
    }

    const headers: Record<string, string> = {
      "Content-Type": "application/json"
    };

    headers.Authorization = `Bearer ${token}`;

    const url = new URL(path, normalizedBaseUrl).toString();

    const response = await fetch(url, {
      method: "POST",
      headers,
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      throw new Error(`Request failed with status ${response.status}`);
    }

    return (await response.json()) as T;
  };

  return {
    runDeterministic: (payload: DeterministicRequest) =>
      postJson("/api/v1/deterministic/run", payload),
    runMonteCarlo: (payload: MonteCarloRequest) => postJson("/api/v1/montecarlo/run", payload)
  };
}
