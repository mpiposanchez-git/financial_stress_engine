from __future__ import annotations

from services.api.app.data_cache import DATA_CACHE, InMemoryDataCache

HBAI_SOURCE_URL = "https://www.gov.uk/government/statistics/households-below-average-income-for-financial-years-ending-1995-to-2024"
HBAI_CACHE_KEY = "dwp_hbai_zip_raw"


def get_uk_reference_values(cache: InMemoryDataCache = DATA_CACHE) -> dict[str, object]:
    """Return UK benchmark reference values with provenance metadata.

    WS7-A02-01 ships a static placeholder median until WS7-A02-02 parses HBAI tables.
    """
    hbai_entry = cache.get(HBAI_CACHE_KEY)

    source_url = HBAI_SOURCE_URL
    fetched_at_utc: str | None = None
    sha256: str | None = None

    if hbai_entry is not None:
        source_url = hbai_entry.meta.source_url
        fetched_at_utc = hbai_entry.meta.fetched_at_utc
        sha256 = hbai_entry.meta.sha256

    return {
        "income_median_bhc": {
            "year_label": "FY2024 (placeholder)",
            "amount_gbp": 35000.0,
        },
        "income_deciles_bhc_gbp": None,
        "provenance": {
            "dataset_key": HBAI_CACHE_KEY,
            "source_url": source_url,
            "fetched_at_utc": fetched_at_utc,
            "sha256": sha256,
            "status": "placeholder_until_hbai_parser",
        },
    }
