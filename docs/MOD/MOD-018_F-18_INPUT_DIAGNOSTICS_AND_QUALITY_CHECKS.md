# MOD-018 - F-18 - Input Diagnostics and Quality Checks

Status: Active (latest methodology)
Source of truth: docs/methodology/methodology_textbook.md
Aligned backlog: docs/implementation/brd_implementation_plan.md and docs/implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md
Tier: Free

## 1. Scope
Real-time validation/warnings for inconsistent or risky input combinations.

## 2. Inputs
Wizard form state.

## 3. Outputs
Blocking errors and non-blocking warnings with rationale.

## 4. Method Rules
- Separate hard validation from soft warnings.
- Link errors to controls via accessibility attributes.
- Avoid collecting personal profile data for diagnostics.

## 5. Validation and Tests
- Invalid inputs block submit with specific messages.
- Warnings appear for configured soft-rule conditions.

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
- [Primary Backlog Task: WS2-F18](../implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-ws2-f18)
- [Decision Log](../decision_log.md)
- [Repository README](../../README.md)
<!-- crossref:end -->


