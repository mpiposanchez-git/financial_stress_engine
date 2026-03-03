# 🏠 UK Household Financial Stress Testing Engine

Anonymous, educational simulation platform for UK household financial stress testing.
**NOT financial advice. No PII collected. No login required.**

---

## Overview

This application allows UK households to anonymously stress test their finances against:

- **Income shocks** — a percentage drop in monthly net income
- **Mortgage rate increases** — e.g. rate at next fixed-rate renewal
- **Essentials inflation** — increased cost of essential spending

It produces both **deterministic** (single-point) and **Monte Carlo probabilistic** outputs (P10/P50/P90 cashflow and savings runway), with a clear educational disclaimer throughout.

---

## Quick Start

### Prerequisites

Install [uv](https://docs.astral.sh/uv/):

```bash
pip install uv
```

### Setup & Run

```bash
# Create virtual environment and install all dependencies
uv venv
uv sync --all-extras

# Start the development server
uv run uvicorn app.main:app --reload
```

Visit [http://localhost:8000](http://localhost:8000) in your browser.

### Run Tests

```bash
uv run pytest -v
```

### Lint & Format

```bash
uv run ruff check .
uv run ruff format --check .
```

---

## Architecture

```
app/
  main.py               # FastAPI application entry point
  api/routes.py         # HTTP routes (UI + JSON API)
  models/
    inputs.py           # Pydantic input models (DeterministicInput, MonteCarloInput)
    outputs.py          # Pydantic output models (DeterministicOutput, MonteCarloOutput)
  engines/
    deterministic.py    # Single-point stress test engine
    monte_carlo.py      # Probabilistic Monte Carlo engine (P10/P50/P90)
  assumptions/
    v1.yaml             # Conservative uncertainty band assumptions
    v2.yaml             # Severe / tail-risk uncertainty band assumptions
  templates/
    index.html          # Input form (Jinja2)
    results.html        # Results display (Jinja2)
  core/config.py        # Application configuration constants

tests/                  # pytest test suite (39 tests)
docs/                   # Assumptions, regulatory disclaimer, privacy policy
.github/workflows/      # CI pipeline (lint + test)
```

### API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | HTML input form |
| `POST` | `/ui/results` | HTML results page (form submission) |
| `POST` | `/api/v1/stress/deterministic` | JSON deterministic stress test |
| `POST` | `/api/v1/stress/monte-carlo` | JSON Monte Carlo stress test |

Interactive API docs available at [http://localhost:8000/docs](http://localhost:8000/docs).

---

## Disclaimer

> **EDUCATIONAL SIMULATION ONLY.** This tool does not provide financial advice, investment advice, or product recommendations. Results are illustrative estimates based on simplified modelling assumptions. Always consult a qualified financial adviser before making financial decisions.

See [`docs/regulatory_disclaimer.md`](docs/regulatory_disclaimer.md) and [`docs/privacy.md`](docs/privacy.md) for full details.
