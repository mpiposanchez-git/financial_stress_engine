import type { DeterministicRequest, InputParameters } from "../types";

const currencies = ["GBP", "EUR", "USD"] as const;

type CurrencyCode = (typeof currencies)[number];

function normalizeFxStress(input: InputParameters): Record<CurrencyCode, number> {
  return {
    GBP: input.fx_stress_bps.GBP ?? 0,
    EUR: input.fx_stress_bps.EUR ?? 0,
    USD: input.fx_stress_bps.USD ?? 0
  };
}

function normalizeFxSpots(input: InputParameters): Record<CurrencyCode, number> {
  return {
    GBP: input.reporting_currency === "GBP" ? 1 : input.fx_spot_rates.GBP,
    EUR: input.reporting_currency === "EUR" ? 1 : input.fx_spot_rates.EUR,
    USD: input.reporting_currency === "USD" ? 1 : input.fx_spot_rates.USD
  };
}

export function buildDeterministicPayload(input: InputParameters): DeterministicRequest {
  return {
    input_parameters: {
      ...input,
      fx_spot_rates: normalizeFxSpots(input),
      fx_stress_bps: normalizeFxStress(input)
    }
  };
}
