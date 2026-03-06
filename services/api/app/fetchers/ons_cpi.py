from __future__ import annotations

import re
from dataclasses import dataclass

import httpx

ONS_CPI_URL = "https://www.ons.gov.uk/economy/inflationandpriceindices"


@dataclass(frozen=True)
class OnsCpihSnapshot:
    measure: str
    annual_rate_percent: float
    month: str
    source_url: str = ONS_CPI_URL


def _parse_ons_cpih(html: str) -> OnsCpihSnapshot:
    match = re.search(
        r"\b(CPIH|CPI)\b[^%\n]{0,120}?(\d+(?:\.\d+)?)\s*%[^\n]{0,120}?"
        r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}",
        html,
        flags=re.IGNORECASE,
    )

    if match is None:
        raise ValueError("Could not parse ONS CPIH/CPI annual rate and month")

    measure = match.group(1).upper()
    rate = float(match.group(2))
    month_match = re.search(
        r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}",
        match.group(0),
        flags=re.IGNORECASE,
    )
    if month_match is None:
        raise ValueError("Could not parse ONS CPIH/CPI reference month")

    return OnsCpihSnapshot(
        measure=measure,
        annual_rate_percent=rate,
        month=month_match.group(0),
    )


def fetch_ons_cpih_12m(client: httpx.Client | None = None) -> OnsCpihSnapshot:
    if client is None:
        with httpx.Client(timeout=15.0) as managed_client:
            response = managed_client.get(ONS_CPI_URL)
    else:
        response = client.get(ONS_CPI_URL)

    response.raise_for_status()
    return _parse_ons_cpih(response.text)
