# POC Detailed Implementation Backlog (WS0-WS9) - Latest Methodology

Version: v0.2.0
Status: Active
Source of truth: docs/methodology/methodology_textbook.md

This backlog provides task-level implementation references for F-01..F-20 and A-01..A-07.

## WS0 - Guardrails

<a id="task-ws0-a04"></a>
## TASK WS0-A04 - Premium entitlements (server-side)

- Implement allowlist-based premium gate with `/api/v1/me` entitlement state.

<a id="task-ws0-a05"></a>
## TASK WS0-A05 - Accessibility baseline (forms + charts)

- Ensure labels, error descriptors, figure/figcaption, keyboard focus behavior.

<a id="task-ws0-a06"></a>
## TASK WS0-A06 - Ethics/fairness disclosure

- Add mandatory percentile disclosure in UI and supporting docs.

<a id="task-ws0-a07"></a>
## TASK WS0-A07 - Privacy-safe aggregate telemetry

- Add aggregate-only counters and admin-protected telemetry endpoint.

## WS1 - Engine Modularization

<a id="task-ws1-f15"></a>
## TASK WS1-F15 - Mortgage mechanics module

- Extract repayment/interest-only payment functions and tests.

<a id="task-ws1-f02"></a>
## TASK WS1-F02 - Savings path module

- Extract savings path, depletion month, and min savings helpers.

<a id="task-ws1-f05"></a>
## TASK WS1-F05 - Shock process module (IID + AR1)

- Extract stochastic path generation with reproducible seed behavior.

## WS2 - Free UX Core

<a id="task-ws2-f01"></a>
## TASK WS2-F01 - Guided onboarding wizard

- Replace demo form flow with step-by-step wizard input capture.

<a id="task-ws2-f09"></a>
## TASK WS2-F09 - Interactive sliders

- Add stress slider controls for income, inflation, rates, and FX.

<a id="task-ws2-f18"></a>
## TASK WS2-F18 - Input diagnostics and quality checks

- Add validation and warning diagnostics with accessible feedback.

<a id="task-ws2-f19"></a>
## TASK WS2-F19 - Limits and assumptions panel

- Add transparent assumptions/caps panel in UX.

## WS3 - Deterministic Result Experience

<a id="task-ws3-f02"></a>
## TASK WS3-F02 - Savings path chart and table

- Add accessible deterministic path visualization with summary text.

<a id="task-ws3-f03"></a>
## TASK WS3-F03 - Mortgage stress module display

- Present current vs stressed mortgage payment with explanation.

<a id="task-ws3-f10"></a>
## TASK WS3-F10 - Emergency fund adequacy indicator

- Show months-of-essentials coverage indicator and context.

<a id="task-ws3-f11"></a>
## TASK WS3-F11 - Explain-the-result narratives and tooltips

- Add plain-language interpretations and glossary support.

<a id="task-ws3-f15"></a>
## TASK WS3-F15 - Mortgage type sandbox (UI)

- Add educational repayment vs interest-only comparison surface.

<a id="task-ws3-f20"></a>
## TASK WS3-F20 - Official-resource signposting

- Add trusted public-resource links with non-advice framing.

## WS4 - Scenarios and Local Saving

<a id="task-ws4-f04"></a>
## TASK WS4-F04 - Scenario comparison

- Add Base vs A/B/C scenario compare workflow and premium gate.

<a id="task-ws4-f17"></a>
## TASK WS4-F17 - Local-only scenario saving

- Add browser-local scenario save/load with tier limits.

## WS5 - Premium Modeling

<a id="task-ws5-f05"></a>
## TASK WS5-F05 - Monte Carlo fan chart

- Provide percentile distribution visualization and premium access.

<a id="task-ws5-f08"></a>
## TASK WS5-F08 - Category inflation toggles

- Add category-level inflation assumptions and integration.

<a id="task-ws5-f12"></a>
## TASK WS5-F12 - Sensitivity/tornado chart

- Add one-factor sensitivity engine and tornado visualization.

<a id="task-ws5-f13"></a>
## TASK WS5-F13 - Shock schedules

- Support step/ramp/stepped stress scheduling over horizon.

<a id="task-ws5-f14"></a>
## TASK WS5-F14 - Non-mortgage debt schedule

- Add optional debt path mechanics and impact reporting.

## WS6 - Data Module

<a id="task-ws6-a01"></a>
## TASK WS6-A01 - Data registry/defaults/verification

- Build data registry and user-visible source/verification surfaces.

<a id="task-ws6-a01b"></a>
## TASK WS6-A01B - Auto-fetch and cache

- Add fetchers, cache metadata, and scheduled refresh support.

## WS7 - UK Benchmarks

<a id="task-ws7-a02a"></a>
## TASK WS7-A02A - UK reference benchmarks (free)

- Provide free reference benchmark values with source/year context.

<a id="task-ws7-a02b"></a>
## TASK WS7-A02B - BHC percentile ranking (premium)

- Provide premium percentile context using HBAI BHC methodology.

## WS8 - Exports

<a id="task-ws8-f06"></a>
## TASK WS8-F06 - PDF export (premium)

- Add premium PDF report generation and delivery.

## Additional Added Features

<a id="task-f-07"></a>
## TASK F-07 - FX and multi-currency integration continuity

- Ensure deterministic/MC flows keep reporting currency and FX assumptions aligned.

<a id="task-f-16"></a>
## TASK F-16 - Household archetype templates

- Add template presets with clear assumptions and user editability.

<a id="task-a-03"></a>
## TASK A-03 - Premium teaser demo

- Add free-tier teaser outputs clearly labeled as illustrative examples.

---

<!-- crossref:start -->
## Related Documents

- [Repository README](../../README.md)
- [Methodology Golden Source](../methodology/methodology_textbook.md)
- [BRD Implementation Plan](brd_implementation_plan.md)
- [Master Backlog (WS1-WS9)](POC_BACKLOG_MASTER_WS1_WS9_INLINE.md)
<!-- crossref:end -->
