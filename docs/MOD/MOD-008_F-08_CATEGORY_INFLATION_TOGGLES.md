# MOD-008 - F-08 - Category Inflation Toggles

Status: Active (latest methodology)
Source of truth: docs/methodology/methodology_textbook.md
Aligned backlog: docs/implementation/brd_implementation_plan.md and docs/implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md
Tier: Premium

## 1. Scope
Apply category-specific inflation shocks instead of single essentials bucket.

## 2. Inputs
Category spends and per-category inflation assumptions.

## 3. Outputs
Category-aware stressed cashflow and path effects.

## 4. Method Rules
- Fallback to single essentials bucket when category split absent.
- Document category definitions and assumptions.
- Preserve pence/bps arithmetic consistency.

## 5. Validation and Tests
- Category and fallback modes both produce valid outputs.
- Premium gate enforced on category controls.

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
- [Primary Backlog Task: WS5-F08](../implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-ws5-f08)
- [Decision Log](../decision_log.md)
- [Repository README](../../README.md)
<!-- crossref:end -->


