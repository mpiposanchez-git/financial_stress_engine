# MOD-004 - F-04 - Scenario Comparison

Status: Active (latest methodology)
Source of truth: docs/methodology/methodology_textbook.md
Aligned backlog: docs/implementation/brd_implementation_plan.md and docs/implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md
Tier: Premium

## 1. Scope
Compare Base vs A/B/C scenario outcomes side-by-side.

## 2. Inputs
Multiple scenario payload variants.

## 3. Outputs
Comparison table across runway, depletion, min savings, mortgage stress.

## 4. Method Rules
- Server-side premium enforcement is mandatory.
- Same methodology assumptions as deterministic core.
- Clearly label scenario provenance and assumptions.

## 5. Validation and Tests
- Non-premium requests return 403.
- Premium users receive comparison payload with required metrics.

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
- [Primary Backlog Task: WS4-F04](../implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-ws4-f04)
- [Decision Log](../decision_log.md)
- [Repository README](../../README.md)
<!-- crossref:end -->


