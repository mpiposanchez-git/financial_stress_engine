# Proof of Concept Development Plan — UK Household Financial Stress Engine 🧠🛠️

**Audience:** smart beginner (teacher-mode).  
**POC goal:** a working, reproducible, auditable web app that runs **deterministic** and **Monte Carlo** household stress tests end-to-end in a **UK context** (GBP by default), with support for **multi-currency inputs** and **FX risk**.

---

## 0) What we’re building (plain English) 🎓

You will build a tool that answers questions like:

- *“If my income drops and my mortgage rate rises, how long will my savings last?”*
- *“What happens if inflation stays high?”*
- *“If I hold some income/expenses in EUR and USD, what does FX volatility do to my runway when I view everything in GBP?”*

### Key outputs
- **Monthly cashflow** under base and stress assumptions.
- **Savings runway** and **month-by-month savings path** over 24 months (default).
- (Monte Carlo) **P10 / P50 / P90** for runway and minimum savings under stochastic shocks.

### What this is *not*
- It is **not** financial advice.
- It does **not** recommend products, lenders, or strategies.
- It is an educational simulator.

---

## 1) Guardrails (mandatory) ⚖️

1) **Clerk authentication is always on**
   - No runtime bypass flags in production or local runs.
   - Testing uses mocks / dependency overrides.

2) **Numerical precision**
   - Money is computed as **integer pence** (`int`).
   - Rates are stored as **integer basis points** (`int`, e.g., 5.25% = 525).
   - Use `Decimal` internally only where necessary (e.g., amortisation exponentiation), then round/quantize to pennies.

3) **Deterministic engine is month-by-month**
   - The deterministic engine must produce a 24-month default savings path.

4) **Monte Carlo uses monthly stochastic paths**
   - Monthly IID shocks in POC.
   - Provide an optional “persistence” mode (AR(1)) design hook.

5) **Multi-currency**
   - Each money input can have a currency.
   - All results are shown in a selected **reporting currency**.
   - FX rates and FX volatility are modelled as a risk driver.

---

## 2) “Definition of Done” (DoD) ✅

A POC release is done only when:

### 2.1 Model correctness
- Specs exist and are kept current:
  - `docs/MOD-001_DETERMINISTIC_ENGINE_SPEC.md`
  - `docs/MOD-002_MONTE_CARLO_SPEC.md`
  - `docs/MOD-003_FX_MULTI_CURRENCY_SPEC.md`
- Unit tests and golden tests cover the model.

### 2.2 End-to-end app functionality
- User can:
  - log in via Clerk
  - enter inputs (including multiple currencies)
  - choose reporting currency
  - run deterministic and Monte Carlo
  - see results and export JSON

### 2.3 Auditability & traceability
- Every change links to:
  - a GitHub Issue/Task ID, and/or
  - a Decision ID (in `docs/decision_log.md`)
- CI must be green for merges.

---

## 3) The audit system (how we stay organised) 🧾

You will maintain three append-only logs:

1) **Decision Log** — “why we made choices”
   - File: `docs/decision_log.md`
2) **Progress Log** — “what we did this week/session”
   - File: `docs/progress_log.md`
3) **Changelog** — “what changed in releases”
   - File: `docs/CHANGELOG.md`

### Traceability rules
- GitHub Issues: `POC-001`, `POC-002`, ...
- Commit titles: `POC-012: <short message>`
- PR template: requires tests + docs checkbox ticked.

---

## 4) Milestones (the work in the right order) 🧩

### Milestone A — Governance + documentation consistency
**Deliverables**
- Remove any runtime auth bypass.
- `docs/privacy.md` updated to reflect Clerk usage.
- Model specs created (MOD-001/002/003).
- Add `docs/progress_log.md` and `docs/CHANGELOG.md`.

**Acceptance**
- A new developer can read docs and accurately explain:
  - auth
  - data handling
  - what the model does
  - what is stored (ideally nothing sensitive)

---

### Milestone B — Precision foundation (pence + bps) 💷
**Deliverables**
- `shared/engine/money.py` conversion + rounding utilities.
- Engine uses pence + bps in all core calculations.
- API accepts user-friendly values but converts at the engine boundary.

**Acceptance**
- No float arithmetic in engine core.
- Golden tests match penny-exact outputs.

---

### Milestone C — Deterministic month-by-month engine 📆
**Deliverables**
- Deterministic returns:
  - `savings_path` for 24 months (default)
  - `min_savings`, `month_of_depletion`, `runway_months`
  - base vs stress cashflow summary

**Acceptance**
- Golden test validates the full savings path.
- Runway matches first depletion month when depletion happens.

---

### Milestone D — FX + multi-currency support 🌍
**Deliverables**
- Inputs support per-field currency.
- Reporting currency selector.
- Deterministic converts all cashflows to reporting currency using:
  - user-provided FX rates (baseline), and
  - stressed FX scenarios (deterministic), and
  - stochastic FX paths (Monte Carlo).

**Acceptance**
- Unit tests cover currency conversion + rounding.
- Golden scenario includes 2 currencies and validates reporting-currency outputs.

---

### Milestone E — Monte Carlo monthly paths + optional AR(1) persistence 🎲
**Deliverables**
- Monte Carlo engine moved to shared engine module.
- Monthly IID draws per factor, per month, per simulation.
- Optional persistence mode (AR(1)) implemented or scaffolded behind a clear flag.

**Acceptance**
- Seeded runs are reproducible.
- `sigma > 0` widens distributions; `sigma = 0` collapses to deterministic-like behaviour.

---

### Milestone F — UI: real form + results UX 📊
**Deliverables**
- Real input form (no hard-coded payload).
- Reporting currency selection.
- Results page shows:
  - deterministic savings chart/table
  - Monte Carlo P10/P50/P90 summary
  - export JSON button

**Acceptance**
- User can complete a scenario without editing code.
- Copy is non-advice and clear.

---

## 5) Testing strategy (what to test, and why) 🧪

### 5.1 Unit tests
- Currency conversion and rounding
- Mortgage payment formulas (repayment + interest-only)
- Deterministic savings path update rule
- FX stress rules
- Monte Carlo seed reproducibility

### 5.2 Golden tests (known-answer)
Store scenarios under `docs/examples/`:
- `scenario_01_input.json`
- `scenario_01_expected.json`

Golden tests prevent regressions forever.

### 5.3 Contract tests
Keep API request/response shape stable. If it changes, version it and update changelog.

---

## 6) Copilot operating mode (how to avoid misunderstandings) 🤖

When instructing Copilot, always use:

- **Task ID**
- **Exact file list**
- **Exact acceptance criteria**
- **Tests required**

Example prompts are provided in `docs/POC_NEXT_STEPS.md`.

---

## 7) Recommended first sprint (smallest high-impact sequence) ✅

1) Remove auth bypass + fix privacy docs  
2) Introduce pence + bps utilities  
3) Deterministic month-by-month savings path  
4) FX + multi-currency deterministic conversion  
5) Monte Carlo monthly paths (+ AR(1) hook)  
6) UI form + reporting currency selector + results presentation

---

**End of plan.**
