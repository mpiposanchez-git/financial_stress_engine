from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from services.api.app.main import app


@pytest.fixture(autouse=True)
def patch_jwt_decode(monkeypatch: pytest.MonkeyPatch) -> None:
    def _fake_decode_and_validate_jwt(token: str, settings):  # noqa: ANN001
        if token == "valid-token":
            return {"sub": "user_123"}
        raise Exception("invalid")

    monkeypatch.setattr(
        "services.api.app.auth.decode_and_validate_jwt",
        _fake_decode_and_validate_jwt,
    )


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def valid_headers() -> dict[str, str]:
    return {"Authorization": "Bearer valid-token"}
