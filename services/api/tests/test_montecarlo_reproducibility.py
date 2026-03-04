from __future__ import annotations

from typing import Any

from fastapi.testclient import TestClient


def _base_input() -> dict[str, Any]:
    return {
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
        "fx_monthly_vol_bps": {"EUR": 50, "USD": 50},
    }


def test_montecarlo_reproducible_iid(authenticated_client: TestClient) -> None:
    payload: dict[str, Any] = {
        "input_parameters": {
            **_base_input(),
            "income_shock_std_percent": 5.0,
            "rate_shock_std_percent": 0.5,
            "inflation_shock_std_percent": 1.0,
            "shock_dynamics": "iid",
            "ar1_phi": 0.0,
        },
        "n_sims": 300,
        "horizon_months": 12,
        "seed": 24680,
    }

    first = authenticated_client.post("/api/v1/montecarlo/run", json=payload)
    second = authenticated_client.post("/api/v1/montecarlo/run", json=payload)

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["metrics"] == second.json()["metrics"]


def test_montecarlo_reproducible_ar1(authenticated_client: TestClient) -> None:
    payload: dict[str, Any] = {
        "input_parameters": {
            **_base_input(),
            "income_shock_std_percent": 5.0,
            "rate_shock_std_percent": 0.5,
            "inflation_shock_std_percent": 1.0,
            "shock_dynamics": "ar1",
            "ar1_phi": 0.6,
        },
        "n_sims": 300,
        "horizon_months": 12,
        "seed": 13579,
    }

    first = authenticated_client.post("/api/v1/montecarlo/run", json=payload)
    second = authenticated_client.post("/api/v1/montecarlo/run", json=payload)

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["metrics"] == second.json()["metrics"]


def test_montecarlo_sigma_zero_collapses_distribution(authenticated_client: TestClient) -> None:
    payload: dict[str, Any] = {
        "input_parameters": {
            **_base_input(),
            "income_shock_std_percent": 0.0,
            "rate_shock_std_percent": 0.0,
            "inflation_shock_std_percent": 0.0,
            "shock_dynamics": "iid",
            "ar1_phi": 0.0,
            "fx_monthly_vol_bps": {"EUR": 0, "USD": 0},
        },
        "n_sims": 250,
        "horizon_months": 12,
        "seed": 11111,
    }

    response = authenticated_client.post("/api/v1/montecarlo/run", json=payload)
    assert response.status_code == 200

    metrics = response.json()["metrics"]
    runway = metrics["runway_months"]
    assert runway["p10"] == runway["p50"] == runway["p90"]

    min_savings = metrics["min_savings"]
    assert min_savings["p10_pence"] == min_savings["p50_pence"] == min_savings["p90_pence"]


def test_montecarlo_positive_sigma_widens_distribution(authenticated_client: TestClient) -> None:
    payload: dict[str, Any] = {
        "input_parameters": {
            **_base_input(),
            "income_shock_std_percent": 7.0,
            "rate_shock_std_percent": 1.0,
            "inflation_shock_std_percent": 2.0,
            "shock_dynamics": "iid",
            "ar1_phi": 0.0,
            "fx_monthly_vol_bps": {"EUR": 300, "USD": 300},
        },
        "n_sims": 500,
        "horizon_months": 12,
        "seed": 22222,
    }

    response = authenticated_client.post("/api/v1/montecarlo/run", json=payload)
    assert response.status_code == 200

    metrics = response.json()["metrics"]
    runway = metrics["runway_months"]
    assert runway["p90"] >= runway["p10"]

    min_savings = metrics["min_savings"]
    assert min_savings["p90_pence"] >= min_savings["p10_pence"]
    assert (min_savings["p90_pence"] - min_savings["p10_pence"]) > 0
