# 🏠 UK Household Financial Stress Testing Engine

Anonymous, educational simulation platform for UK household financial stress testing.
**Educational simulation only. This tool does not provide financial advice, investment advice, product recommendations, or regulated advice of any kind.**
**No login required. No PII required.**

---

## Overview

This Python web app allows UK households to stress test their finances against:

- **Income shocks** — a percentage drop in monthly net income
- **Mortgage rate increases** — e.g., rate at next fixed-rate renewal
- **Essentials inflation** — increased cost of essential spending
- **Savings runway** — months until savings are depleted under negative cashflow

It provides:

- **Deterministic outputs** (single-point scenario results)
- **Premium/advanced Monte Carlo outputs** (P10/P50/P90 cashflow and runway)

All outputs are **illustrative estimates** based on simplified modelling assumptions and should not be relied on as your sole basis for financial decisions.

---

## What This Is Not

- Financial advice
- Investment advice
- Product recommendations
- Regulated advice of any kind
- A mortgage or product comparison tool
- Connected to bank accounts
- A tool for institutional or regulatory capital modelling

---

## Privacy (Anonymous by Design)

- No login required
- No bank linking
- No statement uploads
- No personally identifiable information (PII) required to run the model
- User inputs are processed in-memory and not persisted by the application
- No analytics, tracking pixels, or session recording
- If payment processing is added, it should be delegated to a third-party provider

For full details, see [docs/privacy.md](docs/privacy.md).

---

## Quick Start

### Prerequisites

Install [uv](https://docs.astral.sh/uv/):

```bash
pip install uv
```

### Setup & Run

```bash
# Create virtual environment and install dependencies
uv venv
uv sync --all-extras

# Start the development server
uv run uvicorn app.main:app --reload
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

### Tests

```bash
uv run pytest -v
```

### Lint & Format Checks

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
    inputs.py           # Pydantic input models
    outputs.py          # Pydantic output models
  engines/
    deterministic.py    # Single-point stress test engine
    monte_carlo.py      # Probabilistic Monte Carlo engine (P10/P50/P90)
  assumptions/
    v1.yaml             # Conservative uncertainty assumptions
    v2.yaml             # Severe/tail-risk uncertainty assumptions
  templates/
    index.html          # Input form (Jinja2)
    results.html        # Results display (Jinja2)
  core/config.py        # Application configuration

tests/                  # pytest test suite
docs/                   # assumptions, disclaimer, privacy, licensing docs
```

### API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | HTML input form |
| `POST` | `/ui/results` | HTML results page (form submission) |
| `POST` | `/api/v1/stress/deterministic` | JSON deterministic stress test |
| `POST` | `/api/v1/stress/monte-carlo` | JSON Monte Carlo stress test |

Interactive API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Disclaimer

> **EDUCATIONAL SIMULATION ONLY.** This tool does not provide financial advice, investment advice, or product recommendations. It is not regulated by the UK Financial Conduct Authority (FCA). Results are illustrative estimates based on simplified modelling assumptions and should not be relied on as the sole basis for financial decisions.

See [docs/regulatory_disclaimer.md](docs/regulatory_disclaimer.md) for the full disclaimer.
