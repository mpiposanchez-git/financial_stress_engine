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

## 2026-03-06 — WS3-01 Deterministic Savings Path Chart + Table

### Completed
- WS3-01: Extracted deterministic savings path visualization into `components/charts/SavingsPathChart.tsx`.
- WS3-01: Added accessible chart output with `<figure>`, `<figcaption>`, and plain-language summary text.
- WS3-01: Added month-by-month savings data table (pence + formatted values) for accessible tabular review.
- WS3-01: Updated `ResultsPage` to render the extracted chart component with deterministic path inputs.
- WS3-01: Added dedicated component tests for figcaption/summary and table accessibility.

### In progress
- WS3-02: Mortgage stress panel and plain-English delta explanation.

### Test evidence
- Frontend: `npm --prefix apps/web test -- --run` ✅ (`23 passed`)
- Frontend typecheck: `npm --prefix apps/web run typecheck` ✅
- Backend: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m pytest services/api/tests -q` ✅ (`42 passed`)
- Backend lint: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m ruff check .` ✅

### Decisions made
- Keep both visual and tabular deterministic path views to improve accessibility without changing deterministic output contracts.

### Risks / Blockers
- Large horizon values may produce long tables; pagination/virtualization may be needed in future UX passes.

## 2026-03-06 — WS3-02 Mortgage Stress Panel

### Completed
- WS3-02: Added `MortgageStressPanel` component to display current vs stressed mortgage payment and absolute delta.
- WS3-02: Included plain-English explanation of what the comparison represents, explicitly avoiding recommendation language.
- WS3-02: Integrated panel into `ResultsPage` using deterministic mortgage payment outputs.
- WS3-02: Added a basic unit test for panel rendering and delta text.

### In progress
- WS3-03: Emergency fund adequacy card.

### Test evidence
- Frontend: `npm --prefix apps/web test -- --run` ✅ (`24 passed`)
- Frontend typecheck: `npm --prefix apps/web run typecheck` ✅
- Backend: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m pytest services/api/tests -q` ✅ (`42 passed`)
- Backend lint: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m ruff check .` ✅

### Decisions made
- Delta is shown in pence with directional wording (`higher`, `lower`, `unchanged`) for clear interpretation.

### Risks / Blockers
- Delta presentation is currently pence-centric and does not include localized currency-symbol delta formatting.

## 2026-03-06 — WS3-03 Emergency Fund Adequacy Card

### Completed
- WS3-03: Added `EmergencyFundCard` component to compute and display months of coverage from modeled low-point savings and baseline monthly outgoings.
- WS3-03: Integrated emergency-fund card into `ResultsPage` alongside deterministic and mortgage stress outputs.
- WS3-03: Added a basic unit test covering months-of-coverage calculation and render output.

### In progress
- WS3-04: Explain-the-result narrative and glossary tooltips.

### Test evidence
- Frontend: `npm --prefix apps/web test -- --run` ✅ (`25 passed`)
- Frontend typecheck: `npm --prefix apps/web run typecheck` ✅
- Backend: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m pytest services/api/tests -q` ✅ (`42 passed`)
- Backend lint: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m ruff check .` ✅

### Decisions made
- Coverage is presented as an explanatory adequacy ratio (months), with neutral educational wording.

### Risks / Blockers
- Baseline monthly outgoings currently use available deterministic output fields and may need refinement once direct essentials outgoings are exposed in results contracts.

## 2026-03-06 — WS3-04 Explain-the-Result Narrative + Glossary Tooltips

### Completed
- WS3-04: Added `ExplainResult` component with plain-language narrative describing runway drivers and output interpretation context.
- WS3-04: Added reusable `GlossaryTooltip` component for inline key-term definitions.
- WS3-04: Integrated explain narrative block into `ResultsPage` using deterministic and optional Monte Carlo context.
- WS3-04: Added tests to verify key terms render and glossary tooltip definitions exist.

### In progress
- WS3-05: Assumptions panel (limits, rounding, caps, timestamps placeholder).

### Test evidence
- Frontend: `npm --prefix apps/web test -- --run` ✅ (`26 passed`)
- Frontend typecheck: `npm --prefix apps/web run typecheck` ✅
- Backend: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m pytest services/api/tests -q` ✅ (`42 passed`)
- Backend lint: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m ruff check .` ✅

