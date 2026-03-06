# POC Master Backlog — WS1 to WS9 (Inline, Single File) ✅

**Project:** UK Household Financial Stress Engine  
**Repo:** https://github.com/mpiposanchez-git/financial_stress_engine  
**Version:** v0.2.0  
**Date:** 2026-03-06  
**Audience:** product owner + GitHub Copilot coding agent + auditor/reviewer

> This is the **single, consolidated, Copilot‑ready backlog** containing PR‑sized tasks for **WS1–WS9**.  
> **WS5–WS8 are fully inlined** (no external references).

---

## How to use this file

1) Work in order: **WS1 → WS9** (unless you intentionally reorder).  
2) Create a branch per task: `poc/<task-id>-short-name`.  
3) Keep each PR small: one task, one PR.  
4) After each merge, append a 3–5 line entry to `docs/progress_log.md`.

---

## Global rules (non‑negotiable)

- **Auth always on** (Clerk). No bypass flags.  
- **Premium enforced server-side** (entitlement check), not only UI.  
- **No server-side persistence** of user scenario inputs/outputs.  
- **No request-body or token logging.**  
- **Money = integer pence**, **rates/shocks = integer bps**, explicit rounding (round-half-up).  
- **BHC** (Before Housing Costs) is the default for UK income percentile benchmarking.

---

## Standard acceptance commands

Backend:
```bash
uv run pytest services/api/tests -v
uv run ruff check services/api
```

Frontend:
```bash
cd apps/web
npm run test
npm run typecheck
```

---

# POC Master Backlog — WS1 to WS9 (Single File, Copilot‑Ready) ✅

**Project:** UK Household Financial Stress Engine  
**Repo:** https://github.com/mpiposanchez-git/financial_stress_engine  
**Version:** v0.1.0  
**Date:** 2026-03-06  
**Audience:** product owner + GitHub Copilot coding agent + auditor/reviewer

> This is a **single consolidated backlog** containing PR‑sized tasks for **WS1–WS9**.  
> Each task includes: intent, files, requirements, tests, acceptance criteria, and a copy/paste Copilot prompt.

---

## How to use this file (simple operating rhythm)

1) Work in order: **WS1 → WS9** (unless you intentionally reorder).  
2) Create a branch per task: `poc/<task-id>-short-name`  
3) For each task: run tests + lint and keep PRs small.  
4) Log completion in `docs/progress_log.md` (date, task ID, PR link).
6) Log decisions in `docs/decision_log.md` according to template.
7) Log changes in `docs/CHANGELOG.md` according to template.

---

## Global rules (non‑negotiable)

- **Auth always on** (Clerk). No bypass flags.
- **Premium must be enforced server-side** (entitlement check), not only UI.
- **No server-side persistence** of user scenario inputs/outputs.
- **No request-body or token logging**.
- **Money = integer pence**, **rates = integer bps**, explicit rounding.

---

## Standard acceptance commands

Backend:
```bash
uv run pytest services/api/tests -v
uv run ruff check services/api
```

Frontend:
```bash
cd apps/web
npm run test
npm run typecheck
```

---

# WS1 — Engine modular refactor (UDF separation)

> Objective: modularity + auditability. Each “math family” lives in its own file.

## WS1-01 — Mortgage module extraction

**Files**
- CREATE: `shared/engine/mortgage.py`
- MODIFY: `shared/engine/deterministic.py`
- MODIFY: `shared/engine/montecarlo.py` (only if it computes payments)
- CREATE: `services/api/tests/test_mortgage_math.py`

**Requirements**
- Implement:
  - `mortgage_payment_interest_only(balance_pence:int, annual_rate_bps:int) -> int`
  - `mortgage_payment_repayment(balance_pence:int, annual_rate_bps:int, term_months:int) -> int`
- Handle edge cases (0 rate, 0 balance, invalid term).

**Copilot prompt**
```text
Implement TASK WS1-01 — Mortgage module extraction

Create shared/engine/mortgage.py with interest-only and repayment payment functions (pence/bps).
Refactor shared/engine/deterministic.py to call the new functions.
Add services/api/tests/test_mortgage_math.py covering edge cases and known numeric outputs.
Run pytest and ruff.
```

---

## WS1-02 — Savings path module extraction

**Files**
- CREATE: `shared/engine/savings_path.py`
- MODIFY: `shared/engine/deterministic.py`
- MODIFY: `shared/engine/outputs.py`
- CREATE: `services/api/tests/test_savings_path.py`

**Requirements**
- Implement:
  - `compute_savings_path(s0_pence:int, cashflows_pence:list[int]) -> list[int]` (floor at 0)
  - `month_of_depletion(path:list[int]) -> int|None`
  - `min_savings(path:list[int]) -> int`
- Deterministic outputs must include full path for horizon.

**Copilot prompt**
```text
Implement TASK WS1-02 — Savings path module extraction

Create shared/engine/savings_path.py with savings path + depletion helpers.
Refactor deterministic to use it and return savings_path in outputs.
Add services/api/tests/test_savings_path.py with a hand-computed scenario.
Run pytest and ruff.
```

---

## WS1-03 — Shock process module extraction (IID + AR(1))

**Files**
- CREATE: `shared/engine/shock_process.py`
- MODIFY: `shared/engine/montecarlo.py`
- CREATE: `services/api/tests/test_shock_process.py`

**Requirements**
- Implement generators producing month-by-month bps paths:
  - IID (Normal around mu, sigma)
  - AR(1) (phi persistence)
