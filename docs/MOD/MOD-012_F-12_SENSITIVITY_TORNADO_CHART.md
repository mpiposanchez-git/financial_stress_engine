# MOD-012 - F-12 - Sensitivity / Tornado Chart

Status: Active (latest methodology)
Source of truth: docs/methodology/methodology_textbook.md
Aligned backlog: docs/implementation/brd_implementation_plan.md and docs/implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md
Tier: Premium

## 1. Scope
One-factor perturbation ranking of output sensitivity drivers.

## 2. Inputs
Base scenario and predefined perturbation set.

## 3. Outputs
Ordered impact list and tornado visualization.

## 4. Method Rules
- Server-side premium enforcement is mandatory.
- Perturbation assumptions must be explicit and repeatable.
- Do not mix with advice/recommendation language.

## 5. Validation and Tests
- Sensitivity endpoint returns ordered impacts.
- Non-premium access is rejected.

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
- [Primary Backlog Task: WS5-F12](../implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-ws5-f12)
- [Decision Log](../decision_log.md)
- [Repository README](../../README.md)
<!-- crossref:end -->


