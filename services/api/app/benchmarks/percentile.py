from __future__ import annotations

from services.api.app.benchmarks.reference_values import get_uk_reference_values
from shared.engine.benchmarks.income_percentile import compute_percentile_bucket

DEFAULT_DECILES_BHC_GBP = [
    12000.0,
    15500.0,
    19000.0,
    23000.0,
    28000.0,
    34000.0,
    42000.0,
    55000.0,
    80000.0,
]


def compute_uk_income_percentile(
    *, annual_net_income_reporting_currency: float, reporting_currency: str
) -> dict[str, object]:
    reference = get_uk_reference_values()
    year_label = str(reference["income_median_bhc"]["year_label"])

    percentile_bucket = compute_percentile_bucket(
        annual_income_gbp=annual_net_income_reporting_currency,
        decile_thresholds_gbp=DEFAULT_DECILES_BHC_GBP,
    )

    return {
        "percentile_bucket": percentile_bucket,
        "year_label": year_label,
        "reporting_currency": reporting_currency,
        "thresholds_gbp": DEFAULT_DECILES_BHC_GBP,
        "caveats": [
            "Percentile result is an indicative benchmark and not financial advice.",
            "POC currently uses placeholder decile thresholds until HBAI parsed deciles are wired.",
            "Interpret with caution across differing household compositions and regions.",
        ],
    }
