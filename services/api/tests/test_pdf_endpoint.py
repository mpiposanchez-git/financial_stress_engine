from __future__ import annotations

from fastapi.testclient import TestClient

from services.api.app.auth import AuthContext, require_auth
from services.api.app.main import app


def _payload() -> dict[str, object]:
    return {
        "inputs": {"reporting_currency": "GBP", "income_gbp": 4000},
        "outputs": {"runway_months": 12.5, "min_savings_pence": 123456},
        "disclaimers": ["Educational simulation only.", "Not financial advice."],
        "provenance": {"dataset": "boe_bank_rate", "fetched_at_utc": "2026-03-06T00:00:00Z"},
        "app_version": "0.1.1",
    }


def test_pdf_endpoint_returns_403_for_non_premium(monkeypatch) -> None:
    monkeypatch.setenv("PREMIUM_SUBJECT_ALLOWLIST", "premium-user")
    app.dependency_overrides[require_auth] = lambda: AuthContext(subject="free-user")
    try:
        with TestClient(app) as client:
            response = client.post("/api/v1/reports/pdf", json=_payload())
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 403
    assert response.json()["detail"] == "Premium entitlement required"


def test_pdf_endpoint_returns_pdf_for_premium(monkeypatch) -> None:
    monkeypatch.setenv("PREMIUM_SUBJECT_ALLOWLIST", "premium-user")
    app.dependency_overrides[require_auth] = lambda: AuthContext(subject="premium-user")
    try:
        with TestClient(app) as client:
            response = client.post("/api/v1/reports/pdf", json=_payload())
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/pdf")
    assert len(response.content) > 1000
