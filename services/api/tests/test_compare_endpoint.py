from __future__ import annotations

from typing import Any

from fastapi.testclient import TestClient

from services.api.app.auth import AuthContext, require_auth
from services.api.app.main import app


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


def _compare_payload() -> dict[str, Any]:
    base = _base_input()
    stress = {**base, "shock_monthly_income_drop_percent": 25, "mortgage_rate_percent_stress": 8.0}
    return {
        "scenarios": [
            {"name": "Base", "input_parameters": base, "horizon_months": 24},
            {"name": "Stress A", "input_parameters": stress, "horizon_months": 24},
        ]
    }


def test_compare_endpoint_returns_403_for_non_premium_subject(monkeypatch) -> None:
    monkeypatch.setenv("PREMIUM_SUBJECT_ALLOWLIST", "premium-user")
    app.dependency_overrides[require_auth] = lambda: AuthContext(subject="free-user")
    try:
        with TestClient(app) as client:
            response = client.post("/api/v1/compare/run", json=_compare_payload())
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 403
    assert response.json()["detail"] == "Premium entitlement required"


def test_compare_endpoint_returns_200_for_premium_subject(monkeypatch) -> None:
    monkeypatch.setenv("PREMIUM_SUBJECT_ALLOWLIST", "premium-user")
    app.dependency_overrides[require_auth] = lambda: AuthContext(subject="premium-user")
    try:
        with TestClient(app) as client:
            response = client.post("/api/v1/compare/run", json=_compare_payload())
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    body = response.json()
    assert "scenarios" in body
    assert len(body["scenarios"]) == 2
    assert body["scenarios"][0]["name"] == "Base"
    assert body["scenarios"][1]["name"] == "Stress A"
    assert "min_savings_pence" in body["scenarios"][0]
    assert "runway_months" in body["scenarios"][0]
