import { FormEvent, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";

import { useAuthState } from "../auth/useAuthState";
import { createApiClient } from "../api/client";
import { DiagnosticsPanel } from "../components/DiagnosticsPanel";
import { CurrencySelect } from "../components/inputs/CurrencySelect";
import { MortgageInputs } from "../components/inputs/MortgageInputs";
import { MoneyInput } from "../components/inputs/MoneyInput";
import { PercentSlider } from "../components/inputs/PercentSlider";
import { Wizard } from "../components/wizard/Wizard";
import { WizardNav } from "../components/wizard/WizardNav";
import { WizardStep } from "../components/wizard/WizardStep";
import { buildDeterministicPayload } from "../lib/buildPayload";
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
  const [currentStep, setCurrentStep] = useState(0);
  const navigate = useNavigate();
  const { getToken } = useAuthState();
  const formErrorId = "stress-form-error";
  const totalSteps = 3;
  const stepTitles = ["Currencies and FX spots", "Mortgage inputs", "FX stress and review"] as const;

  const api = useMemo(() => {
    const baseUrl = import.meta.env.VITE_API_BASE_URL as string;
    return createApiClient(baseUrl, getToken);
  }, [getToken]);

  const onSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const deterministicPayload = buildDeterministicPayload(form);
      const deterministic = await api.runDeterministic(deterministicPayload);
      const resultState: ResultsRouteState = { deterministic };
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
      <form onSubmit={onSubmit} aria-describedby={formErrorId}>
        <Wizard
          currentStep={currentStep}
          totalSteps={totalSteps}
          title={stepTitles[currentStep]}
        >
          {currentStep === 0 ? (
            <WizardStep id="wizard-step-1" title="Currencies and FX spots">
              <CurrencySelect
                id="reporting-currency"
                label="Reporting currency"
                value={form.reporting_currency}
                currencies={currencies}
                ariaDescribedBy={formErrorId}
                onChange={(reporting) =>
                  setForm((prev) => ({
                    ...prev,
                    reporting_currency: reporting,
                    fx_spot_rates: {
                      ...prev.fx_spot_rates,
                      [reporting]: 1
                    }
                  }))
                }
              />
              <MoneyInput
                idPrefix="income"
                label="Income"
                amount={form.household_monthly_net_income_gbp}
                currency={form.household_monthly_net_income_currency}
                currencies={currencies}
                ariaDescribedBy={formErrorId}
                onAmountChange={(amount) =>
                  setForm((prev) => ({
                    ...prev,
                    household_monthly_net_income_gbp: amount
                  }))
                }
                onCurrencyChange={(currency) =>
                  setForm((prev) => ({
                    ...prev,
                    household_monthly_net_income_currency: currency
                  }))
                }
              />
              <MoneyInput
                idPrefix="essentials"
                label="Essentials"
                amount={form.household_monthly_essential_spend_gbp}
                currency={form.household_monthly_essential_spend_currency}
                currencies={currencies}
                ariaDescribedBy={formErrorId}
                onAmountChange={(amount) =>
                  setForm((prev) => ({
                    ...prev,
                    household_monthly_essential_spend_gbp: amount
                  }))
                }
                onCurrencyChange={(currency) =>
                  setForm((prev) => ({
                    ...prev,
                    household_monthly_essential_spend_currency: currency
                  }))
                }
              />
              <label htmlFor="debt-currency">
                Debt currency
                <select
                  id="debt-currency"
                  aria-label="Debt currency"
                  aria-describedby={formErrorId}
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
              <label htmlFor="savings-currency">
                Savings currency
                <select
                  id="savings-currency"
                  aria-label="Savings currency"
                  aria-describedby={formErrorId}
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
              <label htmlFor="fx-spot-eur">
                FX spot EUR to reporting
                <input
                  id="fx-spot-eur"
                  aria-label="FX spot EUR to reporting"
                  aria-describedby={formErrorId}
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
              <label htmlFor="fx-spot-usd">
                FX spot USD to reporting
                <input
                  id="fx-spot-usd"
                  aria-label="FX spot USD to reporting"
                  aria-describedby={formErrorId}
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
            </WizardStep>
          ) : currentStep === 1 ? (
            <WizardStep id="wizard-step-2" title="Mortgage inputs">
              <MortgageInputs
                balance={form.mortgage_balance_gbp}
                balanceCurrency={form.mortgage_balance_currency}
                mortgageType={form.mortgage_type}
                termYearsRemaining={form.mortgage_term_years_remaining}
                currentRatePercent={form.mortgage_rate_percent_current}
                stressRatePercent={form.mortgage_rate_percent_stress}
                currencies={currencies}
                ariaDescribedBy={formErrorId}
                onBalanceChange={(value) =>
                  setForm((prev) => ({
                    ...prev,
                    mortgage_balance_gbp: value
                  }))
                }
                onBalanceCurrencyChange={(value) =>
                  setForm((prev) => ({
                    ...prev,
                    mortgage_balance_currency: value
                  }))
                }
                onMortgageTypeChange={(value) =>
                  setForm((prev) => ({
                    ...prev,
                    mortgage_type: value
                  }))
                }
                onTermYearsRemainingChange={(value) =>
                  setForm((prev) => ({
                    ...prev,
                    mortgage_term_years_remaining: value
                  }))
                }
                onCurrentRatePercentChange={(value) =>
                  setForm((prev) => ({
                    ...prev,
                    mortgage_rate_percent_current: value
                  }))
                }
                onStressRatePercentChange={(value) =>
                  setForm((prev) => ({
                    ...prev,
                    mortgage_rate_percent_stress: value
                  }))
                }
              />
            </WizardStep>
          ) : (
            <WizardStep id="wizard-step-3" title="FX stress and review">
              <PercentSlider
                id="income-shock-slider"
                label="Income shock (%)"
                ariaDescribedBy={formErrorId}
                value={form.shock_monthly_income_drop_percent}
                min={0}
                max={100}
                step={0.5}
                onChange={(value) =>
                  setForm((prev) => ({
                    ...prev,
                    shock_monthly_income_drop_percent: value
                  }))
                }
              />
              <PercentSlider
                id="inflation-shock-slider"
                label="Inflation essentials increase (%)"
                ariaDescribedBy={formErrorId}
                value={form.inflation_monthly_essentials_increase_percent}
                min={0}
                max={100}
                step={0.5}
                onChange={(value) =>
                  setForm((prev) => ({
                    ...prev,
                    inflation_monthly_essentials_increase_percent: value
                  }))
                }
              />
              <PercentSlider
                id="mortgage-rate-stress-slider"
                label="Stressed mortgage rate (%)"
                ariaDescribedBy={formErrorId}
                value={form.mortgage_rate_percent_stress}
                min={0}
                max={25}
                step={0.1}
                onChange={(value) =>
                  setForm((prev) => ({
                    ...prev,
                    mortgage_rate_percent_stress: value
                  }))
                }
              />
              <PercentSlider
                id="fx-stress-eur-slider"
                label="FX stress EUR (bps)"
                ariaDescribedBy={formErrorId}
                value={form.fx_stress_bps.EUR ?? 0}
                valueKind="bps"
                min={-3000}
                max={3000}
                step={25}
                onChange={(value) =>
                  setForm((prev) => ({
                    ...prev,
                    fx_stress_bps: {
                      ...prev.fx_stress_bps,
                      EUR: value
                    }
                  }))
                }
              />
              <PercentSlider
                id="fx-stress-usd-slider"
                label="FX stress USD (bps)"
                ariaDescribedBy={formErrorId}
                value={form.fx_stress_bps.USD ?? 0}
                valueKind="bps"
                min={-3000}
                max={3000}
                step={25}
                onChange={(value) =>
                  setForm((prev) => ({
                    ...prev,
                    fx_stress_bps: {
                      ...prev.fx_stress_bps,
                      USD: value
                    }
                  }))
                }
              />
            </WizardStep>
          )}
        </Wizard>
        <WizardNav
          currentStep={currentStep}
          totalSteps={totalSteps}
          onBack={() => setCurrentStep((prev) => Math.max(0, prev - 1))}
          onNext={() => setCurrentStep((prev) => Math.min(totalSteps - 1, prev + 1))}
          isSubmitting={loading}
        />
        <DiagnosticsPanel input={form} />
      </form>
      <p id={formErrorId} role="alert" aria-live="assertive" className={error ? "form-error" : "sr-only"}>
        {error ?? "No validation errors."}
      </p>
    </main>
  );
}
