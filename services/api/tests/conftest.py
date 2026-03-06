from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from services.api.app.auth import AuthContext, require_auth
from services.api.app.entitlements import require_premium
from services.api.app.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def authenticated_client() -> TestClient:
    app.dependency_overrides[require_auth] = lambda: AuthContext(subject="test_user")
    app.dependency_overrides[require_premium] = lambda: AuthContext(subject="test_user")
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()
