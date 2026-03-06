# MOD-015 - F-15 - Mortgage Type Sandbox

Status: Active (latest methodology)
Source of truth: docs/methodology/methodology_textbook.md
Aligned backlog: docs/implementation/brd_implementation_plan.md and docs/implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md
Tier: Free

## 1. Scope
Educational comparison of repayment vs interest-only behavior.

## 2. Inputs
Shared mortgage parameters and type selection.

## 3. Outputs
Side-by-side payment behavior and narrative explanation.

## 4. Method Rules
- Use same core formulas as production mortgage engine.
- Explain behavioral differences without recommendations.
- Handle zero-rate and zero-balance edge cases.

## 5. Validation and Tests
- Sandbox values align with mortgage engine unit tests.
- UI renders both type outcomes with explanatory text.

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
- [Primary Backlog Task: WS1-F15](../implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-ws1-f15)
- [Primary Backlog Task: WS3-F15](../implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-ws3-f15)
- [Decision Log](../decision_log.md)
- [Repository README](../../README.md)
<!-- crossref:end -->


