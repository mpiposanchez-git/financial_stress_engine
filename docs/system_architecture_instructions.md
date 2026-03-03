# UK Household Financial Stress Engine
# Final Cloud Deployment Plan (Locked v5 — Implementation Specification)

---

## Document Purpose

This document defines:

- Cloud deployment architecture
- Technology stack definitions
- Infrastructure responsibilities
- API contracts (implementation-only)
- Environment configuration
- CI/CD requirements (frontend + API)
- Definition of Done
- A hardened GitHub Copilot execution prompt

This document intentionally excludes modelling methodology decisions.
Those are handled in the separate MOD (Methodology) specification.

---

# PART I — Cloud Architecture Foundations (IT Concepts)

## 1. Layered Architecture Overview

Modern web applications use a layered structure:

1. **Frontend (Client Application)**
2. **Backend (API Server)**
3. **Authentication Provider**
4. **Hosting Infrastructure**

This separation improves scalability, maintainability, security, and deployment flexibility.

---

## 2. Technology Stack Definitions

### React
A JavaScript library for building component-based user interfaces.

### Vite
A frontend build tool that bundles TypeScript/JavaScript, provides a fast development server, and outputs optimized production assets.

### GitHub Pages
A static hosting platform that serves HTML/CSS/JS files and does not run server-side code. Suitable for frontend SPAs.

### FastAPI
A Python web framework for building REST APIs with automatic validation, structured JSON responses, and OpenAPI schema generation.

### Render
A cloud hosting platform that deploys backend services from GitHub and manages infrastructure automatically.

### Clerk
An authentication provider that manages login/logout and issues JWT tokens. Integrates with React apps and supports OAuth2 / OIDC.

### JWT
A signed token containing user identity claims. The backend verifies JWT signatures using Clerk’s JWKS endpoint.

---

# PART II — Final Locked Architecture

## Components

- React SPA hosted on **GitHub Pages (default URL)**
- Clerk for authentication
- FastAPI backend hosted on Render
- Deterministic engine (server-side)
- Monte Carlo engine (server-side)
- Stateless architecture (no database for PoC)

---

## Architecture Diagram

```mermaid
flowchart LR
  U[User Browser] -->|HTTPS| GH[GitHub Pages React SPA]
  GH -->|Login| CL[Clerk Identity Provider]
  GH -->|Bearer Token| API[FastAPI on Render]
  API --> DET[Deterministic Engine]
  API --> MC[Monte Carlo Engine]
```

---

# PART III — API Contracts (Implementation Only)

## 1. Health Endpoint

**GET** `/health`

### Response
```json
{"status":"ok"}
```

---

## 2. Deterministic Endpoint

**POST** `/api/v1/deterministic/run`

### Request
```json
{"input_parameters": { } }
```

### Response (minimum fields)
```json
{
  "runway_months": 12,
  "min_savings": 0.0,
  "month_by_month": [],
  "warnings": []
}
```

---

## 3. Monte Carlo Endpoint

**POST** `/api/v1/montecarlo/run`

### Request Schema
```json
{
  "input_parameters": { },
  "n_sims": 2000,
  "horizon_months": 24,
  "seed": 12345
}
```

### Backend Behaviour
- Validate Clerk JWT
- Validate schema
- Enforce caps and rate limits
- Execute simulations
- Compute percentiles (P10, P50, P90)
- Return structured JSON
- Do **NOT** log raw inputs

### Response Schema
```json
{
  "n_sims": 2000,
  "horizon_months": 24,
  "seed": 12345,
  "runtime_ms": 123.4,
  "metrics": {
    "runway_months": {"p10": 3.0, "p50": 10.0, "p90": 24.0},
    "min_savings": {"p10": 0.0, "p50": 1200.0, "p90": 5000.0},
    "max_monthly_deficit": {"p10": 900.0, "p50": 400.0, "p90": 50.0}
  }
}
```

### Constraints (PoC)
- `MAX_MONTE_CARLO_SIMS <= 2000`
- `MAX_HORIZON_MONTHS <= 120`
- `REQUEST_TIMEOUT_SECONDS` enforced (server-side)
- Percentile computation must be deterministic
- If seed provided → output must be reproducible
- If seed missing → server generates seed and returns it

---

# PART IV — Environment Variables

## Frontend (React)

| Variable | Dev | Prod |
|----------|------|------|
| `VITE_API_BASE_URL` | `http://localhost:8000` | Render API URL |
| `VITE_CLERK_PUBLISHABLE_KEY` | Dev key | Prod key |
| `VITE_APP_BASE_PATH` | `/` | `/<repo-name>/` |

## Backend (FastAPI)

| Variable | Dev | Prod |
|----------|------|------|
| `ENV` | `dev` | `prod` |
| `CORS_ORIGINS` | `http://localhost:5173` | `https://<user>.github.io` |
| `CLERK_JWKS_URL` | Dev JWKS | Prod JWKS |
| `CLERK_ISSUER` | Dev issuer | Prod issuer |
| `MAX_MONTE_CARLO_SIMS` | `2000` | `2000` |
| `MAX_HORIZON_MONTHS` | `120` | `120` |
| `RATE_LIMIT_RPM` | `60` | `60` |
| `REQUEST_TIMEOUT_SECONDS` | `30` | `30` |

---

# PART V — Definition of Done

Deployment is complete when:

