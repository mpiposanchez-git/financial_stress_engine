# MOD-003 — Multi-Currency + FX Risk Specification 🌍💱

**Status:** Draft  
**Scope:** currency handling for deterministic and Monte Carlo engines.

---

## 1) Problem statement (plain English) 🎓
Users may earn, spend, borrow, or save in more than one currency (e.g., GBP + EUR).  
They want outputs displayed in a chosen **reporting currency** (e.g., GBP).  
FX rates can move, so FX is a **risk driver**.

---

## 2) Currency model 🧾

### 2.1 Input representation
Each monetary amount is provided as:
- `amount` (user-friendly, e.g., 1234.56)
- `currency` (ISO code, e.g., "GBP", "EUR", "USD")

Internally:
- convert `amount` to **pence-like smallest unit** per currency.
  - For POC: assume 2 decimal places for all supported currencies (GBP/EUR/USD).
  - Document this as a limitation.

### 2.2 Reporting currency
User selects a reporting currency `C_report`.  
All engine outputs are expressed in `C_report` pence.

---

## 3) FX rates (baseline) 💱
User provides:
- spot FX rates for all required pairs to reporting currency
  - Example: EUR→GBP = 0.86

For deterministic:
- convert each amount using spot rates.

Rounding:
- after conversion, quantize to 1 penny in reporting currency.

---

## 4) Deterministic FX stress 📉
Provide a deterministic stress parameter per currency pair:
- e.g., “GBP weakens 10% vs EUR” (equivalently EUR→GBP increases)

Apply:
- stressed FX rate = spot FX × (1 + fx_stress%)

Compute stressed cashflows in reporting currency accordingly.

---

## 5) Monte Carlo FX paths 🎲
Add FX dynamics to Monte Carlo:
- Monthly FX return `r_fx[t] ~ Normal(mu_fx, sigma_fx)` (POC)
- FX rate path:
  - `FX[t+1] = FX[t] * exp(r_fx[t])` (lognormal path)
- Optionally use AR(1) in returns later for persistence.

Outputs must reflect how FX affects:
- monthly cashflow (converted to reporting currency)
- savings path
- runway distribution

---

## 6) Output formatting (both pence + human readable) 📤
You requested “both”:
- numeric fields returned as:
  - `*_pence` (int) in reporting currency
  - `*_gbp_str` (or `*_formatted`) for display
- Include:
  - `reporting_currency`
  - FX spot rates used
  - FX stress/shock parameters used

---

## 7) Limitations (explicit) ⚠️
- POC supports a limited set of currencies (start with GBP/EUR/USD).
- Assumes 2 decimals for all supported currencies.
- No cross-currency mortgage amortisation beyond conversion for reporting.
