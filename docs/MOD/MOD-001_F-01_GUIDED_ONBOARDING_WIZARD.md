# MOD-001 - F-01 - Guided Onboarding Wizard

Status: Active (latest methodology)
Source of truth: docs/methodology/methodology_textbook.md
Aligned backlog: docs/implementation/brd_implementation_plan.md and docs/implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md
Tier: Free

## 1. Scope
Step-by-step baseline household input capture with validation and review before run.

## 2. Inputs
Income, essentials, debt, savings, mortgage, FX, reporting currency, horizon.

## 3. Outputs
Validated deterministic/MC-ready payload.

## 4. Method Rules
- Use explicit labels and aria-describedby for validation messages.
- Keep auth on; no anonymous protected simulation routes.
- Default horizon is 24 months unless user changes it.

## 5. Validation and Tests
- Wizard can complete full flow with keyboard-only navigation.
- Invalid required fields block submit and show linked error text.

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
- [Primary Backlog Task: WS2-F01](../implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-ws2-f01)
- [Decision Log](../decision_log.md)
- [Repository README](../../README.md)
<!-- crossref:end -->


