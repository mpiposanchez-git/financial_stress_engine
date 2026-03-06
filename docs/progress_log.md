# Progress Log (Append-only) 🧾

> One entry per dev session or per week. Keep it factual and lightweight.

---

## YYYY-MM-DD — Session Title

### Completed
- POC-XXX: <short description> (PR/commit link)

### In progress
- POC-YYY: <next steps>

### Test evidence
- CI run: <link>
- Backend: `uv run pytest -v` ✅ / ❌
- Frontend: `cd apps/web && npm run test` ✅ / ❌

### Decisions made
- DECISION-ID: <summary> (link to `docs/decision_log.md`)

### Risks / Blockers
- <bullet list>

---

## 2026-03-06 — Immediate Next Steps Execution (POC Follow-Through)

### Completed
- POC-Release-Readiness: Frozen deployment configuration snapshot in the runbook, including canonical release tag/date and deployment variables.
- POC-Results-UI: Implemented chart-based Results view for Monte Carlo percentiles and deterministic savings path with responsive readability improvements.
- POC-Smoke-Automation: Added script and GitHub workflow for post-deploy smoke checks (`/health`, authenticated deterministic run, authenticated Monte Carlo run).
- POC-Auth-Diagnostics: Improved non-sensitive auth failure diagnostics in backend and frontend user-facing API error handling.
- POC-Observability-Basics: Documented baseline error-rate and latency checks and integrated latency thresholds into smoke automation.
- POC-Compliance-Docs: Refined disclaimer consistency to reflect current multi-currency behavior and refreshed review dates.

### In progress
- Introduce richer historical trend charts once persistent run history is available.

### Test evidence
- Frontend: `npm --prefix apps/web test -- --run` (to be re-run after changes)
- Backend: `uv run pytest services/api/tests -q` (to be re-run after changes)

### Decisions made
- Use non-sensitive auth diagnostics only (no token/body echo in UI or logs).
- Keep smoke checks manual-dispatch for now to avoid hard coupling with deployment timing across services.

### Risks / Blockers
- Smoke automation requires a valid short-lived `SMOKE_TEST_BEARER_TOKEN` secret.
- Post-deploy observability remains log-driven until metrics dashboards are introduced.

## 2026-03-06 — WS2-02 Money Inputs + Currency Select Components

### Completed
- WS2-02: Added reusable `MoneyInput` and `CurrencySelect` components with accessible labels and `aria-describedby` support for error association.
- WS2-02: Integrated `MoneyInput` for household monthly income and essentials values/currencies in `StressTestPage` wizard step 1.
- WS2-02: Added `MoneyInput` unit tests and kept existing stress page navigation/submission tests green.

### In progress
- WS2-03: Mortgage step UI extraction and validation wiring.

### Test evidence
- Frontend: `npm --prefix apps/web test -- --run` ✅ (`11 passed`)
- Frontend typecheck: `npm --prefix apps/web run typecheck` ✅
- Backend: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m pytest services/api/tests -q` ✅ (`42 passed`)
- Backend lint: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m ruff check .` ✅

### Decisions made
- Use shared input components for amount/currency pairs to reduce duplicate form logic ahead of additional wizard steps.

### Risks / Blockers
- Amount fields currently map directly to existing `*_gbp` API fields; true per-currency normalization remains a future enhancement.

## 2026-03-06 — WS2-03 Mortgage Step UI

### Completed
- WS2-03: Added `MortgageInputs` component covering mortgage balance + currency, mortgage type, term remaining (years), current rate, and stressed rate.
- WS2-03: Wired `MortgageInputs` into `StressTestPage` as a dedicated middle wizard step; updated wizard flow from 2 to 3 steps.
- WS2-03: Added mortgage input unit tests for rendering and validation messages (`term required when balance > 0`, `rate >= 0`).

### In progress
- WS2-04: Stress slider controls for shock/stress parameter tuning.

### Test evidence
- Frontend: `npm --prefix apps/web test -- --run` ✅ (`13 passed`)
- Frontend typecheck: `npm --prefix apps/web run typecheck` ✅
- Backend: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m pytest services/api/tests -q` ✅ (`42 passed`)
- Backend lint: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m ruff check .` ✅

### Decisions made
- Keep mortgage term capture in years to align with existing API shape (`mortgage_term_years_remaining`) while satisfying term capture requirements.

### Risks / Blockers
- If future API changes require term in months, a conversion or additional UI control will be needed.

## 2026-03-06 — WS2-04 Stress Sliders

### Completed
- WS2-04: Added reusable `PercentSlider` input component with dual display (`%` and `bps`) and range-slider interaction.
- WS2-04: Integrated sliders into `StressTestPage` step 3 for income shock, inflation increase, stressed mortgage rate, and FX stress (EUR/USD).
- WS2-04: Added unit tests for slider rendering, percent/bps formatting behavior, and value-change callbacks.

### In progress
- WS2-05: Review + Run payload shaping and endpoint flow hardening.

### Test evidence
- Frontend: `npm --prefix apps/web test -- --run` ✅ (`16 passed`)
- Frontend typecheck: `npm --prefix apps/web run typecheck` ✅
- Backend: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m pytest services/api/tests -q` ✅ (`42 passed`)
- Backend lint: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m ruff check .` ✅

### Decisions made
- Keep FX stress values represented as bps in state while showing user-friendly `%` equivalents in slider readouts.

### Risks / Blockers
- Range bounds for stress sliders are currently static defaults and may need product tuning against methodology guidance.

## 2026-03-06 — WS2-05 Review + Run Deterministic Flow

