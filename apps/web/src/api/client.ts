import type {
  DeterministicRequest,
  DeterministicResponse,
  MonteCarloRequest,
  MonteCarloResponse
} from "../types";

type TokenProvider = () => Promise<string | null>;

type ApiErrorBody = {
  detail?: string;
};

async function extractErrorDetail(response: Response): Promise<string | null> {
  try {
    const payload = (await response.json()) as ApiErrorBody;
    if (typeof payload.detail === "string" && payload.detail.trim().length > 0) {
      return payload.detail;
    }
  } catch {
    return null;
  }

  return null;
}

function buildErrorMessage(statusCode: number, detail: string | null): string {
  if (statusCode === 401) {
    return "Authentication failed. Please sign in again and retry from the official app URL.";
  }

  if (statusCode === 429) {
    return "Too many requests. Please wait a moment and try again.";
  }

  if (statusCode === 504) {
    return "Simulation timed out. Reduce input size and retry.";
  }

  if (detail) {
    return `Request failed (${statusCode}): ${detail}`;
  }

  return `Request failed with status ${statusCode}`;
}

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
      const detail = await extractErrorDetail(response);
      throw new Error(buildErrorMessage(response.status, detail));
    }

    return (await response.json()) as T;
  };

  return {
    runDeterministic: (payload: DeterministicRequest) =>
      postJson<DeterministicResponse>("/api/v1/deterministic/run", payload),
    runMonteCarlo: (payload: MonteCarloRequest) =>
      postJson<MonteCarloResponse>("/api/v1/montecarlo/run", payload)
  };
}
