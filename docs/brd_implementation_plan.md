# UK Household Financial Stress Engine — BRD + Backlog (Copilot-Ready) 🧩

**Version:** v0.2.0  
**Status:** Draft / living document  
**Date:** 2026-03-06  
**Repo:** https://github.com/mpiposanchez-git/financial_stress_engine  
**Evidence snapshot:** _Insert commit SHA (`git rev-parse HEAD`)_  
**Audience:** product owner + GitHub Copilot coding agent + reviewer/auditor

> This document is explicit by design. It defines *what to build*, *how to build it*, and *how to prove it works*.

---

## 0) Key decisions (must be treated as requirements)
- Auth always on (Clerk) — no runtime bypass
- Money in integer pence, rates in integer bps
- Default horizon 24 months, month-by-month outputs
- Monte Carlo monthly paths with optional AR(1) dynamics
- Multi-currency + reporting currency, FX stress + FX volatility
- UK benchmarking default **BHC**
- Auto-fetch official data + allow manual overrides

---

## 1) POC feature catalog (functionalities 1–20 + additions)

### Feature IDs (F-xx)
We map your requested “1–20” set into stable feature IDs used in backlog tasks.

| Original # | Feature ID | Capability | Tier |
|---:|---|---|---|
| 1 | F-01 | Guided onboarding wizard | Free |
| 2 | F-02 | Month-by-month runway chart (24m default) | Free |
| 3 | F-03 | Mortgage rate stress module | Free |
| 4 | F-04 | Scenario comparison (Base vs A vs B) | Premium |
| 5 | F-05 | Monte Carlo fan chart (P10/P50/P90) | Premium |
| 6 | F-06 | PDF export | Premium |
| 7 | F-07 | FX + multi-currency + reporting currency | Free (basic) + Premium (volatility) |
| 8 | F-08 | Category inflation toggles | Premium |
| 9 | F-09 | Interactive sliders | Free |
| 10 | F-10 | Emergency fund adequacy indicator | Free |
| 11 | F-11 | Explain-the-result narratives + tooltips | Free |
| 12 | F-12 | Sensitivity / tornado chart | Premium |
| 13 | F-13 | Shock schedules (step/ramp/stepped) | Premium |
| 14 | F-14 | Non-mortgage debt schedule (optional) | Premium |
| 15 | F-15 | Mortgage type sandbox (repayment vs IO) | Free |
| 16 | F-16 | Household archetype templates | Free |
| 17 | F-17 | Local-only scenario saving (hybrid) | Free limited + Premium unlimited |
| 18 | F-18 | Input diagnostics & quality checks | Free |
| 19 | F-19 | Limits & assumptions transparency panel | Free |
| 20 | F-20 | Official-resource signposting (non-advice) | Free |

### Added features (A-xx)
| Feature ID | Capability | Tier |
|---|---|---|
| A-01 | Data module: sources, provenance, verification, auto-fetch, overrides | Free |
| A-02 | UK benchmarks: free reference values + premium BHC percentile | Free/Premium |
| A-03 | Premium teaser demo (dummy example outputs in free) | Free |
| A-04 | Premium entitlements mechanism (allowlist now, Stripe later) | Internal |
| A-05 | Accessibility requirements for charts and forms | All |
| A-06 | Ethics/fairness note for percentile ranking | All |
| A-07 | Privacy-safe measurement (aggregate counters only) | Internal |

---

## 2) Modular architecture requirements (mandatory)

### 2.1 Engine (`shared/engine/`)
Existing: `deterministic.py`, `montecarlo.py`, `fx.py`, `money.py`, `inputs.py`, `outputs.py`

Required refactor to enforce modularity and UDF separation:
- `mortgage.py` — mortgage payment functions
- `savings_path.py` — savings path + depletion metrics
- `shock_process.py` — IID + AR(1) path generator
- `benchmarks/` — HBAI fetch/parse + percentile compute
- `reports/` — PDF report generator
- `inflation_categories.py` — category inflation rules
- `schedules.py` — shock schedules

### 2.2 API (`services/api/app/`)
Add thin, explicit routers:
- `routes_deterministic.py`
- `routes_montecarlo.py`
- `routes_data.py`
- `routes_benchmarks.py`
- `routes_reports.py`
- `entitlements.py` (A-04)
- `telemetry.py` (A-07)

### 2.3 Web (`apps/web/src/`)
Add pages/components:
- `pages/StressWizardPage.tsx` (F-01)
- `pages/DataSourcesPage.tsx` (A-01)
- `components/charts/*` with accessible summaries (A-05)
- `components/premium/LockedCard.tsx` (tier gating)
- `lib/storage/localScenarioStore.ts` (F-17)

