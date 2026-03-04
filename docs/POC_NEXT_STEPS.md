# POC Next Steps — Concrete Implementation Sequence ✅

This is the “do this next” list aligned with your decisions:
1) Clerk always on (no bypass)
2) Exact arithmetic (pence + bps)
3) Deterministic month-by-month path (24m default)
4) Multi-currency + FX risk + reporting currency selection
5) Monte Carlo monthly paths + optional AR(1)
6) UI: real inputs + results UX

---

## Step 1 — Remove auth bypass and fix privacy docs (LEG-002)

### What to do
- Delete any runtime bypass flags in backend/frontend.
- Update `docs/privacy.md` to accurately describe Clerk usage and data handling.

### Acceptance criteria
- Unauthenticated requests fail in runtime environments.
- Tests still pass via mocks/overrides.
- Privacy doc is truthful.

### Copilot prompt
```text
Implement TASK: POC-001 — Remove runtime auth bypass (Clerk always on)

Files to read:
- services/api/app/auth.py
- services/api/app/main.py
- services/api/app/routes.py
- apps/web/src/main.tsx (and any auth wrappers)
- docs/privacy.md

Changes:
1) Remove any AUTH_DISABLED/VITE_AUTH_DISABLED runtime bypass logic.
2) Add a FastAPI dependency override fixture in tests to simulate an authenticated user.
3) Update docs/privacy.md to reflect Clerk usage and what data is stored (prefer stateless).

Tests:
- Update/add API tests to authenticate via override fixture.
- Ensure CI passes.

Acceptance:
- No runtime path allows unauthenticated access.
- All tests green.
```

---

## Step 2 — Exact money/rate utilities (TEC-004)

### What to do
- Create `shared/engine/money.py` with:
  - gbp_to_pence / pence_to_str
  - percent_to_bps / bps_to_decimal
  - explicit rounding rules (round-half-up)
- Convert engine internals to pence + bps.

### Copilot prompt
```text
Implement TASK: POC-002 — Exact arithmetic (pence + bps)

Create:
- shared/engine/money.py

Modify:
- shared/engine/inputs.py
- shared/engine/outputs.py
- shared/engine/deterministic.py
- services/api/app/models.py
- services/api/app/routes.py

Requirements:
1) Money computed as int pence internally.
2) Rates stored as int bps internally.
3) Explicit rounding rules implemented + unit tested.
4) Keep API JSON ergonomic: return both pence ints and formatted strings.

Tests:
- Unit tests for conversion + rounding.
- Update contract tests as needed.

Acceptance:
- pytest passes, CI green
- No float arithmetic in engine core.
```

---

## Step 3 — Deterministic month-by-month savings path (MOD-003)

### Copilot prompt
```text
Implement TASK: POC-003 — Deterministic month-by-month savings path

Modify:
- shared/engine/deterministic.py
- shared/engine/outputs.py
- shared/engine/inputs.py
- services/api/app/models.py
- services/api/app/routes.py
- apps/web/src/pages/ResultsPage.tsx (display savings path)

Requirements:
1) Add horizon_months with default 24.
2) Produce savings_path_pence length horizon+1.
3) Add min_savings_pence, month_of_depletion, runway_months.
4) Return formatted strings alongside pence ints.

Tests:
- Add golden test with explicit expected savings path.

Acceptance:
- All tests + CI green
- UI can display the path.
```

---

## Step 4 — Multi-currency + FX risk + reporting currency (MOD-005)

### What to implement first (POC)
- Support currencies: GBP/EUR/USD
- Add reporting currency selector
- Accept FX spot rates and FX stress parameters

### Copilot prompt
```text
Implement TASK: POC-004 — Multi-currency + FX risk + reporting currency

Create:
- shared/engine/fx.py (conversion + FX path helpers)
- docs/MOD-003_FX_MULTI_CURRENCY_SPEC.md

Modify:
- shared/engine/inputs.py (currency fields + reporting_currency + fx inputs)
- shared/engine/deterministic.py (convert all flows to reporting currency)
- shared/engine/outputs.py (include reporting currency + both pence and formatted)
- services/api/app/models.py and routes.py (wire through)
- apps/web/src/pages/StressTestPage.tsx (currency fields + reporting selection)

Requirements:
1) Each money input can carry a currency (GBP/EUR/USD).
2) Convert to reporting currency using spot FX.
3) Deterministic FX stress supported (simple % shock on FX).
4) Return outputs in reporting currency (pence + formatted).

Tests:
- Unit tests for FX conversion + rounding.
- Golden scenario with two currencies.

Acceptance:
- Tests + CI green
- UI shows reporting currency outputs correctly.
```

---

## Step 5 — Monte Carlo monthly paths + optional AR(1) persistence (MOD-004)

### Copilot prompt
```text
Implement TASK: POC-005 — Monte Carlo monthly paths + optional AR(1)

Create:
- shared/engine/montecarlo.py

Modify:
- services/api/app/routes.py (thin orchestration)
- services/api/app/models.py
- tests: services/api/tests/*
- docs/MOD-002_MONTE_CARLO_SPEC.md

Requirements:
1) Monthly shocks per sim per month (IID default).
2) Optional AR(1) shock_dynamics="ar1".
3) Include FX paths from fx module.
4) Seed reproducibility guarantee.
5) Output P10/P50/P90 for runway_months, min_savings_pence, month_of_depletion.

Tests:
- Reproducibility tests for iid and ar1.
- Sensitivity tests: sigma=0 collapses; sigma>0 widens.

Acceptance:
- CI green, stable outputs with seed.
```

---

## Step 6 — UI polish (PRD)
- Replace any hard-coded payload with forms.
- Add tooltips explaining each field in beginner-friendly language.
- Results show deterministic chart/table + Monte Carlo percentiles.

---

## Recommended sequencing
Do Steps 1→5 before heavy UI styling.