### Decisions made
- Glossary terms use inline tooltip definitions to keep narrative readable without adding extra navigation.

### Risks / Blockers
- Tooltip-based definitions rely on hover/title affordance and may later need explicit tap-target alternatives for mobile-first glossary UX.

## 2026-03-06 — WS3-05 Assumptions Panel

### Completed
- WS3-05: Added `AssumptionsPanel` component that surfaces model horizon, pence/bps conventions, rounding policy, Monte Carlo cap transparency, and a data-timestamp placeholder.
- WS3-05: Integrated assumptions panel into `ResultsPage` with available run context (`horizon_months` when present).
- WS3-05: Added a basic unit test validating assumptions/limits content rendering.

### In progress
- WS3-06: Official resource signposting panel.

### Test evidence
- Frontend: `npm --prefix apps/web test -- --run` ✅ (`27 passed`)
- Frontend typecheck: `npm --prefix apps/web run typecheck` ✅
- Backend: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m pytest services/api/tests -q` ✅ (`42 passed`)
- Backend lint: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m ruff check .` ✅

### Decisions made
- Assumptions panel wording is explicitly educational/transparency-focused and avoids prescriptive language.

### Risks / Blockers
- Monte Carlo cap/premium lock text is currently static and should eventually be bound to entitlement/config values.

## 2026-03-06 — WS3-06 Official Resource Signposting

### Completed
- WS3-06: Added `OfficialResources` component with curated links to MoneyHelper and Citizens Advice.
- WS3-06: Included explicit "information only" disclaimer to reinforce non-advice framing.
- WS3-06: Integrated official-resources section into `ResultsPage`.
- WS3-06: Added unit test coverage for resource links and disclaimer text.

### In progress
- WS4-01: Scenario tabs UI scaffolding.

### Test evidence
- Frontend: `npm --prefix apps/web test -- --run` ✅ (`28 passed`)
- Frontend typecheck: `npm --prefix apps/web run typecheck` ✅
- Backend: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m pytest services/api/tests -q` ✅ (`42 passed`)
- Backend lint: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m ruff check .` ✅

### Decisions made
- External links open in a new tab with `rel="noreferrer"` to keep navigation intent clear and reduce referrer leakage.

### Risks / Blockers
- Resource list is intentionally minimal for this task and may need expansion/localization for broader coverage.

## 2026-03-06 — WS4-01 Scenario Tabs UI

### Completed
- WS4-01: Added `ScenarioTabs` component for Base/A/B/C scenario selection UI.
- WS4-01: Added Base-clone prompt/action flow for empty premium scenarios (A/B/C).
- WS4-01: Integrated scenario tab state into `StressTestPage`, including per-scenario draft storage and active-scenario editing state.
- WS4-01: Applied premium gating in UI for non-base scenarios (A/B/C disabled when premium is not unlocked).
- WS4-01: Added tests for tab behavior (selection + clone flow under premium, and lock behavior when premium is unavailable).

### In progress
- WS4-02: Scenario compare backend endpoint (premium gated).

### Test evidence
- Frontend: `npm --prefix apps/web test -- --run` ✅ (`30 passed`)
- Frontend typecheck: `npm --prefix apps/web run typecheck` ✅
- Backend: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m pytest services/api/tests -q` ✅ (`42 passed`)
- Backend lint: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m ruff check .` ✅

### Decisions made
- Scenario drafts are stored client-side and cloned from Base using a deep copy of FX objects to avoid shared-reference edits.

### Risks / Blockers
- Premium unlock is currently static (`false`) in UI wiring and should later bind to real entitlement signals.

## 2026-03-06 — WS4-02 Scenario Compare Endpoint (Premium)

### Completed
- WS4-02: Added premium-gated endpoint `POST /api/v1/compare/run` to execute deterministic runs across multiple named scenarios.
- WS4-02: Added compare DTOs in API models for scenario-list request and comparison-ready response payload.
- WS4-02: Endpoint now returns scenario rows including runway, depletion month, stressed cashflow/payment, min savings, reporting currency, and warnings.
- WS4-02: Added endpoint tests for both `403` non-premium access and `200` premium access paths.

