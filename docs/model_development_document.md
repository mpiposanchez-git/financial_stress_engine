# UK Household Financial Stress Engine  
## Model Development Document (BRD + Model Development & Validation Report)

**Document ID:** FSE-MDD  
**Version:** v0.2.0 (Draft)  
**Status:** Draft (auditor-grade first; user guide second)  
**Date:** 2026-03-04  
**Repository:** `https://github.com/mpiposanchez-git/financial_stress_engine`  
**Evidence snapshot (commit SHA):** `29ff7c117fe768b877bdf4b35181e18f37e7d437`  
**Primary audience:** users (non-specialists) + independent reviewer/auditor (technical)  

---

## Abstract

This document specifies and explains the **UK Household Financial Stress Engine**, an educational web application for simulating household financial stress scenarios in the UK context. The tool supports:

- **Deterministic stress testing** (single scenario), and  
- **Probabilistic stress testing** (Monte Carlo simulation with month-by-month stochastic paths).

The application is designed to be **anonymous and privacy-minimising**: authentication is handled by a third-party identity provider (**Clerk**), and the backend is designed to avoid persisting household inputs/outputs.

The methodology is intentionally transparent, reproducible, and testable. Numerical correctness is prioritised through the use of **minor units (pence)** for money and **basis points (bps)** for rates, plus a suite of unit/contract tests.

---

## Executive Summary (for non-specialists)

Households face uncertainty around:

- income (job loss / reduced hours),
- living costs (inflation), and
- debt servicing costs (mortgage rate changes).

This tool asks you for a few numbers and then simulates how your **monthly budget** and **savings** might evolve under stress.

It produces:

- a **monthly savings path** over a chosen horizon (default 24 months),
- an estimate of **runway** (how long savings can cover a monthly deficit), and
- for Monte Carlo: **P10 / P50 / P90** outcomes that summarize downside / typical / upside results.

**Important:** this tool is **not financial advice**. It is an educational simulator.

---

# Document Governance & Control Framework 🧾

## Versioning

This document uses semantic versioning: **vMAJOR.MINOR.PATCH**

- **MAJOR**: major scope change (new product intent)  
- **MINOR**: new implemented capability or modelling component  
- **PATCH**: editorial improvements, typos, reformatting, non-substantive clarifications  

## Change control

All material changes must reference:
- a GitHub Issue/Task (recommended), and/or  
- a Decision ID in `docs/decision_log.md` (required for methodology changes).

**Material change examples**
- modifying formulas, distributions, or clipping rules  
- changing output fields or interpretation  
- adding/removing input fields  
- changing data handling or persistence posture  

## Evidence snapshot rule (auditability)

Any published version of this document must include the **exact commit SHA** it is describing.  
This version is tied to: `29ff7c117fe768b877bdf4b35181e18f37e7d437`.

---

# Table of Contents

1. Background and Problem Statement  
2. Scope and Requirements  
3. User Journeys  
4. Model Methodology (Deterministic)  
5. Model Methodology (Monte Carlo)  
6. FX and Multi-Currency Methodology  
7. Implementation Architecture  
8. Validation & Testing Evidence  
9. Risks, Limitations, and Guardrails  
10. Requirements Traceability Matrix (RTM)  
11. Glossary  

---

# Part I — Business Requirements Document (BRD)

## 1. Background and Problem Statement

### 1.1 Motivation
Households often want a simple way to understand financial resilience. A practical lens is **runway**: how long savings can absorb a deficit if income falls or costs rise.

### 1.2 Intended users
- **Non-specialists:** want clear results and explanations.
- **Financially literate users:** want transparency and reproducibility.
- **Auditors/reviewers:** want traceability, test evidence, and control framework.

### 1.3 Intended use vs non-intended use
**Intended use**
- Educational simulation of household cashflows and savings under stress.

**Non-intended use**
- No personalised advice.
- No product recommendation (mortgage selection, investments, etc).
- No bank linking or document uploads.

---

## 2. Scope

### 2.1 In scope (implemented in `29ff7c117fe768b877bdf4b35181e18f37e7d437`)

**Core modelling**
- Deterministic stress test producing:
  - stressed vs base monthly cashflow
  - **24-month (configurable) savings path**
  - runway estimate and month-of-depletion (if applicable)
