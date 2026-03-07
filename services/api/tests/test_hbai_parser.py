from __future__ import annotations

import io
import zipfile

import pytest

from shared.engine.benchmarks.hbai_parser import parse_bhc_decile_thresholds_from_hbai_zip


def _build_synthetic_ods_content(values: list[int]) -> bytes:
    numbers = " ".join(str(value) for value in values)
    content_xml = "".join(
        [
            "<office:document-content>",
            "<table:table table:name='BHC deciles'>",
            "<table:table-row><table:table-cell office:value-type='string'>",
            "BHC</table:table-cell></table:table-row>",
            "<table:table-row><table:table-cell office:value-type='float'>",
            f"{numbers}</table:table-cell></table:table-row>",
            "</table:table></office:document-content>",
        ]
    )

    ods_buffer = io.BytesIO()
    with zipfile.ZipFile(ods_buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as ods_zip:
        ods_zip.writestr("content.xml", content_xml)
    return ods_buffer.getvalue()


def _build_hbai_zip_with_ods(ods_bytes: bytes) -> bytes:
    hbai_buffer = io.BytesIO()
    with zipfile.ZipFile(hbai_buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as hbai_zip:
        hbai_zip.writestr("tables/hbai_tables.ods", ods_bytes)
    return hbai_buffer.getvalue()


def test_parse_bhc_deciles_from_synthetic_hbai_zip() -> None:
    expected = [10000, 13000, 16000, 19000, 22000, 26000, 30000, 36000, 45000]
    ods_bytes = _build_synthetic_ods_content(expected)
    hbai_zip_bytes = _build_hbai_zip_with_ods(ods_bytes)

    parsed = parse_bhc_decile_thresholds_from_hbai_zip(hbai_zip_bytes)

    assert parsed == [float(value) for value in expected]


def test_parse_bhc_deciles_raises_when_ods_missing() -> None:
    hbai_buffer = io.BytesIO()
    with zipfile.ZipFile(hbai_buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as hbai_zip:
        hbai_zip.writestr("readme.txt", "no ods here")

    with pytest.raises(ValueError, match="No ODS file"):
        parse_bhc_decile_thresholds_from_hbai_zip(hbai_buffer.getvalue())