- GitHub Pages deployment succeeds on push to `main`
- Clerk authentication blocks protected routes
- FastAPI runs locally and on Render
- `/health` returns `{"status":"ok"}`
- Deterministic endpoint returns valid JSON and UI renders summary
- Monte Carlo endpoint returns P10/P50/P90 and UI renders summary + diagnostics
- No personal data stored or logged

---

# PART VI — CI/CD Requirements (Frontend + API)

## 1. Frontend CI/CD (GitHub Pages)

### Workflow file
`.github/workflows/deploy-pages.yml`

### Triggers
- On push to `main` affecting `apps/web/**`
- Optionally on manual `workflow_dispatch`

### Steps (required)
- Checkout
- Setup Node (LTS)
- Install deps (choose one: `npm ci` or `pnpm install --frozen-lockfile`)
- Build `apps/web`
- Deploy `apps/web/dist` to GitHub Pages

### Quality gates (required)
Before building:
- Typecheck
- Lint
- Unit tests (Vitest)

---

## 2. API CI (required) — tests, lint, typecheck

### Workflow file
`.github/workflows/api-ci.yml`

### Triggers
- On pull_request targeting `main` affecting `services/api/**`
- On push to `main` affecting `services/api/**`

### Steps (required)
- Checkout
- Setup Python 3.11+
- Install API dependencies (prefer `uv` if repo uses it; otherwise pip)
- Run:
  - `ruff` (lint)
  - `pytest` (unit tests)
  - Optional: `mypy` (typecheck) if configured

### Failure behaviour
- Any failed step must fail the workflow.

---

## 3. API CD (recommended) — Render deployment model

### Preferred approach (low-ops)
Use **Render Auto-Deploy** from GitHub:
- Render pulls from `main` and redeploys on new commits.
- CI runs on PRs to protect `main` (via branch protection rules).

### Optional hardening (still simple)
- Add a `render.yaml` blueprint (if desired) to define service config as code.
- Keep secrets (Clerk issuer/JWKS URL, etc.) configured in Render dashboard env vars.

**Note:** Avoid GitHub Actions “deploy-to-Render” scripts in PoC because they require storing deploy API keys/secrets in GitHub. Auto-deploy + CI is simpler and safer.

---

# PART VII — GitHub Copilot Implementation Instructions (Hardened)

## How to use this section
Tell Copilot exactly:

> **“Implement PART VII of this document.”**

Copilot must implement the repository according to PART II–VI and the constraints below.

---

## Copilot Constraints (Do not deviate)
1. **Ask** clarifying questions. Don't implement anything different to what is specified without asking.
2. Keep dependencies minimal.
3. Do not introduce a database or persistence in PoC.
4. Do not log raw inputs or tokens.
5. Use HashRouter and Vite base path suitable for GitHub Pages.
6. Use Clerk for auth; do not implement custom username/password.
7. Server-side executes deterministic + Monte Carlo.
8. Add CI workflows exactly at the specified paths.
9. Create `.env.example` files (frontend and API) and do not commit `.env`.

---

## Required repo structure
```
repo-root/
  apps/
    web/
  services/
    api/
  docs/
  .github/
    workflows/
      deploy-pages.yml
      api-ci.yml
```

---

## Frontend implementation requirements (apps/web)
- Vite + React + TypeScript scaffold
- Routing via `HashRouter`
- Pages:
  - Home (public)
  - Stress Test (protected)
  - Results (protected)
  - About/Disclaimer (public)
- Clerk integration:
  - Sign-in/sign-out UI
  - Route protection wrapper
- API client:
  - Base URL from `VITE_API_BASE_URL`
  - Include `Authorization: Bearer <token>` for API calls
- UX:
  - Non-advisory language (“simulation”, “illustrative”, “not financial advice”)

### Frontend tests
- Use Vitest
- Minimum tests:
  - A protected route denies unauthenticated access (mock auth)
  - API client attaches auth header (unit test)

---

## API implementation requirements (services/api)
- FastAPI app with:
  - `GET /health`
  - `POST /api/v1/deterministic/run`
  - `POST /api/v1/montecarlo/run`
- Auth:
  - Validate Clerk JWT signature using JWKS URL
  - Validate issuer
  - Reject unauthenticated requests with 401
- Validation:
  - Reject invalid input schema with 422
- Safety controls:
  - Enforce caps: `MAX_MONTE_CARLO_SIMS`, `MAX_HORIZON_MONTHS`
  - Enforce `REQUEST_TIMEOUT_SECONDS`
  - Apply simple rate limit (in-memory is acceptable for PoC)
- Monte Carlo outputs:
  - Return exactly the schema in PART III
  - If seed absent: generate and return it
  - Percentiles must be deterministic

### API tests
- Use pytest
- Minimum tests:
  - `/health` returns status ok
  - Auth middleware rejects missing token
  - Deterministic endpoint returns required keys
  - Monte Carlo endpoint returns `metrics` with p10/p50/p90
  - Seed reproducibility: same inputs + same seed → same outputs

---

## CI/CD implementation requirements
- Create GitHub Actions workflows:
  - `.github/workflows/deploy-pages.yml` (build/test/deploy web)
  - `.github/workflows/api-ci.yml` (lint/test API)
- Ensure workflows run only when relevant paths change (path filters).

---

## Acceptance Criteria (Copilot “Done”)
1. `apps/web` builds successfully.
2. GitHub Pages deployment workflow succeeds on `main`.
3. Clerk login works locally in dev mode (via `.env` values).
4. API runs locally and passes all tests.
5. API CI passes on PR.
6. Render auto-deploy is compatible (Dockerfile or start command documented in `services/api/README.md`).

---

END OF DOCUMENT
