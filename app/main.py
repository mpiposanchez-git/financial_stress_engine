from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(
    title="UK Household Financial Stress Testing Engine",
    description=(
        "Anonymous, educational simulation platform for UK household financial stress testing. "
        "NOT financial advice. No PII collected."
    ),
    version="0.1.0",
)

app.include_router(router)