### In progress
- WS4-03: Scenario compare UI integration and premium-gated UX.

### Test evidence
- Backend: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m pytest services/api/tests -q` ✅ (`44 passed`)
- Backend lint: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m ruff check .` ✅
- Frontend: `npm --prefix apps/web test -- --run` ✅ (`30 passed`)
- Frontend typecheck: `npm --prefix apps/web run typecheck` ✅

### Decisions made
- Reused existing deterministic engine invocation per scenario to keep compare behavior aligned with single-scenario deterministic semantics.

### Risks / Blockers
- Compare endpoint currently runs scenarios sequentially; future scaling may require batched/parallel execution controls.

## 2026-03-06 — WS4-03 Scenario Compare UI (Premium)

### Completed
- WS4-03: Added `ScenarioCompareTable` component to render side-by-side scenario comparison output (runway, depletion month, min savings, stressed cashflow, stressed mortgage payment).
- WS4-03: Integrated compare rendering into `ResultsPage` with premium gating: table is shown only when `premiumUnlocked` is true; otherwise a locked message is displayed.
- WS4-03: Extended route-state typings to include compare response payload and premium flag for view gating.
- WS4-03: Added tests covering scenario compare table headers/rows and Results page premium unlocked vs locked behaviors.

### In progress
- WS4-04: Local-only scenario storage with free/premium limits and device-only warning.

### Test evidence
- Frontend: `npm --prefix apps/web test -- --run` ✅ (`33 passed`)
- Frontend typecheck: `npm --prefix apps/web run typecheck` ✅
- Backend: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m pytest services/api/tests -q` ✅ (`44 passed`)
- Backend lint: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m ruff check .` ✅

### Decisions made
- Compare table consumes backend compare DTO fields directly to preserve contract clarity and avoid duplicate calculation logic in UI.

### Risks / Blockers
- `ResultsPage` rendering currently relies on compare data being present in route state; end-to-end compare fetch wiring is expected in subsequent workflow tasks.

## 2026-03-06 — WS4-04 Local-only Scenario Store (Hybrid)

### Completed
- WS4-04: Added browser-only scenario persistence utility `localScenarioStore` with robust read/parse handling and cloning safeguards.
- WS4-04: Implemented free-vs-premium save limits in storage flow (`2` scenarios on free plan, unlimited when premium is unlocked).
- WS4-04: Added `SavedScenarios` UI to save, list, load, and delete local scenario snapshots from the wizard flow.
- WS4-04: Integrated saved-scenario load/save/delete into `StressTestPage` and surfaced explicit device-local warning text: `Saved only on this device.`
- WS4-04: Added tests for local storage limit behavior and saved-scenarios UI interactions/warning text.

### In progress
- WS5-F05-01: Monte Carlo DTO alignment and API contract hardening.

### Test evidence
- Frontend: `npm --prefix apps/web test -- --run` ✅ (`38 passed`)
- Frontend typecheck: `npm --prefix apps/web run typecheck` ✅
- Backend: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m pytest services/api/tests -q` ✅ (`44 passed`)
- Backend lint: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m ruff check .` ✅

### Decisions made
- Kept scenario persistence local-only via `localStorage` and did not introduce backend persistence to preserve the privacy/device-local scope for this task.

### Risks / Blockers
- Premium entitlement source is still static in page wiring; when entitlement service wiring is added, UI limits should be bound to real auth claims.

## 2026-03-06 — WS5-F05-01 Monte Carlo DTO Alignment + API Contract Hardening

### Completed
- WS5-F05-01: Extended Monte Carlo API response DTO with explicit top-level percentile fields for runway, min savings (pence), and month of depletion.
- WS5-F05-01: Preserved existing nested `metrics` object for compatibility while adding explicit stable keys for downstream UI contracts.
- WS5-F05-01: Updated Monte Carlo route response construction to populate all new top-level percentile fields.
- WS5-F05-01: Hardened API contract tests to assert presence and concrete types of `n_sims`, `horizon_months`, `seed`, `runtime_ms`, and all top-level percentile keys.
- WS5-F05-01: Added consistency assertions confirming top-level percentile values match nested metrics values.