---

## 3) Implementation backlog (workstreams → tasks → sub-tasks)

> Each task is written so you can paste it to Copilot and it can implement without guessing.

### WS0 — Implement the 4 recommendations (DO FIRST)

#### TASK A-04 — Premium entitlements (POC allowlist)
**Goal:** server-side premium gating.

**Backend**
- Create `services/api/app/entitlements.py` with:
  - `PREMIUM_SUBJECT_ALLOWLIST` env var (comma-separated Clerk `sub`)
  - `is_premium(auth: AuthContext) -> bool`
  - `require_premium` dependency raising 403 if not premium
- Add endpoint `GET /api/v1/me` returning:
  - `subject`
  - `is_premium`

**Apply gating**
- Apply `require_premium` to premium endpoints:
  - Monte Carlo fan chart data (F-05)
  - Scenario compare (F-04)
  - Tornado data (F-12)
  - Percentile ranking (A-02B)
  - PDF export (F-06)
  - FX volatility controls (F-07B)

**Tests**
- Add `services/api/tests/test_entitlements.py`:
  - allowlisted subject passes
  - non-allowlisted subject gets 403
- Update API route tests accordingly.

**Acceptance**
- Premium features cannot be accessed by non-premium users even if UI is bypassed.

---

#### TASK A-05 — Accessibility (charts + wizard)
**Goal:** inclusive and defensible UI.

**Frontend**
- Ensure every input has:
  - explicit `<label>`
  - `aria-describedby` for error text
- For each chart component:
  - wrap in `<figure>`
  - add `<figcaption>`
  - add a plain-text summary below (visible or screen-reader-only)
- Add keyboard focus styles and ensure tab order is logical.

**Tests**
- Add unit tests for presence of labels/captions in key components.

**Acceptance**
- All charts have a text summary.
- Wizard is usable without a mouse.

---

#### TASK A-06 — Ethics / fairness disclosure for percentile ranking
**Goal:** prevent misinterpretation and reduce harm.

**Frontend**
- Create `components/benchmarks/PercentileDisclosure.tsx` with:
  - “Approximate”
  - “BHC definition”
  - “depends on year and definitions”
  - “not advice”
  - “not a measure of worth”
- Render it wherever percentile is shown.

**Docs**
- Add an “Ethics & limitations” subsection to:
  - `docs/methodology_textbook.md`
  - `docs/poc_flyer.md` (short version)

**Acceptance**
- Percentile display always includes disclosure.

---

#### TASK A-07 — Privacy-safe measurement (aggregate only)
**Goal:** measure product health without tracking people.

**Backend**
- Create `services/api/app/telemetry.py` with in-memory counters:
  - `deterministic_runs_total`
  - `montecarlo_runs_total`
  - `pdf_exports_total`
  - `errors_total`
  - coarse runtime buckets
- Increment counters in routes without storing:
  - user IDs
  - payloads
- Add admin endpoint:
  - `GET /api/v1/admin/telemetry` protected by `ADMIN_METRICS_TOKEN` header.

**Docs**
- Update privacy policy to disclose aggregate operational metrics (no third-party analytics).

**Acceptance**
- No PII stored.
- Telemetry endpoint is not publicly accessible.

---

### WS1 — Free tier UX core (F-01, F-09, F-18, F-19)
(Implementation tasks omitted here for brevity in this excerpt; keep in repo doc. Copy from earlier WS1/WS2/WS3 sections and expand per task with “files to modify” + acceptance criteria.)

> **Note:** In the repository version of this document, WS1–WS9 should include one task block per feature (F-01 to F-20) with: files, requirements, tests, acceptance criteria.  

---

## 4) Copilot prompt template
```text
Implement TASK: <TASK-ID> — <Title>

Files to read first:
- <exact paths>

Files to create/modify:
- <exact paths>

Requirements:
1) ...
2) ...

Tests:
- Backend: uv run pytest -v
- Backend lint: uv run ruff check .
- Frontend: npm run test
- Frontend typecheck: npm run typecheck

Acceptance criteria:
- All tests pass and CI is green
- Premium endpoints are server-side gated
- Charts have text summaries
- No PII is stored for telemetry
```

---

## 5) Extra recommendations (you didn’t ask, but you’ll thank yourself later)
1) **Tag releases** (milestone tags) and write the commit SHA into exports.  
2) **Security hygiene:** enable GitHub secret scanning; add a basic `pre-commit` config.  
3) **Benchmark year/versioning:** always display year + dataset hash for HBAI percentiles.  
4) **PR checklist:** add “accessibility summary present” and “disclosure present” checks.

---

**End of BRD + backlog.**
