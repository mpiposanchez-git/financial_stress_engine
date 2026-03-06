# UK Household Financial Stress Engine — Golden Source Methodology 📘

**Version:** v0.2.0  
**Status:** Golden source / living document  
**Date:** 2026-03-06  
**Repo:** https://github.com/mpiposanchez-git/financial_stress_engine  
**Evidence snapshot:** _Insert commit SHA for the release (`git rev-parse HEAD`)_  
**Audience order:** (1) auditor/reviewer, (2) end user learner

> This document is the single source of truth for model and methodology content in this repository.
> If any discrepancy is found with historical methodology documents, this file takes absolute precedence.

---

## Abstract

This document specifies and explains the UK Household Financial Stress Engine as an educational simulation tool for household financial stress testing.
It covers deterministic modelling, stochastic/Monte Carlo modelling, assumptions, controls, data provenance, privacy posture, and validation.

## Executive summary

The system simulates how household finances can change under stress scenarios such as income shocks, inflation, mortgage-rate changes, and FX movements.
It is designed for learning and decision support context only.

Key outputs include:
- month-by-month savings path
- runway and depletion timing
- percentile outcomes (P10/P50/P90) for uncertainty analysis

This tool is not financial advice.

## Document governance and control framework

### Versioning

This document uses semantic versioning (`vMAJOR.MINOR.PATCH`):
- MAJOR: major scope change
- MINOR: new model capability or substantive methodology change
- PATCH: editorial clarification

### Change control

Material methodology changes should be accompanied by:
- decision log update
- corresponding tests and evidence updates
- documentation update in this file

### Evidence snapshot rule

Published versions should include the exact commit SHA they describe.

---

## Table of Contents
Abstract
Executive summary
Document governance and control framework
0. Reader guide  
1. Purpose, scope, and guardrails  
2. System architecture overview  
3. Core financial concepts (beginner section)  
4. Numerical correctness (pence + bps, rounding)  
5. Deterministic model methodology  
6. Monte Carlo methodology (monthly paths, IID vs AR(1))  
7. FX & multi-currency methodology (reporting currency)  
8. Additional modelling features (categories, schedules, debt)  
9. UK benchmarking methodology (BHC percentile ranking)  
10. Data module (sources, auto-fetch, user verification, overrides)  
11. Exports (JSON + PDF)  
12. Premium entitlements (POC allowlist; V1 Stripe)  
13. Accessibility & interpretability controls  
14. Privacy-safe measurement (aggregate only)  
15. Validation & testing framework  
15A. Requirements traceability matrix
16. Governance, modularity, and change management  
Appendix: Glossary  

---

## Methodology to Implementation Crosswalk

This index provides direct traceability from methodology chapters to implementation specs (MOD) and execution tasks.

