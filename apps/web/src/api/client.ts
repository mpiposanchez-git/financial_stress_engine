import type { DeterministicRequest, MonteCarloRequest } from "../types";

type TokenProvider = () => Promise<string | null>;

export function createApiClient(baseUrl: string, getToken: TokenProvider) {
  const postJson = async <T>(path: string, payload: unknown): Promise<T> => {
    const token = await getToken();
    const headers: Record<string, string> = {
      "Content-Type": "application/json"
    };

    if (token) {
      headers.Authorization = `Bearer ${token}`;
    }

    const response = await fetch(`${baseUrl}${path}`, {
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
