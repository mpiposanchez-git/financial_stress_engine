# MOD-002 - F-02 - Month-by-Month Runway Chart

Status: Active (latest methodology)
Source of truth: docs/methodology/methodology_textbook.md
Aligned backlog: docs/implementation/brd_implementation_plan.md and docs/implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md
Tier: Free

## 1. Scope
Deterministic month index vs savings trajectory with depletion context.

## 2. Inputs
Initial savings and stressed monthly cashflow path.

## 3. Outputs
Savings path, min savings, month of depletion, runway interpretation.

## 4. Method Rules
- Compute path month-by-month with floor at zero.
- Provide chart plus accessible tabular/text summary.
- Keep outputs in reporting currency minor units internally.

## 5. Validation and Tests
- Golden test verifies expected savings path for fixed scenario.
- UI shows chart caption and text summary.

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
- [Primary Backlog Task: WS1-F02](../implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-ws1-f02)
- [Primary Backlog Task: WS3-F02](../implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-ws3-f02)
- [Decision Log](../decision_log.md)
- [Repository README](../../README.md)
<!-- crossref:end -->


