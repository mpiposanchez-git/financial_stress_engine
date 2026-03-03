# Assumptions Documentation

This document describes the Monte Carlo uncertainty assumptions used in the financial stress testing engine.

## Overview

The engine ships with two assumption sets (`v1.yaml` and `v2.yaml`) that define the **standard deviation (uncertainty band)** parameters used in Monte Carlo simulations. These are **not macro forecasts** — they describe the spread of uncertainty around the user-provided deterministic inputs.

---

## v1.yaml — Conservative Baseline

```yaml
income_shock_std_percent: 5.0
rate_shock_std_percent: 0.5
inflation_shock_std_percent: 1.0
```

- **Use case:** Central-case stress testing with moderate uncertainty bands.
- **Interpretation:** Income shock varies ±5% around the user's chosen shock; rate varies ±0.5%; essentials inflation varies ±1%.
- **Suitable for:** General household stress testing, illustrative guidance.

## v2.yaml — Severe / Tail-Risk

```yaml
income_shock_std_percent: 10.0
rate_shock_std_percent: 1.0
inflation_shock_std_percent: 2.0
```

- **Use case:** Tail-risk scenario analysis with wider uncertainty bands.
- **Interpretation:** Double the uncertainty of v1, intended to stress-test resilience under more extreme distributional uncertainty.
- **Suitable for:** Sensitivity analysis, worst-case planning.

---

## How Assumptions Are Used

Each Monte Carlo trial samples:

1. **Income shock** from `Normal(μ=user_shock, σ=income_shock_std_percent)`, clipped to [0, 100].
2. **Mortgage rate** from `Normal(μ=user_stress_rate, σ=rate_shock_std_percent)`, clipped to [0, 100].
3. **Essentials inflation** from `Normal(μ=user_inflation, σ=inflation_shock_std_percent)`, clipped to [0, 100].

The standard deviations come from the active assumption set. The default in the API uses the values passed directly by the user (with defaults from v1).

---

## Updating Assumptions

1. Edit the relevant YAML file (`app/assumptions/v1.yaml` or `v2.yaml`).
2. All values are percentages (e.g. `5.0` means 5%).
3. Do **not** set `std` values to 0 unless you explicitly want a deterministic simulation.
4. Commit changes under version control with a descriptive message explaining the rationale.

### Version Control Guidelines

- Bump the `version` field in the YAML when making substantive changes.
- Document the reason for changes in the commit message.
- Consider tagging releases when assumption sets are updated (e.g. `assumptions-v1.1`).
- Do **not** treat these values as macro forecasts — they are uncertainty envelope parameters.

---

## Important Notes

- These assumptions do **not** constitute financial forecasts or regulatory guidance.
- They should be reviewed periodically against observed UK macroeconomic data and updated accordingly.
- Any update should be reviewed by a qualified person before deployment in an advisory context.