- Monte Carlo simulation producing:
  - month-by-month stochastic paths (income shock, inflation shock, mortgage rate path)
  - optional **AR(1)** persistence (“momentum” in shocks)
  - percentile summaries (P10/P50/P90)
- Multi-currency inputs and reporting:
  - each main input can be assigned a currency (GBP/EUR/USD)
  - user selects a **reporting currency**
  - FX spot rates and stress shocks are modelled and applied

**Engineering and controls**
- Authentication always on (Clerk JWT validation).
- In-memory rate limiting keyed by authenticated subject.
- Guardrails: caps on Monte Carlo size/horizon + request timeout.
- CI pipelines for API lint/tests and frontend tests/build.

### 2.2 Out of scope (by design)
- Bank/Open Banking ingestion.
- Uploading personal documents.
- Any feature that could be interpreted as regulated financial advice.

---

## 3. User Journeys (current POC)

### Journey A — Run a deterministic + Monte Carlo stress test
1. User signs in via Clerk (email-based account).
2. User fills in a simple form (income, spending, savings, mortgage, FX assumptions).
3. User runs the simulation.
4. Results page shows key deterministic numbers and Monte Carlo percentiles.

---

# Part II — Model Development & Validation Report (MDR)

## 4. Key modelling concepts (learning section)

### 4.1 Minor units and basis points (why we use them)
- **Minor units (pence):** avoids floating point rounding issues for money.
  - £1.23 is represented as 123 pence (an integer).
- **Basis points (bps):** avoids rounding issues for rates.
  - 1.00% = 100 bps, 4.75% = 475 bps.

This is a standard numerical-stability technique in financial systems.

### 4.2 Percentiles (P10 / P50 / P90)
- **P10:** a downside outcome (worse than typical)
- **P50:** the median outcome (“typical”)
- **P90:** an upside outcome (better than typical)

---

## 5. Deterministic Model Specification

### 5.1 Inputs (high level)
Deterministic inputs include monthly:
- net income (pence + currency)
- essentials spending (pence + currency)
- debt payments (pence + currency)
- cash savings (pence + currency)
- mortgage balance (pence + currency)
- mortgage type (repayment / interest-only)
- mortgage rates: current and stress (bps)
- income shock and inflation shock (bps)
- reporting currency + FX rates + FX stress (bps)
- horizon months (default 24)