### Completed
- WS2-05: Added `buildDeterministicPayload` helper to normalize wizard-state payloads into deterministic API request DTO shape.
- WS2-05: Updated stress-run submission flow to call deterministic endpoint with built payload and route to results using deterministic response state.
- WS2-05: Updated `ResultsPage` to support deterministic-only route state while still rendering Monte Carlo analytics when present.
- WS2-05: Added payload-builder unit test and adjusted page tests for deterministic-only result navigation and rendering.

### In progress
- WS2-06: Input diagnostics panel with warning/error checks.

### Test evidence
- Frontend: `npm --prefix apps/web test -- --run` ✅ (`18 passed`)
- Frontend typecheck: `npm --prefix apps/web run typecheck` ✅
- Backend: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m pytest services/api/tests -q` ✅ (`42 passed`)
- Backend lint: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m ruff check .` ✅

### Decisions made
- Preserve optional Monte Carlo rendering path in `ResultsPage` to avoid breaking existing views while WS2-05 enforces deterministic-first run flow.

### Risks / Blockers
- Deterministic-only submit path currently omits immediate Monte Carlo fetch; this is intentional for WS2-05 scope and may be expanded in later tasks.

## 2026-03-06 — WS2-06 Input Diagnostics Panel

### Completed
- WS2-06: Added `DiagnosticsPanel` component with rule checks for essentials-over-income (warning), zero-savings with negative monthly balance (warning), and reporting-currency FX spot not equal to 1.0 (error).
- WS2-06: Added plain-language "Why this matters" tooltip text for each diagnostic entry.
- WS2-06: Integrated diagnostics panel into `StressTestPage` so checks update as wizard inputs change.
- WS2-06: Added diagnostics component unit tests covering all required conditions.

### In progress
- WS3-01: Deterministic savings path chart/table extraction and accessibility enhancements.

### Test evidence
- Frontend: `npm --prefix apps/web test -- --run` ✅ (`21 passed`)
- Frontend typecheck: `npm --prefix apps/web run typecheck` ✅
- Backend: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m pytest services/api/tests -q` ✅ (`42 passed`)
- Backend lint: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m ruff check .` ✅

### Decisions made
- Diagnostics are presented as quality checks only (warnings/errors with rationale), without recommendation language.

### Risks / Blockers
- Diagnostics currently evaluate the GBP-denominated input fields directly and do not apply cross-currency normalization.

## 2026-03-04 — Deployment, Auth Stabilization, and Security Cleanup

### Completed
- POC-Deployment: Frontend deployed to GitHub Pages and backend deployed to Render; end-to-end simulation execution confirmed.
- POC-CI-CD: Documented workflow trigger behavior and build-time nature of `VITE_*` variables.
- POC-Auth-Stabilization: Resolved Clerk issuer/JWKS/origin/path mismatches and verified authenticated deterministic + Monte Carlo execution.
- POC-001: Removed temporary runtime auth bypass logic and environment flags from frontend and backend.

### In progress
- POC-Results-UI: Add chart-based visualization for Monte Carlo percentile outputs.
- POC-Release-Readiness: Freeze deployment config snapshot and prepare release notes/version tag.
- POC-Smoke-Automation: Add post-deploy smoke checks for `/health` + authenticated deterministic + Monte Carlo runs.

### Test evidence
- Backend: `pytest services/api/tests -q` ✅
- Frontend: `npm --prefix apps/web test -- --run` ✅
- Production check: Auth-enabled deterministic and Monte Carlo runs confirmed after configuration correction ✅

### Decisions made
- Authentication enforcement is mandatory in runtime environments; no bypass flags retained.
- Production validation should target `/health` for backend status checks.
- Clerk configuration must be strictly issuer/JWKS/path aligned with deployed domain and project path.

### Risks / Blockers
- VPN or DNS/proxy filtering can intermittently block Clerk script loading and break login flow.
- Environment drift risk remains until deployment configuration is fully snapshotted in runbook form.

---

## 2026-03-04 — Exact Arithmetic + Deterministic Savings Path Delivery

### Completed
- POC-002: Migrated engine arithmetic to integer pence and integer bps with explicit round-half-up conversion/utilities.
- POC-002: Updated API contracts to return money values as `*_pence` and `*_formatted`, and updated frontend typing/consumption accordingly.
- POC-002: Added money unit tests for conversion, rounding, and formatting behavior.
- POC-003: Implemented deterministic month-by-month savings projection with `horizon_months` defaulting to `24`.
- POC-003: Added deterministic outputs for `savings_path_pence`, `min_savings_pence`, `month_of_depletion`, and `runway_months` with formatted strings.
- POC-003: Added golden deterministic test with explicit expected savings path and API contract assertions for path length and fields.

### In progress
- POC-Results-UI: Expand results presentation from basic text to richer visual summaries for deterministic path and Monte Carlo percentiles.
- POC-Release-Readiness: Consolidate API contract changes into release notes/changelog entries.

### Test evidence
- Backend: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m pytest services/api/tests -q` ✅ (`11 passed`)
- Frontend: `npm --prefix apps/web test -- --run` ✅ (`5 passed`)

### Decisions made
- Monetary and rate calculations in engine core are integer-only (`pence`/`bps`) to eliminate float drift.
- API reporting must include both machine-safe integer values and user-readable formatted currency strings.
- Deterministic path outputs are treated as reproducible golden-contract artifacts.

### Risks / Blockers
- Any external consumer still expecting pre-POC-002 float money fields may break without coordinated contract update.
- Golden tests require strict maintenance discipline when deterministic logic intentionally changes.

<!-- crossref:start -->
## Related Documents

- [Repository README](../README.md)
- [Methodology Golden Source](methodology/methodology_textbook.md)
- [BRD Implementation Plan](implementation/brd_implementation_plan.md)
<!-- crossref:end -->