- Must support seed reproducibility.
- Clipping bounds explicit.

**Copilot prompt**
```text
Implement TASK WS1-03 — Shock process module extraction

Create shared/engine/shock_process.py implementing IID and AR(1) bps path generation with seed.
Refactor shared/engine/montecarlo.py to use it.
Add services/api/tests/test_shock_process.py for seed reproducibility and phi behavior.
Run pytest and ruff.
```

---

## WS1-04 — Engine output schema consistency

**Files**
- MODIFY: `shared/engine/outputs.py`
- MODIFY: `services/api/app/models.py`
- MODIFY: `services/api/app/routes.py`
- MODIFY: `services/api/tests/test_api_contracts.py`

**Requirements**
- Ensure deterministic and MC outputs have stable, documented fields.
- Align API response DTOs with engine outputs; remove dead/unused schemas.

**Copilot prompt**
```text
Implement TASK WS1-04 — Output schema consistency

Align shared/engine/outputs.py with services/api/app/models.py.
Ensure routes return DTOs consistently and update contract tests to match.
Remove unused/duplicate output models if present.
Run pytest and ruff.
```

---

# WS2 — Free tier wizard + baseline deterministic UX

> Objective: replace demo payload with real wizard, strong validation, accessible UI.

## WS2-01 — Wizard skeleton + navigation

**Files**
- MODIFY: `apps/web/src/pages/StressTestPage.tsx`
- CREATE: `apps/web/src/components/wizard/Wizard.tsx`
- CREATE: `apps/web/src/components/wizard/WizardStep.tsx`
- CREATE: `apps/web/src/components/wizard/WizardNav.tsx`
- CREATE: `apps/web/src/pages/StressTestPage.test.tsx`

**Requirements**
- Multi-step container with Next/Back.
- Keyboard-accessible navigation and focus.

**Copilot prompt**
```text
Implement TASK WS2-01 — Wizard skeleton + navigation

Create Wizard components and refactor StressTestPage to use them.
Add basic tests for step navigation and presence of labels.
Run npm test + typecheck.
```

---

## WS2-02 — Money input + currency select components

**Files**
- CREATE: `apps/web/src/components/inputs/MoneyInput.tsx`
- CREATE: `apps/web/src/components/inputs/CurrencySelect.tsx`
- MODIFY: `apps/web/src/pages/StressTestPage.tsx`
- CREATE: `apps/web/src/components/inputs/MoneyInput.test.tsx`

**Requirements**
- Money input supports:
  - amount field (string/number)
  - currency (GBP/EUR/USD)
  - validation display (aria-describedby)

**Copilot prompt**
```text
Implement TASK WS2-02 — MoneyInput + CurrencySelect

Create MoneyInput and CurrencySelect components with labels and accessible error display.
Integrate into the wizard for income and essentials steps.
Add unit tests.
```

---

## WS2-03 — Mortgage step UI (type, term, rates, stress)

**Files**
- CREATE: `apps/web/src/components/inputs/MortgageInputs.tsx`
- MODIFY: `apps/web/src/pages/StressTestPage.tsx`
- CREATE: `apps/web/src/components/inputs/MortgageInputs.test.tsx`

**Requirements**
- Capture:
  - balance + currency
  - mortgage type (repayment/interest-only)
  - term months/years
  - current rate % (or bps)
  - stressed rate % (or bps)

**Copilot prompt**
```text
Implement TASK WS2-03 — Mortgage step UI

Create MortgageInputs.tsx and wire it into the wizard.
Validation: term required if balance>0; rate bounds >=0.
Add tests for rendering and validation messages.
```

---

## WS2-04 — Stress sliders (income/inflation/rate/FX)

**Files**
- CREATE: `apps/web/src/components/inputs/PercentSlider.tsx`
- MODIFY: `apps/web/src/pages/StressTestPage.tsx`
- CREATE: `apps/web/src/components/inputs/PercentSlider.test.tsx`

**Requirements**
- Sliders update the scenario state; show value in % and bps.

**Copilot prompt**
```text
Implement TASK WS2-04 — Stress sliders

Create PercentSlider and add to wizard steps for income shock, inflation, stressed rate, FX stress.
Add tests for value changes.
```

---

## WS2-05 — Review + Run (call deterministic endpoint)

**Files**
- MODIFY: `apps/web/src/api/client.ts`
- MODIFY: `apps/web/src/pages/StressTestPage.tsx`
- MODIFY: `apps/web/src/pages/ResultsPage.tsx`
- CREATE: `apps/web/src/lib/buildPayload.ts`

**Requirements**
- Build deterministic request payload from wizard state.
- Call API; route to Results page with response.

**Copilot prompt**
```text
Implement TASK WS2-05 — Review + Run deterministic

Create buildPayload.ts to convert wizard state into API request DTO.
Update api/client.ts with deterministic run call.
Update StressTestPage to run and navigate to ResultsPage.
```

---

## WS2-06 — Input diagnostics & quality checks (free)

**Files**
- CREATE: `apps/web/src/components/DiagnosticsPanel.tsx`
- MODIFY: `apps/web/src/pages/StressTestPage.tsx`
- CREATE: tests

**Requirements**
- Warnings:
  - essentials > income (warn)
  - savings=0 with deficit (warn)
  - missing FX=1.0 for reporting currency (error)

**Copilot prompt**
```text
Implement TASK WS2-06 — Diagnostics panel

Add DiagnosticsPanel and wire to wizard state.
Show warnings with “why this matters” tooltips.
Add tests for a few diagnostic conditions.
```

