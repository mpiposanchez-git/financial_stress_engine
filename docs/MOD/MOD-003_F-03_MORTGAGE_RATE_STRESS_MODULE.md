# MOD-003 - F-03 - Mortgage Rate Stress Module

Status: Active (latest methodology)
Source of truth: docs/methodology/methodology_textbook.md
Aligned backlog: docs/implementation/brd_implementation_plan.md and docs/implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md
Tier: Free

## 1. Scope
Shows current vs stressed mortgage payment impact on cashflow.

## 2. Inputs
Mortgage balance, term, type, current rate, stressed rate.

## 3. Outputs
Base payment, stressed payment, delta and explanation.

## 4. Method Rules
- Support repayment and interest-only mechanics.
- Handle zero balance/rate edge cases safely.
- Use pence and bps internal representation.

## 5. Validation and Tests
- Unit tests for repayment and interest-only payment formulas.
- Results page displays both base and stressed values.

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
- [Primary Backlog Task: WS3-F03](../implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-ws3-f03)
- [Decision Log](../decision_log.md)
- [Repository README](../../README.md)
<!-- crossref:end -->


