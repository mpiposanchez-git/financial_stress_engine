from __future__ import annotations

import pytest

from services.api.app.data_cache import InMemoryDataCache
from services.api.app.data_fetcher import refresh_all
from services.api.app.fetchers.dwp_hbai import fetch_dwp_hbai_zip


class _MockResponse:
    def __init__(self, content: bytes, status_code: int = 200) -> None:
        self.content = content
        self.status_code = status_code

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise RuntimeError("http error")


class _MockClient:
    def __init__(self, content: bytes) -> None:
        self._content = content

    def get(self, _url: str) -> _MockResponse:
        return _MockResponse(self._content)


def test_fetch_dwp_hbai_zip_returns_raw_bytes() -> None:
    payload = b"PK\x03\x04FAKEZIP"

    snapshot = fetch_dwp_hbai_zip(client=_MockClient(payload))

    assert snapshot.zip_bytes == payload


def test_refresh_all_stores_hbai_raw_zip_in_cache() -> None:
    cache = InMemoryDataCache()

    def _fake_rate_fetcher():
        return type(
            "RateSnapshot",
            (),
            {
                "rate_percent": 4.5,
                "as_of_date": "2026-03-06",
                "source_url": "https://example.test/boe-rate",
            },
        )()

    def _fake_fx_fetcher():
        return type(
            "FxSnapshot",
            (),
            {
                "eur_per_gbp": 1.17,
                "usd_per_gbp": 1.27,
                "as_of_date": "2026-03-06",
                "source_url": "https://example.test/boe-fx",
            },
        )()

    def _fake_ons_fetcher():
        return type(
            "OnsSnapshot",
            (),
            {
                "measure": "CPIH",
                "annual_rate_percent": 3.2,
                "month": "January 2026",
                "source_url": "https://example.test/ons-cpih",
            },
        )()

    def _fake_ofgem_fetcher():
        return type(
            "OfgemSnapshot",
            (),
            {
                "region": "Great Britain",
                "annual_bill_gbp": 1834.0,
                "period_start": "1 April 2026",
                "source_url": "https://example.test/ofgem-cap",
            },
        )()

    def _fake_hbai_fetcher():
        return type(
            "HbaiSnapshot",
            (),
            {
                "zip_bytes": b"PK\x03\x04FAKEZIP",
                "source_url": "https://example.test/hbai-zip",
            },
        )()

    result = refresh_all(
        cache=cache,
        bank_rate_fetcher=_fake_rate_fetcher,
        boe_fx_fetcher=_fake_fx_fetcher,
        ons_cpi_fetcher=_fake_ons_fetcher,
        ofgem_cap_fetcher=_fake_ofgem_fetcher,
        hbai_zip_fetcher=_fake_hbai_fetcher,
    )

    entry = cache.get("dwp_hbai_zip_raw")

    assert result["updated"][-1] == "dwp_hbai_zip_raw"
    assert entry is not None
    assert entry.value == b"PK\x03\x04FAKEZIP"
    assert entry.meta.source_url == "https://example.test/hbai-zip"
    assert len(entry.meta.sha256) == 64


def test_fetch_dwp_hbai_zip_raises_on_empty_payload() -> None:
    with pytest.raises(ValueError):
        fetch_dwp_hbai_zip(client=_MockClient(b""))
