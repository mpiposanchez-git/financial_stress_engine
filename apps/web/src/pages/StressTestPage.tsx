import { FormEvent, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";

import { useAuthState } from "../auth/useAuthState";
import { createApiClient } from "../api/client";

const defaultInput = {
  household_monthly_net_income_gbp: 4000,
  household_monthly_essential_spend_gbp: 1500,
  household_monthly_debt_payments_gbp: 200,
  cash_savings_gbp: 10000,
  mortgage_balance_gbp: 250000,
  mortgage_term_years_remaining: 25,
  mortgage_rate_percent_current: 4.5,
  mortgage_rate_percent_stress: 6,
  mortgage_type: "repayment",
  shock_monthly_income_drop_percent: 10,
  inflation_monthly_essentials_increase_percent: 5,
  income_shock_std_percent: 5,
  rate_shock_std_percent: 0.5,
  inflation_shock_std_percent: 1
};

export function StressTestPage() {
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { getToken } = useAuthState();

  const api = useMemo(() => {
    const baseUrl = import.meta.env.VITE_API_BASE_URL as string;
    return createApiClient(baseUrl, getToken);
  }, [getToken]);

  const onSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const deterministic = await api.runDeterministic({
        input_parameters: defaultInput
      });
      const montecarlo = await api.runMonteCarlo({
        input_parameters: defaultInput,
        n_sims: 1000,
        horizon_months: 24
      });

      navigate("/results", { state: { deterministic, montecarlo } });
    } catch (submitError) {
      setError(submitError instanceof Error ? submitError.message : "Request failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main>
      <h1>Stress Test</h1>
      <p>Run an illustrative simulation. This is not financial advice.</p>
      <form onSubmit={onSubmit}>
        <button type="submit" disabled={loading}>
          {loading ? "Running…" : "Run simulation"}
        </button>
      </form>
      {error ? <p role="alert">{error}</p> : null}
    </main>
  );
}
