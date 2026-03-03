export type DeterministicRequest = {
  input_parameters: Record<string, unknown>;
};

export type MonteCarloRequest = {
  input_parameters: Record<string, unknown>;
  n_sims: number;
  horizon_months: number;
  seed?: number;
};
