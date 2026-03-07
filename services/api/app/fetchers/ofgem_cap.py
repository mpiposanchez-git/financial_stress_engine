from __future__ import annotations

import re
from dataclasses import dataclass

import httpx

OFGEM_CAP_URL = "https://www.ofgem.gov.uk/information-consumers/energy-advice-households/check-if-energy-price-cap-affects-you"


@dataclass(frozen=True)
class OfgemCapSnapshot:
    region: str
    annual_bill_gbp: float
    period_start: str
    source_url: str = OFGEM_CAP_URL


def _parse_ofgem_cap(html: str) -> OfgemCapSnapshot:
    region_match = re.search(r"\b(Great Britain|England|Scotland|Wales|London)\b", html)
    cap_match = re.search(r"£\s*([\d,]+(?:\.\d{1,2})?)", html)
    date_match = re.search(
        r"(\d{1,2}\s+"
        r"(?:January|February|March|April|May|June|July|August|September|October|November|December)"
        r"\s+\d{4})",
        html,
        flags=re.IGNORECASE,
    )

    if region_match is None:
        raise ValueError("Could not parse Ofgem price cap region")
    if cap_match is None:
        raise ValueError("Could not parse Ofgem annual bill cap value")
    if date_match is None:
        raise ValueError("Could not parse Ofgem price cap period start date")

    return OfgemCapSnapshot(
        region=region_match.group(1),
        annual_bill_gbp=float(cap_match.group(1).replace(",", "")),
        period_start=date_match.group(1),
    )


def fetch_ofgem_price_cap(client: httpx.Client | None = None) -> OfgemCapSnapshot:
    if client is None:
        with httpx.Client(timeout=15.0) as managed_client:
            response = managed_client.get(OFGEM_CAP_URL)
    else:
        response = client.get(OFGEM_CAP_URL)

    response.raise_for_status()
    return _parse_ofgem_cap(response.text)
