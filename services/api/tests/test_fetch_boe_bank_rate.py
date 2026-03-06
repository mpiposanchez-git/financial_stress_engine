from __future__ import annotations

import pytest

from services.api.app.data_cache import InMemoryDataCache
from services.api.app.data_fetcher import refresh_all
from services.api.app.fetchers.boe_bank_rate import fetch_boe_bank_rate


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


def test_fetch_boe_bank_rate_parses_latest_value_and_date() -> None:
    html = "<html><body>Bank Rate currently 4.75% effective 06 March 2026.</body></html>"

    snapshot = fetch_boe_bank_rate(client=_MockClient(html))

    assert snapshot.rate_percent == 4.75
    assert snapshot.as_of_date == "06 March 2026"


def test_refresh_all_stores_boe_bank_rate_in_cache() -> None:
    cache = InMemoryDataCache()

    def _fake_fetcher():
        return type(
            "Snapshot",
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
                "annual_rate_percent": 3.1,
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
        bank_rate_fetcher=_fake_fetcher,
        boe_fx_fetcher=_fake_fx_fetcher,
        ons_cpi_fetcher=_fake_ons_fetcher,
        ofgem_cap_fetcher=_fake_ofgem_fetcher,
    )
    entry = cache.get("boe_bank_rate")

    assert result == {
        "updated": ["boe_bank_rate", "boe_fx_spot", "ons_cpih_12m", "ofgem_price_cap"]
    }
    assert entry is not None
    assert entry.value == {"rate_percent": 4.5, "as_of_date": "2026-03-06"}
    assert entry.meta.source_url == "https://example.test/boe-rate"
    assert len(entry.meta.sha256) == 64


def test_fetch_boe_bank_rate_raises_when_missing_rate_or_date() -> None:
    html = "<html><body>No parsable content.</body></html>"

    with pytest.raises(ValueError):
        fetch_boe_bank_rate(client=_MockClient(html))