### In progress
- WS5-F05-02: Fan chart UI (table-first, chart-second).

### Test evidence
- Backend: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m pytest services/api/tests -q` ✅ (`44 passed`)
- Backend lint: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m ruff check .` ✅
- Frontend: `npm --prefix apps/web test -- --run` ✅ (`38 passed`)
- Frontend typecheck: `npm --prefix apps/web run typecheck` ✅

### Decisions made
- Kept both nested and top-level Monte Carlo percentile fields in this step to avoid breaking existing consumers while introducing explicit contract keys required for future premium UI slices.

### Risks / Blockers
- Response currently duplicates percentile values in two shapes (`metrics` and top-level), which should be rationalized in a later breaking-change window if contract simplification is desired.

## 2026-03-06 — WS5-F05-02 Fan Chart UI (Table-first)

### Completed
- WS5-F05-02: Added `FanChart` component with a summary-percentile table for runway, min savings, and depletion month.
- WS5-F05-02: Added lightweight placeholder percentile-band visualization with clear labeling for summary percentile interpretation.
- WS5-F05-02: Integrated fan chart into `ResultsPage` and gated rendering by premium entitlement.
- WS5-F05-02: Added locked-state card when Monte Carlo exists but premium is not unlocked.
- WS5-F05-02: Updated frontend Monte Carlo response typing to include explicit top-level percentile fields from backend contract.
- WS5-F05-02: Added dedicated fan chart tests and updated `ResultsPage` tests for unlocked/locked fan chart states.

### In progress
- WS5-F12-01: Sensitivity engine perturbation calculator.

### Test evidence
- Frontend: `npm --prefix apps/web test -- --run` ✅ (`40 passed`)
- Frontend typecheck: `npm --prefix apps/web run typecheck` ✅
- Backend: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m pytest services/api/tests -q` ✅ (`44 passed`)
- Backend lint: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m ruff check .` ✅

### Decisions made
- Replaced previous percentile disclosure/card stack with a single fan-chart section to keep premium Monte Carlo interpretation focused and consistent with WS5-F05-02 scope.

### Risks / Blockers
- Fan chart currently uses percentile summary values (not full monthly percentile paths); richer fan-surface detail depends on future path-level percentile outputs.

## 2026-03-06 — WS5-F12-01 Sensitivity Engine Perturbation Calculator

### Completed
- WS5-F12-01: Added `shared/engine/sensitivity.py` with `compute_sensitivity(...)` for deterministic one-factor perturbation analysis.
- WS5-F12-01: Implemented perturbations for income shock, inflation shock, stressed mortgage rate, and FX stress, each shifted by `delta_bps` with guardrail clamping.
- WS5-F12-01: Added ranked sensitivity output model including runway impact and min-savings impact per driver.
- WS5-F12-01: Ranking is deterministic and ordered by absolute min-savings impact (descending), with stable tie-break by driver name.
- WS5-F12-01: Added `services/api/tests/test_sensitivity.py` covering driver coverage/ranking and deterministic repeatability.

### In progress
- WS5-F12-02: Sensitivity API endpoint (premium gated).

### Test evidence
- Backend: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m pytest services/api/tests -q` ✅ (`46 passed`)
- Backend lint: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m ruff check .` ✅
- Frontend: `npm --prefix apps/web test -- --run` ✅ (`40 passed`)
- Frontend typecheck: `npm --prefix apps/web run typecheck` ✅

### Decisions made
- Used one-direction `+delta_bps` perturbations per factor for predictable comparison semantics and deterministic ranking.

### Risks / Blockers
- Current ranking key emphasizes min-savings sensitivity; if product preference shifts to runway-first ranking, sorting policy should be updated consistently across API/UI consumers.

## 2026-03-06 — WS5-F12-02 Sensitivity Endpoint (Premium gated)

### Completed
- WS5-F12-02: Added sensitivity endpoint DTOs in API models (`SensitivityRunRequest`, `SensitivityDriverImpact`, `SensitivityRunResponse`).
- WS5-F12-02: Added `POST /api/v1/sensitivity/run` in main router, gated by `require_premium`.
- WS5-F12-02: Endpoint applies existing rate limiting and request timeout guards, then executes deterministic sensitivity computation.
- WS5-F12-02: Added endpoint tests for non-premium `403` behavior and premium `200` ranked-driver response contract.

