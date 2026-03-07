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


def _sensitivity_payload() -> dict[str, Any]:
    return {
        "input_parameters": _base_input(),
        "horizon_months": 24,
        "delta_bps": 100,
    }


def test_sensitivity_endpoint_returns_403_for_non_premium_subject(monkeypatch) -> None:
    monkeypatch.setenv("PREMIUM_SUBJECT_ALLOWLIST", "premium-user")
    app.dependency_overrides[require_auth] = lambda: AuthContext(subject="free-user")
    try:
        with TestClient(app) as client:
            response = client.post("/api/v1/sensitivity/run", json=_sensitivity_payload())
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 403
    assert response.json()["detail"] == "Premium entitlement required"


def test_sensitivity_endpoint_returns_ranked_impacts_for_premium_subject(monkeypatch) -> None:
    monkeypatch.setenv("PREMIUM_SUBJECT_ALLOWLIST", "premium-user")
    app.dependency_overrides[require_auth] = lambda: AuthContext(subject="premium-user")
    try:
        with TestClient(app) as client:
            response = client.post("/api/v1/sensitivity/run", json=_sensitivity_payload())
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    body = response.json()
    impacts = body["impacts"]

    assert len(impacts) == 4
    assert {item["driver"] for item in impacts} == {
        "income_shock_bps",
        "inflation_shock_bps",
        "mortgage_rate_stress_bps",
        "fx_stress_bps",
    }

    for impact in impacts:
        assert isinstance(impact["delta_bps"], int)
        assert isinstance(impact["base_min_savings_pence"], int)
        assert isinstance(impact["perturbed_min_savings_pence"], int)
        assert isinstance(impact["min_savings_impact_pence"], int)

    abs_impacts = [abs(item["min_savings_impact_pence"]) for item in impacts]
    assert abs_impacts == sorted(abs_impacts, reverse=True)