---

# WS3 — Deterministic results UX expansions (non-advice guidance)

## WS3-01 — Savings path chart + table (accessible)

**Files**
- CREATE: `apps/web/src/components/charts/SavingsPathChart.tsx`
- MODIFY: `apps/web/src/pages/ResultsPage.tsx`
- CREATE: `apps/web/src/components/charts/SavingsPathChart.test.tsx`

**Requirements**
- Chart + table + figcaption + text summary.

**Copilot prompt**
```text
Implement TASK WS3-01 — Savings path chart + table

Create SavingsPathChart.tsx with <figure>/<figcaption> and a text summary.
Render it in ResultsPage using deterministic savings_path.
Add tests for figcaption and summary.
```

---

## WS3-02 — Mortgage stress panel (free)

**Files**
- CREATE: `apps/web/src/components/MortgageStressPanel.tsx`
- MODIFY: `apps/web/src/pages/ResultsPage.tsx`

**Requirements**
- Show current vs stressed mortgage payment and delta, with plain-English explanation (no advice).

**Copilot prompt**
```text
Implement TASK WS3-02 — Mortgage stress panel

Create MortgageStressPanel.tsx and render in ResultsPage.
Include plain English text; avoid recommendation language.
Add a basic test.
```

---

## WS3-03 — Emergency fund adequacy (free)

**Files**
- CREATE: `apps/web/src/components/EmergencyFundCard.tsx`
- MODIFY: `apps/web/src/pages/ResultsPage.tsx`

**Requirements**
- Compute months of essentials covered and show explanation.

**Copilot prompt**
```text
Implement TASK WS3-03 — Emergency fund adequacy card

Create EmergencyFundCard.tsx computing months of essentials from outputs.
Render in ResultsPage and add a basic test.
```

---

## WS3-04 — Explain-the-result narrative + glossary tooltips (free)

**Files**
- CREATE: `apps/web/src/components/ExplainResult.tsx`
- CREATE: `apps/web/src/components/GlossaryTooltip.tsx`
- MODIFY: `apps/web/src/pages/ResultsPage.tsx`
- CREATE: tests

**Requirements**
- Narrative: what drove runway; definitions for key terms.

**Copilot prompt**
```text
Implement TASK WS3-04 — Explain-the-result + glossary tooltips

Create ExplainResult and GlossaryTooltip components.
Render narrative in ResultsPage.
Add tests that key terms render and tooltips exist.
```

---

## WS3-05 — Assumptions panel (limits + rounding + caps)

**Files**
- CREATE: `apps/web/src/components/AssumptionsPanel.tsx`
- MODIFY: `apps/web/src/pages/ResultsPage.tsx`

**Requirements**
- Show horizon, pence/bps, rounding policy, MC caps (locked if premium), data timestamps placeholder.

**Copilot prompt**
```text
Implement TASK WS3-05 — Assumptions panel

Create AssumptionsPanel.tsx and render in ResultsPage.
Include transparency items; keep wording educational.
```

---

## WS3-06 — Official resource signposting (free)

**Files**
- CREATE: `apps/web/src/components/OfficialResources.tsx`
- MODIFY: `apps/web/src/pages/ResultsPage.tsx`

**Requirements**
- Links to MoneyHelper and Citizens Advice; “information only” disclaimer.

**Copilot prompt**
```text
Implement TASK WS3-06 — Official resource signposting

Create OfficialResources.tsx with curated links and disclaimers.
Render on ResultsPage.
```

---

# WS4 — Scenario compare + local-only saving

## WS4-01 — Scenario tabs (Base + A + B + C UI)

**Files**
- CREATE: `apps/web/src/components/scenarios/ScenarioTabs.tsx`
- MODIFY: `apps/web/src/pages/StressTestPage.tsx`

**Requirements**
- Allow cloning Base into A/B/C and editing sliders.
- Premium-gate extra scenarios beyond Base (server gating later).

**Copilot prompt**
```text
Implement TASK WS4-01 — Scenario tabs UI

Create ScenarioTabs.tsx allowing Base/A/B/C editing by cloning Base.
Integrate into wizard.
Ensure UI works even before compare endpoint exists.
Add tests for tab switching.
```

---

## WS4-02 — Scenario compare backend (premium)

**Files**
- MODIFY: `services/api/app/models.py`
- CREATE: `services/api/app/routes_compare.py` (or extend routes)
- MODIFY: `services/api/app/main.py`
- CREATE: `services/api/tests/test_compare_endpoint.py`

**Requirements**
- Endpoint `POST /api/v1/compare/run`:
  - takes list of scenarios
  - runs deterministic for each
  - returns comparison table
- Premium gated.

**Copilot prompt**
```text
Implement TASK WS4-02 — Scenario compare endpoint (premium)

Add POST /api/v1/compare/run gated by require_premium.
DTOs: list of scenario inputs + names.
Return list of scenario outputs for comparison.
Add tests for 403 non-premium and 200 premium.
```

---

## WS4-03 — Scenario compare UI (premium)

**Files**
- CREATE: `apps/web/src/components/scenarios/ScenarioCompareTable.tsx`
- MODIFY: `apps/web/src/pages/ResultsPage.tsx`

**Requirements**
- Display side-by-side runway, depletion month, min savings, mortgage payments.

**Copilot prompt**
```text
Implement TASK WS4-03 — Scenario compare UI

Create ScenarioCompareTable.tsx to render compare API result.
Render in ResultsPage for premium users; locked otherwise.
Add tests for headers and rows.
```

