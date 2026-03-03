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

## Key Endpoints

- `GET /health`
- `POST /api/v1/deterministic/run`
- `POST /api/v1/montecarlo/run`

## References

- Architecture and implementation spec: [docs/system_architecture_instructions.md](docs/system_architecture_instructions.md)
- Privacy: [docs/privacy.md](docs/privacy.md)
- Regulatory disclaimer: [docs/regulatory_disclaimer.md](docs/regulatory_disclaimer.md)
