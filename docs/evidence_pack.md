# Evidence Pack and Release Checklist

Last reviewed: 2026-03-06

This document defines the minimum evidence pack required for milestone releases.

## 1) Exact Validation Commands

Run from repository root.

```bash
c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m ruff check .
c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m pytest services/api/tests -q
npm --prefix apps/web test -- --run
npm --prefix apps/web run typecheck
```

Optional post-deploy smoke validation:

```bash
c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe services/api/scripts/post_deploy_smoke.py --base-url https://<render-service>.onrender.com --token <bearer-token>
```

## 2) Artifacts to Retain

For every release candidate keep:

- Git commit SHA used for the release.
- Git tag name and creation timestamp.
- CI run links and status for backend/frontend pipelines.
- Backend test output summary (`passed/failed` counts).
- Frontend test output summary (`passed/failed` counts).
- Typecheck output summary.
- Dataset provenance snapshot:
  - cache keys
  - `fetched_at_utc`
  - `sha256`

Recommended storage location:

- release notes/changelog entry
- `docs/progress_log.md` execution section
- release PR description (if applicable)

## 3) Release Tagging Procedure

1. Ensure validation commands in Section 1 pass.
2. Create release tag:

```bash
git tag poc-milestone-<n>-YYYY-MM-DD
```

3. Push tag:

```bash
git push origin poc-milestone-<n>-YYYY-MM-DD
```

4. Capture and store commit SHA:

```bash
git rev-parse HEAD
```

5. Record tag + SHA in:
- `docs/CHANGELOG.md`
- `docs/progress_log.md`
- deployment/release notes

## 4) Minimal Release Checklist

- Lint is green.
- Backend tests are green.
- Frontend tests are green.
- Frontend typecheck is green.
- Smoke checks are green (if deploying).
- Dataset provenance hashes are captured.
- Tag and SHA recorded in docs.

<!-- crossref:start -->
## Related Documents

- [Repository README](../README.md)
- [Deployment Runbook](implementation/deployment_runbook.md)
- [Progress Log](progress_log.md)
<!-- crossref:end -->
