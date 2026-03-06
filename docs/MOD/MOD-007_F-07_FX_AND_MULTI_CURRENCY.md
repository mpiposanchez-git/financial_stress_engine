# MOD-007 - F-07 - FX and Multi-Currency

Status: Active (latest methodology)
Source of truth: docs/methodology/methodology_textbook.md
Aligned backlog: docs/implementation/brd_implementation_plan.md and docs/implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md
Tier: Free + Premium

## 1. Scope
Convert mixed-currency household values into a reporting currency with optional stress/volatility.

## 2. Inputs
Per-field currency, reporting currency, spot FX, stress bps, optional vol bps.

## 3. Outputs
Reporting-currency deterministic and stochastic metrics.

## 4. Method Rules
- Reporting currency spot must equal 1.0.
- Deterministic mode applies FX stress level shifts.
- Monte Carlo mode may include FX stochastic paths for premium flows.

## 5. Validation and Tests
- FX conversion unit tests pass for expected pairs.
- Invalid/missing required FX rates are rejected.

## 6. Non-Goals
- This module does not provide regulated financial advice.
- This module must not weaken authentication, entitlement, or privacy controls.

## 7. Change Control
- Any material behavior change requires updates to this file and the methodology textbook.
- Changes should include corresponding test updates and a decision/progress log entry.

<!-- crossref:start -->
## Related Documents

- [Methodology Golden Source](../methodology/methodology_textbook.md)
- [BRD Feature Catalog](../implementation/brd_implementation_plan.md#1-poc-feature-catalog-functionalities-120--additions)
- [Primary Backlog Task: F-07](../implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-f-07)
- [Decision Log](../decision_log.md)
- [Repository README](../../README.md)
<!-- crossref:end -->