---

## WS4-04 — Local-only scenario store (hybrid)

**Files**
- CREATE: `apps/web/src/lib/storage/localScenarioStore.ts`
- CREATE: `apps/web/src/components/scenarios/SavedScenarios.tsx`
- MODIFY: `apps/web/src/pages/StressTestPage.tsx`
- CREATE: tests

**Requirements**
- Store scenarios only in browser storage.
- Free limit 2; premium unlimited.
- Must warn: “saved only on this device”.

**Copilot prompt**
```text
Implement TASK WS4-04 — Local-only scenario store

Create localScenarioStore.ts and SavedScenarios.tsx.
Integrate save/load into wizard.
Enforce free limit 2 vs premium unlimited.
Add tests for store get/set and UI warning.
```

---

# WS5 — Premium modelling (granular)

## WS5-F05-01 — Monte Carlo DTO alignment + API contract hardening
**Goal:** ensure MC response contains exactly what the UI needs (and is stable).

**Files**
- READ: `services/api/app/models.py`, `services/api/app/routes.py`
- MODIFY: `services/api/app/models.py`
- MODIFY: `services/api/app/routes.py`
- MODIFY: `services/api/tests/test_api_contracts.py`

**Requirements**
1) MC response must include:
   - P10/P50/P90 for: runway_months, min_savings, month_of_depletion
   - runtime_ms, seed, horizon_months, n_sims
2) Ensure types are explicit and stable (no optional surprises).
3) Contract test asserts presence and types.

**Copilot prompt**
```text
Implement TASK WS5-F05-01 — Monte Carlo DTO alignment + API contract hardening

Update services/api/app/models.py and services/api/app/routes.py so Monte Carlo response includes:
- runway_months_p10/p50/p90
- min_savings_p10/p50/p90
- month_of_depletion_p10/p50/p90
- runtime_ms, seed, horizon_months, n_sims

Update services/api/tests/test_api_contracts.py to assert keys and types.
Run backend tests and ruff.
```

---

## WS5-F05-02 — Fan chart UI (table-first, chart-second)
**Goal:** ship MC value in UI safely even before complex charting.

**Files**
- READ: `apps/web/src/pages/ResultsPage.tsx`, `apps/web/src/api/client.ts`
- CREATE: `apps/web/src/components/charts/FanChart.tsx`
- MODIFY: `apps/web/src/pages/ResultsPage.tsx`
- MODIFY: `apps/web/src/api/client.ts`
- CREATE: `apps/web/src/components/charts/FanChart.test.tsx` (or ResultsPage test)

**Requirements**
1) Add a premium section that shows:
   - a table of P10/P50/P90 for runway, min savings, depletion month
2) Add a simple “fan chart” visual:
   - if you don’t have path percentiles yet, render a lightweight band component (placeholder),
   - clearly label “summary percentiles”.
3) Must display LockedCard when not premium.

**Copilot prompt**
```text
Implement TASK WS5-F05-02 — Fan chart UI (table-first)

Create FanChart.tsx that renders P10/P50/P90 table and a simple band visualization.
Update ResultsPage.tsx to show it for premium users; locked otherwise.
Add tests that fan chart renders headings and values when provided.
Run npm test + typecheck.
```

---

## WS5-F12-01 — Sensitivity engine: perturbation calculator (no UI yet)
**Goal:** compute tornado inputs deterministically.

**Files**
- CREATE: `shared/engine/sensitivity.py`
- READ/MODIFY: `shared/engine/deterministic.py` (reusable runner)
- CREATE: `services/api/tests/test_sensitivity.py`

**Requirements**
1) Implement `compute_sensitivity(...)`:
   - base scenario
   - perturb one driver at a time by `delta_bps`:
     - income shock, inflation, mortgage stress rate, fx stress
2) Output: list of drivers with impact on runway_months (or min_savings).
3) Must be deterministic and unit-tested.

**Copilot prompt**
```text
Implement TASK WS5-F12-01 — Sensitivity engine perturbation calculator

Create shared/engine/sensitivity.py with compute_sensitivity that perturbs each driver by delta_bps and recomputes deterministic outputs.
Return ordered impacts.
Add services/api/tests/test_sensitivity.py with a small scenario asserting impacts are computed and sorted.
Run pytest.
```

---

## WS5-F12-02 — Sensitivity API endpoint (premium gated)
**Goal:** expose sensitivity outputs via API.

**Files**
- CREATE: `services/api/app/routes_sensitivity.py` (or extend routes.py if you keep single router)
- MODIFY: `services/api/app/main.py` (router include)
- MODIFY: `services/api/app/models.py` (request/response DTOs)
- CREATE: `services/api/tests/test_sensitivity_endpoint.py`

**Requirements**
1) Endpoint: `POST /api/v1/sensitivity/run`
2) Requires premium entitlement
3) Returns ranked drivers with numeric impacts

**Copilot prompt**
```text
Implement TASK WS5-F12-02 — Sensitivity endpoint (premium gated)

Add POST /api/v1/sensitivity/run, gated by require_premium.
Define DTOs in services/api/app/models.py.
Add endpoint tests: non-premium gets 403; premium returns ranked drivers.
Run pytest.
```

---

## WS5-F12-03 — Tornado chart UI
**Goal:** visualize sensitivity drivers.

**Files**
- CREATE: `apps/web/src/components/charts/TornadoChart.tsx`
- MODIFY: `apps/web/src/pages/ResultsPage.tsx`
- CREATE: `apps/web/src/components/charts/TornadoChart.test.tsx`

