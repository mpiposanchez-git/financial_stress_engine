export type InputParameters = {
  household_monthly_net_income_gbp: number;
  household_monthly_essential_spend_gbp: number;
  household_monthly_debt_payments_gbp: number;
  cash_savings_gbp: number;
  mortgage_balance_gbp: number;
  mortgage_term_years_remaining: number;
  mortgage_rate_percent_current: number;
  mortgage_rate_percent_stress: number;
  mortgage_type: "repayment" | "interest_only";
  shock_monthly_income_drop_percent: number;
  inflation_monthly_essentials_increase_percent: number;
  household_monthly_net_income_currency: "GBP" | "EUR" | "USD";
  household_monthly_essential_spend_currency: "GBP" | "EUR" | "USD";
  household_monthly_debt_payments_currency: "GBP" | "EUR" | "USD";
  cash_savings_currency: "GBP" | "EUR" | "USD";
  mortgage_balance_currency: "GBP" | "EUR" | "USD";
  reporting_currency: "GBP" | "EUR" | "USD";
  fx_spot_rates: Record<"GBP" | "EUR" | "USD", number>;
  fx_stress_bps: Partial<Record<"GBP" | "EUR" | "USD", number>>;
  income_shock_std_percent: number;
  rate_shock_std_percent: number;
  inflation_shock_std_percent: number;
};

export type DeterministicRequest = {
  input_parameters: InputParameters;
};

export type MonteCarloRequest = {
  input_parameters: InputParameters;
  n_sims: number;
  horizon_months: number;
  seed?: number;
};

export type DeterministicResponse = {
  reporting_currency: "GBP" | "EUR" | "USD";
  fx_spot_rates_used: Record<string, number>;
  fx_stressed_rates_used: Record<string, number>;
  fx_stress_bps: Record<string, number>;
  monthly_cashflow_base_pence: number;
  monthly_cashflow_base_formatted: string;
  monthly_cashflow_stress_pence: number;
  monthly_cashflow_stress_formatted: string;
  mortgage_payment_current_pence: number;
  mortgage_payment_current_formatted: string;
  mortgage_payment_stress_pence: number;
  mortgage_payment_stress_formatted: string;
  runway_months: number | null;
  savings_path_pence: number[];
  savings_path_formatted: string[];
  min_savings_pence: number;
  min_savings_formatted: string;
  month_of_depletion: number | null;
  warnings: string[];
};

export type RunwayPercentileTriplet = {
  p10: number;
  p50: number;
  p90: number;
};

export type MoneyPercentileTriplet = {
  p10_pence: number;
  p10_formatted: string;
  p50_pence: number;
  p50_formatted: string;
  p90_pence: number;
  p90_formatted: string;
};

export type MonteCarloMetrics = {
  runway_months: RunwayPercentileTriplet;
  min_savings: MoneyPercentileTriplet;
  month_of_depletion: RunwayPercentileTriplet;
};

export type MonteCarloResponse = {
  n_sims: number;
  horizon_months: number;
  seed: number;
  runtime_ms: number;
  runway_months_p10: number;
  runway_months_p50: number;
  runway_months_p90: number;
  min_savings_p10_pence: number;
  min_savings_p50_pence: number;
  min_savings_p90_pence: number;
  month_of_depletion_p10: number;
  month_of_depletion_p50: number;
  month_of_depletion_p90: number;
  metrics: MonteCarloMetrics;
};

export type CompareScenarioResult = {
  name: string;
  reporting_currency: "GBP" | "EUR" | "USD";
  runway_months: number | null;
  month_of_depletion: number | null;
  min_savings_pence: number;
  min_savings_formatted: string;
  monthly_cashflow_stress_pence: number;
  monthly_cashflow_stress_formatted: string;
  mortgage_payment_stress_pence: number;
  mortgage_payment_stress_formatted: string;
  warnings: string[];
};

export type CompareRunResponse = {
  scenarios: CompareScenarioResult[];
};

export type ResultsRouteState = {
  deterministic: DeterministicResponse;
  montecarlo?: MonteCarloResponse;
  compare?: CompareRunResponse;
  premiumUnlocked?: boolean;
};