### In progress
- WS5-F12-03: Tornado chart UI.

### Test evidence
- Backend: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m pytest services/api/tests -q` ✅ (`48 passed`)
- Backend lint: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m ruff check .` ✅
- Frontend: `npm --prefix apps/web test -- --run` ✅ (`40 passed`)
- Frontend typecheck: `npm --prefix apps/web run typecheck` ✅

### Decisions made
- Reused the existing single-router pattern (`routes.py`) for this endpoint to keep premium endpoint behavior consistent with compare and Monte Carlo flows.

### Risks / Blockers
- Endpoint currently returns deterministic ranking sorted by min-savings impact from engine output; if a different ranking policy is required by UI, both endpoint and tests should be aligned explicitly.

## 2026-03-06 — WS5-F12-03 Tornado Chart UI

### Completed
- WS5-F12-03: Added `TornadoChart` component rendering ranked sensitivity bars and an accessible summary line for the top driver.
- WS5-F12-03: Wired `ResultsPage` to call `/api/v1/sensitivity/run` via API client for premium runs when input parameters are available.
- WS5-F12-03: Added loading/error/unavailable states for sensitivity fetch flow in `ResultsPage`.
- WS5-F12-03: Added premium-locked card state for tornado chart when premium is not unlocked.
- WS5-F12-03: Extended frontend route-state typing to carry original input parameters into results page API workflows.
- WS5-F12-03: Added tests for tornado component rendering and results-page premium sensitivity fetch/locked behavior.

### In progress
- WS5-F13-01: Schedule schema + deterministic engine application.

### Test evidence
- Frontend: `npm --prefix apps/web test -- --run` ✅ (`43 passed`)
- Frontend typecheck: `npm --prefix apps/web run typecheck` ✅
- Backend: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m pytest services/api/tests -q` ✅ (`48 passed`)
- Backend lint: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m ruff check .` ✅

### Decisions made
- Sensitivity API invocation is executed from results page only when premium is unlocked and source input parameters are present, preventing unnecessary premium endpoint calls.

### Risks / Blockers
- Tornado bars currently visualize min-savings impact magnitude; if product requirements shift toward runway-first visual ranking, chart labels and sorting semantics should be updated together.

## 2026-03-06 — WS5-F13-01 Shock Schedules in Deterministic Engine

### Completed
- WS5-F13-01: Added `shared/engine/schedules.py` with schedule resolution for `step`, `ramp`, and `stepped` modes.
- WS5-F13-01: Extended deterministic input schema with optional schedule DTOs (`income_shock_schedule`, `inflation_shock_schedule`, `mortgage_rate_stress_schedule`).
- WS5-F13-01: Updated deterministic engine to compute month-by-month stressed cashflow series using resolved schedule levels.
- WS5-F13-01: Savings path now consumes the month-by-month stressed cashflow series in deterministic runs.
- WS5-F13-01: Added deterministic schedule tests covering each schedule type in `services/api/tests/test_schedules_deterministic.py`.

### In progress
- WS5-F13-02: Schedules in Monte Carlo monthly paths.

### Test evidence
- Backend: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m pytest services/api/tests -q` ✅ (`51 passed`)
- Backend lint: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m ruff check .` ✅
- Frontend: `npm --prefix apps/web test -- --run` ✅ (`43 passed`)
- Frontend typecheck: `npm --prefix apps/web run typecheck` ✅

### Decisions made
- Applied schedule resolution to monthly stress drivers while preserving existing top-level deterministic output fields (`monthly_cashflow_stress_pence`, runway summary) based on first stressed month for backward compatibility.

### Risks / Blockers
- Backward-compatible first-month stress summary may under-represent later-month schedule severity; if needed, summary contract can be extended in a future non-backward-compatible revision.

## 2026-03-06 — WS5-F13-02 Schedules in Monte Carlo Monthly Paths

