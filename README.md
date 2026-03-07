# UK Household Financial Stress Engine

Cloud deployment architecture with a React frontend and FastAPI backend.
Educational simulation only. This application does not provide financial advice.

## Final Structure

```
apps/
  web/                 # Vite + React + Clerk frontend
services/
  api/                 # FastAPI API service
shared/
  engine/              # Shared deterministic models/logic
.github/workflows/
  deploy-pages.yml     # Frontend build/test/deploy
  api-ci.yml           # API lint/test CI
docs/
  system_architecture_instructions.md
```

## Run Backend Locally

```bash
uv sync --all-extras
uv run uvicorn services.api.app.main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

## Run Frontend Locally

```bash
cd apps/web
npm ci
npm run dev
```

## Tests

```bash
uv run pytest services/api/tests -v
cd apps/web && npm run test
```

## Lightweight Pre-Commit Hooks

This repository includes lightweight pre-commit checks for:

- `ruff` (with safe auto-fix)
- basic secrets-pattern detection

Install and enable:

```bash
uv run pip install pre-commit
uv run pre-commit install
uv run pre-commit run --all-files
```

The hook set is intentionally lightweight to avoid blocking day-to-day development.

## Key Endpoints

- `GET /health`
- `POST /api/v1/deterministic/run`
- `POST /api/v1/montecarlo/run`

## References

- Architecture and implementation spec: [docs/implementation/system_architecture_instructions.md](docs/implementation/system_architecture_instructions.md)
- Model Development Document (golden source): [docs/methodology/methodology_textbook.md](docs/methodology/methodology_textbook.md)
- POC flyer: [docs/commercial/poc_flyer.md](docs/commercial/poc_flyer.md)
- BRD implementation plan: [docs/implementation/brd_implementation_plan.md](docs/implementation/brd_implementation_plan.md)
- Detailed implementation backlog (WS0-WS9): [docs/implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md](docs/implementation/POC_BACKLOG_DETAILED_TASKS_WS0_WS9.md)
- Master implementation backlog (WS1-WS9 inline): [docs/implementation/POC_BACKLOG_MASTER_WS1_WS9_INLINE.md](docs/implementation/POC_BACKLOG_MASTER_WS1_WS9_INLINE.md)
- MOD specifications (one per functionality):
- F-01 guided onboarding wizard: [docs/MOD/MOD-001_F-01_GUIDED_ONBOARDING_WIZARD.md](docs/MOD/MOD-001_F-01_GUIDED_ONBOARDING_WIZARD.md)
- F-05 Monte Carlo fan chart: [docs/MOD/MOD-005_F-05_MONTE_CARLO_FAN_CHART.md](docs/MOD/MOD-005_F-05_MONTE_CARLO_FAN_CHART.md)
- F-06 PDF export: [docs/MOD/MOD-006_F-06_PDF_EXPORT.md](docs/MOD/MOD-006_F-06_PDF_EXPORT.md)
- A-01 data module and provenance: [docs/MOD/MOD-021_A-01_DATA_MODULE_AND_PROVENANCE.md](docs/MOD/MOD-021_A-01_DATA_MODULE_AND_PROVENANCE.md)
- A-02 UK benchmarks: [docs/MOD/MOD-022_A-02_UK_BENCHMARKS_REFERENCE_AND_PERCENTILE.md](docs/MOD/MOD-022_A-02_UK_BENCHMARKS_REFERENCE_AND_PERCENTILE.md)
- A-07 privacy-safe measurement: [docs/MOD/MOD-027_A-07_PRIVACY_SAFE_MEASUREMENT.md](docs/MOD/MOD-027_A-07_PRIVACY_SAFE_MEASUREMENT.md)
- Privacy: [docs/disclaimers/privacy.md](docs/disclaimers/privacy.md)
- Regulatory disclaimer: [docs/disclaimers/regulatory_disclaimer.md](docs/disclaimers/regulatory_disclaimer.md)

<!-- crossref:start -->
## Related Documents

- [Methodology Golden Source](docs/methodology/methodology_textbook.md)
- [BRD Implementation Plan](docs/implementation/brd_implementation_plan.md)
<!-- crossref:end -->