| Methodology chapter | Primary MOD specifications | Primary backlog tasks |
|---|---|---|
| Ch. 5 Deterministic model methodology | [MOD-002](../MOD/MOD-002_F-02_MONTH_BY_MONTH_RUNWAY_CHART.md), [MOD-003](../MOD/MOD-003_F-03_MORTGAGE_RATE_STRESS_MODULE.md), [MOD-010](../MOD/MOD-010_F-10_EMERGENCY_FUND_ADEQUACY_INDICATOR.md) | [WS1-F02](../implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-ws1-f02), [WS1-F15](../implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-ws1-f15), [WS3-F10](../implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-ws3-f10) |
| Ch. 6 Monte Carlo methodology | [MOD-005](../MOD/MOD-005_F-05_MONTE_CARLO_FAN_CHART.md), [MOD-012](../MOD/MOD-012_F-12_SENSITIVITY_TORNADO_CHART.md), [MOD-013](../MOD/MOD-013_F-13_SHOCK_SCHEDULES.md) | [WS5-F05](../implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-ws5-f05), [WS5-F12](../implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-ws5-f12), [WS5-F13](../implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-ws5-f13) |
| Ch. 7 FX and multi-currency | [MOD-007](../MOD/MOD-007_F-07_FX_AND_MULTI_CURRENCY.md) | [F-07](../implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-f-07) |
| Ch. 8 Additional modelling features | [MOD-008](../MOD/MOD-008_F-08_CATEGORY_INFLATION_TOGGLES.md), [MOD-013](../MOD/MOD-013_F-13_SHOCK_SCHEDULES.md), [MOD-014](../MOD/MOD-014_F-14_NON_MORTGAGE_DEBT_SCHEDULE.md), [MOD-015](../MOD/MOD-015_F-15_MORTGAGE_TYPE_SANDBOX.md) | [WS5-F08](../implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-ws5-f08), [WS5-F13](../implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-ws5-f13), [WS5-F14](../implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-ws5-f14), [WS3-F15](../implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-ws3-f15) |
| Ch. 9 UK benchmarking | [MOD-022](../MOD/MOD-022_A-02_UK_BENCHMARKS_REFERENCE_AND_PERCENTILE.md), [MOD-026](../MOD/MOD-026_A-06_ETHICS_AND_FAIRNESS_DISCLOSURE.md) | [WS7-A02A](../implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-ws7-a02a), [WS7-A02B](../implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-ws7-a02b), [WS0-A06](../implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-ws0-a06) |
| Ch. 10 Data module | [MOD-021](../MOD/MOD-021_A-01_DATA_MODULE_AND_PROVENANCE.md) | [WS6-A01](../implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-ws6-a01), [WS6-A01B](../implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-ws6-a01b) |
| Ch. 11 Exports | [MOD-006](../MOD/MOD-006_F-06_PDF_EXPORT.md) | [WS8-F06](../implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-ws8-f06) |
| Ch. 12 Premium entitlements | [MOD-024](../MOD/MOD-024_A-04_PREMIUM_ENTITLEMENTS.md) | [WS0-A04](../implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-ws0-a04) |
| Ch. 13 Accessibility and interpretability | [MOD-025](../MOD/MOD-025_A-05_ACCESSIBILITY_REQUIREMENTS.md), [MOD-011](../MOD/MOD-011_F-11_EXPLAIN_THE_RESULT_NARRATIVES_AND_TOOLTIPS.md) | [WS0-A05](../implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-ws0-a05), [WS3-F11](../implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-ws3-f11) |
| Ch. 14 Privacy-safe measurement | [MOD-027](../MOD/MOD-027_A-07_PRIVACY_SAFE_MEASUREMENT.md) | [WS0-A07](../implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-ws0-a07) |

---

## 0. Reader guide
- Want “what does this do?” → Ch. 1–2  
- Want to understand outputs → Ch. 3 + Ch. 5  
- Want uncertainty modelling → Ch. 6  
- Want FX/multi-currency → Ch. 7  
- Want UK percentiles → Ch. 9  
- Want audit evidence → Ch. 15–16  

---

## 1. Purpose, scope, and guardrails ⚖️

### 1.1 Purpose
The tool simulates household financial resilience under stress (income, costs, rates, FX).

### 1.2 Intended use
Educational scenario simulation.

### 1.3 Non-intended use (important)
- No personalised advice.
- No product recommendation.
- No bank linking / Open Banking.
- No uploads (statements/payslips).

### 1.4 Privacy posture
Authentication uses Clerk. The application is designed not to persist scenario inputs/outputs in a project database.

---

## 2. System architecture overview 🧩
High-level components:
- **Frontend (React):** user inputs, charts, premium gating, exports
- **API (FastAPI):** auth, rate limiting, caps/timeouts, orchestration
- **Engine (shared/engine):** deterministic, Monte Carlo, FX, money utilities
- **Data module:** official defaults, provenance, verification steps, caching
- **Benchmark module:** UK reference values + premium percentiles (BHC)

---

## 3. Core financial concepts (beginner section) 🧠

### 3.1 Cashflow
Monthly cashflow is:

\[
CF = I - E - D - M
\]

Where:
- \(I\): net income  
- \(E\): essential spending  
- \(D\): debt payments (non-mortgage)  
- \(M\): mortgage payment  

### 3.2 Savings dynamics
If cashflow is positive, savings increase; if negative, savings decrease.

### 3.3 Runway
Approximate runway:

\[
\text{runway} \approx \frac{S}{|CF|}
\]

The tool also computes a month-by-month savings path, which is more interpretable.

### 3.4 Percentiles
For Monte Carlo results:
- P10 = downside
- P50 = median
- P90 = upside

---

## 4. Numerical correctness (pence + bps) ✅

### 4.1 Money in minor units (pence)
All monetary values are represented internally as **integer pence** to avoid floating point drift.

### 4.2 Rates in basis points (bps)
All rates and shocks are stored as **integer basis points**:
- 1% = 100 bps

