from __future__ import annotations

from typing import Any

from fastapi.testclient import TestClient

from services.api.app.auth import AuthContext, require_auth
from services.api.app.main import app


def _montecarlo_payload() -> dict[str, Any]:
    return {
        "input_parameters": {
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
        },
        "n_sims": 300,
        "horizon_months": 12,
        "seed": 24680,
    }


def test_allowlisted_subject_passes_montecarlo(monkeypatch) -> None:
    monkeypatch.setenv("PREMIUM_SUBJECT_ALLOWLIST", "premium-user")
    app.dependency_overrides[require_auth] = lambda: AuthContext(subject="premium-user")
    try:
        with TestClient(app) as client:
            response = client.post("/api/v1/montecarlo/run", json=_montecarlo_payload())
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200


def test_non_allowlisted_subject_gets_403(monkeypatch) -> None:
    monkeypatch.setenv("PREMIUM_SUBJECT_ALLOWLIST", "premium-user")
    app.dependency_overrides[require_auth] = lambda: AuthContext(subject="free-user")
    try:
        with TestClient(app) as client:
            response = client.post("/api/v1/montecarlo/run", json=_montecarlo_payload())
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 403
    assert response.json()["detail"] == "Premium entitlement required"


def test_me_returns_subject_and_is_premium(monkeypatch) -> None:
    monkeypatch.setenv("PREMIUM_SUBJECT_ALLOWLIST", "premium-user")
    app.dependency_overrides[require_auth] = lambda: AuthContext(subject="premium-user")
    try:
        with TestClient(app) as client:
            response = client.get("/api/v1/me")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {"subject": "premium-user", "is_premium": True}
