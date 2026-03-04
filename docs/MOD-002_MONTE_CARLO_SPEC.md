# MOD-002 — Monte Carlo Engine Specification 🎲

**Status:** Implemented (POC-005)  
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
All monetary aggregation is reported in reporting-currency pence.

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

Parameter `shock_dynamics`:
- `"iid"` (default POC)
- `"ar1"` (optional)

For AR(1):
- `x[t] = a*x[t-1] + (1-a)*mu + eps[t]`
- where `eps[t] ~ Normal(0, sigma_eps)`

Implemented behavior:
- `iid`: independent monthly innovations.
- `ar1`: persistence via `x[t] = mu + phi * (x[t-1] - mu) + eps[t]` with configurable `ar1_phi`.

---

## 5) Outputs (what we report) 📤

At minimum report P10/P50/P90 for:
- `runway_months`
- `min_savings_pence`
- `month_of_depletion`

Also include:
- runtime_ms
- seed used (if provided)

---

## 6) Reproducibility contract ✅
If a seed is provided:
- The same inputs + same seed must produce identical outputs.

This contract is covered by reproducibility tests for both `iid` and `ar1` dynamics.

---

## 7) Limits & stability ⚠️
Enforce:
- max `n_sims`
- max `horizon_months`
- response time budget

FX note:
- Monte Carlo includes stochastic monthly FX paths per configured currency with optional volatility.