See: `shared/engine/inputs.py` (https://github.com/mpiposanchez-git/financial_stress_engine/blob/29ff7c117fe768b877bdf4b35181e18f37e7d437/shared/engine/inputs.py).

### 5.2 Mortgage payment
- **Interest-only:** monthly payment = balance × monthly_rate  
- **Repayment (amortising):** standard annuity payment formula with edge-case handling for 0% rates.

### 5.3 Base and stressed cashflow
Cashflow is computed in the reporting currency.

- Base cashflow = income − essentials − debt − mortgage(current)
- Stressed cashflow:
  - stressed income = income × (1 − income_shock)
  - stressed essentials = essentials × (1 + inflation)
  - mortgage uses stressed rate
  - (and FX-stressed conversion rates if FX stress is supplied)

### 5.4 Savings path and runway
The model produces a month-by-month savings path:

- `savings[0] = initial_savings`
- `savings[t] = max(0, savings[t-1] + stressed_cashflow)`

Outputs include:
- `min_savings` (minimum over horizon)
- `month_of_depletion` (first month savings hits zero, if it does)
- `runway_months` (ratio-based estimate when cashflow < 0)

Deterministic engine: `shared/engine/deterministic.py` (https://github.com/mpiposanchez-git/financial_stress_engine/blob/29ff7c117fe768b877bdf4b35181e18f37e7d437/shared/engine/deterministic.py).

---

## 6. Monte Carlo Model Specification (monthly stochastic paths)

### 6.1 What is Monte Carlo here?
Monte Carlo means we run the model many times (e.g., 1,000 simulations), each time drawing different random shocks, and then summarize the distribution of outcomes.

### 6.2 Drivers simulated
This PoC models uncertainty in:
- income shock path (bps)
- inflation path (bps)
- mortgage rate stress path (bps)
- (optional) FX monthly volatility for non-reporting currencies

### 6.3 IID vs AR(1) shocks
- **IID (independent):** each month’s shock is independent of the previous month.
- **AR(1):** shock has persistence:  
  `shock_t = φ * shock_(t-1) + ε_t`, where `0 ≤ φ < 1`.

AR(1) allows multi-month “bad streaks” (more realistic for some risks).

Monte Carlo engine: `shared/engine/montecarlo.py` (https://github.com/mpiposanchez-git/financial_stress_engine/blob/29ff7c117fe768b877bdf4b35181e18f37e7d437/shared/engine/montecarlo.py).

### 6.4 Outputs
Current Monte Carlo API returns percentile summaries for:
- runway months (P10/P50/P90)
- min savings (P10/P50/P90) in pence + formatted strings
- month-of-depletion (P10/P50/P90)

API contract models: `services/api/app/models.py` (https://github.com/mpiposanchez-git/financial_stress_engine/blob/29ff7c117fe768b877bdf4b35181e18f37e7d437/services/api/app/models.py).

---

## 7. FX and Multi-Currency Methodology

### 7.1 Why FX is included
Some households have income, expenses, or savings in different currencies. A stress test should be able to express results in a single **reporting currency** and allow FX shocks.

### 7.2 FX inputs
- `fx_spot_rates`: mapping from currency → rate to reporting currency (reporting currency must be 1.0)
- `fx_stress_bps`: optional stress per currency applied to the spot rate
- `fx_monthly_vol_bps`: optional monthly FX volatility (Monte Carlo)

FX utilities: `shared/engine/fx.py` (https://github.com/mpiposanchez-git/financial_stress_engine/blob/29ff7c117fe768b877bdf4b35181e18f37e7d437/shared/engine/fx.py).

---

## 8. Implementation Architecture (what runs where)

### 8.1 Repository layout
- `apps/web/` — React frontend (Clerk + UI)
- `services/api/` — FastAPI backend
- `shared/engine/` — modelling engine (deterministic, Monte Carlo, money, FX)

### 8.2 API endpoints
- `GET /health`
- `POST /api/v1/deterministic/run`
- `POST /api/v1/montecarlo/run`

Router: `services/api/app/routes.py` (https://github.com/mpiposanchez-git/financial_stress_engine/blob/29ff7c117fe768b877bdf4b35181e18f37e7d437/services/api/app/routes.py).

### 8.3 Security and privacy controls
- Clerk JWT validation is mandatory (no bypass present in this snapshot).
- Rate limiting uses `auth.subject` stored in `request.state`.
- Timeout and caps are enforced in API routes.

Auth: `services/api/app/auth.py` (https://github.com/mpiposanchez-git/financial_stress_engine/blob/29ff7c117fe768b877bdf4b35181e18f37e7d437/services/api/app/auth.py)  
Settings/caps: `services/api/app/settings.py` (https://github.com/mpiposanchez-git/financial_stress_engine/blob/29ff7c117fe768b877bdf4b35181e18f37e7d437/services/api/app/settings.py)

### 8.4 CI pipelines
- API: `ruff` + `pytest` on backend + shared engine  
  Workflow: `.github/workflows/api-ci.yml` (https://github.com/mpiposanchez-git/financial_stress_engine/blob/29ff7c117fe768b877bdf4b35181e18f37e7d437/.github/workflows/api-ci.yml)

---

## 9. Validation & Testing Evidence (auditor-grade)

### 9.1 What “validation” means here
Validation means answering: **“Does the model do what it claims, consistently, and safely?”**

This repo includes:
- **Golden tests** for deterministic calculations
- **FX unit tests**
- **Monte Carlo reproducibility tests**
- **API contract tests**
- **Logging hardening tests** to reduce risk of sensitive leakage

Examples (see `services/api/tests/`):
- `test_deterministic_golden.py` (https://github.com/mpiposanchez-git/financial_stress_engine/blob/29ff7c117fe768b877bdf4b35181e18f37e7d437/services/api/tests/test_deterministic_golden.py)
- `test_fx.py` (https://github.com/mpiposanchez-git/financial_stress_engine/blob/29ff7c117fe768b877bdf4b35181e18f37e7d437/services/api/tests/test_fx.py)
- `test_montecarlo_reproducibility.py` (https://github.com/mpiposanchez-git/financial_stress_engine/blob/29ff7c117fe768b877bdf4b35181e18f37e7d437/services/api/tests/test_montecarlo_reproducibility.py)
- `test_api_contracts.py` (https://github.com/mpiposanchez-git/financial_stress_engine/blob/29ff7c117fe768b877bdf4b35181e18f37e7d437/services/api/tests/test_api_contracts.py)
- `test_logging_hardening.py` (https://github.com/mpiposanchez-git/financial_stress_engine/blob/29ff7c117fe768b877bdf4b35181e18f37e7d437/services/api/tests/test_logging_hardening.py)
- `test_no_sensitive_logging.py` (https://github.com/mpiposanchez-git/financial_stress_engine/blob/29ff7c117fe768b877bdf4b35181e18f37e7d437/services/api/tests/test_no_sensitive_logging.py)

### 9.2 Recommended next validation steps (forward-looking)
- Add scenario library (named household archetypes) with expected outputs.
- Add property-based tests around edge cases:
  - zero mortgage term, zero rates, extreme FX shocks, etc.
- Add explicit “model limitations” banner in UI per output section.

---

## 10. Risks, Guardrails, and Limitations

### 10.1 Regulatory risk
Mitigation: disclaimers, no product recommendations, no “what you should do” guidance.

### 10.2 Numerical risk
Mitigation: pence + bps inputs, explicit rounding functions, reproducibility tests.

### 10.3 Abuse/performance risk
Mitigation: auth always on + rate limiting + caps + timeout.

---

# 11. Requirements Traceability Matrix (RTM) ✅

> **Goal:** If an auditor asks “Where is this implemented and how is it tested?”, the RTM answers it.

**Legend**
- **Code link**: primary implementation location  
- **Evidence/tests**: what to run to validate it  
- **Status**: Implemented / Partially implemented / Not implemented  

| ID | Requirement | Code (primary) | Evidence / Tests | Status |
|---|---|---|---|---|
| FR-001 | Clerk authentication required | `services/api/app/auth.py` | API endpoints require `require_auth` dependency | Implemented |
| FR-002 | API validates Clerk JWT signatures | `services/api/app/auth.py` | unit tests + manual verification with Clerk token | Implemented |
| FR-003 | Deterministic stress test | `shared/engine/deterministic.py` | `test_deterministic_golden.py` | Implemented |
| FR-004 | Deterministic month-by-month savings path (default 24m) | `shared/engine/deterministic.py` | `test_deterministic_golden.py` | Implemented |
| FR-005 | Monte Carlo simulation | `shared/engine/montecarlo.py` | `test_montecarlo_reproducibility.py` | Implemented |
| FR-006 | Monthly stochastic paths for shocks | `shared/engine/montecarlo.py` | reproducibility + distribution sanity checks | Implemented |
| FR-007 | AR(1) option | `shared/engine/montecarlo.py` + `inputs.py` | reproducibility tests | Implemented |
| FR-008 | Multi-currency inputs | `shared/engine/inputs.py` | schema validation (missing FX rates fails) | Implemented |
| FR-009 | Reporting currency selection | `shared/engine/inputs.py` + web form | UI selects reporting currency | Implemented |
| FR-010 | FX stress (bps) | `shared/engine/fx.py` + deterministic | `test_fx.py` | Implemented |
| FR-011 | FX monthly volatility (Monte Carlo) | `shared/engine/inputs.py` + `montecarlo.py` | `test_fx.py` + MC tests | Implemented |
| FR-012 | Exact arithmetic (pence + bps) | `shared/engine/money.py` + inputs | money tests + golden tests | Implemented |
| FR-013 | Rate limiting keyed by auth subject | `services/api/app/routes.py` + `rate_limit.py` | manual test + future unit test | Implemented |
| FR-014 | Caps on sims/horizon + timeout | `routes.py` + `settings.py` | try invalid payloads → 422; timeout → 504 | Implemented |
| FR-015 | Export JSON | UI route-state + API JSON response | inherent (API returns JSON) | Implemented |
| FR-016 | Export PDF | (not evidenced in this snapshot) | N/A | **Not implemented (in repo snapshot)** |

---

## 12. Glossary (quick)

- **Cashflow:** income minus expenses (monthly).  
- **Runway:** approximate months savings can cover a deficit.  
- **Stress test:** apply an adverse scenario and observe impact.  
- **Monte Carlo:** many random simulations to produce a distribution.  
- **Pence / minor units:** integer representation of money.  
- **Basis points (bps):** integer representation of rates; 100 bps = 1%.  
- **AR(1):** “autoregressive” process with persistence.  
- **JWT/JWKS:** mechanisms for verifying signed auth tokens.

---

**End of document.**
