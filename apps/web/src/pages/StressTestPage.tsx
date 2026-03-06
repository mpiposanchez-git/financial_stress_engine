import { FormEvent, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";

import { useAuthState } from "../auth/useAuthState";
import { createApiClient } from "../api/client";
import { InputParameters, ResultsRouteState } from "../types";

const currencies = ["GBP", "EUR", "USD"] as const;

function parseFiniteNumber(value: string): number | null {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : null;
}

const defaultInput: InputParameters = {
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
  household_monthly_net_income_currency: "GBP",
  household_monthly_essential_spend_currency: "GBP",
  household_monthly_debt_payments_currency: "GBP",
  cash_savings_currency: "GBP",
  mortgage_balance_currency: "GBP",
  reporting_currency: "GBP",
  fx_spot_rates: {
    GBP: 1,
    EUR: 0.86,
    USD: 0.78
  },
  fx_stress_bps: {
    GBP: 0,
    EUR: 0,
    USD: 0
  },
  income_shock_std_percent: 5,
  rate_shock_std_percent: 0.5,
  inflation_shock_std_percent: 1
};

export function StressTestPage() {
  const [form, setForm] = useState<InputParameters>(defaultInput);
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
        input_parameters: form
      });
      const montecarlo = await api.runMonteCarlo({
        input_parameters: form,
        n_sims: 1000,
        horizon_months: 24
      });

      const resultState: ResultsRouteState = { deterministic, montecarlo };
      navigate("/results", { state: resultState });
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
        <label>
          Reporting currency
          <select
            value={form.reporting_currency}
            onChange={(event) =>
              setForm((prev) => {
                const reporting = event.target.value as (typeof currencies)[number];
                return {
                  ...prev,
                  reporting_currency: reporting,
                  fx_spot_rates: {
                    ...prev.fx_spot_rates,
                    [reporting]: 1
                  }
                };
              })
            }
          >
            {currencies.map((currency) => (
              <option key={currency} value={currency}>
                {currency}
              </option>
            ))}
          </select>
        </label>
        <label>
          Income currency
          <select
            value={form.household_monthly_net_income_currency}
            onChange={(event) =>
              setForm((prev) => ({
                ...prev,
                household_monthly_net_income_currency: event.target.value as (typeof currencies)[number]
              }))
            }
          >
            {currencies.map((currency) => (
              <option key={currency} value={currency}>
                {currency}
              </option>
            ))}
          </select>
        </label>
        <label>
          Essentials currency
          <select
            value={form.household_monthly_essential_spend_currency}
            onChange={(event) =>
              setForm((prev) => ({
                ...prev,
                household_monthly_essential_spend_currency: event.target.value as (typeof currencies)[number]
              }))
            }
          >
            {currencies.map((currency) => (
              <option key={currency} value={currency}>
                {currency}
              </option>
            ))}
          </select>
        </label>
        <label>
          Debt currency
          <select
            value={form.household_monthly_debt_payments_currency}
            onChange={(event) =>
              setForm((prev) => ({
                ...prev,
                household_monthly_debt_payments_currency: event.target.value as (typeof currencies)[number]
              }))
            }
          >
            {currencies.map((currency) => (
              <option key={currency} value={currency}>
                {currency}
              </option>
            ))}
          </select>
        </label>
        <label>
          Savings currency
          <select
            value={form.cash_savings_currency}
            onChange={(event) =>
              setForm((prev) => ({
                ...prev,
                cash_savings_currency: event.target.value as (typeof currencies)[number]
              }))
            }
          >
            {currencies.map((currency) => (
              <option key={currency} value={currency}>
                {currency}
              </option>
            ))}
          </select>
        </label>
        <label>
          Mortgage currency
          <select
            value={form.mortgage_balance_currency}
            onChange={(event) =>
              setForm((prev) => ({
                ...prev,
                mortgage_balance_currency: event.target.value as (typeof currencies)[number]
              }))
            }
          >
            {currencies.map((currency) => (
              <option key={currency} value={currency}>
                {currency}
              </option>
            ))}
          </select>
        </label>
        <label>
          FX spot EUR→reporting
          <input
            type="number"
            step="0.0001"
            value={form.fx_spot_rates.EUR}
            onChange={(event) =>
              setForm((prev) => {
                const next = parseFiniteNumber(event.target.value);
                if (next === null) {
                  return prev;
                }

                return {
                  ...prev,
                  fx_spot_rates: {
                    ...prev.fx_spot_rates,
                    EUR: next
                  }
                };
              })
            }
          />
        </label>
        <label>
          FX spot USD→reporting
          <input
            type="number"
            step="0.0001"
            value={form.fx_spot_rates.USD}
            onChange={(event) =>
              setForm((prev) => {
                const next = parseFiniteNumber(event.target.value);
                if (next === null) {
                  return prev;
                }

                return {
                  ...prev,
                  fx_spot_rates: {
                    ...prev.fx_spot_rates,
                    USD: next
                  }
                };
              })
            }
          />
        </label>
        <label>
          FX stress EUR (bps)
          <input
            type="number"
            value={form.fx_stress_bps.EUR ?? 0}
            onChange={(event) =>
              setForm((prev) => {
                const next = parseFiniteNumber(event.target.value);
                if (next === null) {
                  return prev;
                }

                return {
                  ...prev,
                  fx_stress_bps: {
                    ...prev.fx_stress_bps,
                    EUR: next
                  }
                };
              })
            }
          />
        </label>
        <label>
          FX stress USD (bps)
          <input
            type="number"
            value={form.fx_stress_bps.USD ?? 0}
            onChange={(event) =>
              setForm((prev) => {
                const next = parseFiniteNumber(event.target.value);
                if (next === null) {
                  return prev;
                }

                return {
                  ...prev,
                  fx_stress_bps: {
                    ...prev.fx_stress_bps,
                    USD: next
                  }
                };
              })
            }
          />
        </label>
        <button type="submit" disabled={loading}>
          {loading ? "Running…" : "Run simulation"}
        </button>
      </form>
      {error ? <p role="alert">{error}</p> : null}
    </main>
  );
}
