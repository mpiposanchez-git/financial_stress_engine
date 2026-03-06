# MOD-017 - F-17 - Local-Only Scenario Saving

Status: Active (latest methodology)
Source of truth: docs/methodology/methodology_textbook.md
Aligned backlog: docs/implementation/brd_implementation_plan.md and docs/implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md
Tier: Free limited + Premium unlimited

## 1. Scope
Store scenario definitions on user device only.

## 2. Inputs
Scenario payload, title/tags, local storage context.

## 3. Outputs
Saved/reloaded local scenarios.

## 4. Method Rules
- No server persistence for scenario contents in this feature.
- Free tier applies storage count limit; premium unlocks unlimited.
- Show clear device/browser-only storage disclosure.

## 5. Validation and Tests
- Scenarios can be saved and restored locally.
- Free-tier cap is enforced in UI logic.

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
- [Primary Backlog Task: WS4-F17](../implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-ws4-f17)
- [Decision Log](../decision_log.md)
- [Repository README](../../README.md)
<!-- crossref:end -->


