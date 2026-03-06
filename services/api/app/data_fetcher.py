from __future__ import annotations

import argparse
import hashlib
import json
from collections.abc import Callable
from datetime import UTC, datetime

from .data_cache import DATA_CACHE, CacheMeta, InMemoryDataCache
from .fetchers.boe_bank_rate import BankRateSnapshot, fetch_boe_bank_rate
from .fetchers.boe_fx import BofxSnapshot, fetch_boe_fx_spot
from .fetchers.dwp_hbai import DwpHbaiZipSnapshot, fetch_dwp_hbai_zip
from .fetchers.ofgem_cap import OfgemCapSnapshot, fetch_ofgem_price_cap
from .fetchers.ons_cpi import OnsCpihSnapshot, fetch_ons_cpih_12m


def _utc_now_iso() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def refresh_all(
    *,
    cache: InMemoryDataCache = DATA_CACHE,
    bank_rate_fetcher: Callable[[], BankRateSnapshot] = fetch_boe_bank_rate,
    boe_fx_fetcher: Callable[[], BofxSnapshot] = fetch_boe_fx_spot,
    ons_cpi_fetcher: Callable[[], OnsCpihSnapshot] = fetch_ons_cpih_12m,
    ofgem_cap_fetcher: Callable[[], OfgemCapSnapshot] = fetch_ofgem_price_cap,
    hbai_zip_fetcher: Callable[[], DwpHbaiZipSnapshot] = fetch_dwp_hbai_zip,
) -> dict[str, object]:
    bank_rate = bank_rate_fetcher()

    value = {
        "rate_percent": bank_rate.rate_percent,
        "as_of_date": bank_rate.as_of_date,
    }
    sha256 = hashlib.sha256(json.dumps(value, sort_keys=True).encode("utf-8")).hexdigest()

    cache.set(
        "boe_bank_rate",
        value,
        CacheMeta(
            fetched_at_utc=_utc_now_iso(),
            source_url=bank_rate.source_url,
            sha256=sha256,
        ),
    )

    boe_fx = boe_fx_fetcher()
    fx_value = {
        "base_currency": "GBP",
        "eur": boe_fx.eur_per_gbp,
        "usd": boe_fx.usd_per_gbp,
        "as_of_date": boe_fx.as_of_date,
        "indicative_only": True,
    }
    fx_sha256 = hashlib.sha256(json.dumps(fx_value, sort_keys=True).encode("utf-8")).hexdigest()

    cache.set(
        "boe_fx_spot",
        fx_value,
        CacheMeta(
            fetched_at_utc=_utc_now_iso(),
            source_url=boe_fx.source_url,
            sha256=fx_sha256,
        ),
    )

    ons_cpi = ons_cpi_fetcher()
    ons_value = {
        "measure": ons_cpi.measure,
        "annual_rate_percent": ons_cpi.annual_rate_percent,
        "month": ons_cpi.month,
    }
    ons_sha256 = hashlib.sha256(json.dumps(ons_value, sort_keys=True).encode("utf-8")).hexdigest()

    cache.set(
        "ons_cpih_12m",
        ons_value,
        CacheMeta(
            fetched_at_utc=_utc_now_iso(),
            source_url=ons_cpi.source_url,
            sha256=ons_sha256,
        ),
    )

    ofgem_cap = ofgem_cap_fetcher()
    ofgem_value = {
        "region": ofgem_cap.region,
        "annual_bill_gbp": ofgem_cap.annual_bill_gbp,
        "period_start": ofgem_cap.period_start,
    }
    ofgem_sha256 = hashlib.sha256(
        json.dumps(ofgem_value, sort_keys=True).encode("utf-8")
    ).hexdigest()

    cache.set(
        "ofgem_price_cap",
        ofgem_value,
        CacheMeta(
            fetched_at_utc=_utc_now_iso(),
            source_url=ofgem_cap.source_url,
            sha256=ofgem_sha256,
        ),
    )

    hbai_zip = hbai_zip_fetcher()
    hbai_sha256 = hashlib.sha256(hbai_zip.zip_bytes).hexdigest()

    cache.set(
        "dwp_hbai_zip_raw",
        hbai_zip.zip_bytes,
        CacheMeta(
            fetched_at_utc=_utc_now_iso(),
            source_url=hbai_zip.source_url,
            sha256=hbai_sha256,
        ),
    )

    return {
        "updated": [
            "boe_bank_rate",
            "boe_fx_spot",
            "ons_cpih_12m",
            "ofgem_price_cap",
            "dwp_hbai_zip_raw",
        ]
    }


def _build_cli_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Data refresh utilities")
    subcommands = parser.add_subparsers(dest="command", required=True)
    subcommands.add_parser("refresh-all", help="Refresh and cache all external datasets")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_cli_parser()
    args = parser.parse_args(argv)

    if args.command == "refresh-all":
        result = refresh_all()
        print(json.dumps(result, sort_keys=True))
        return 0

    parser.error("Unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
