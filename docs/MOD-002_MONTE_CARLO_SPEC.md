# MOD-002 — Monte Carlo Engine Specification 🎲

**Status:** Draft  
**Scope:** stochastic simulation over monthly horizon.  
**Default horizon:** 24 months.  
**Outputs:** percentile summaries (P10/P50/P90) and reproducibility.

---

## 1) Intended use / not intended use ⚖️
Same guardrails as MOD-001 (educational simulation only).

---

## 2) Simulation definition (POC) 🧠

We simulate many alternate futures (“paths”). Each simulation `i` produces a monthly sequence of:
- income shock %
- inflation %
- mortgage rate %
- FX rate changes (from MOD-003)

Then we compute monthly cashflow and savings path, exactly as in MOD-001, but with time-varying shocks.

---

## 3) Distributions for shocks (POC default: monthly IID) 📈

For each simulation `i` and month `t`:

- Income shock %:
  - `shock_income[i,t] ~ Normal(mu_income, sigma_income)` clipped to [0, 100]
- Inflation %:
  - `infl[i,t] ~ Normal(mu_infl, sigma_infl)` clipped to [0, 100]
- Mortgage rate %:
  - `rate[i,t] ~ Normal(mu_rate, sigma_rate)` clipped to [0, 100]

All units are percent; internal engine may store in bps.

---

## 4) Optional persistence mode (AR(1) hook) 🧷

Add a parameter `shock_dynamics`:
- `"iid"` (default POC)
- `"ar1"` (optional)

For AR(1):
- `x[t] = a*x[t-1] + (1-a)*mu + eps[t]`
- where `eps[t] ~ Normal(0, sigma_eps)`

Design goal:
- Keep `"iid"` stable for POC.
- Implement `"ar1"` behind a flag or scaffold it with tests.

---

## 5) Outputs (what we report) 📤

At minimum report P10/P50/P90 for:
- `runway_months`
- `min_savings_pence`
- `month_of_depletion`
- optional: `end_savings_pence` at horizon end

Also include:
- runtime_ms
- seed used (if provided)

---

## 6) Reproducibility contract ✅
If a seed is provided:
- The same inputs + same seed must produce identical outputs.

---

## 7) Limits & stability ⚠️
Enforce:
- max `n_sims`
- max `horizon_months`
- response time budget