**Requirements**
1) Use API call to fetch sensitivity results
2) Render ranked bars and a text summary (accessibility)
3) LockedCard when not premium

**Copilot prompt**
```text
Implement TASK WS5-F12-03 — Tornado chart UI

Create TornadoChart.tsx and render in ResultsPage for premium users.
Add accessible figcaption + text summary.
Add test ensuring labels render.
```

---

## WS5-F13-01 — Schedule schema + engine application (deterministic only)
**Goal:** implement schedules safely in deterministic first.

**Files**
- CREATE: `shared/engine/schedules.py`
- MODIFY: `shared/engine/inputs.py` (schedule DTO)
- MODIFY: `shared/engine/deterministic.py`
- CREATE: `services/api/tests/test_schedules_deterministic.py`

**Requirements**
1) Schedule types:
   - step
   - ramp (linear from month 1 to month k)
   - stepped list [(month, level_bps)]
2) Apply schedule to:
   - income shock and/or inflation shock and/or rate stress
3) Unit tests for each schedule type.

**Copilot prompt**
```text
Implement TASK WS5-F13-01 — Shock schedules in deterministic engine

Add shared/engine/schedules.py with step/ramp/stepped schedules.
Extend shared/engine/inputs.py to accept optional schedule objects.
Update deterministic engine to compute month-by-month cashflow using scheduled shocks.
Add tests for schedule behavior.
```

---

## WS5-F13-02 — Schedules in Monte Carlo (monthly paths)
**Goal:** allow scheduled means (mu) plus stochastic variation.

**Files**
- MODIFY: `shared/engine/montecarlo.py`
- MODIFY: `shared/engine/shock_process.py`
- CREATE: `services/api/tests/test_schedules_montecarlo.py`

**Requirements**
1) If schedule is provided, schedule defines monthly mean path `mu_t`.
2) Shock process draws around `mu_t` (IID/AR1).
3) Seed reproducibility preserved.

**Copilot prompt**
```text
Implement TASK WS5-F13-02 — Schedules in Monte Carlo

Update montecarlo.py and shock_process.py so scheduled mean paths are supported.
Add tests for seed reproducibility with schedules.
```

---

## WS5-F08-01 — Category inflation model (engine only)
**Goal:** split essentials into categories with separate inflation.

**Files**
- CREATE: `shared/engine/inflation_categories.py`
- MODIFY: `shared/engine/inputs.py`
- MODIFY: `shared/engine/deterministic.py`
- CREATE: `services/api/tests/test_category_inflation.py`

**Requirements**
1) Optional `essentials_categories` mapping:
   - category_name → monthly_spend_pence + inflation_bps
2) If provided, total essentials = sum categories; stressed essentials uses per-category inflation.
3) Backwards compatible: if not provided, use single essentials bucket.

**Copilot prompt**
```text
Implement TASK WS5-F08-01 — Category inflation (engine)

Add inflation_categories.py and extend inputs to accept categories.
Update deterministic to compute stressed essentials per category when provided.
Add tests for category inflation vs single bucket equivalence.
```

---

## WS5-F08-02 — Category inflation UI (premium)
**Goal:** UI toggles for category splits.

**Files**
- MODIFY: `apps/web/src/pages/StressTestPage.tsx`
- CREATE: `apps/web/src/components/inputs/CategoryInflationEditor.tsx`
- CREATE: tests for editor

**Requirements**
1) Premium users can toggle “use categories”
2) Editor captures category spends + inflation bps
3) Non-premium users see LockedCard / teaser

**Copilot prompt**
```text
Implement TASK WS5-F08-02 — Category inflation UI (premium)

Create CategoryInflationEditor.tsx and integrate into wizard.
Gate behind premium.
Add tests for rendering and basic validation.
```

---

## WS5-F14-01 — Debt schedule engine (simple amortisation)
**Goal:** add optional unsecured debt dynamics.

**Files**
- CREATE: `shared/engine/debt.py`
- MODIFY: `shared/engine/inputs.py`
- MODIFY: `shared/engine/deterministic.py`
- CREATE: `services/api/tests/test_debt_schedule.py`

**Requirements**
1) Debt item:
   - balance_pence, apr_bps, min_payment_pence
2) Monthly update:
   - interest accrues
   - payment reduces balance (min of payment and balance+interest)
3) Debt payments included in cashflow; return debt balance path as optional output.

**Copilot prompt**
```text
Implement TASK WS5-F14-01 — Debt schedule engine

Create shared/engine/debt.py with a simple monthly amortisation.
Extend inputs for optional debts list.
Update deterministic to compute debt payment path and include in cashflow.
Add tests for payoff and interest accrual.
```

---

# WS6 — Data module (sources, verification, auto-fetch, overrides)

## WS6-A01-01 — Data registry (static) + Data Sources page
**Goal:** ship transparency first, fetch later.

**Files**
- CREATE: `services/api/app/data_registry.py`
- MODIFY: `services/api/app/routes.py` (GET /api/v1/data/registry)
- CREATE: `apps/web/src/pages/DataSourcesPage.tsx`
- MODIFY: `apps/web/src/App.tsx` (route)
- CREATE: `apps/web/src/pages/DataSourcesPage.test.tsx`

**Requirements**
1) Registry includes each dataset with:
   - name, provider, url, refresh cadence, license note
   - verification steps (numbered)
2) UI renders the registry cleanly.

