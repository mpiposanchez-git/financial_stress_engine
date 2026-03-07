# Data Refresh Cron Setup (Render)

Last reviewed: 2026-03-06

This document explains how to run the dataset refresh command on a schedule using Render Cron Jobs.

## Command

The refresh command is exposed as a Python module entrypoint:

```bash
uv run python -m services.api.app.data_fetcher refresh-all
```

If `uv` is not available in your environment, use the venv Python directly:

```bash
c:/Users/mpipo/Codes/financial_stress_engine/.venv/Scripts/python.exe -m services.api.app.data_fetcher refresh-all
```

## What It Does

`refresh-all` downloads and caches the latest external data snapshots currently used by the API:

- BoE bank rate
- BoE FX spot snapshot
- ONS CPIH 12-month rate
- Ofgem price cap headline snapshot
- DWP HBAI raw ZIP

Each cache write includes provenance metadata:

- `fetched_at_utc`
- `source_url`
- `sha256`

## Render Cron Job Configuration

1. Open Render Dashboard.
2. Select your service environment.
3. Create a **Cron Job**.
4. Set the command to:

```bash
uv run python -m services.api.app.data_fetcher refresh-all
```

5. Set schedule cadence. Recommended starting point:
- `0 6 * * *` (daily at 06:00 UTC)

6. Ensure runtime environment has the same environment variables as the API service for consistent behavior and observability.

## Verification

Run the command once manually and verify JSON output includes the updated key list.

Example output:

```json
{"updated": ["boe_bank_rate", "boe_fx_spot", "ons_cpih_12m", "ofgem_price_cap", "dwp_hbai_zip_raw"]}
```

Then call:

- `GET /api/v1/data/defaults`
- `GET /api/v1/data/registry`

to confirm refreshed values are available.

## Operational Notes

- Do not place secrets in command arguments.
- Keep scheduler frequency conservative to avoid accidental source over-polling.
- If source formats change, refresh may fail loudly; review logs and parser tests.
