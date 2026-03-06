import type {
  DeterministicRequest,
  DeterministicResponse,
  InputParameters,
  MonteCarloRequest,
  MonteCarloResponse,
  SensitivityRequest,
  SensitivityResponse
} from "../types";

type TokenProvider = () => Promise<string | null>;

type ApiErrorBody = {
  detail?: string | ApiValidationIssue[];
};

type ApiValidationIssue = {
  loc?: Array<string | number>;
  msg?: string;
  type?: string;
};

function formatValidationIssues(issues: ApiValidationIssue[]): string | null {
  if (!issues.length) {
    return null;
  }

  const first = issues[0];
  const location = Array.isArray(first.loc) ? first.loc.join(".") : "request";
  const message = typeof first.msg === "string" ? first.msg : "Invalid input";
  return `${location}: ${message}`;
}

async function extractErrorDetail(response: Response): Promise<string | null> {
  try {
    const payload = (await response.json()) as ApiErrorBody;
    if (typeof payload.detail === "string" && payload.detail.trim().length > 0) {
      return payload.detail;
    }

    if (Array.isArray(payload.detail)) {
      return formatValidationIssues(payload.detail);
    }
  } catch {
    return null;
  }

  return null;
}

function buildErrorMessage(statusCode: number, detail: string | null): string {
  if (statusCode === 422) {
    if (detail) {
      return `Invalid simulation input: ${detail}`;
    }
    return "Invalid simulation input. Please check numeric fields and retry.";
  }

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
    runDeterministicFromInput: (inputParameters: InputParameters) =>
      postJson<DeterministicResponse>("/api/v1/deterministic/run", { input_parameters: inputParameters }),
    runMonteCarlo: (payload: MonteCarloRequest) =>
      postJson<MonteCarloResponse>("/api/v1/montecarlo/run", payload),
    runSensitivity: (payload: SensitivityRequest) =>
      postJson<SensitivityResponse>("/api/v1/sensitivity/run", payload)
  };
}
