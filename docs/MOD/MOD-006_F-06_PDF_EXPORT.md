# MOD-006 - F-06 - PDF Export

Status: Active (latest methodology)
Source of truth: docs/methodology/methodology_textbook.md
Aligned backlog: docs/implementation/brd_implementation_plan.md and docs/implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md
Tier: Premium

## 1. Scope
Auditable report export of assumptions, outputs, and disclosures.

## 2. Inputs
Run inputs/outputs plus source/provenance metadata.

## 3. Outputs
Downloadable PDF artifact.

## 4. Method Rules
- Server-side premium enforcement is mandatory.
- Include non-advice and limitations disclosures.
- Embed version and evidence snapshot metadata when available.

## 5. Validation and Tests
- Unauthorized export requests fail with 403.
- Generated PDF contains required sections.

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
- [Primary Backlog Task: WS8-F06](../implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-ws8-f06)
- [Decision Log](../decision_log.md)
- [Repository README](../../README.md)
<!-- crossref:end -->


