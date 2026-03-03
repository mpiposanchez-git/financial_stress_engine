from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import router
from .settings import get_settings

settings = get_settings()

app = FastAPI(
    title="Financial Stress Engine API Service",
    version="0.1.0",
    description="Cloud API for deterministic and Monte Carlo stress test execution.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(router)
