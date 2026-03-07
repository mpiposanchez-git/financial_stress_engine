from __future__ import annotations

from pydantic import BaseModel, Field


class DataRegistryEntry(BaseModel):
    key: str
    name: str
    provider: str
    url: str
    refresh_cadence: str
    license_note: str
    verification_steps: list[str] = Field(..., min_length=1)


DATA_REGISTRY: list[DataRegistryEntry] = [
    DataRegistryEntry(
        key="boe_bank_rate",
        name="Bank of England Bank Rate",
        provider="Bank of England",
        url="https://www.bankofengland.co.uk/boeapps/database/Bank-Rate.asp",
        refresh_cadence="Daily check; publish when official rate changes",
        license_note="Source data remains subject to Bank of England terms.",
        verification_steps=[
            "Confirm statement date on the official Bank Rate page.",
            "Cross-check latest value against Bank of England publication notes.",
            "Record retrieval timestamp and URL in cache metadata.",
        ],
    ),
    DataRegistryEntry(
        key="boe_fx_spot",
        name="GBP FX Spot Snapshot (EUR/USD)",
        provider="Bank of England",
        url="https://www.bankofengland.co.uk/boeapps/database/Rates.asp",
        refresh_cadence="Daily check on UK business days",
        license_note=(
            "Indicative market rates only; not official reference rates and not transaction quotes."
        ),
        verification_steps=[
            "Confirm table date and currency pair labels on the source page.",
            "Verify GBP base alignment for EUR and USD extracts.",
            "Store source timestamp and checksum for audit traceability.",
        ],
    ),
    DataRegistryEntry(
        key="ons_cpih_12m",
        name="ONS CPIH 12-Month Rate",
        provider="Office for National Statistics",
        url="https://www.ons.gov.uk/economy/inflationandpriceindices",
        refresh_cadence="Monthly after ONS release",
        license_note="Contains public sector information licensed under OGL.",
        verification_steps=[
            "Confirm CPIH series month and annual rate from ONS publication.",
            "Cross-reference release calendar date for the dataset month.",
            "Persist source series code or table reference in metadata.",
        ],
    ),
    DataRegistryEntry(
        key="ofgem_price_cap",
        name="Ofgem Energy Price Cap Snapshot",
        provider="Ofgem",
        url="https://www.ofgem.gov.uk/information-consumers/energy-advice-households/check-if-energy-price-cap-affects-you",
        refresh_cadence="Quarterly aligned to cap update windows",
        license_note="Use for educational benchmarking only; supplier tariffs vary.",
        verification_steps=[
            "Confirm cap period start date on the official Ofgem page.",
            "Verify units and region assumptions used in snapshot extraction.",
            "Capture source URL and retrieval date in registry metadata.",
        ],
    ),
]
