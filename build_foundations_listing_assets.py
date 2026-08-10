#!/usr/bin/env python3
"""Build square TPT listing images from the latest Chemistry Foundations PDF."""

from __future__ import annotations

from pathlib import Path

import pymupdf as fitz
from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent
PRODUCT_DIR = ROOT / "products" / "chemistry-foundations-pilot"
PDF_PATH = PRODUCT_DIR / "product.pdf"

NAVY = "#0B1F3A"
TEAL = "#148C7E"
TEAL_DARK = "#0F6D63"
INK = "#243447"
PALE = "#F5F8FA"
LIGHT = "#EAF7F4"
AMBER_PALE = "#FFF4E8"
AMBER = "#F4A261"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    path = Path(r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf")
    return ImageFont.truetype(str(path), size)


def render_page(document: fitz.Document, page_index: int, width: int) -> Image.Image:
    page = document.load_page(page_index)
    scale = width / page.rect.width
    pixmap = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
    return Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)


def paste_page(canvas: Image.Image, page: Image.Image, box: tuple[int, int, int, int]) -> None:
    x1, y1, x2, y2 = box
    page.thumbnail((x2 - x1, y2 - y1), Image.Resampling.LANCZOS)
    x = x1 + (x2 - x1 - page.width) // 2
    y = y1 + (y2 - y1 - page.height) // 2
    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rectangle((x + 12, y + 12, x + page.width + 12, y + page.height + 12), fill=(18, 35, 55, 55))
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    canvas.paste(shadow, (0, 0), shadow)
    canvas.paste(page, (x, y))


def build_student_image(document: fitz.Document) -> None:
    canvas = Image.new("RGBA", (1800, 1800), PALE)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 1800, 310), fill=NAVY)
    draw.text((90, 78), "SEE WHAT STUDENTS ACTUALLY DO", font=font(66, True), fill="white")
    draw.text((92, 198), "Functional classroom visuals with traceable sources", font=font(31), fill="#DCE8F2")

    page_indices = [3, 4, 6, 11]
    x_positions = [55, 465, 875, 1285]
    for index, x in zip(page_indices, x_positions):
        paste_page(canvas, render_page(document, index, 430), (x, 420, x + 360, 1110))

    draw.rounded_rectangle((70, 1280, 1730, 1710), radius=36, fill=LIGHT, outline=TEAL, width=5)
    labels = [
        "Scenario-based safety",
        "Official GHS symbols",
        "Sourced equipment visuals",
        "Meniscus + precision",
    ]
    starts = [120, 530, 940, 1350]
    for label, x in zip(labels, starts):
        draw.ellipse((x, 1370, x + 30, 1400), fill=TEAL)
        draw.text((x + 47, 1357), label, font=font(25, True), fill=NAVY)
    draw.text((900, 1608), "PRINT-READY | US LETTER | GRADES 9-11", font=font(31, True), fill=TEAL_DARK, anchor="mm")
    canvas.convert("RGB").save(PRODUCT_DIR / "listing-02-inside.png", quality=95)


def build_teacher_image(document: fitz.Document) -> None:
    canvas = Image.new("RGBA", (1800, 1800), PALE)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 1800, 300), fill=NAVY)
    draw.text((90, 62), "TEACHER-READY FROM DAY ONE", font=font(64, True), fill="white")
    draw.text((92, 181), "Plan it, teach it, assess it, and give feedback", font=font(31), fill="#DCE8F2")

    page_indices = [1, 14, 17]
    x_positions = [80, 650, 1220]
    labels = ["TEACHER GUIDE", "PRACTICAL + RUBRIC", "FULL ANSWER KEY"]
    for index, x, label in zip(page_indices, x_positions, labels):
        paste_page(canvas, render_page(document, index, 500), (x, 355, x + 500, 1105))
        draw.rounded_rectangle((x + 20, 1145, x + 480, 1235), radius=22, fill=NAVY)
        draw.text((x + 250, 1190), label, font=font(25, True), fill="white", anchor="mm")

    draw.rounded_rectangle((70, 1350, 1730, 1715), radius=36, fill=AMBER_PALE, outline=AMBER, width=5)
    draw.text((120, 1410), "INCLUDED:", font=font(29, True), fill="#C44536")
    draw.text((120, 1480), "3-5 day pacing | differentiation | station setup | quiz | scoring notes", font=font(27), fill=INK)
    draw.text((120, 1555), "Student-only packet included for easy printing", font=font(28, True), fill=NAVY)
    draw.text((120, 1630), "Editable DOCX + full PDF + watermarked preview", font=font(25), fill=TEAL_DARK)
    canvas.convert("RGB").save(PRODUCT_DIR / "listing-03-teacher-ready.png", quality=95)


def main() -> None:
    if not PDF_PATH.exists():
        raise SystemExit(f"Missing PDF: {PDF_PATH}")
    document = fitz.open(PDF_PATH)
    try:
        build_student_image(document)
        build_teacher_image(document)
    finally:
        document.close()
    print(PRODUCT_DIR / "listing-02-inside.png")
    print(PRODUCT_DIR / "listing-03-teacher-ready.png")


if __name__ == "__main__":
    main()
