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
1. **Guided onboarding wizard** (step-by-step baseline budget capture)  
2. **Month-by-month runway chart** (24m default)  
9. **Interactive stress sliders** (income / inflation / rates / FX)  
16. **Household archetype templates** (starter scenarios)  
18. **Input quality checks & diagnostics** (prevent garbage-in)  
19. **Limits & assumptions panel** (transparent caps and modelling rules)  

### Stress & modelling features
3. **Mortgage rate stress module** (payment under stress)  
4. **Scenario comparison** (Base vs Stress A vs Stress B)  
5. **Monte Carlo fan chart (P10/P50/P90)**  
8. **Category inflation toggles** (food/energy/housing etc.)  
12. **Sensitivity / tornado chart** (drivers ranked by impact)  
13. **Shock schedules** (one-off vs gradual vs stepped)  
14. **Debt schedule (optional)** for non-mortgage debt (generic)  
15. **Mortgage type sandbox** (repayment vs interest-only mechanics)  

### Reporting, trust, and guidance (non-advice)
6. **PDF report export (premium)**  
10. **Emergency fund adequacy indicator** (months of essentials)  
11. **Explain-the-result panel** (plain-English narrative + tooltips)  
17. **Local-only scenario saving** (“save on this device” toggle)  
20. **Official-resource signposting** (MoneyHelper/Citizens Advice links, non-advice)

### Plus your added modules
- **Data module:** official defaults + provenance + “how to verify”  
- **UK benchmarks:** free reference values; premium BHC percentile ranking  
- **Premium previews in free:** dummy “cool” premium demo outputs  

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

---

## Disclaimers
This tool is an educational simulator and does not provide regulated financial advice or recommend products/actions.
