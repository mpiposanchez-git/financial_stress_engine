from __future__ import annotations

import pytest

from services.api.app.data_cache import InMemoryDataCache
from services.api.app.data_fetcher import refresh_all
from services.api.app.fetchers.ofgem_cap import fetch_ofgem_price_cap


class _MockResponse:
    def __init__(self, text: str, status_code: int = 200) -> None:
        self.text = text
        self.status_code = status_code

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise RuntimeError("http error")


class _MockClient:
    def __init__(self, html: str) -> None:
        self._html = html

    def get(self, _url: str) -> _MockResponse:
        return _MockResponse(self._html)


def test_fetch_ofgem_price_cap_parses_headline_snapshot() -> None:
    html = "<html><body>Great Britain typical annual bill £1,834 from 1 April 2026.</body></html>"

    snapshot = fetch_ofgem_price_cap(client=_MockClient(html))

    assert snapshot.region == "Great Britain"
    assert snapshot.annual_bill_gbp == 1834.0
    assert snapshot.period_start == "1 April 2026"


def test_refresh_all_stores_ofgem_snapshot_in_cache() -> None:
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

    result = refresh_all(
        cache=cache,
        bank_rate_fetcher=_fake_rate_fetcher,
        boe_fx_fetcher=_fake_fx_fetcher,
        ons_cpi_fetcher=_fake_ons_fetcher,
        ofgem_cap_fetcher=_fake_ofgem_fetcher,
    )

    entry = cache.get("ofgem_price_cap")

    assert result["updated"][-1] == "ofgem_price_cap"
    assert entry is not None
    assert entry.value == {
        "region": "Great Britain",
        "annual_bill_gbp": 1834.0,
        "period_start": "1 April 2026",
    }
    assert entry.meta.source_url == "https://example.test/ofgem-cap"
    assert len(entry.meta.sha256) == 64


def test_fetch_ofgem_price_cap_raises_when_missing_fields() -> None:
    html = "<html><body>No cap info present.</body></html>"

    with pytest.raises(ValueError):
        fetch_ofgem_price_cap(client=_MockClient(html))
