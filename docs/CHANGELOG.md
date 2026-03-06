# Changelog

All notable changes to this project are documented in this file.

## Release Checklist

Before publishing a milestone release:

1. Run validation gates:
	- `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m ruff check .`
	- `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m pytest services/api/tests -q`
	- `npm --prefix apps/web test -- --run`
	- `npm --prefix apps/web run typecheck`
2. Capture evidence artifacts:
	- CI links
	- test/typecheck summaries
	- dataset hash/timestamp snapshot
3. Tag release using:
	- `poc-milestone-<n>-YYYY-MM-DD`
4. Record tag + commit SHA in `docs/progress_log.md` and release notes.

## v0.1.1-poc4 — 2026-03-06

### Added
- Frontend: Added Results visualization cards and chart-based rendering for Monte Carlo percentile bands and deterministic savings path in [apps/web/src/pages/ResultsPage.tsx](../apps/web/src/pages/ResultsPage.tsx).
- Frontend: Added responsive shared styling for readability improvements across pages in [apps/web/src/styles.css](../apps/web/src/styles.css).
- Operations: Added post-deploy smoke automation script for `/health`, deterministic, and Monte Carlo checks in [services/api/scripts/post_deploy_smoke.py](../services/api/scripts/post_deploy_smoke.py).
- CI/CD: Added manual smoke-check workflow in [\.github/workflows/post-deploy-smoke.yml](../.github/workflows/post-deploy-smoke.yml).

### Changed
- Frontend: Improved API error handling with non-sensitive auth diagnostics and status-specific guidance in [apps/web/src/api/client.ts](../apps/web/src/api/client.ts).
- Backend: Refined authentication error detail messages for clearer but non-sensitive troubleshooting in [services/api/app/auth.py](../services/api/app/auth.py).
- Documentation: Frozen deployment snapshot and added smoke/observability runbook sections in [docs/implementation/deployment_runbook.md](implementation/deployment_runbook.md).
- Documentation: Refined disclaimer consistency for multi-currency support and review dates in [docs/disclaimers/regulatory_disclaimer.md](disclaimers/regulatory_disclaimer.md), [docs/disclaimers/proprietary_license_and_terms.md](disclaimers/proprietary_license_and_terms.md), and [docs/disclaimers/privacy.md](disclaimers/privacy.md).

## v0.1.0-poc3 — 2026-03-04

### Added
- POC-002: Introduced exact-money utilities in [shared/engine/money.py](../shared/engine/money.py) for pence/bps conversion, round-half-up behavior, and currency formatting.
- POC-002: Added unit tests for conversion and rounding behavior in [services/api/tests/test_money.py](../services/api/tests/test_money.py).
- POC-003: Added deterministic month-by-month savings projection outputs in [shared/engine/deterministic.py](../shared/engine/deterministic.py):
	- `savings_path_pence` (length `horizon_months + 1`)
	- `savings_path_formatted`
	- `min_savings_pence` / `min_savings_formatted`
	- `month_of_depletion`
	- `runway_months`
- POC-003: Added deterministic golden test with explicit expected path in [services/api/tests/test_deterministic_golden.py](../services/api/tests/test_deterministic_golden.py).
- Frontend: Added explicit typed API response contracts and result rendering tests in:
	- [apps/web/src/types.ts](../apps/web/src/types.ts)
	- [apps/web/src/pages/ResultsPage.test.tsx](../apps/web/src/pages/ResultsPage.test.tsx)
	- [apps/web/src/pages/StressTestPage.test.tsx](../apps/web/src/pages/StressTestPage.test.tsx)

### Changed
- POC-001: Removed runtime authentication bypass behavior and switched tests to dependency override-based auth mocking.
- POC-002: Migrated engine core from float money/rates to integer `pence` and `bps` in:
	- [shared/engine/inputs.py](../shared/engine/inputs.py)
	- [shared/engine/outputs.py](../shared/engine/outputs.py)
	- [shared/engine/deterministic.py](../shared/engine/deterministic.py)
- POC-002: Updated deterministic and Monte Carlo API responses to include integer money plus formatted display values in:
	- [services/api/app/models.py](../services/api/app/models.py)
	- [services/api/app/routes.py](../services/api/app/routes.py)
- POC-003: Set deterministic `horizon_months` default to `24` and aligned API payload/response contract accordingly.

### Validation
- Backend tests: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m pytest services/api/tests -q` ✅ (`11 passed`)
- Frontend tests: `npm --prefix apps/web test -- --run` ✅ (`5 passed`)

<!-- crossref:start -->
## Related Documents

- [Repository README](../README.md)
- [Methodology Golden Source](methodology/methodology_textbook.md)
- [BRD Implementation Plan](implementation/brd_implementation_plan.md)
<!-- crossref:end -->