**Copilot prompt**
```text
Implement TASK WS6-A01-01 — Data registry + Data Sources page

Add data_registry.py and GET /api/v1/data/registry.
Create DataSourcesPage.tsx to render it.
Add tests that dataset names and URLs appear.
```

---

## WS6-A01-02 — Data cache abstraction
**Goal:** create a clean seam for cron fetcher to write into.

**Files**
- CREATE: `services/api/app/data_cache.py`
- CREATE: `services/api/tests/test_data_cache.py`

**Requirements**
1) Cache API:
   - `get(key)`, `set(key, value, meta)`
   - meta includes fetched_at_utc, source_url, sha256
2) Default implementation: in-memory dict (POC)

**Copilot prompt**
```text
Implement TASK WS6-A01-02 — Data cache abstraction

Create services/api/app/data_cache.py with simple in-memory cache + metadata.
Add tests for set/get behavior.
```

---

## WS6-A01-03 — Fetcher: BoE Bank Rate
**Files**
- CREATE: `services/api/app/fetchers/boe_bank_rate.py`
- MODIFY: `services/api/app/data_fetcher.py`
- CREATE: `services/api/tests/test_fetch_boe_bank_rate.py`

**Requirements**
1) Fetch latest Bank Rate value + date.
2) Store in cache under key `boe_bank_rate`.
3) Test uses mocked HTTP response (no live calls in unit tests).

**Copilot prompt**
```text
Implement TASK WS6-A01-03 — Fetch BoE Bank Rate

Create fetchers/boe_bank_rate.py that parses Bank Rate from BoE source.
Integrate into data_fetcher refresh-all.
Mock HTTP in tests.
```

---

## WS6-A01-04 — Fetcher: BoE FX spot rates (GBP base)
**Files**
- CREATE: `services/api/app/fetchers/boe_fx.py`
- MODIFY: `services/api/app/data_fetcher.py`
- CREATE: `services/api/tests/test_fetch_boe_fx.py`

**Requirements**
1) Fetch spot rates needed for GBP/EUR/USD (minimum).
2) Store in cache under key `boe_fx_spot`.
3) Clearly mark as “indicative/not official” in registry meta.

**Copilot prompt**
```text
Implement TASK WS6-A01-04 — Fetch BoE FX spot rates

Create fetchers/boe_fx.py to fetch and parse EUR and USD rates vs GBP.
Integrate into refresh-all and store in cache.
Mock HTTP in tests.
```

---

## WS6-A01-05 — Fetcher: ONS CPI/CPIH (latest 12m rate)
**Files**
- CREATE: `services/api/app/fetchers/ons_cpi.py`
- MODIFY: `services/api/app/data_fetcher.py`
- CREATE: `services/api/tests/test_fetch_ons_cpi.py`

**Requirements**
1) Fetch CPIH (or CPI) latest annual rate and month.
2) Store in cache under `ons_cpih_12m` and metadata.
3) Unit test with mocked response.

**Copilot prompt**
```text
Implement TASK WS6-A01-05 — Fetch ONS CPIH/CPI

Create fetchers/ons_cpi.py that parses latest CPIH 12m rate from ONS dataset.
Integrate into refresh-all, store in cache, mock HTTP in tests.
```

---

## WS6-A01-06 — Fetcher: Ofgem price cap (basic snapshot)
**Files**
- CREATE: `services/api/app/fetchers/ofgem_cap.py`
- MODIFY: `services/api/app/data_fetcher.py`
- CREATE: `services/api/tests/test_fetch_ofgem_cap.py`

**Requirements**
1) Fetch a minimal “headline” or table snapshot for a chosen region (or national default).
2) Store in cache under `ofgem_price_cap`.
3) Unit test with mocked HTML/table.

**Copilot prompt**
```text
Implement TASK WS6-A01-06 — Fetch Ofgem price cap snapshot

Create fetchers/ofgem_cap.py to parse a minimal unit-rate snapshot (start with a single region).
Integrate into refresh-all and cache it.
Mock in tests.
```

---

## WS6-A01-07 — Fetcher: DWP HBAI ZIP (store raw)
**Files**
- CREATE: `services/api/app/fetchers/dwp_hbai.py`
- MODIFY: `services/api/app/data_fetcher.py`
- CREATE: `services/api/tests/test_fetch_hbai_zip.py`

**Requirements**
1) Download the HBAI tables ZIP and store raw bytes in cache (or filesystem path).
2) Compute sha256.
3) Do not parse yet (WS7 will parse).

**Copilot prompt**
```text
Implement TASK WS6-A01-07 — Fetch DWP HBAI ZIP (raw storage)

Create fetchers/dwp_hbai.py to download the tables ZIP.
Store bytes + sha256 + fetched_at in cache.
Mock HTTP in tests.
```

---

## WS6-A01-08 — Defaults endpoint + override integration
**Files**
- MODIFY: `services/api/app/routes.py` (GET /api/v1/data/defaults)
- MODIFY: `apps/web/src/pages/StressTestPage.tsx` (use defaults, allow override)

**Requirements**
1) `/api/v1/data/defaults` returns:
   - bank_rate_bps default
   - cpih_12m_bps default
   - fx_spot rates for EUR/USD
   - energy reference values (optional)
   - fetched_at timestamps
2) UI shows “Use defaults” toggle and allows manual override.

**Copilot prompt**
```text
Implement TASK WS6-A01-08 — Defaults endpoint + override integration

Add GET /api/v1/data/defaults returning latest cached values and timestamps.
Update wizard to prefill and allow manual overrides.
Add basic UI tests.
```

