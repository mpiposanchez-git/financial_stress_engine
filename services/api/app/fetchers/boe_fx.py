from __future__ import annotations

import re
from dataclasses import dataclass

import httpx

BOE_FX_URL = "https://www.bankofengland.co.uk/boeapps/database/Rates.asp"


@dataclass(frozen=True)
class BofxSnapshot:
    eur_per_gbp: float
    usd_per_gbp: float
    as_of_date: str
    source_url: str = BOE_FX_URL


def _parse_boe_fx(html: str) -> BofxSnapshot:
    eur_match = re.search(r"EUR[^0-9]*(\d+(?:\.\d+)?)", html, flags=re.IGNORECASE)
    usd_match = re.search(r"USD[^0-9]*(\d+(?:\.\d+)?)", html, flags=re.IGNORECASE)
    date_match = re.search(
        r"(\d{1,2}\s+[A-Za-z]+\s+\d{4}|\d{4}-\d{2}-\d{2})",
        html,
    )

    if eur_match is None:
        raise ValueError("Could not parse EUR rate from BoE FX source")
    if usd_match is None:
        raise ValueError("Could not parse USD rate from BoE FX source")
    if date_match is None:
        raise ValueError("Could not parse BoE FX date from source")

    return BofxSnapshot(
        eur_per_gbp=float(eur_match.group(1)),
        usd_per_gbp=float(usd_match.group(1)),
        as_of_date=date_match.group(1),
    )


def fetch_boe_fx_spot(client: httpx.Client | None = None) -> BofxSnapshot:
    if client is None:
        with httpx.Client(timeout=15.0) as managed_client:
            response = managed_client.get(BOE_FX_URL)
    else:
        response = client.get(BOE_FX_URL)

    response.raise_for_status()
    return _parse_boe_fx(response.text)
