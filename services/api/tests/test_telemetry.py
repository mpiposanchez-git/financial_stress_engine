from __future__ import annotations

from typing import Any

from fastapi.testclient import TestClient

from services.api.app.telemetry import reset_telemetry


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
    }


def test_admin_telemetry_requires_token(authenticated_client: TestClient, monkeypatch) -> None:
    reset_telemetry()
    monkeypatch.setenv("ADMIN_METRICS_TOKEN", "secret-token")

    response = authenticated_client.get("/api/v1/admin/telemetry")

    assert response.status_code == 403


def test_admin_telemetry_returns_aggregate_counters(
    authenticated_client: TestClient,
    monkeypatch,
) -> None:
    reset_telemetry()
    monkeypatch.setenv("ADMIN_METRICS_TOKEN", "secret-token")

    deterministic_payload = {"input_parameters": _base_input()}
    montecarlo_payload = {
        "input_parameters": {
            **_base_input(),
            "income_shock_std_percent": 5.0,
            "rate_shock_std_percent": 0.5,
            "inflation_shock_std_percent": 1.0,
        },
        "n_sims": 200,
        "horizon_months": 12,
        "seed": 20260306,
    }

    deterministic_response = authenticated_client.post(
        "/api/v1/deterministic/run",
        json=deterministic_payload,
    )
    montecarlo_response = authenticated_client.post(
        "/api/v1/montecarlo/run",
        json=montecarlo_payload,
    )

    assert deterministic_response.status_code == 200
    assert montecarlo_response.status_code == 200
    assert authenticated_client.get("/not-found").status_code == 404

    telemetry = authenticated_client.get(
        "/api/v1/admin/telemetry",
        headers={"X-Admin-Metrics-Token": "secret-token"},
    )

    assert telemetry.status_code == 200
    body = telemetry.json()

    assert body["deterministic_runs_total"] >= 1
    assert body["montecarlo_runs_total"] >= 1
    assert body["pdf_exports_total"] == 0
    assert body["errors_total"] >= 1
    runtime_keys = set(body["runtime_buckets"].keys())
    assert runtime_keys == {"lt_100ms", "100_to_499ms", "500_to_999ms", "gte_1000ms"}
    assert "subject" not in body
    assert "payload" not in body
