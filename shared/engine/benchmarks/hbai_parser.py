from __future__ import annotations

import io
import re
import zipfile


def _extract_first_ods_bytes(hbai_zip_bytes: bytes) -> bytes:
    with zipfile.ZipFile(io.BytesIO(hbai_zip_bytes)) as hbai_zip:
        ods_candidates = [name for name in hbai_zip.namelist() if name.lower().endswith(".ods")]
        if not ods_candidates:
            raise ValueError("No ODS file found in HBAI ZIP payload")
        return hbai_zip.read(ods_candidates[0])


def _extract_content_xml(ods_bytes: bytes) -> str:
    with zipfile.ZipFile(io.BytesIO(ods_bytes)) as ods_zip:
        try:
            content = ods_zip.read("content.xml")
        except KeyError as exc:
            raise ValueError("ODS payload missing content.xml") from exc
    return content.decode("utf-8", errors="ignore")


def parse_bhc_decile_thresholds_from_hbai_zip(hbai_zip_bytes: bytes) -> list[float]:
    """Extract a POC BHC decile-threshold series from raw HBAI ZIP bytes.

    The parser currently uses a heuristic over ODS content XML and returns the
    first nine non-negative ascending numeric values in a plausible income range.
    """
    ods_bytes = _extract_first_ods_bytes(hbai_zip_bytes)
    content_xml = _extract_content_xml(ods_bytes)

    number_matches = re.findall(r"[-+]?\d+(?:\.\d+)?", content_xml)
    values: list[float] = []
    for match in number_matches:
        value = float(match)
        if 0 <= value <= 1_000_000:
            values.append(value)

    if len(values) < 9:
        raise ValueError("Could not extract enough numeric candidates from HBAI ODS content")

    # Build the first strictly non-decreasing 9-value window.
    for idx in range(0, len(values) - 8):
        window = values[idx : idx + 9]
        if all(window[i] <= window[i + 1] for i in range(8)):
            return window

    raise ValueError("Could not identify ordered BHC decile thresholds in ODS content")
