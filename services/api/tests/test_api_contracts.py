from __future__ import annotations

from services.api.app.data_cache import DATA_CACHE, CacheMeta


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


def test_data_registry_returns_datasets(client):
    response = client.get("/api/v1/data/registry")
    assert response.status_code == 200

    body = response.json()
    datasets = body["datasets"]
    assert isinstance(datasets, list)
    assert len(datasets) >= 4

    first = datasets[0]
    assert isinstance(first["name"], str)
    assert isinstance(first["provider"], str)
    assert isinstance(first["url"], str)
    assert isinstance(first["refresh_cadence"], str)
    assert isinstance(first["license_note"], str)
    assert isinstance(first["verification_steps"], list)


def test_data_defaults_returns_required_keys(client):
    DATA_CACHE.set(
        "boe_bank_rate",
        {"rate_percent": 4.75, "as_of_date": "2026-03-01"},
        CacheMeta(
            fetched_at_utc="2026-03-01T00:00:00Z",
            source_url="https://example.test/boe",
            sha256="abc",
        ),
    )
    DATA_CACHE.set(
        "ons_cpih_12m",
        {"annual_rate_percent": 3.4, "month": "2026-01"},
        CacheMeta(
            fetched_at_utc="2026-03-01T00:00:00Z",
            source_url="https://example.test/ons",
            sha256="def",
        ),
    )
    DATA_CACHE.set(
        "boe_fx_spot",
        {"eur": 0.88, "usd": 0.79, "base_currency": "GBP", "as_of_date": "2026-03-01"},
        CacheMeta(
            fetched_at_utc="2026-03-01T00:00:00Z",
            source_url="https://example.test/fx",
            sha256="ghi",
        ),
    )
    DATA_CACHE.set(
        "ofgem_price_cap",
        {"region": "GB", "annual_bill_gbp": 1738, "period_start": "2025-01-01"},
        CacheMeta(
            fetched_at_utc="2026-03-01T00:00:00Z",
            source_url="https://example.test/ofgem",
            sha256="jkl",
        ),
    )

    response = client.get("/api/v1/data/defaults")
    assert response.status_code == 200

    body = response.json()
    assert body["bank_rate_bps"] == 475
    assert body["cpih_12m_bps"] == 340
    assert body["fx_spot_rates"] == {"EUR": 0.88, "USD": 0.79}
    assert body["energy_reference_values"] == {"annual_bill_gbp": 1738.0}
    assert set(body["fetched_at"].keys()) == {
        "boe_bank_rate",
        "ons_cpih_12m",
        "boe_fx_spot",
        "ofgem_price_cap",
    }


def test_uk_reference_values_returns_required_keys(client):
    response = client.get("/api/v1/benchmarks/uk/reference")
    assert response.status_code == 200

    body = response.json()
    assert set(body.keys()) == {
        "income_median_bhc",
        "income_deciles_bhc_gbp",
        "provenance",
    }
    assert set(body["income_median_bhc"].keys()) == {"year_label", "amount_gbp"}
    assert set(body["provenance"].keys()) == {
        "dataset_key",
        "source_url",
        "fetched_at_utc",
        "sha256",
        "status",
    }


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
    assert "warnings" in body
    assert len(body["savings_path_pence"]) == 25


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
    body = response.json()
    assert isinstance(body["n_sims"], int)
    assert isinstance(body["horizon_months"], int)
    assert isinstance(body["seed"], int)
    assert isinstance(body["runtime_ms"], float)
    assert isinstance(body["runway_months_p10"], float)
    assert isinstance(body["runway_months_p50"], float)
    assert isinstance(body["runway_months_p90"], float)
    assert isinstance(body["min_savings_p10_pence"], int)
    assert isinstance(body["min_savings_p50_pence"], int)
    assert isinstance(body["min_savings_p90_pence"], int)
    assert isinstance(body["month_of_depletion_p10"], float)
    assert isinstance(body["month_of_depletion_p50"], float)
    assert isinstance(body["month_of_depletion_p90"], float)

    metrics = body["metrics"]
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

    assert body["runway_months_p10"] == metrics["runway_months"]["p10"]
    assert body["runway_months_p50"] == metrics["runway_months"]["p50"]
    assert body["runway_months_p90"] == metrics["runway_months"]["p90"]
    assert body["min_savings_p10_pence"] == metrics["min_savings"]["p10_pence"]
    assert body["min_savings_p50_pence"] == metrics["min_savings"]["p50_pence"]
    assert body["min_savings_p90_pence"] == metrics["min_savings"]["p90_pence"]
    assert body["month_of_depletion_p10"] == metrics["month_of_depletion"]["p10"]
    assert body["month_of_depletion_p50"] == metrics["month_of_depletion"]["p50"]
    assert body["month_of_depletion_p90"] == metrics["month_of_depletion"]["p90"]


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


def test_deterministic_accepts_category_inflation_inputs(authenticated_client):
    payload = {
        "input_parameters": {
            **_base_input(),
            "household_monthly_net_income_gbp": 2000,
            "household_monthly_essential_spend_gbp": 1,
            "household_monthly_debt_payments_gbp": 100,
            "mortgage_balance_gbp": 0,
            "mortgage_term_years_remaining": 0,
            "shock_monthly_income_drop_percent": 0,
            "essentials_categories": {
                "food": {"monthly_spend_gbp": 1000, "inflation_bps": 0},
                "energy": {"monthly_spend_gbp": 500, "inflation_bps": 2000},
            },
        }
    }

    response = authenticated_client.post("/api/v1/deterministic/run", json=payload)

    assert response.status_code == 200
    body = response.json()

    # Categories override single-bucket essentials in stress calculation.
    assert body["monthly_cashflow_stress_pence"] == 30000
