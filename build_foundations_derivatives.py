#!/usr/bin/env python3
"""Create student-only and watermarked preview PDFs from the pilot product PDF."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen.canvas import Canvas


ROOT = Path(__file__).resolve().parent
PRODUCT_DIR = ROOT / "products" / "chemistry-foundations-pilot"
SOURCE = PRODUCT_DIR / "product.pdf"

# PDF page indices are zero-based. Keep all student pages and assessments while
# excluding the cover, teacher guide/setup pages, and answer keys.
STUDENT_PAGES = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16]

# Listing preview: cover, teacher support, three representative student visuals,
# measurement practice, practical rubric, and an answer-key sample.
PREVIEW_PAGES = [0, 1, 3, 4, 6, 11, 14, 17]


def write_selected(indices: list[int], destination: Path, watermark: bool = False) -> None:
    reader = PdfReader(str(SOURCE))
    writer = PdfWriter()
    for index in indices:
        page = reader.pages[index]
        if watermark:
            width = float(page.mediabox.width)
            height = float(page.mediabox.height)
            stream = BytesIO()
            canvas = Canvas(stream, pagesize=(width, height))
            canvas.saveState()
            canvas.setFillColorRGB(0.72, 0.76, 0.80)
            if hasattr(canvas, "setFillAlpha"):
                canvas.setFillAlpha(0.55)
            canvas.setFont("Helvetica-Bold", 20)
            canvas.translate(width - 12, height / 2)
            canvas.rotate(90)
            canvas.drawCentredString(0, 0, "CURIONEST PREVIEW")
            canvas.restoreState()
            canvas.save()
            stream.seek(0)
            page.merge_page(PdfReader(stream).pages[0])
        writer.add_page(page)

    temporary = destination.with_suffix(destination.suffix + ".tmp")
    with temporary.open("wb") as handle:
        writer.write(handle)
    temporary.replace(destination)


def main() -> None:
    if not SOURCE.exists():
        raise SystemExit(f"Missing product PDF: {SOURCE}")
    write_selected(STUDENT_PAGES, PRODUCT_DIR / "student-packet.pdf")
    write_selected(PREVIEW_PAGES, PRODUCT_DIR / "preview.pdf", watermark=True)
    print(PRODUCT_DIR / "student-packet.pdf")
    print(PRODUCT_DIR / "preview.pdf")


if __name__ == "__main__":
    main()