---

## WS6-A01-09 — Cron refresh command wiring (Render)
**Files**
- CREATE: `services/api/app/data_fetcher.py` CLI entrypoint (if not already)
- UPDATE docs: `docs/runbook.md` (or create `docs/data_refresh.md`)

**Requirements**
1) Command: `uv run python -m services.api.app.data_fetcher refresh-all`
2) Document Render Cron Job setup steps.
3) Ensure no secrets in docs.

**Copilot prompt**
```text
Implement TASK WS6-A01-09 — Cron refresh command wiring + docs

Ensure data_fetcher has a module entrypoint refresh-all.
Write docs/data_refresh.md explaining how to set up a Render Cron Job to run it.
```

---

# WS7 — UK benchmarks (BHC reference values + premium percentile)

## WS7-A02-01 — Reference values endpoint (free)
**Files**
- CREATE: `services/api/app/benchmarks/reference_values.py`
- MODIFY: `services/api/app/routes.py` (GET /api/v1/benchmarks/uk/reference)
- CREATE: `services/api/tests/test_reference_values.py`

**Requirements**
1) Return a small set:
   - income_median_bhc (year-labeled)
   - optionally deciles if you can extract them
2) Include provenance:
   - source_url, fetched_at, sha256

**Copilot prompt**
```text
Implement TASK WS7-A02-01 — UK reference values endpoint

Create reference_values.py reading from cached HBAI (or a static placeholder until parsed).
Expose GET /api/v1/benchmarks/uk/reference.
Add tests.
```

---

## WS7-A02-02 — HBAI ZIP parser (extract table)
**Files**
- CREATE: `shared/engine/benchmarks/hbai_parser.py`
- CREATE: `services/api/tests/test_hbai_parser.py`

**Requirements**
1) Given raw ZIP bytes, locate an ODS containing distribution table(s).
2) Extract a decile threshold table (POC) for BHC.
3) Unit test using a small fixture (you can store a tiny synthetic ODS fixture if licensing allows; otherwise mock parser output).

**Copilot prompt**
```text
Implement TASK WS7-A02-02 — HBAI ZIP parser (BHC deciles)

Create hbai_parser.py that can extract BHC decile thresholds from HBAI ZIP.
Write tests using mocked parsed data if real fixtures are not feasible.
```

---

## WS7-A02-03 — Percentile computation (premium)
**Files**
- CREATE: `shared/engine/benchmarks/income_percentile.py`
- CREATE: `services/api/app/benchmarks/percentile.py`
- MODIFY: `services/api/app/routes.py` (POST /api/v1/benchmarks/uk/percentile, premium)
- CREATE: `services/api/tests/test_percentile_endpoint.py`

**Requirements**
1) Input: annual net income in reporting currency.
2) Output: percentile bucket (10,20,…,90) + year + caveats.
3) Must be premium-gated.
4) UI disclosure (WS0-A06) must be displayed.

**Copilot prompt**
```text
Implement TASK WS7-A02-03 — Premium percentile endpoint (BHC)

Add income_percentile.py to compute bucket from decile thresholds.
Expose POST /api/v1/benchmarks/uk/percentile gated by require_premium.
Add endpoint tests for 403 non-premium and valid output premium.
```

---

## WS7-A02-04 — UI integration for UK context + premium ranking
**Files**
- MODIFY: `apps/web/src/pages/ResultsPage.tsx`
- CREATE: `apps/web/src/components/benchmarks/UKContextBox.tsx`
- CREATE: `apps/web/src/components/benchmarks/UKRankingCard.tsx`

**Requirements**
1) Always show UK context box (free):
   - median reference values + year + source link
2) Premium users see ranking card:
   - percentile bucket + disclosure component

**Copilot prompt**
```text
Implement TASK WS7-A02-04 — UI UK benchmarks integration

Create UKContextBox and UKRankingCard components.
Show reference values for all users and ranking only for premium.
Include PercentileDisclosure component.
Add basic tests.
```

---

# WS8 — Exports (JSON + PDF)

## WS8-F06-01 — PDF generator core (ReportLab)
**Files**
- CREATE: `shared/engine/reports/pdf_report.py`
- CREATE: `services/api/tests/test_pdf_report.py`

**Requirements**
1) Generate PDF bytes from:
   - inputs + outputs
   - disclaimers
   - provenance block (dataset timestamps/hashes)
2) PDF must be deterministic for same inputs (no random IDs/time in content unless explicitly included).

**Copilot prompt**
```text
Implement TASK WS8-F06-01 — PDF generator core

Create pdf_report.py using reportlab.
Add a unit test that generates PDF bytes and asserts:
- bytes length > 1000
- contains key headings when text extracted (best-effort)
```

---

## WS8-F06-02 — PDF API endpoint (premium)
**Files**
- MODIFY: `services/api/app/routes.py` (POST /api/v1/reports/pdf)
- MODIFY: `services/api/app/models.py` (PDF request DTO)
- CREATE: `services/api/tests/test_pdf_endpoint.py`

**Requirements**
1) Premium-gated endpoint.
2) Returns `application/pdf`.
3) Includes version metadata and disclaimers.

**Copilot prompt**
```text
Implement TASK WS8-F06-02 — PDF API endpoint (premium)

Add POST /api/v1/reports/pdf gated by require_premium.
Return application/pdf.
Add tests for 403 non-premium and 200 premium with correct content-type.
```

---

