from __future__ import annotations


def _base_input() -> dict:
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
    }


def test_health_returns_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_auth_rejects_missing_token(client):
    payload = {"input_parameters": _base_input()}
    response = client.post("/api/v1/deterministic/run", json=payload)
    assert response.status_code == 401


def test_deterministic_returns_required_keys(authenticated_client):
    payload = {"input_parameters": _base_input()}
    response = authenticated_client.post("/api/v1/deterministic/run", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert "reporting_currency" in body
    assert "fx_spot_rates_used" in body
    assert "fx_stressed_rates_used" in body
    assert "fx_stress_bps" in body
    assert "monthly_cashflow_base_pence" in body
    assert "monthly_cashflow_base_formatted" in body
    assert "monthly_cashflow_stress_pence" in body
    assert "monthly_cashflow_stress_formatted" in body
    assert "mortgage_payment_current_pence" in body
    assert "mortgage_payment_current_formatted" in body
    assert "mortgage_payment_stress_pence" in body
    assert "mortgage_payment_stress_formatted" in body
    assert "runway_months" in body
    assert "savings_path_pence" in body
    assert "savings_path_formatted" in body
    assert "min_savings_pence" in body
    assert "min_savings_formatted" in body
    assert "month_of_depletion" in body
    assert "month_by_month" in body
    assert "warnings" in body
    assert len(body["savings_path_pence"]) == 25
    assert body["month_by_month"] == body["savings_path_pence"]


def test_montecarlo_returns_metrics_percentiles(authenticated_client):
    payload = {
        "input_parameters": {
            **_base_input(),
            "income_shock_std_percent": 5.0,
            "rate_shock_std_percent": 0.5,
            "inflation_shock_std_percent": 1.0,
        },
        "n_sims": 500,
        "horizon_months": 24,
        "seed": 12345,
    }
    response = authenticated_client.post("/api/v1/montecarlo/run", json=payload)
    assert response.status_code == 200
    metrics = response.json()["metrics"]
    assert set(metrics["runway_months"].keys()) == {"p10", "p50", "p90"}
    assert set(metrics["min_savings"].keys()) == {
        "p10_pence",
        "p10_formatted",
        "p50_pence",
        "p50_formatted",
        "p90_pence",
        "p90_formatted",
    }
    assert set(metrics["month_of_depletion"].keys()) == {"p10", "p50", "p90"}


def test_montecarlo_seed_reproducibility(authenticated_client):
    payload = {
        "input_parameters": {
            **_base_input(),
            "income_shock_std_percent": 5.0,
            "rate_shock_std_percent": 0.5,
            "inflation_shock_std_percent": 1.0,
        },
        "n_sims": 400,
        "horizon_months": 24,
        "seed": 98765,
    }

    first = authenticated_client.post("/api/v1/montecarlo/run", json=payload)
    second = authenticated_client.post("/api/v1/montecarlo/run", json=payload)

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["metrics"] == second.json()["metrics"]
    assert first.json()["seed"] == second.json()["seed"]