### Completed
- WS5-F13-02: Updated Monte Carlo shock generation to support time-varying monthly mean paths (`mu_t`) for income shock, inflation shock, and mortgage-rate stress.
- WS5-F13-02: Extended `generate_shock_paths` in `shock_process.py` to accept either scalar means or per-month mean arrays.
- WS5-F13-02: Implemented AR(1) behavior around moving means using prior-step deviation from prior mean (`mu_{t-1}`).
- WS5-F13-02: Wired schedule-derived mean paths from input schedules into Monte Carlo run flow.
- WS5-F13-02: Added schedule-focused Monte Carlo tests for fixed-seed reproducibility and schedule-effect behavior under zero-volatility settings.

### In progress
- WS5-F08-01: Category inflation model (engine only).

### Test evidence
- Backend: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m pytest services/api/tests -q` ✅ (`53 passed`)
- Backend lint: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m ruff check .` ✅
- Frontend: `npm --prefix apps/web test -- --run` ✅ (`43 passed`)
- Frontend typecheck: `npm --prefix apps/web run typecheck` ✅

### Decisions made
- Reproducibility assertions compare deterministic output metrics and seed metadata while intentionally excluding runtime timing variance.

### Risks / Blockers
- Schedule-aware mean paths currently apply to stress dimensions only; any future category/debt schedule features must align mean-path conventions to avoid drift across model modules.

## 2026-03-06 — WS5-F08-01 Category Inflation Model (Engine Only)

### Completed
- WS5-F08-01: Extended deterministic input schema with optional `essentials_categories` map and `EssentialsCategory` entries (`monthly_spend_pence`, `inflation_bps`).
- WS5-F08-01: Added category-inflation helper module (`shared/engine/inflation_categories.py`) for base and stressed category totals.
- WS5-F08-01: Updated deterministic engine to use category totals when `essentials_categories` is provided, while preserving existing single-bucket behavior when not provided.
- WS5-F08-01: Added engine tests validating (a) single-category equivalence with legacy single-bucket behavior and (b) per-category inflation override behavior.

### In progress
- WS5-F08-02: Category inflation API surface and contract behavior.

### Test evidence
- Backend: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m pytest services/api/tests -q` ✅ (`55 passed`)
- Backend lint: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m ruff check .` ✅
- Frontend: `npm --prefix apps/web test -- --run` ✅ (`43 passed`)
- Frontend typecheck: `npm --prefix apps/web run typecheck` ✅

### Decisions made
- Category totals are authoritative when provided, enabling finer-grained inflation stress without breaking existing deterministic input contracts.

### Risks / Blockers
- Category maps currently require non-empty names and non-empty payload; any future UX support for optional/partial category forms must align with this strict validation behavior.

## 2026-03-06 — WS5-F08-02 Category Inflation UI (Premium)

### Completed
- WS5-F08-02: Added `CategoryInflationEditor` component with premium lock teaser and premium-only toggle for category inflation mode.
- WS5-F08-02: Added category spend/inflation-bps inputs for core categories (food, energy, housing, transport) with basic numeric input guards.
- WS5-F08-02: Integrated category inflation editor into `StressTestPage` wizard and preserved deep cloning of category maps across scenario drafts.
- WS5-F08-02: Extended frontend input typing to include optional `essentials_categories` payload shape.
- WS5-F08-02: Extended backend deterministic request model to accept `essentials_categories` and convert category spend/inflation inputs into engine pence/bps schema.
- WS5-F08-02: Added frontend tests for editor rendering/change behavior and backend API contract test for category inflation payload acceptance.

### In progress
- WS5-F14-01: Debt schedule engine (simple amortisation).

### Test evidence
- Backend: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m pytest services/api/tests -q` ✅ (`56 passed`)
- Backend lint: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m ruff check .` ✅
- Frontend: `npm --prefix apps/web test -- --run` ✅ (`45 passed`)
- Frontend typecheck: `npm --prefix apps/web run typecheck` ✅

### Decisions made
- Kept premium gating explicit in-page with a locked teaser card and only render editable category controls when premium is unlocked.
- Used `inflation_bps` directly in UI/API category schema to align with model precision and avoid repeated percent-bps conversions for category overrides.

### Risks / Blockers
- Premium entitlement remains statically set in stress-page wiring (`premiumUnlocked = false`), so live category editing remains functionally locked until entitlement integration is wired.

## 2026-03-06 — WS5-F14-01 Debt Schedule Engine (Simple Amortisation)

