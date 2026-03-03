from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    env: str
    cors_origins: list[str]
    clerk_jwks_url: str
    clerk_issuer: str
    max_monte_carlo_sims: int
    max_horizon_months: int
    rate_limit_rpm: int
    request_timeout_seconds: int


def _parse_cors_origins(raw: str) -> list[str]:
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


def get_settings() -> Settings:
    return Settings(
        env=os.getenv("ENV", "dev"),
        cors_origins=_parse_cors_origins(os.getenv("CORS_ORIGINS", "http://localhost:5173")),
        clerk_jwks_url=os.getenv("CLERK_JWKS_URL", "https://example.com/.well-known/jwks.json"),
        clerk_issuer=os.getenv("CLERK_ISSUER", "https://example.com"),
        max_monte_carlo_sims=int(os.getenv("MAX_MONTE_CARLO_SIMS", "2000")),
        max_horizon_months=int(os.getenv("MAX_HORIZON_MONTHS", "120")),
        rate_limit_rpm=int(os.getenv("RATE_LIMIT_RPM", "60")),
        request_timeout_seconds=int(os.getenv("REQUEST_TIMEOUT_SECONDS", "30")),
    )
