"""Build truthful TPT listing images from verified CurioNest PDF renders.

The images use only pages that are actually delivered to the buyer.  Decorative
shapes and typography organize the listing; they do not replace instructional
visuals or imply editable content.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = Path(__file__).resolve().parent.parent
QUALITY_CONTRACT_PATH = REPO_ROOT / "product-lines" / "complete-unit-quality-baseline.json"
QUALITY_CONTRACT = json.loads(QUALITY_CONTRACT_PATH.read_text(encoding="utf-8"))


NAVY = "#203B4D"
ORANGE = "#C86543"
CREAM = "#F5EFE3"
WHITE = "#FFFEFA"
MUTED = "#657178"
GOLD = "#F3E1A8"
LINE = "#D7D1C6"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        Path(r"C:\Windows\Fonts\aptos-bold.ttf" if bold else r"C:\Windows\Fonts\aptos.ttf"),
        Path(r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    raise FileNotFoundError("No supported listing font was found")


def fit_page(path: Path, box: tuple[int, int, int, int]) -> tuple[Image.Image, tuple[int, int]]:
    page = Image.open(path).convert("RGB")
    page.thumbnail((box[2] - box[0], box[3] - box[1]), Image.Resampling.LANCZOS)
    x = box[0] + (box[2] - box[0] - page.width) // 2
    y = box[1] + (box[3] - box[1] - page.height) // 2
    return page, (x, y)


def paste_page(canvas: Image.Image, draw: ImageDraw.ImageDraw, path: Path, box: tuple[int, int, int, int]) -> None:
    draw.rounded_rectangle((box[0] + 12, box[1] + 12, box[2] + 12, box[3] + 12), 18, fill="#C7C1B7")
    draw.rounded_rectangle((box[0] - 8, box[1] - 8, box[2] + 8, box[3] + 8), 18, fill=WHITE, outline=LINE, width=4)
    page, position = fit_page(path, box)
    canvas.paste(page, position)


def wrapped(draw: ImageDraw.ImageDraw, text: str, xy: tuple[int, int], width: int, text_font, fill: str, spacing: int = 10) -> int:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textbbox((0, 0), trial, font=text_font)[2] <= width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    y = xy[1]
    for line in lines:
        draw.text((xy[0], y), line, font=text_font, fill=fill)
        height = draw.textbbox((0, 0), line, font=text_font)[3]
        y += height + spacing
    return y


def base(headline: str, subtitle: str) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    canvas = Image.new("RGB", (1600, 1600), CREAM)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 58, 1600), fill=NAVY)
    draw.rectangle((58, 76, 72, 268), fill=ORANGE)
    draw.text((112, 68), "CURIONEST CHEMISTRY", font=font(37, True), fill=NAVY)
    draw.text((112, 128), headline, font=font(62, True), fill=NAVY)
    draw.text((112, 220), subtitle, font=font(31, True), fill=ORANGE)
    return canvas, draw


def badge(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, width: int = 390) -> None:
    x, y = xy
    draw.rounded_rectangle((x, y, x + width, y + 84), 18, fill=WHITE, outline=LINE, width=3)
    draw.ellipse((x + 20, y + 20, x + 64, y + 64), fill=ORANGE)
    draw.text((x + 84, y + 23), text, font=font(30, True), fill=NAVY)


def footer(draw: ImageDraw.ImageDraw, copyright_line: str) -> None:
    draw.text((112, 1550), copyright_line, font=font(21), fill=MUTED)


def build(product_dir: Path, render_dir: Path | None = None) -> list[Path]:
    product = product_dir.resolve()
    data = json.loads((product / "source" / "source.json").read_text(encoding="utf-8"))
    if data.get("quality_contract_version") != QUALITY_CONTRACT["version"]:
        raise ValueError(
            f"Source quality_contract_version must be {QUALITY_CONTRACT['version']}; "
            f"found {data.get('quality_contract_version', 'missing')}"
        )
    instruction = QUALITY_CONTRACT["instruction"]
    package_contract = QUALITY_CONTRACT["package"]
    if render_dir is not None:
        render = render_dir
    else:
        final_render = product / "output" / "qa" / "final-renders" / f"{data['file_prefix']}_Complete"
        render = final_render if final_render.exists() else product / "output" / "qa" / "render-v3" / "complete"
    upload = product / "output" / "tpt-upload"
    upload.mkdir(parents=True, exist_ok=True)
    required_pages = [1, 5, 20, 31, 46]
    pages = {number: render / f"page-{number:02d}.png" for number in required_pages}
    missing = [str(path) for path in pages.values() if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing verified render(s): " + ", ".join(missing))

    outputs: list[Path] = []

    # Image 1: the real cover plus an exact inventory snapshot.
    canvas, draw = base(data["short_title"].upper(), "COMPLETE INSTRUCTIONAL UNIT · GRADES 9–10")
    paste_page(canvas, draw, pages[1], (100, 330, 950, 1460))
    draw.text((1035, 355), "WHAT IS INSIDE", font=font(30, True), fill=ORANGE)
    inventory_badges = (
        f"{instruction['lesson_count']} LESSONS",
        f"{package_contract['pages']['lesson_slides']} SLIDES",
        f"{package_contract['pages']['student_guided_notes_and_practice']} STUDENT PAGES",
        "TESTS A + B",
        "FULL RATIONALES",
    )
    for index, label in enumerate(inventory_badges):
        badge(draw, (1030, 425 + index * 132), label, width=455)
    draw.rounded_rectangle((1030, 1110, 1485, 1370), 22, fill=NAVY)
    wrapped(draw, "Teach first. Model the thinking. Practice with support. Assess after learning.", (1070, 1150), 380, font(34, True), WHITE, 12)
    draw.text((1065, 1418), "PDF ONLY · US LETTER", font=font(27, True), fill=ORANGE)
    footer(draw, data["copyright"])
    path = upload / "listing-01-cover.png"
    canvas.save(path, quality=95)
    outputs.append(path)

    # Image 2: evidence that explicit instruction precedes student practice.
    canvas, draw = base("TEACH BEFORE PRACTICE", "PROJECTABLE MODELING + GUIDED STUDENT WORK")
    paste_page(canvas, draw, pages[5], (105, 340, 1495, 865))
    draw.rounded_rectangle((105, 900, 910, 1480), 22, fill=WHITE, outline=LINE, width=4)
    paste_page(canvas, draw, pages[20], (145, 945, 565, 1435))
    draw.text((600, 970), "EACH LESSON", font=font(27, True), fill=ORANGE)
    lesson_features = ("Engage prompt", "Explicit teaching", "Worked example", "Guided practice", "Independent practice", "Exit ticket")
    y = 1035
    for feature in lesson_features:
        draw.ellipse((600, y + 8, 622, y + 30), fill=ORANGE)
        draw.text((640, y), feature, font=font(24, True), fill=NAVY)
        y += 66
    draw.rounded_rectangle((950, 900, 1495, 1480), 22, fill=GOLD)
    draw.text((995, 955), str(instruction["lesson_count"]), font=font(110, True), fill=NAVY)
    draw.text((1105, 995), "complete lessons", font=font(32, True), fill=NAVY)
    draw.text((995, 1130), str(package_contract["pages"]["lesson_slides"]), font=font(110, True), fill=NAVY)
    draw.text((1150, 1170), "teaching slides", font=font(32, True), fill=NAVY)
    wrapped(draw, "Designed for a coherent sequence—not a worksheet dropped before instruction.", (995, 1325), 440, font(26, True), NAVY, 8)
    footer(draw, data["copyright"])
    path = upload / "listing-02-teach-practice.png"
    canvas.save(path, quality=95)
    outputs.append(path)

    # Image 3: the real test and the corresponding rationale-key page.
    canvas, draw = base("ASSESS AFTER LEARNING", "TWO PARALLEL FORMS + TEACHER RATIONALES")
    draw.text((170, 324), "STUDENT TEST", font=font(27, True), fill=ORANGE)
    draw.text((985, 324), "RATIONALE KEY", font=font(27, True), fill=ORANGE)
    paste_page(canvas, draw, pages[31], (105, 380, 760, 1390))
    paste_page(canvas, draw, pages[46], (840, 380, 1495, 1390))
    draw.rounded_rectangle((105, 1425, 1495, 1515), 18, fill=NAVY)
    draw.text((160, 1450), f"TEST A + TEST B  ·  {instruction['test_items_per_form']} MULTIPLE-CHOICE ITEMS PER FORM  ·  ANSWERS EXPLAINED", font=font(27, True), fill=WHITE)
    footer(draw, data["copyright"])
    path = upload / "listing-03-assessment-key.png"
    canvas.save(path, quality=95)
    outputs.append(path)

    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("product_dir")
    parser.add_argument("--render-dir")
    args = parser.parse_args()
    paths = build(Path(args.product_dir), Path(args.render_dir) if args.render_dir else None)
    for path in paths:
        print(path)


if __name__ == "__main__":
    main()
