# MOD-013 - F-13 - Shock Schedules

Status: Active (latest methodology)
Source of truth: docs/methodology/methodology_textbook.md
Aligned backlog: docs/implementation/brd_implementation_plan.md and docs/implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md
Tier: Premium

## 1. Scope
Time-structured stress profiles (step/ramp/stepped) over horizon.

## 2. Inputs
Schedule type and month-level parameters.

## 3. Outputs
Month-by-month shock sequence applied to simulation.

## 4. Method Rules
- Support step, ramp, and stepped schedules.
- Validate month indices and bounds.
- Maintain deterministic reproducibility when seed supplied.

## 5. Validation and Tests
- Schedule parser/validator covers invalid shapes.
- Applied schedules change path outcomes as expected.

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
- [Primary Backlog Task: WS5-F13](../implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-ws5-f13)
- [Decision Log](../decision_log.md)
- [Repository README](../../README.md)
<!-- crossref:end -->


