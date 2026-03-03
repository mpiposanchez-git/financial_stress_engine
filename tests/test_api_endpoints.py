"""Tests for FastAPI endpoints."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

BASE_PAYLOAD = {
    "household_monthly_net_income_gbp": 3500.0,
    "household_monthly_essential_spend_gbp": 1800.0,
    "household_monthly_debt_payments_gbp": 200.0,
    "cash_savings_gbp": 10000.0,
    "mortgage_balance_gbp": 200000.0,
    "mortgage_term_years_remaining": 22.0,
    "mortgage_rate_percent_current": 4.5,
    "mortgage_rate_percent_stress": 6.5,
    "mortgage_type": "repayment",
    "shock_monthly_income_drop_percent": 20.0,
    "inflation_monthly_essentials_increase_percent": 5.0,
}


class TestDeterministicEndpoint:
    def test_success(self):
        resp = client.post("/api/v1/stress/deterministic", json=BASE_PAYLOAD)
        assert resp.status_code == 200
        data = resp.json()
        assert "monthly_cashflow_base_gbp" in data
        assert "monthly_cashflow_stress_gbp" in data
        assert "disclaimer" in data

    def test_validation_error_negative_income(self):
        bad = {**BASE_PAYLOAD, "household_monthly_net_income_gbp": -100}
        resp = client.post("/api/v1/stress/deterministic", json=bad)
        assert resp.status_code == 422

    def test_validation_error_invalid_mortgage_type(self):
        bad = {**BASE_PAYLOAD, "mortgage_type": "balloon"}
        resp = client.post("/api/v1/stress/deterministic", json=bad)
        assert resp.status_code == 422

    def test_zero_mortgage_balance(self):
        payload = {**BASE_PAYLOAD, "mortgage_balance_gbp": 0, "mortgage_term_years_remaining": 0}
        resp = client.post("/api/v1/stress/deterministic", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["mortgage_payment_current_gbp"] == 0.0

    def test_interest_only(self):
        payload = {**BASE_PAYLOAD, "mortgage_type": "interest_only"}
        resp = client.post("/api/v1/stress/deterministic", json=payload)
        assert resp.status_code == 200


class TestMonteCarloEndpoint:
    MC_PAYLOAD = {**BASE_PAYLOAD, "num_trials": 500}

    def test_success(self):
        resp = client.post("/api/v1/stress/monte-carlo", json=self.MC_PAYLOAD)
        assert resp.status_code == 200
        data = resp.json()
        assert "p10_monthly_cashflow_gbp" in data
        assert "p50_monthly_cashflow_gbp" in data
        assert "p90_monthly_cashflow_gbp" in data
        assert "probability_negative_cashflow" in data

    def test_percentile_ordering(self):
        resp = client.post("/api/v1/stress/monte-carlo", json=self.MC_PAYLOAD)
        data = resp.json()
        assert data["p10_monthly_cashflow_gbp"] <= data["p50_monthly_cashflow_gbp"]
        assert data["p50_monthly_cashflow_gbp"] <= data["p90_monthly_cashflow_gbp"]

    def test_trials_exceeding_max_rejected(self):
        bad = {**self.MC_PAYLOAD, "num_trials": 100_000}
        resp = client.post("/api/v1/stress/monte-carlo", json=bad)
        assert resp.status_code == 422

    def test_disclaimer_in_response(self):
        resp = client.post("/api/v1/stress/monte-carlo", json=self.MC_PAYLOAD)
        data = resp.json()
        assert "EDUCATIONAL SIMULATION ONLY" in data["disclaimer"]


class TestUIEndpoints:
    def test_index_returns_html(self):
        resp = client.get("/")
        assert resp.status_code == 200
        assert "text/html" in resp.headers["content-type"]
        assert "Stress Test" in resp.text

    def test_ui_results_returns_html(self):
        form_data = {
            "household_monthly_net_income_gbp": "3500",
            "household_monthly_essential_spend_gbp": "1800",
            "household_monthly_debt_payments_gbp": "200",
            "cash_savings_gbp": "10000",
            "mortgage_balance_gbp": "200000",
            "mortgage_term_years_remaining": "22",
            "mortgage_rate_percent_current": "4.5",
            "mortgage_rate_percent_stress": "6.5",
            "mortgage_type": "repayment",
            "shock_monthly_income_drop_percent": "20",
            "inflation_monthly_essentials_increase_percent": "5",
        }
        resp = client.post("/ui/results", data=form_data)
        assert resp.status_code == 200
        assert "text/html" in resp.headers["content-type"]
        assert "Results" in resp.text
