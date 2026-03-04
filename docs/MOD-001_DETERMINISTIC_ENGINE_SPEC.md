# MOD-001 — Deterministic Engine Specification 🧠

**Status:** Draft  
**Scope:** Deterministic engine only (no Monte Carlo).  
**Time step:** monthly.  
**Default horizon:** 24 months.

---

## 1) Intended use / not intended use ⚖️

### Intended use
Educational simulation of household cashflow stress, savings depletion, and runway.

### Not intended use
- No financial advice
- No product or lender recommendations
- No “what should I do” guidance

---

## 2) Inputs (definitions + validation) 🧾

All monetary inputs support a currency (see MOD-003).

### 2.1 Money representation (internal)
- Store money as **integer pence**:
  - £123.45 → 12345
- Validation:
  - money amounts must be >= 0 unless explicitly allowed
  - mortgage term must be > 0 if balance > 0
  - shock percentages must be within [0, 100]

### 2.2 Rates representation (internal)
- Store rates as **basis points (bps)**:
  - 5.25% → 525 bps
- Validation:
  - rates within [0, 10000] bps (0% to 100%) unless specified otherwise

---

## 3) Outputs (definitions) 📤

### 3.1 Summary outputs
- `monthly_cashflow_base_pence`
- `monthly_cashflow_stress_pence`
- `runway_months` (integer months until savings reach 0; `None` if never depleted within horizon)
- `month_of_depletion` (first month index where savings is 0; `None` if not depleted)
- `min_savings_pence`

### 3.2 Path outputs
- `savings_path_pence`: length `horizon_months + 1` including month 0 initial savings

### 3.3 Reporting currency outputs
Engine outputs should be produced in reporting currency pence.  
UI may also show formatted GBP strings (see MOD-003 for formatting).

---

## 4) Core formulas (the contract) 🧮

### 4.1 Mortgage monthly payment (pence)
Support:
- repayment mortgage
- interest-only mortgage

**Repayment mortgage (concept)**  
Monthly payment is the standard amortising payment over `n` months at monthly rate `r`.

Implementation rule:
- Use `Decimal` for exponentiation and then quantize to 1 penny.
- Return 0 if balance is 0.

**Interest-only**  
Monthly payment = balance × monthly_rate.

Edge cases:
- 0% rate
- 0 term with positive balance (reject)

---

### 4.2 Monthly cashflow
Define:
- `income_base_pence`
- `essentials_base_pence`
- `debt_payments_pence`
- `mortgage_payment_base_pence`

Then:
- `cashflow_base = income_base - essentials_base - debt_payments - mortgage_payment_base`

**Stress adjustments**
- Income shock: `income_stress = income_base × (1 - shock_income%)`
- Inflation: `essentials_stress = essentials_base × (1 + inflation%)`
- Mortgage stress: stress rate affects mortgage payment

Then:
- `cashflow_stress = income_stress - essentials_stress - debt_payments - mortgage_payment_stress`

All calculations in pence with explicit rounding.

---

### 4.3 Savings path
Let `S0` be initial savings in pence, `CF` be stressed monthly cashflow in pence:

For `t = 0..H-1`:
- `S[t+1] = max(0, S[t] + CF)`

Derived:
- `min_savings = min(S)`
- `month_of_depletion` = first `t` where `S[t] == 0` (if any)
- `runway_months` = `month_of_depletion` if depletion occurs, else `None`

---

## 5) Edge cases (must be explicit) ⚠️
- zero income
- zero savings
- mortgage balance = 0
- 0% rate
- shock = 100%
- horizon_months = 0 (should return just initial savings)

---

## 6) Worked examples (testable) ✅
Provide at least 2 worked numeric examples with all intermediate steps:
- Example A: cashflow stays positive → savings grows
- Example B: cashflow negative → depletion month exists
