# Deployment Runbook (Single Source of Truth)

Last reviewed: 2026-03-04

This runbook provides the exact configuration needed to deploy and operate this project with authentication enabled.

---

## 1) Canonical URLs

- GitHub username: `mpiposanchez-git`
- Repository: `financial_stress_engine`
- GitHub Pages app URL: `https://mpiposanchez-git.github.io/financial_stress_engine/`
- GitHub Pages host (origin): `https://mpiposanchez-git.github.io`

---

## 2) Clerk Configuration

Use one Clerk instance consistently across frontend and backend.

### Required values to copy from Clerk

- Publishable key (`pk_test_...` or `pk_live_...`)
- Issuer URL (must match JWT `iss` claim exactly)
- JWKS URL (`<issuer>/.well-known/jwks.json`)

### Paths (Clerk Dashboard → Developers → Paths)

- Fallback development host: `mpiposanchez-git.github.io`
- Home URL: `/financial_stress_engine/#/stress-test`
- Unauthorized sign in URL: `/financial_stress_engine/`

> Note: Path fields must be relative paths (start with `/`), not full URLs.

---

## 3) GitHub Repository Variables/Secrets (Frontend Build-Time)

Location: GitHub repo → Settings → Secrets and variables → Actions

### Repository Variables

- `VITE_API_BASE_URL` = `https://<your-render-service>.onrender.com`
- `VITE_APP_BASE_PATH` = `/financial_stress_engine/`

### Repository Secrets

- `VITE_CLERK_PUBLISHABLE_KEY` = `<from Clerk publishable key>`

> `VITE_*` values are injected at build-time. Any change requires a new GitHub Pages deployment.

---

## 4) Render Environment Variables (Backend Runtime)

Location: Render service → Environment

Required:

- `ENV=prod`
- `CORS_ORIGINS=https://mpiposanchez-git.github.io`
- `CLERK_ISSUER=<exact issuer from Clerk>`
- `CLERK_JWKS_URL=<exact jwks url from Clerk>`
- `MAX_MONTE_CARLO_SIMS=2000`
- `MAX_HORIZON_MONTHS=120`
- `RATE_LIMIT_RPM=60`
- `REQUEST_TIMEOUT_SECONDS=30`

Optional operational values can be added as needed, but do not remove auth variables.

---

## 5) Deploy Commands and Service Type

Use Render **Web Service** (Python runtime), not Docker service, for this baseline.

- Build command: `pip install .`
- Start command: `uvicorn services.api.app.main:app --host 0.0.0.0 --port $PORT`

---

## 6) Redeploy Rules

- If you change `VITE_*` variables: redeploy **GitHub Pages**.
- If you change Render env vars or API code: redeploy **Render**.
- If both changed: redeploy both.

---

## 7) Verification Checklist

### Backend

1. Open `https://<render-service>.onrender.com/health`
2. Expect: `{"status":"ok"}`

### Frontend

1. Open `https://mpiposanchez-git.github.io/financial_stress_engine/`
2. Sign in via Clerk
3. Open Stress Test and run simulation
4. Confirm deterministic + montecarlo JSON appears in Results

### If 401 occurs

1. Confirm request includes `Authorization: Bearer ...`
2. Decode JWT and compare `iss` to `CLERK_ISSUER`
3. Confirm `CLERK_JWKS_URL` is issuer + `/.well-known/jwks.json`

---

## 8) Security/Operations Notes

- Do not log raw bearer tokens.
- If a token was exposed in logs/chat, sign out and re-authenticate to rotate session token.
- Keep VPN/content filtering from blocking Clerk domains during auth troubleshooting.
