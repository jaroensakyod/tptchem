"""Create labeled contact sheets from rendered PDF page PNGs."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import argparse
import re


def natural_key(path):
    return [int(part) if part.isdigit() else part for part in re.split(r"(\d+)", path.stem)]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("render_dir")
    parser.add_argument("output_dir")
    parser.add_argument("--title", default="PDF visual QA")
    args = parser.parse_args()

    render_dir = Path(args.render_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    pages = sorted(render_dir.glob("*.png"), key=natural_key)
    font_path = Path(r"C:\Windows\Fonts\arial.ttf")
    bold_path = Path(r"C:\Windows\Fonts\arialbd.ttf")
    font = ImageFont.truetype(str(font_path), 22)
    bold = ImageFont.truetype(str(bold_path), 30)
    per_sheet = 12
    for sheet_index in range((len(pages) + per_sheet - 1) // per_sheet):
        sheet = Image.new("RGB", (1800, 2500), "#E9E6DF")
        draw = ImageDraw.Draw(sheet)
        draw.text((50, 30), f"{args.title} - sheet {sheet_index + 1}", font=bold, fill="#203B4D")
        subset = pages[sheet_index * per_sheet : (sheet_index + 1) * per_sheet]
        for i, page_path in enumerate(subset):
            row, col = divmod(i, 3)
            x, y = 45 + col * 585, 95 + row * 590
            image = Image.open(page_path).convert("RGB")
            image.thumbnail((535, 520))
            px = x + (535 - image.width) // 2
            py = y + 32 + (520 - image.height) // 2
            draw.rectangle((x - 4, y + 28, x + 539, y + 556), fill="white", outline="#BDB8AE", width=3)
            sheet.paste(image, (px, py))
            draw.text((x, y), page_path.stem, font=font, fill="#202B33")
        sheet.save(output_dir / f"contact-{sheet_index + 1:02d}.png")
    print(f"{len(pages)} pages -> {(len(pages) + per_sheet - 1) // per_sheet} contact sheets")


if __name__ == "__main__":
    main()
