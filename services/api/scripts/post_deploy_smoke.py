from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from typing import Any


def _headers(token: str | None = None) -> dict[str, str]:
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _request_json(method: str, url: str, headers: dict[str, str], payload: dict[str, Any] | None = None) -> tuple[int, Any, float]:
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url=url, data=body, method=method, headers=headers)
    started = time.perf_counter()

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            elapsed_ms = (time.perf_counter() - started) * 1000.0
            raw = response.read().decode("utf-8")
            parsed = json.loads(raw) if raw else {}
            return response.status, parsed, elapsed_ms
    except urllib.error.HTTPError as http_error:
        elapsed_ms = (time.perf_counter() - started) * 1000.0
        raw = http_error.read().decode("utf-8")
        parsed = None
        if raw:
            try:
                parsed = json.loads(raw)
            except json.JSONDecodeError:
                parsed = raw
        return http_error.code, parsed, elapsed_ms


def _base_input() -> dict[str, Any]:
    return {
        "household_monthly_net_income_gbp": 4000,
        "household_monthly_essential_spend_gbp": 1500,
        "household_monthly_debt_payments_gbp": 200,
        "cash_savings_gbp": 10000,
        "mortgage_balance_gbp": 250000,
        "mortgage_term_years_remaining": 25,
        "mortgage_rate_percent_current": 4.5,
        "mortgage_rate_percent_stress": 6.0,
        "mortgage_type": "repayment",
        "shock_monthly_income_drop_percent": 10,
        "inflation_monthly_essentials_increase_percent": 5,
        "household_monthly_net_income_currency": "GBP",
        "household_monthly_essential_spend_currency": "GBP",
        "household_monthly_debt_payments_currency": "GBP",
        "cash_savings_currency": "GBP",
        "mortgage_balance_currency": "GBP",
        "reporting_currency": "GBP",
        "fx_spot_rates": {"GBP": 1.0, "EUR": 0.86, "USD": 0.78},
        "fx_stress_bps": {"GBP": 0, "EUR": 0, "USD": 0},
        "income_shock_std_percent": 5.0,
        "rate_shock_std_percent": 0.5,
        "inflation_shock_std_percent": 1.0,
    }


def _print_result(label: str, status: int, elapsed_ms: float) -> None:
    print(f"[{label}] status={status} latency_ms={elapsed_ms:.2f}")


def run(base_url: str, token: str, max_latency_ms: float) -> int:
    health_url = f"{base_url}/health"
    det_url = f"{base_url}/api/v1/deterministic/run"
    mc_url = f"{base_url}/api/v1/montecarlo/run"

    checks: list[tuple[str, int, float, str | None]] = []

    status, body, elapsed = _request_json("GET", health_url, headers=_headers())
    _print_result("health", status, elapsed)
    checks.append(("health", status, elapsed, None if status == 200 and body == {"status": "ok"} else "Expected {'status': 'ok'}"))

    det_payload = {"input_parameters": _base_input()}
    status, body, elapsed = _request_json("POST", det_url, headers=_headers(token), payload=det_payload)
    _print_result("deterministic", status, elapsed)
    det_error = None
    if status != 200:
        det_error = f"Unexpected status/body: status={status}, body={body}"
    elif not isinstance(body, dict) or "runway_months" not in body or "min_savings_pence" not in body:
        det_error = "Missing deterministic response keys"
    checks.append(("deterministic", status, elapsed, det_error))

    mc_payload = {
        "input_parameters": _base_input(),
        "n_sims": 200,
        "horizon_months": 24,
        "seed": 314159,
    }
    status, body, elapsed = _request_json("POST", mc_url, headers=_headers(token), payload=mc_payload)
    _print_result("montecarlo", status, elapsed)
    mc_error = None
    if status != 200:
        mc_error = f"Unexpected status/body: status={status}, body={body}"
    elif not isinstance(body, dict) or "metrics" not in body:
        mc_error = "Missing Monte Carlo metrics"
    checks.append(("montecarlo", status, elapsed, mc_error))

    failures: list[str] = []
    for label, status, elapsed, error in checks:
        if status >= 400:
            failures.append(f"{label}: HTTP {status}")
        if elapsed > max_latency_ms:
            failures.append(f"{label}: latency {elapsed:.2f}ms exceeded threshold {max_latency_ms:.2f}ms")
        if error:
            failures.append(f"{label}: {error}")

    if failures:
        print("Smoke checks failed:")
        for item in failures:
            print(f" - {item}")
        return 1

    print("Smoke checks passed.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Post-deploy smoke checks for API health and core endpoints")
    parser.add_argument("--base-url", default=os.getenv("STRESS_API_BASE_URL"), help="Backend base URL, e.g. https://service.onrender.com")
    parser.add_argument("--token", default=os.getenv("STRESS_API_TOKEN"), help="Bearer token used for authenticated endpoint checks")
    parser.add_argument("--max-latency-ms", type=float, default=float(os.getenv("STRESS_SMOKE_MAX_LATENCY_MS", "3000")))
    args = parser.parse_args()

    if not args.base_url:
        print("Missing --base-url or STRESS_API_BASE_URL", file=sys.stderr)
        return 2

    if not args.token:
        print("Missing --token or STRESS_API_TOKEN", file=sys.stderr)
        return 2

    return run(args.base_url.rstrip("/"), args.token, args.max_latency_ms)


if __name__ == "__main__":
    raise SystemExit(main())
