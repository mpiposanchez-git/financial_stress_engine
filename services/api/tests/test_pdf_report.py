from __future__ import annotations

from shared.engine.reports.pdf_report import generate_pdf_report


def test_generate_pdf_report_contains_expected_headings_and_size() -> None:
    pdf_bytes = generate_pdf_report(
        inputs={"reporting_currency": "GBP", "income_gbp": 4000},
        outputs={"runway_months": 12.5, "min_savings_pence": 123456},
        disclaimers=["Educational simulation only.", "Not financial advice."],
        provenance={"dataset": "boe_bank_rate", "fetched_at_utc": "2026-03-06T00:00:00Z"},
        app_version="0.1.1",
    )

    assert len(pdf_bytes) > 1000
    assert b"Financial Stress Report" in pdf_bytes
    assert b"Inputs" in pdf_bytes
    assert b"Outputs" in pdf_bytes
    assert b"Provenance" in pdf_bytes
    assert b"Disclaimers" in pdf_bytes
