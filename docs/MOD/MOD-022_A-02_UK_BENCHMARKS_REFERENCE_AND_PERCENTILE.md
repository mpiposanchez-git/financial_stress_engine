# MOD-022 - A-02 - UK Benchmarks (Reference and Percentile)

Status: Active (latest methodology)
Source of truth: docs/methodology/methodology_textbook.md
Aligned backlog: docs/implementation/brd_implementation_plan.md and docs/implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md
Tier: Free/Premium

## 1. Scope
Free reference benchmarks plus premium BHC percentile context.

## 2. Inputs
Household income context, benchmark tables, reference year.

## 3. Outputs
Reference metrics and percentile bucket with caveats.

## 4. Method Rules
- Use UK HBAI BHC framing for percentile feature.
- Always show year/definition caveats.
- Premium gate applies to percentile ranking endpoint.

## 5. Validation and Tests
- Reference endpoint returns year-labeled values.
- Percentile endpoint enforces premium entitlement.

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
- [Primary Backlog Task: WS7-A02A](../implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-ws7-a02a)
- [Primary Backlog Task: WS7-A02B](../implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-ws7-a02b)
- [Decision Log](../decision_log.md)
- [Repository README](../../README.md)
<!-- crossref:end -->