### Completed
- WS5-F14-01: Added `shared/engine/debt.py` with monthly unsecured debt amortisation logic (interest accrual then capped payment application).
- WS5-F14-01: Extended deterministic input schema with optional `debts` list (`balance_pence`, `apr_bps`, `min_payment_pence`).
- WS5-F14-01: Updated deterministic engine to use debt-payment series in monthly stressed cashflow and to return optional `debt_balance_path_pence`.
- WS5-F14-01: Extended deterministic API models/routes to accept optional debts and return optional debt balance path.
- WS5-F14-01: Added debt schedule tests for both payoff behavior and interest-accrual behavior.

### In progress
- WS6-A01-01: Data registry (static) + Data Sources page.

### Test evidence
- Backend: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m pytest services/api/tests -q` ✅ (`58 passed`)
- Backend lint: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m ruff check .` ✅
- Frontend: `npm --prefix apps/web test -- --run` ✅ (`45 passed`)
- Frontend typecheck: `npm --prefix apps/web run typecheck` ✅

### Decisions made
- Debt schedules are treated as authoritative debt outflow when provided, preserving legacy fixed monthly debt behavior when `debts` is absent.
- Debt amortisation uses monthly APR accrual with round-half-up integer arithmetic to remain consistent with pence/bps precision rules.

### Risks / Blockers
- Debt schedule items currently assume pence values directly in engine/API schema; if UI capture is added, currency/normalization rules will need explicit contract alignment.

## 2026-03-06 — WS6-A01-01 Data Registry (Static) + Data Sources Page

### Completed
- WS6-A01-01: Added static backend data registry module `services/api/app/data_registry.py` with dataset metadata fields (name, provider, URL, refresh cadence, license note, verification steps).
- WS6-A01-01: Added `GET /api/v1/data/registry` endpoint in API routes returning `datasets` payload.
- WS6-A01-01: Added backend API contract test validating registry endpoint availability and dataset shape.
- WS6-A01-01: Added frontend `DataSourcesPage` to fetch and render registry entries with URLs and verification steps.
- WS6-A01-01: Added app route `/data-sources` and navigation link from home page.
- WS6-A01-01: Added frontend test asserting dataset names and URLs render from mocked API response.

### In progress
- WS6-A01-02: Data cache abstraction.

### Test evidence
- Backend: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m pytest services/api/tests -q` ✅ (`59 passed`)
- Backend lint: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m ruff check .` ✅
- Frontend: `npm --prefix apps/web test -- --run` ✅ (`46 passed`)
- Frontend typecheck: `npm --prefix apps/web run typecheck` ✅

### Decisions made
- Kept registry response read-only and unauthenticated for transparency use-cases and lightweight frontend rendering.
- Encoded verification steps as ordered lists in payload to preserve source-audit workflow context.

### Risks / Blockers
- Data Sources page currently performs direct `fetch` without shared client retry policy; if network resilience requirements increase, migrate to a shared API utility.

## 2026-03-06 — WS6-A01-02 Data Cache Abstraction

### Completed
- WS6-A01-02: Added `services/api/app/data_cache.py` with a simple in-memory cache implementation (`InMemoryDataCache`).
- WS6-A01-02: Implemented required cache API: `get(key)` and `set(key, value, meta)`.
- WS6-A01-02: Added strict metadata schema (`fetched_at_utc`, `source_url`, `sha256`) via `CacheMeta` validation.
- WS6-A01-02: Added tests for set/get round-trip behavior, missing-key behavior, and metadata validation failures.

### In progress
- WS6-A01-03: Fetcher for BoE Bank Rate.

### Test evidence
- Backend: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m pytest services/api/tests -q` ✅ (`62 passed`)
- Backend lint: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m ruff check .` ✅
- Frontend: `npm --prefix apps/web test -- --run` ✅ (`46 passed`)
- Frontend typecheck: `npm --prefix apps/web run typecheck` ✅

### Decisions made
- Kept the cache implementation intentionally in-process and synchronous for POC simplicity, while preserving metadata required for source traceability.

### Risks / Blockers
- In-memory cache is process-local and non-persistent; multi-instance deployments or restarts will require a shared backend cache in later phases.

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