### 4.3 Rounding rule
When converting intermediate decimals to pennies: **round-half-up**.

### 4.4 Why this matters
Auditors and users require penny-accurate, reproducible results.

---

## 5. Deterministic model methodology 📆

### 5.1 Inputs (conceptual)
- Income, essentials, debt, savings (each with currency)
- Mortgage balance, term, type, current and stress rate
- Income shock, inflation shock
- Reporting currency and FX spot rates
- FX stress (optional)
- Horizon months (default 24)

### 5.2 Mortgage payment mechanics
- Interest-only:

\[
P = B \cdot r_m
\]

- Repayment:

\[
P = B \cdot \frac{r_m(1+r_m)^n}{(1+r_m)^n - 1}
\]

Edge cases are handled (0% rate, 0 balance).

### 5.3 Stress mechanics
- Income stress: reduce income by shock percentage  
- Essentials inflation: increase essentials by inflation percentage  
- Rate stress: recompute mortgage payment using stressed rate  
- FX stress: adjust FX rate used for conversion (if set)

### 5.4 Month-by-month savings path

\[
S_{t+1} = \max(0, S_t + CF_t^*)
\]

Outputs:
- savings path array
- minimum savings
- month of depletion
- runway estimate

---

## 6. Monte Carlo methodology (monthly paths) 🎲

### 6.1 Overview
Monte Carlo runs the model many times, drawing random shocks, to produce a distribution of outcomes.

### 6.2 Shock paths (IID vs AR(1))
**IID:** each month independent  
**AR(1):**

\[
x_t = \mu + \phi(x_{t-1} - \mu) + \epsilon_t
\]

This creates persistent periods of stress.

### 6.3 What is stochastic
- income shock path
- inflation path
- mortgage rate path
- FX path (if FX volatility is set)

### 6.4 Outputs and interpretation
Report P10/P50/P90 for:
- runway months
- min savings
- month of depletion

---

## 7. FX & multi-currency methodology 🌍💱

### 7.1 Reporting currency
All outputs are shown in one selected currency.

### 7.2 FX spot rates
User can accept defaults or override. Reporting currency rate is 1.0 by definition.

### 7.3 FX stress and volatility
- Deterministic FX stress: percentage shock to FX level.
- Monte Carlo FX: lognormal path via monthly returns, with optional AR(1) persistence.

### 7.4 Disclosure
BoE FX rates are disclosed as indicative (not official).

---

## 8. Additional modelling features (functionalities 8, 13, 14, 15)

### 8.1 Category inflation
Different inflation rates by category (e.g., food vs energy vs transport).  
Implemented by splitting essentials into categories and applying category-specific inflation.

### 8.2 Shock schedules
Stress can be:
- immediate step change
- gradual ramp
- stepped schedule (month indices)

### 8.3 Debt schedule (optional)
Simplified non-mortgage debt dynamics:
- balance, APR, minimum payment
- simulate balance evolution and payment burden

### 8.4 Mortgage type sandbox
Educational comparison of repayment vs interest-only behaviour.

---

## 9. UK benchmarking methodology (BHC) 🇬🇧

### 9.1 Purpose
Provide context:
- Free: UK reference values (median/average)
- Premium: “you are approximately in X percentile”

### 9.2 Source
DWP HBAI data tables (BHC). (https://www.gov.uk/government/statistics/households-below-average-income-for-financial-years-ending-1995-to-2024)

### 9.3 Method (BHC)
- Convert monthly net income to annual net income.
- Compare to income thresholds from HBAI tables for the reference year.
- Return percentile bucket (approximate).

### 9.4 Ethics and limitations (mandatory)
- Percentiles are approximate.
- Depends on definition/year and household composition.
- Not a measure of personal worth.
- Presented as context, not advice.

### 9.5 Ethics & limitations disclosure text (UI reference)
Use this plain-language disclosure wherever percentile ranking is displayed:
- Approximate benchmark only.
- Uses the UK HBAI BHC definition and depends on year and definitions.
- Not advice.
- Not a measure of worth.

---

## 10. Data module (sources, auto-fetch, verification, overrides) 🔍

### 10.1 Datasets used
- ONS CPI/CPIH: https://www.ons.gov.uk/economy/inflationandpriceindices/datasets/consumerpriceindices/current  
- BoE Bank Rate: https://www.bankofengland.co.uk/boeapps/database/Bank-Rate.asp  
- BoE FX: https://www.bankofengland.co.uk/boeapps/database/Rates.asp  
- Ofgem price cap: https://www.ofgem.gov.uk/information-consumers/energy-advice-households/get-energy-price-cap-standing-charges-and-unit-rates-region  
- DWP HBAI: https://www.gov.uk/government/statistics/households-below-average-income-for-financial-years-ending-1995-to-2024  

### 10.2 Auto-fetch design
Use scheduled jobs (Render Cron Jobs pattern): https://render.com/docs/cronjobs

Store:
- fetched_at timestamp
- source URL
- hash (sha256)
- values used in defaults

### 10.3 User verification steps
For each dataset:
1) open official link
2) download table/CSV
3) confirm “as of” value matches the tool’s displayed value

