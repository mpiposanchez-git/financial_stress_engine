from __future__ import annotations

import pytest

from services.api.app.data_cache import CacheMeta, InMemoryDataCache


def test_data_cache_set_and_get_round_trip() -> None:
    cache = InMemoryDataCache()

    cache.set(
        "boe_bank_rate",
        {"rate_percent": 4.5, "as_of": "2026-03-06"},
        CacheMeta(
            fetched_at_utc="2026-03-06T10:00:00Z",
            source_url="https://example.test/boe",
            sha256="abc123",
        ),
    )

    item = cache.get("boe_bank_rate")

    assert item is not None
    assert item.value == {"rate_percent": 4.5, "as_of": "2026-03-06"}
    assert item.meta.fetched_at_utc == "2026-03-06T10:00:00Z"
    assert item.meta.source_url == "https://example.test/boe"
    assert item.meta.sha256 == "abc123"


def test_data_cache_get_missing_key_returns_none() -> None:
    cache = InMemoryDataCache()

    assert cache.get("missing") is None


def test_data_cache_validates_required_meta_fields() -> None:
    cache = InMemoryDataCache()

    with pytest.raises(ValueError):
        cache.set(
            "ons_cpih_12m",
            {"value": 2.1},
            {
                "fetched_at_utc": "",
                "source_url": "https://example.test/ons",
                "sha256": "def456",
            },
        )
