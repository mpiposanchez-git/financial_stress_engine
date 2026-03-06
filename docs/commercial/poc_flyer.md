# UK Household Financial Stress Engine — POC Feature Flyer (Marketing Draft) 🚀🇬🇧

**Version:** v0.2.0  
**Date:** 2026-03-06  
**Repo:** https://github.com/mpiposanchez-git/financial_stress_engine  
**Audience:** prospective users + early adopters + reviewers

> **Educational simulation only — not financial advice.**  
> No bank linking. No document uploads. Scenarios are processed in-memory and not stored in a project database.

---

## One‑liner
**Stress test your household finances** against income shocks, mortgage rate rises, inflation, energy costs, and FX moves — and see your **month‑by‑month runway**.

---

## What makes it different
- **Month‑by‑month runway** (not a single snapshot)
- **Uncertainty-aware** outputs (Monte Carlo) for premium users
- **Multi‑currency + FX risk** (useful for expats and international households)
- **UK benchmarks** (free reference values; premium “percentile ranking”)
- **Transparent official data sources** with “how to verify” steps

---

## Core outputs (what you’ll see)
- Base vs stressed monthly cashflow
- 24‑month savings path (chart/table) + month of depletion
- Mortgage payment sensitivity to rate stress
- FX-adjusted runway (if multi-currency)
- (Premium) P10/P50/P90 uncertainty bands + “fan chart”
- (Premium) Scenario comparisons and sensitivity (“what matters most”)
- Exports: JSON (free), PDF report (premium)

---

## Full POC functionality list (1–20) ✅
These are the POC capabilities the product is aiming to deliver.

### Input & UX
1. **Guided onboarding wizard** (step-by-step baseline budget capture) ([MOD-001](../MOD/MOD-001_F-01_GUIDED_ONBOARDING_WIZARD.md))  
2. **Month-by-month runway chart** (24m default) ([MOD-002](../MOD/MOD-002_F-02_MONTH_BY_MONTH_RUNWAY_CHART.md))  
9. **Interactive stress sliders** (income / inflation / rates / FX) ([MOD-009](../MOD/MOD-009_F-09_INTERACTIVE_SLIDERS.md))  
16. **Household archetype templates** (starter scenarios) ([MOD-016](../MOD/MOD-016_F-16_HOUSEHOLD_ARCHETYPE_TEMPLATES.md))  
18. **Input quality checks & diagnostics** (prevent garbage-in) ([MOD-018](../MOD/MOD-018_F-18_INPUT_DIAGNOSTICS_AND_QUALITY_CHECKS.md))  
19. **Limits & assumptions panel** (transparent caps and modelling rules) ([MOD-019](../MOD/MOD-019_F-19_LIMITS_AND_ASSUMPTIONS_PANEL.md))  

### Stress & modelling features
3. **Mortgage rate stress module** (payment under stress) ([MOD-003](../MOD/MOD-003_F-03_MORTGAGE_RATE_STRESS_MODULE.md))  
4. **Scenario comparison** (Base vs Stress A vs Stress B) ([MOD-004](../MOD/MOD-004_F-04_SCENARIO_COMPARISON.md))  
5. **Monte Carlo fan chart (P10/P50/P90)** ([MOD-005](../MOD/MOD-005_F-05_MONTE_CARLO_FAN_CHART.md))  
8. **Category inflation toggles** (food/energy/housing etc.) ([MOD-008](../MOD/MOD-008_F-08_CATEGORY_INFLATION_TOGGLES.md))  
12. **Sensitivity / tornado chart** (drivers ranked by impact) ([MOD-012](../MOD/MOD-012_F-12_SENSITIVITY_TORNADO_CHART.md))  
13. **Shock schedules** (one-off vs gradual vs stepped) ([MOD-013](../MOD/MOD-013_F-13_SHOCK_SCHEDULES.md))  
14. **Debt schedule (optional)** for non-mortgage debt (generic) ([MOD-014](../MOD/MOD-014_F-14_NON_MORTGAGE_DEBT_SCHEDULE.md))  
15. **Mortgage type sandbox** (repayment vs interest-only mechanics) ([MOD-015](../MOD/MOD-015_F-15_MORTGAGE_TYPE_SANDBOX.md))  

