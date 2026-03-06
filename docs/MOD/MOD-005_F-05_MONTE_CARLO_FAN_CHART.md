# MOD-005 - F-05 - Monte Carlo Fan Chart

Status: Active (latest methodology)
Source of truth: docs/methodology/methodology_textbook.md
Aligned backlog: docs/implementation/brd_implementation_plan.md and docs/implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md
Tier: Premium

## 1. Scope
Uncertainty distribution reporting with percentile outputs.

## 2. Inputs
Stress distributions, n_sims, horizon, seed, optional AR(1) parameters.

## 3. Outputs
P10/P50/P90 metrics and runtime/seed reproducibility metadata.

## 4. Method Rules
- Percentiles must be deterministic for same seed and inputs.
- Enforce max sims and max horizon caps.
- Expose uncertainty as context, not advice.

## 5. Validation and Tests
- Reproducibility tests pass for IID and AR(1).
- Premium gate blocks non-entitled access.

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
- [Primary Backlog Task: WS5-F05](../implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-ws5-f05)
- [Decision Log](../decision_log.md)
- [Repository README](../../README.md)
<!-- crossref:end -->


