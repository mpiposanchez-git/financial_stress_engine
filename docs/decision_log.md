# UK Financial Stress Engine

## Master Decision Log (Single Source of Truth)

This document consolidates all strategic, technical, legal, and
operational decisions.

------------------------------------------------------------------------

# STR-001 --- Strategic Positioning

## Decision

Build an anonymous, educational UK household financial stress testing
platform focused on deterministic and probabilistic simulations.

Explicitly exclude: - Financial advice - Product recommendations -
Mortgage selection guidance - Institutional targeting

## Rationale

Minimises regulatory and employer conflict risk while preserving
monetisation optionality.

## Review Date

2026-04-14

------------------------------------------------------------------------

# TEC-001 --- Technology Stack

## Decision

-   Python 3.11+
-   FastAPI backend
-   Modular engine architecture
-   Pydantic validation
-   pytest for testing
-   Ruff for linting
-   GitHub Actions CI
-   uv for dependency management
-   Proprietary repository (private)

## Rationale

Maximises modelling control, scalability, automation, and low
maintenance.

## Review Date

2026-04-14

------------------------------------------------------------------------

# LEG-001 --- Legal Scope & Compliance

## Decision

Operate strictly as an educational simulation tool. Include prominent
disclaimers. Collect minimal data. Avoid storing PII. Delegate payments
to third-party provider.

## Rationale

Reduces FCA risk, GDPR exposure, and reputational risk.

## Review Date

2026-04-14

------------------------------------------------------------------------

# LEG-002 --- Licensing Strategy

## Decision

Use a proprietary closed-source license. All rights reserved. No
open-source release at this stage.

## Rationale

Preserves intellectual property control, monetisation flexibility, and
long-term optionality.

## Review Date

2026-09-01

------------------------------------------------------------------------

# PRD-001 --- Dual Product Strategy

## Decision

Develop two versions in parallel:

V1 (Mass Market): - Deterministic stress testing - Lower price point

V2 (Advanced): - Monte Carlo simulations - P10/P50/P90 outputs -
Sensitivity analysis - Premium pricing

## Rationale

Allows modelling depth without sacrificing commercial reach.

## Review Date

2026-04-14

------------------------------------------------------------------------

# FIN-001 --- Capital & Time Guardrails

## Decision

Maximum acceptable annual capital loss: £3,000 Maximum sustained weekly
time commitment (pre-validation): 10 hours

Kill criteria (6 months): - Conversion \< 1% - MAU \< 100 - Maintenance
\> 5h/week - Regulatory ambiguity persists

## Rationale

Prevents sunk cost fallacy and protects family-first downside.

## Review Date

2026-09-01

------------------------------------------------------------------------

# SCL-001 --- Scaling Criteria

## Decision

Scale only if ALL conditions met: - ≥2% conversion sustained 3 months -
≥300 paying users - Churn \< 8% - Maintenance \< 3h/week - Legal risk
controlled

## Review Date

Triggered by metrics

------------------------------------------------------------------------

# OPS-001 --- Cloud Deployment Baseline Confirmed

## Decision

Adopt GitHub Pages (frontend) + Render (API) + Clerk (authentication) as
the operational baseline for current live development.

## Rationale

This architecture has been validated end-to-end in production-like
conditions, including authenticated simulation execution.

## Review Date

2026-06-01

------------------------------------------------------------------------

# SEC-001 --- Temporary Auth Bypass Forbidden in Normal Operation

## Decision

Temporary auth bypass controls were used for diagnostics and then fully
removed from code and env templates. Authentication remains mandatory in
normal operation.

## Rationale

Bypass was useful for isolating simulation-path issues but is not
acceptable for routine deployment due to security and compliance risks.

## Review Date

2026-04-01

------------------------------------------------------------------------

# Decision Log — New Entries (Append to docs/decision_log.md)

> Date: 2026-03-04  
> Append these entries to the end of `docs/decision_log.md`.

---

## LEG-002 — Clerk authentication always on (no runtime bypass)

**Context**  
Bypass toggles were included for testing convenience. Production posture must be “auth always on”.

**Options considered**  
1) Keep runtime bypass flags for local/CI  
2) Remove bypass flags and test using dependency overrides/mocks ✅  
3) Keep bypass but hard-gate to local env only

**Decision**  
Option 2.

**Assumptions**  
- Tests can inject a fake authenticated principal via dependency overrides.

**Risks & mitigations**  
- Risk: more test setup.  
  Mitigation: a single reusable `override_auth()` fixture.

**Capacity impact**  
~1–2 sessions.

**Validation metrics**  
- Unauthenticated requests fail outside tests; CI tests pass without bypass flags.

**Review date**  
2026-03-18

---

## TEC-004 — Exact arithmetic: integer pence + integer basis points, explicit rounding

**Context**  
You want no numerical drift.

**Options considered**  
1) floats everywhere  
2) Decimal everywhere  
3) integer pence for money + integer bps for rates, Decimal only internally where needed ✅

**Decision**  
Option 3.

**Rounding policy**  
- Convert user inputs to pence by rounding to nearest penny (round-half-up).  
- Apply percent changes in pence with explicit rounding.  
- Mortgage payment quantized to 1 penny.

**Capacity impact**  
~2–4 sessions.

**Validation metrics**  
- Golden tests are penny-exact; no floats appear in engine core.

**Review date**  
2026-03-25

---

## MOD-003 — Deterministic outputs include month-by-month savings path (24 months default)

**Context**  
Dynamic view required; a single-month snapshot is insufficient.

**Decision**  
Implement month-by-month savings path (monthly time step) with:
- `savings_path`, `min_savings`, `month_of_depletion`, `runway_months`.

**Capacity impact**  
~1–2 sessions.

**Validation metrics**  
- Golden scenario includes full savings path and depletion month.

**Review date**  
2026-03-18

---

## MOD-004 — Monte Carlo uses monthly shock paths (IID), with AR(1) persistence as an option

**Context**  
You want monthly paths and a hook for persistence.

**Decision**  
- Default: monthly IID draws per simulation and month.  
- Optional: AR(1) mode for persistence (behind a flag).

**Capacity impact**  
~2–5 sessions.

**Validation metrics**  
- Seed reproducibility; sigma sensitivity checks; optional AR(1) tests.

**Review date**  
2026-04-01

---

## MOD-005 — Multi-currency inputs + FX risk driver + selectable reporting currency

**Context**  
Users can have multiple currencies. FX is a risk driver. Outputs must be displayed in a chosen reporting currency.

**Options considered**  
1) Single currency only (GBP)  
2) Multi-currency without FX risk (static conversion)  
3) Multi-currency + FX risk + reporting currency selector ✅

**Decision**  
Option 3.

**Design rules**  
- Each monetary input has a currency code.  
- Convert to reporting currency using spot FX; quantize to pennies.  
- Deterministic FX stress parameter supported.  
- Monte Carlo FX paths supported (lognormal via monthly Normal returns).

**Capacity impact**  
~3–6 sessions (engine + API + UI + tests).

**Validation metrics**  
- Unit tests for conversion and rounding.  
- Golden scenario with 2+ currencies.  
- Monte Carlo sensitivity: higher FX sigma widens distributions.

**Review date**  
2026-04-08

<!-- crossref:start -->
## Related Documents

- [Repository README](../README.md)
- [Methodology Golden Source](methodology/methodology_textbook.md)
- [BRD Implementation Plan](implementation/brd_implementation_plan.md)
<!-- crossref:end -->

