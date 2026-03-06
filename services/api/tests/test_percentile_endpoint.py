from __future__ import annotations

from fastapi.testclient import TestClient

from services.api.app.auth import AuthContext, require_auth
from services.api.app.main import app


def _payload() -> dict[str, object]:
    return {
        "annual_net_income_reporting_currency": 36000,
        "reporting_currency": "GBP",
    }


def test_percentile_endpoint_returns_403_for_non_premium(monkeypatch) -> None:
    monkeypatch.setenv("PREMIUM_SUBJECT_ALLOWLIST", "premium-user")
    app.dependency_overrides[require_auth] = lambda: AuthContext(subject="free-user")
    try:
        with TestClient(app) as client:
            response = client.post("/api/v1/benchmarks/uk/percentile", json=_payload())
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 403
    assert response.json()["detail"] == "Premium entitlement required"


def test_percentile_endpoint_returns_bucket_for_premium(monkeypatch) -> None:
    monkeypatch.setenv("PREMIUM_SUBJECT_ALLOWLIST", "premium-user")
    app.dependency_overrides[require_auth] = lambda: AuthContext(subject="premium-user")
    try:
        with TestClient(app) as client:
            response = client.post("/api/v1/benchmarks/uk/percentile", json=_payload())
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    body = response.json()
    assert body["percentile_bucket"] == 70
    assert body["year_label"]
    assert body["reporting_currency"] == "GBP"
    assert len(body["caveats"]) >= 1
    assert len(body["thresholds_gbp"]) == 9
