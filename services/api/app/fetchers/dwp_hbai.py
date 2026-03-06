from __future__ import annotations

from dataclasses import dataclass

import httpx

DWP_HBAI_ZIP_URL = "https://www.gov.uk/government/statistics/households-below-average-income-for-financial-years-ending-1995-to-2024"


@dataclass(frozen=True)
class DwpHbaiZipSnapshot:
    zip_bytes: bytes
    source_url: str = DWP_HBAI_ZIP_URL


def fetch_dwp_hbai_zip(client: httpx.Client | None = None) -> DwpHbaiZipSnapshot:
    if client is None:
        with httpx.Client(timeout=30.0) as managed_client:
            response = managed_client.get(DWP_HBAI_ZIP_URL)
    else:
        response = client.get(DWP_HBAI_ZIP_URL)

    response.raise_for_status()
    if not response.content:
        raise ValueError("Downloaded HBAI ZIP payload is empty")

    return DwpHbaiZipSnapshot(zip_bytes=response.content)
