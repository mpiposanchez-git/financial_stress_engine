# MOD-014 - F-14 - Non-Mortgage Debt Schedule

Status: Active (latest methodology)
Source of truth: docs/methodology/methodology_textbook.md
Aligned backlog: docs/implementation/brd_implementation_plan.md and docs/implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md
Tier: Premium

## 1. Scope
Optional debt balance evolution for non-mortgage obligations.

## 2. Inputs
Debt balance, APR bps, minimum payment and related assumptions.

## 3. Outputs
Debt path and resulting cashflow burden over time.

## 4. Method Rules
- Prevent negative balances and invalid payment logic.
- Clearly separate debt schedule assumptions from mortgage module.
- Expose limitations of simplified debt dynamics.

## 5. Validation and Tests
- Debt schedule unit tests cover amortization edge cases.
- Premium gate enforced for debt-schedule functionality.

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
- [Primary Backlog Task: WS5-F14](../implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-ws5-f14)
- [Decision Log](../decision_log.md)
- [Repository README](../../README.md)
<!-- crossref:end -->


