from __future__ import annotations

import pytest

from services.api.app.data_cache import InMemoryDataCache
from services.api.app.data_fetcher import refresh_all
from services.api.app.fetchers.boe_fx import fetch_boe_fx_spot


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


def test_fetch_boe_fx_spot_parses_eur_usd_and_date() -> None:
    html = "<html><body>EUR 1.1702 USD 1.2710 rates as of 2026-03-06</body></html>"

    snapshot = fetch_boe_fx_spot(client=_MockClient(html))

    assert snapshot.eur_per_gbp == 1.1702
    assert snapshot.usd_per_gbp == 1.271
    assert snapshot.as_of_date == "2026-03-06"


def test_refresh_all_stores_boe_fx_spot_in_cache() -> None:
    cache = InMemoryDataCache()

    def _fake_bank_rate_fetcher():
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

    def _fake_hbai_fetcher():
        return type(
            "HbaiSnapshot",
            (),
            {
                "zip_bytes": b"PK\\x03\\x04FAKEZIP",
                "source_url": "https://example.test/hbai-zip",
            },
        )()

    refresh_all(
        cache=cache,
        bank_rate_fetcher=_fake_bank_rate_fetcher,
        boe_fx_fetcher=_fake_fx_fetcher,
        ons_cpi_fetcher=_fake_ons_fetcher,
        ofgem_cap_fetcher=_fake_ofgem_fetcher,
        hbai_zip_fetcher=_fake_hbai_fetcher,
    )

    entry = cache.get("boe_fx_spot")

    assert entry is not None
    assert entry.value["base_currency"] == "GBP"
    assert entry.value["eur"] == 1.17
    assert entry.value["usd"] == 1.27
    assert entry.value["indicative_only"] is True
    assert entry.meta.source_url == "https://example.test/boe-fx"
    assert len(entry.meta.sha256) == 64


def test_fetch_boe_fx_spot_raises_when_currency_missing() -> None:
    html = "<html><body>USD 1.2710 rates as of 2026-03-06</body></html>"

    with pytest.raises(ValueError):
        fetch_boe_fx_spot(client=_MockClient(html))