## WS8-F06-03 — PDF download UI (premium)
**Files**
- MODIFY: `apps/web/src/pages/ResultsPage.tsx`
- CREATE: `apps/web/src/components/PdfDownloadButton.tsx`
- CREATE: tests

**Requirements**
1) Premium: button downloads PDF.
2) Free: locked card with teaser.

**Copilot prompt**
```text
Implement TASK WS8-F06-03 — PDF download UI

Add PdfDownloadButton.tsx that calls the pdf endpoint and triggers browser download.
Gate behind premium.
Add tests ensuring locked state for non-premium.
```

---

## WS8-JSON-01 — JSON export hardening (always on)
**Files**
- MODIFY: `apps/web/src/pages/ResultsPage.tsx`
- CREATE: `apps/web/src/lib/exportJson.ts`

**Requirements**
1) Export JSON must include:
   - input payload
   - deterministic outputs
   - (if premium) MC outputs + sensitivity outputs
   - provenance metadata (data timestamps, model/app versions)
2) File name includes date (not time) and “reporting currency”.

**Copilot prompt**
```text
Implement TASK WS8-JSON-01 — JSON export hardening

Create exportJson.ts helper and update ResultsPage to export a complete bundle.
Add unit test for file name formatting and required keys.
```

---

# Suggested execution order (lowest risk → highest complexity)

1) WS5-F05-01 → WS5-F05-02  
2) WS5-F12-01 → WS5-F12-02 → WS5-F12-03  
3) WS6-A01-01 → WS6-A01-02 → WS6-A01-03/04/05/06/07 → WS6-A01-08 → WS6-A01-09  
4) WS7-A02-02 → WS7-A02-03 → WS7-A02-04 → WS7-A02-01  
5) WS8-JSON-01 → WS8-F06-01 → WS8-F06-02 → WS8-F06-03  
6) WS5-F13-01 → WS5-F13-02 → WS5-F08-01 → WS5-F08-02 → WS5-F14-01

---

**End of addendum.**

# WS9 — QA, audit pack, release discipline

## WS9-01 — Logging & sensitive-data guards (backend)
**Files**
- CREATE: `services/api/tests/test_no_sensitive_logging.py` (if not already)
- CREATE: `services/api/tests/test_no_payload_logging_config.py` (best-effort)
- MODIFY: `docs/disclaimers/privacy.md` (confirm logging posture)

**Requirements**
- CI fails if request body logging is introduced.
- No logs include Authorization headers or Bearer tokens.

**Copilot prompt**
```text
Implement TASK WS9-01 — Logging & sensitive-data guards

Add backend tests that scan services/api/app/*.py for request.body()/request.json() logging and Authorization/Bearer logging patterns.
Ensure tests fail with clear messages if patterns are present.
Update privacy docs only if needed for accuracy.
Run pytest.
```

---

## WS9-02 — Secrets hygiene (repo)
**Files**
- CREATE: `.gitattributes` (optional)
- CREATE: `.pre-commit-config.yaml` (optional)
- UPDATE: `README.md` (dev setup notes)

**Requirements**
- Add lightweight pre-commit hooks:
  - ruff
  - basic secrets pattern check (no keys committed)
- Do not block developer productivity.

**Copilot prompt**
```text
Implement TASK WS9-02 — Lightweight pre-commit hooks

Add a .pre-commit-config.yaml with ruff and a simple secrets pattern hook.
Document how to install pre-commit in README.
Do not add heavyweight tools.
```

---

## WS9-03 — Evidence pack & release checklist docs
**Files**
- CREATE: `docs/evidence_pack.md`
- MODIFY: `docs/CHANGELOG.md`
- MODIFY: `docs/progress_log.md`

**Requirements**
- Evidence pack includes:
  - exact commands to run
  - which artifacts to retain (CI link, test output, dataset hashes)
  - how to tag releases and capture commit SHA

**Copilot prompt**
```text
Implement TASK WS9-03 — Evidence pack + release checklist

Create docs/evidence_pack.md with step-by-step commands and artifact retention guidance.
Add a release checklist section to docs/CHANGELOG.md.
Ensure progress_log format is append-only.
```

---

## WS9-04 — Single-source-of-truth docs wiring
**Files**
- MODIFY: `README.md`
- ADD: `docs/commercial/poc_flyer.md`, `docs/methodology/methodology_textbook.md`, `docs/implementation/brd_implementation_plan.md`
- ADD: this backlog file as `docs/implementation/POC_BACKLOG_MASTER_WS1_WS9_INLINE.md`

**Requirements**
- README references all governance docs.
- Keep paths stable.

**Copilot prompt**
```text
Implement TASK WS9-04 — Wire docs into repo

Add the key docs into docs/ and update README References:
- docs/commercial/poc_flyer.md
- docs/methodology/methodology_textbook.md
- docs/implementation/brd_implementation_plan.md
- docs/implementation/POC_BACKLOG_MASTER_WS1_WS9_INLINE.md
Ensure links work in GitHub.
```

---

## WS9-05 — Tagging discipline (manual but documented)
**Requirement**
- For each milestone release:
  - tag: `poc-milestone-<n>-YYYY-MM-DD`
  - record SHA in PDF exports and docs

---

**End of WS1–WS9 master backlog.**



**End of master backlog.**

<!-- crossref:start -->
## Related Documents

- [Repository README](../../README.md)
- [Methodology Golden Source](../methodology/methodology_textbook.md)
- [BRD Implementation Plan](brd_implementation_plan.md)
<!-- crossref:end -->

