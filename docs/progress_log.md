# Progress Log (Append-only) 🧾

> One entry per dev session or per week. Keep it factual and lightweight.

---

## YYYY-MM-DD — Session Title

### Completed
- POC-XXX: <short description> (PR/commit link)

### In progress
- POC-YYY: <next steps>

### Test evidence
- CI run: <link>
- Backend: `uv run pytest -v` ✅ / ❌
- Frontend: `cd apps/web && npm run test` ✅ / ❌

### Decisions made
- DECISION-ID: <summary> (link to `docs/decision_log.md`)

### Risks / Blockers
- <bullet list>

---

## 2026-03-04 — Deployment, Auth Stabilization, and Security Cleanup

### Completed
- POC-Deployment: Frontend deployed to GitHub Pages and backend deployed to Render; end-to-end simulation execution confirmed.
- POC-CI-CD: Documented workflow trigger behavior and build-time nature of `VITE_*` variables.
- POC-Auth-Stabilization: Resolved Clerk issuer/JWKS/origin/path mismatches and verified authenticated deterministic + Monte Carlo execution.
- POC-001: Removed temporary runtime auth bypass logic and environment flags from frontend and backend.

### In progress
- POC-Results-UI: Add chart-based visualization for Monte Carlo percentile outputs.
- POC-Release-Readiness: Freeze deployment config snapshot and prepare release notes/version tag.
- POC-Smoke-Automation: Add post-deploy smoke checks for `/health` + authenticated deterministic + Monte Carlo runs.

### Test evidence
- Backend: `pytest services/api/tests -q` ✅
- Frontend: `npm --prefix apps/web test -- --run` ✅
- Production check: Auth-enabled deterministic and Monte Carlo runs confirmed after configuration correction ✅

### Decisions made
- Authentication enforcement is mandatory in runtime environments; no bypass flags retained.
- Production validation should target `/health` for backend status checks.
- Clerk configuration must be strictly issuer/JWKS/path aligned with deployed domain and project path.

### Risks / Blockers
- VPN or DNS/proxy filtering can intermittently block Clerk script loading and break login flow.
- Environment drift risk remains until deployment configuration is fully snapshotted in runbook form.

---

## 2026-03-04 — Exact Arithmetic + Deterministic Savings Path Delivery

### Completed
- POC-002: Migrated engine arithmetic to integer pence and integer bps with explicit round-half-up conversion/utilities.
- POC-002: Updated API contracts to return money values as `*_pence` and `*_formatted`, and updated frontend typing/consumption accordingly.
- POC-002: Added money unit tests for conversion, rounding, and formatting behavior.
- POC-003: Implemented deterministic month-by-month savings projection with `horizon_months` defaulting to `24`.
- POC-003: Added deterministic outputs for `savings_path_pence`, `min_savings_pence`, `month_of_depletion`, and `runway_months` with formatted strings.
- POC-003: Added golden deterministic test with explicit expected savings path and API contract assertions for path length and fields.

### In progress
- POC-Results-UI: Expand results presentation from basic text to richer visual summaries for deterministic path and Monte Carlo percentiles.
- POC-Release-Readiness: Consolidate API contract changes into release notes/changelog entries.

### Test evidence
- Backend: `c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m pytest services/api/tests -q` ✅ (`11 passed`)
- Frontend: `npm --prefix apps/web test -- --run` ✅ (`5 passed`)

### Decisions made
- Monetary and rate calculations in engine core are integer-only (`pence`/`bps`) to eliminate float drift.
- API reporting must include both machine-safe integer values and user-readable formatted currency strings.
- Deterministic path outputs are treated as reproducible golden-contract artifacts.

### Risks / Blockers
- Any external consumer still expecting pre-POC-002 float money fields may break without coordinated contract update.
- Golden tests require strict maintenance discipline when deterministic logic intentionally changes.
