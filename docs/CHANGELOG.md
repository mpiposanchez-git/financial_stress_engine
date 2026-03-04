# Changelog

All notable changes to this project are documented in this file.

## v0.1.0-poc3 — 2026-03-04

### Added
- POC-002: Introduced exact-money utilities in [shared/engine/money.py](shared/engine/money.py) for pence/bps conversion, round-half-up behavior, and currency formatting.
- POC-002: Added unit tests for conversion and rounding behavior in [services/api/tests/test_money.py](services/api/tests/test_money.py).
- POC-003: Added deterministic month-by-month savings projection outputs in [shared/engine/deterministic.py](shared/engine/deterministic.py):
	- `savings_path_pence` (length `horizon_months + 1`)
	- `savings_path_formatted`
	- `min_savings_pence` / `min_savings_formatted`
	- `month_of_depletion`
	- `runway_months`
- POC-003: Added deterministic golden test with explicit expected path in [services/api/tests/test_deterministic_golden.py](services/api/tests/test_deterministic_golden.py).
- Frontend: Added explicit typed API response contracts and result rendering tests in:
	- [apps/web/src/types.ts](apps/web/src/types.ts)
	- [apps/web/src/pages/ResultsPage.test.tsx](apps/web/src/pages/ResultsPage.test.tsx)
	- [apps/web/src/pages/StressTestPage.test.tsx](apps/web/src/pages/StressTestPage.test.tsx)

### Changed
- POC-001: Removed runtime authentication bypass behavior and switched tests to dependency override-based auth mocking.
- POC-002: Migrated engine core from float money/rates to integer `pence` and `bps` in:
	- [shared/engine/inputs.py](shared/engine/inputs.py)
	- [shared/engine/outputs.py](shared/engine/outputs.py)
	- [shared/engine/deterministic.py](shared/engine/deterministic.py)
- POC-002: Updated deterministic and Monte Carlo API responses to include integer money plus formatted display values in:
	- [services/api/app/models.py](services/api/app/models.py)
	- [services/api/app/routes.py](services/api/app/routes.py)
- POC-003: Set deterministic `horizon_months` default to `24` and aligned API payload/response contract accordingly.

### Validation
- Backend tests: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m pytest services/api/tests -q` ✅ (`11 passed`)
- Frontend tests: `npm --prefix apps/web test -- --run` ✅ (`5 passed`)

