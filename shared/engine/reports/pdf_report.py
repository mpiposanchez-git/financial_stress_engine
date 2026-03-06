from __future__ import annotations

import io
import json

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def _draw_wrapped_text(pdf: canvas.Canvas, text: str, x: int, y: int, line_height: int = 14) -> int:
    for line in text.splitlines() or [""]:
        pdf.drawString(x, y, line)
        y -= line_height
    return y


def generate_pdf_report(
    *,
    inputs: dict[str, object],
    outputs: dict[str, object],
    disclaimers: list[str],
    provenance: dict[str, object],
    app_version: str,
) -> bytes:
    """Generate deterministic PDF bytes for report exports.

    Determinism notes:
    - page compression disabled so test can inspect heading text in bytes.
    - no generation timestamps or random IDs are embedded.
    """
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4, pageCompression=0)
    width, height = A4

    y = height - 48
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(48, y, "Financial Stress Report")

    y -= 28
    pdf.setFont("Helvetica", 11)
    pdf.drawString(48, y, f"App version: {app_version}")

    y -= 24
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(48, y, "Inputs")
    y -= 16
    pdf.setFont("Helvetica", 10)
    y = _draw_wrapped_text(pdf, json.dumps(inputs, sort_keys=True, indent=2), 48, y)

    y -= 10
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(48, y, "Outputs")
    y -= 16
    pdf.setFont("Helvetica", 10)
    y = _draw_wrapped_text(pdf, json.dumps(outputs, sort_keys=True, indent=2), 48, y)

    y -= 10
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(48, y, "Provenance")
    y -= 16
    pdf.setFont("Helvetica", 10)
    y = _draw_wrapped_text(pdf, json.dumps(provenance, sort_keys=True, indent=2), 48, y)

    y -= 10
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(48, y, "Disclaimers")
    y -= 16
    pdf.setFont("Helvetica", 10)
    for disclaimer in disclaimers:
        y = _draw_wrapped_text(pdf, f"- {disclaimer}", 48, y)

    pdf.showPage()
    pdf.save()
    return buffer.getvalue()
