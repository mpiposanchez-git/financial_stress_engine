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

End of Master Decision Log
