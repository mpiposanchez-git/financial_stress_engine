from __future__ import annotations

import re
from dataclasses import dataclass

import httpx

BOE_BANK_RATE_URL = "https://www.bankofengland.co.uk/boeapps/database/Bank-Rate.asp"


@dataclass(frozen=True)
class BankRateSnapshot:
    rate_percent: float
    as_of_date: str
    source_url: str = BOE_BANK_RATE_URL


def _parse_bank_rate(html: str) -> BankRateSnapshot:
    rate_match = re.search(r"(\d+(?:\.\d+)?)\s*%", html)
    date_match = re.search(
        r"(\d{1,2}\s+[A-Za-z]+\s+\d{4}|\d{4}-\d{2}-\d{2})",
        html,
    )

    if rate_match is None:
        raise ValueError("Could not parse Bank Rate value from source")
    if date_match is None:
        raise ValueError("Could not parse Bank Rate date from source")

    return BankRateSnapshot(
        rate_percent=float(rate_match.group(1)),
        as_of_date=date_match.group(1),
    )


def fetch_boe_bank_rate(client: httpx.Client | None = None) -> BankRateSnapshot:
    if client is None:
        with httpx.Client(timeout=15.0) as managed_client:
            response = managed_client.get(BOE_BANK_RATE_URL)
    else:
        response = client.get(BOE_BANK_RATE_URL)

    response.raise_for_status()
    return _parse_bank_rate(response.text)
