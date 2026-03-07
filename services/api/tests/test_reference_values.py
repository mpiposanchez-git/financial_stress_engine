from __future__ import annotations

from services.api.app.benchmarks.reference_values import get_uk_reference_values
from services.api.app.data_cache import CacheMeta, InMemoryDataCache


def test_get_uk_reference_values_uses_cache_provenance_when_present() -> None:
    cache = InMemoryDataCache()
    cache.set(
        "dwp_hbai_zip_raw",
        b"zip-bytes",
        CacheMeta(
            fetched_at_utc="2026-03-06T12:00:00Z",
            source_url="https://example.test/hbai.zip",
            sha256="abc123",
        ),
    )

    result = get_uk_reference_values(cache)

    assert result["income_median_bhc"]["year_label"] == "FY2024 (placeholder)"
    assert result["income_median_bhc"]["amount_gbp"] == 35000.0
    assert result["income_deciles_bhc_gbp"] is None
    assert result["provenance"]["dataset_key"] == "dwp_hbai_zip_raw"
    assert result["provenance"]["source_url"] == "https://example.test/hbai.zip"
    assert result["provenance"]["fetched_at_utc"] == "2026-03-06T12:00:00Z"
    assert result["provenance"]["sha256"] == "abc123"


def test_get_uk_reference_values_falls_back_when_cache_missing() -> None:
    cache = InMemoryDataCache()
    result = get_uk_reference_values(cache)

    assert result["income_median_bhc"]["amount_gbp"] == 35000.0
    assert result["provenance"]["dataset_key"] == "dwp_hbai_zip_raw"
    assert "gov.uk" in result["provenance"]["source_url"]
    assert result["provenance"]["fetched_at_utc"] is None
    assert result["provenance"]["sha256"] is None