### Reporting, trust, and guidance (non-advice)
6. **PDF report export (premium)** ([MOD-006](../MOD/MOD-006_F-06_PDF_EXPORT.md))  
10. **Emergency fund adequacy indicator** (months of essentials) ([MOD-010](../MOD/MOD-010_F-10_EMERGENCY_FUND_ADEQUACY_INDICATOR.md))  
11. **Explain-the-result panel** (plain-English narrative + tooltips) ([MOD-011](../MOD/MOD-011_F-11_EXPLAIN_THE_RESULT_NARRATIVES_AND_TOOLTIPS.md))  
17. **Local-only scenario saving** ("save on this device" toggle) ([MOD-017](../MOD/MOD-017_F-17_LOCAL_ONLY_SCENARIO_SAVING.md))  
20. **Official-resource signposting** (MoneyHelper/Citizens Advice links, non-advice) ([MOD-020](../MOD/MOD-020_F-20_OFFICIAL_RESOURCE_SIGNPOSTING.md))

### Plus your added modules
- **Data module:** official defaults + provenance + "how to verify" ([MOD-021](../MOD/MOD-021_A-01_DATA_MODULE_AND_PROVENANCE.md))  
- **UK benchmarks:** free reference values; premium BHC percentile ranking ([MOD-022](../MOD/MOD-022_A-02_UK_BENCHMARKS_REFERENCE_AND_PERCENTILE.md))  
- **Premium previews in free:** dummy "cool" premium demo outputs ([MOD-023](../MOD/MOD-023_A-03_PREMIUM_TEASER_DEMO.md))  

---

## Free vs Premium (hook ladder) 🎣

### Free: **Quick Stress Check**
- Wizard + deterministic runway path (24m)
- One scenario
- Mortgage stress view
- Basic charts + JSON export
- **UK reference values** (averages/medians) for selected metrics
- **Premium teaser demo** (dummy household; not your data)
- Data Sources page (provenance + verification steps)

### Premium: **Uncertainty + Compare + Report**
- Monte Carlo uncertainty (P10/P50/P90) + fan chart
- Scenario compare A/B/C + sensitivity chart
- PDF export report
- FX volatility + AR(1) shock persistence options
- “You are in the Xth percentile” (UK income distribution, **BHC**) + caveats
- Saved scenarios: unlimited (still local-only)

---

## Official data sources (defaults & benchmarks) 🔎
- Inflation (ONS CPI/CPIH): https://www.ons.gov.uk/economy/inflationandpriceindices/datasets/consumerpriceindices/current  
- Interest rates (BoE Bank Rate): https://www.bankofengland.co.uk/boeapps/database/Bank-Rate.asp  
- FX spot rates (BoE): https://www.bankofengland.co.uk/boeapps/database/Rates.asp  
- Energy price cap tables (Ofgem): https://www.ofgem.gov.uk/information-consumers/energy-advice-households/get-energy-price-cap-standing-charges-and-unit-rates-region  
- UK income distribution (DWP HBAI): https://www.gov.uk/government/statistics/households-below-average-income-for-financial-years-ending-1995-to-2024  

Auto-refresh is planned/implemented via a scheduled job pattern (Render Cron Jobs): https://render.com/docs/cronjobs

---

## Privacy, fairness, and accessibility (trust builders) 🔒♿⚖️
- **Privacy:** no scenario storage server-side; premium uses allowlist entitlement (POC).  
- **Fairness:** percentile ranking is approximate and definition-dependent (BHC, year).  
- **Accessibility:** charts have text summaries; keyboard navigation supported.  
- **Measurement:** only privacy-safe aggregate usage counters (no third-party trackers).

### Ethics & limitations (short disclosure)
- Percentile ranking is approximate.
- It uses the UK HBAI BHC definition and depends on year and definitions.
- It is not advice.
- It is not a measure of worth.

---

## Disclaimers
This tool is an educational simulator and does not provide regulated financial advice or recommend products/actions.

<!-- crossref:start -->
## Related Documents

- [Repository README](../../README.md)
- [Methodology Golden Source](../methodology/methodology_textbook.md)
- [BRD Implementation Plan](../implementation/brd_implementation_plan.md)
<!-- crossref:end -->

