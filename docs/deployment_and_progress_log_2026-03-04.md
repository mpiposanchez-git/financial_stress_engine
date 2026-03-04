# Deployment and Progress Log (2026-03-04)

## Scope Covered

This log records deployment, authentication, troubleshooting, and stabilization work completed up to 2026-03-04.

---

## Achievements Completed

### 1) Cloud Deployment Baseline Established

- Frontend deployed to GitHub Pages.
- Backend deployed to Render.
- End-to-end simulation execution confirmed in production environment.

### 2) CI/CD and Runtime Configuration Clarified

- Confirmed GitHub Pages workflow trigger behavior (path-based and manual workflow_dispatch).
- Clarified that Vite `VITE_*` variables are build-time values and require a Pages rebuild to take effect.
- Confirmed Render root `/` may return `{"detail":"Not Found"}` while `/health` is the correct health probe endpoint.

### 3) Authentication Root Cause Isolated and Verified

- Isolated non-auth engine behavior using temporary bypass controls.
- Verified deterministic and Monte Carlo endpoints return valid production results when auth is bypassed.
- Re-enabled full authentication and confirmed secured flow works after correcting Clerk/issuer/origin configuration.

### 4) Security Hardening Cleanup Completed

- Removed all temporary auth bypass code and env flags from frontend and backend.
- Verified frontend and backend tests pass after bypass removal.

---

## Key Configuration Lessons Learned

1. **Clerk issuer/JWKS must match token issuer exactly**
   - `CLERK_ISSUER` must equal JWT `iss` claim.
   - `CLERK_JWKS_URL` must be the corresponding `/.well-known/jwks.json` URL.

2. **GitHub username/domain mismatch causes auth and redirect failures**
   - Correct host for this project deployment: `https://mpiposanchez-git.github.io`.

3. **GitHub Pages project path must be included in app and auth redirects**
   - App lives under `/financial_stress_engine/`.

4. **VPN/network filtering can silently break Clerk script loading and login flow**
   - DNS/proxy filtering caused intermittent auth script failures.

---

## Current Known-Good Outcome

- App loads on GitHub Pages.
- Stress test execution returns deterministic and Monte Carlo payloads.
- Auth-enabled run has been confirmed successful after config correction.

---

## Immediate Next Steps (Priority Order)

1. **Freeze deployment config snapshot**
   - Record final values for Render env vars, GitHub repo variables/secrets, and Clerk paths in a single runbook section.

2. **Add frontend results visualization**
   - Implement chart-based display for Monte Carlo percentile outputs.

3. **Add production smoke checklist automation**
   - Verify `/health`, one authenticated deterministic run, and one Monte Carlo run post-deploy.

4. **Strengthen auth diagnostics (non-sensitive)**
   - Improve user-facing error messages for auth failures without exposing token content.

5. **Prepare release notes and version tag**
   - Summarize deployment, auth stabilization, and current feature status.

---

## Suggested Follow-Up Workstream

- UI/UX pass for results page (charts + readability)
- Observability basics (error-rate and latency checks)
- Optional compliance docs refinement (privacy + terms consistency review)
