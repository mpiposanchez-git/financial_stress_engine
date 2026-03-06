# UK Household Financial Stress Engine - BRD Implementation Plan

Version: v0.2.0
Status: Active
Date: 2026-03-06

This file is the BRD entrypoint for implementation planning and document navigation.

## Scope

- Defines the feature catalog used for implementation tracking.
- Aligns implementation work to the methodology golden source.
- Points to the detailed and master backlog execution plans.

## Methodology Precedence

Methodology source of truth: `docs/methodology/methodology_textbook.md`.
If planning content conflicts with methodology assumptions, the methodology textbook takes precedence.

<a id="1-poc-feature-catalog-functionalities-120--additions"></a>
## Feature Catalog

- F-01 to F-20: core product functionalities.
- A-01 to A-07: added controls and governance features.

For task-level detail, see the linked backlogs.

## Feature-to-Spec Quick Links

| Capability | MOD spec | Primary backlog task |
|---|---|---|
| Deterministic runway and path | [MOD-002](../MOD/MOD-002_F-02_MONTH_BY_MONTH_RUNWAY_CHART.md) | [WS1-F02](POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-ws1-f02) |
| Mortgage stress and payment mechanics | [MOD-003](../MOD/MOD-003_F-03_MORTGAGE_RATE_STRESS_MODULE.md) | [WS1-F15](POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-ws1-f15) |
| Monte Carlo fan chart | [MOD-005](../MOD/MOD-005_F-05_MONTE_CARLO_FAN_CHART.md) | [WS5-F05](POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-ws5-f05) |
| FX and multi-currency | [MOD-007](../MOD/MOD-007_F-07_FX_AND_MULTI_CURRENCY.md) | [F-07](POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-f-07) |
| Data module and provenance | [MOD-021](../MOD/MOD-021_A-01_DATA_MODULE_AND_PROVENANCE.md) | [WS6-A01](POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-ws6-a01) |
| UK benchmarks and percentiles | [MOD-022](../MOD/MOD-022_A-02_UK_BENCHMARKS_REFERENCE_AND_PERCENTILE.md) | [WS7-A02B](POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-ws7-a02b) |
| Premium entitlements | [MOD-024](../MOD/MOD-024_A-04_PREMIUM_ENTITLEMENTS.md) | [WS0-A04](POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-ws0-a04) |
| Accessibility controls | [MOD-025](../MOD/MOD-025_A-05_ACCESSIBILITY_REQUIREMENTS.md) | [WS0-A05](POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-ws0-a05) |
| Ethics and fairness disclosure | [MOD-026](../MOD/MOD-026_A-06_ETHICS_AND_FAIRNESS_DISCLOSURE.md) | [WS0-A06](POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-ws0-a06) |
| Privacy-safe aggregate telemetry | [MOD-027](../MOD/MOD-027_A-07_PRIVACY_SAFE_MEASUREMENT.md) | [WS0-A07](POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md#task-ws0-a07) |

## Implementation Backlogs

- Detailed backlog (WS0-WS9): `docs/implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md`
- Master backlog (WS1-WS9): `docs/implementation/POC_BACKLOG_MASTER_WS1_WS9_INLINE.md`

## Document Map

- System architecture instructions: `docs/implementation/system_architecture_instructions.md`
- Deployment runbook: `docs/implementation/deployment_runbook.md`
- Methodology textbook: `docs/methodology/methodology_textbook.md`
- POC flyer: `docs/commercial/poc_flyer.md`
- MOD specifications: `docs/MOD/`

<!-- crossref:start -->
## Related Documents

- [Repository README](../../README.md)
- [Methodology Golden Source](../methodology/methodology_textbook.md)
- [Detailed Backlog (WS0-WS9)](POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md)
- [Master Backlog (WS1-WS9)](POC_BACKLOG_MASTER_WS1_WS9_INLINE.md)
- [Deployment Runbook](deployment_runbook.md)
- [System Architecture Instructions](system_architecture_instructions.md)
<!-- crossref:end -->