### 10.4 Manual overrides
Users can override defaults. Exports record:
- default vs override
- dataset timestamp and hash

---

## 11. Exports (JSON + PDF) 📤

### 11.1 JSON export
Always available; includes full inputs, outputs, and provenance.

### 11.2 PDF export (premium)
Includes:
- summary + charts (static)
- inputs and assumptions
- version metadata
- data sources and timestamps
- disclaimers and limitations

---

## 12. Premium entitlements (recommendation #1) 💳

### 12.1 POC entitlement (no payments)
Premium access granted via server-side allowlist (preferably by Clerk subject `sub`).

### 12.2 V1 upgrade path
Stripe subscription with webhook-based entitlement updates.

---

## 13. Accessibility & interpretability (recommendation #2) ♿

### 13.1 Accessibility principle
Charts must have:
- clear labels
- keyboard focus
- a text summary describing the result (“what the chart shows”)

### 13.2 Interpretability principle
Use tooltips, glossary definitions, and “explain-the-result” narratives.

---

## 14. Privacy-safe measurement (recommendation #4) 🔒📈

### 14.1 What we measure
Only aggregate counters (e.g., number of deterministic runs, number of Monte Carlo runs).

### 14.2 What we do not measure
- no third-party analytics trackers
- no user-level tracking or profiling
- no scenario contents stored

### 14.3 Disclosure
Privacy policy states that aggregate operational metrics may be collected.

---

## 15. Validation & testing framework ✅

- Unit tests: mortgage, rounding, FX conversion, schedules
- Golden tests: known-answer scenarios
- Monte Carlo: reproducibility (seed), sigma sensitivity
- Contract tests: API schema stability
- Security tests: prevent logging request bodies and auth headers

### 15A. Requirements traceability matrix (RTM)

| ID | Requirement | Code (primary) | Evidence/tests | Status |
|---|---|---|---|---|
| FR-001 | Clerk auth required | `services/api/app/auth.py` | protected route coverage | Implemented |
| FR-002 | JWT signature and issuer validation | `services/api/app/auth.py` | auth validation tests/manual verification | Implemented |
| FR-003 | Deterministic stress run | `shared/engine/deterministic.py` | `services/api/tests/test_deterministic_golden.py` | Implemented |
| FR-004 | Month-by-month savings path | `shared/engine/deterministic.py` | deterministic golden tests | Implemented |
| FR-005 | Monte Carlo simulation | `shared/engine/montecarlo.py` | `services/api/tests/test_montecarlo_reproducibility.py` | Implemented |
| FR-006 | Multi-currency and FX support | `shared/engine/fx.py`, `shared/engine/inputs.py` | `services/api/tests/test_fx.py` | Implemented |
| FR-007 | Premium server-side gating | `services/api/app/entitlements.py` | `services/api/tests/test_entitlements.py` | Implemented |
| FR-008 | Privacy-safe aggregate telemetry | `services/api/app/telemetry.py` | `services/api/tests/test_telemetry.py` | Implemented |

---

## 16. Governance, modularity, and change management 🧾

### 16.1 Modularity
Each capability is a module with clear boundaries.

### 16.2 UDF separation
User-defined functions are placed in dedicated scripts to reduce “blast radius” of changes.

### 16.3 Change control
Any modelling change requires:
- Decision log entry
- Spec update (this doc and/or MOD specs)
- Tests updated and CI green

---

## Appendix — Glossary
(Expand over time: cashflow, runway, BHC, CPIH, bps, AR(1), etc.)

---

**End of methodology textbook.**

<!-- crossref:start -->
## Related Documents

- [Repository README](../../README.md)
- [BRD Implementation Plan](../implementation/brd_implementation_plan.md)
<!-- crossref:end -->

