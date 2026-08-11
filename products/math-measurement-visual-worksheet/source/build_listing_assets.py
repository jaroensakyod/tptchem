"""Create TPT listing images from final rendered pages and licensed assets."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter


HERE = Path(__file__).resolve().parent
PRODUCT = HERE.parent
ASSETS = PRODUCT / "assets"
OUT = PRODUCT / "output"
UPLOAD = OUT / "tpt-upload"
COMPLETE = OUT / "qa" / "pdf" / "complete"

NAVY = "#203B4D"
ORANGE = "#C86543"
OCHRE = "#DDB75F"
CREAM = "#F5EFE3"
WHITE = "#FFFEFA"
INK = "#202B33"
MUTED = "#6D7478"

FONT_REGULAR = r"C:\Windows\Fonts\aptos.ttf"
FONT_BOLD = r"C:\Windows\Fonts\aptos-bold.ttf"
if not Path(FONT_REGULAR).exists():
    FONT_REGULAR = r"C:\Windows\Fonts\arial.ttf"
if not Path(FONT_BOLD).exists():
    FONT_BOLD = r"C:\Windows\Fonts\arialbd.ttf"


def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REGULAR, size)


def multiline(draw, xy, text, size, fill, width, spacing=10, bold=False):
    words = text.split()
    lines = []
    current = ""
    f = font(size, bold)
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textbbox((0, 0), trial, font=f)[2] <= width:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    draw.multiline_text(xy, "\n".join(lines), font=f, fill=fill, spacing=spacing)
    return lines


def add_page_mockup(canvas, page_path, box, angle=0):
    x, y, w, h = box
    page = Image.open(page_path).convert("RGB")
    page.thumbnail((w, h), Image.Resampling.LANCZOS)
    shadow = Image.new("RGBA", (page.width + 34, page.height + 34), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle((18, 18, page.width + 18, page.height + 18), 10, fill=(0, 0, 0, 90))
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    layer = Image.new("RGBA", shadow.size, (0, 0, 0, 0))
    layer.alpha_composite(shadow)
    layer.paste(page, (0, 0))
    if angle:
        layer = layer.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    canvas.alpha_composite(layer, (x, y))


def cover():
    canvas = Image.new("RGB", (2000, 2000), CREAM)
    d = ImageDraw.Draw(canvas)
    d.rectangle((0, 0, 150, 2000), fill=NAVY)
    d.rectangle((150, 235, 185, 680), fill=ORANGE)
    d.text((255, 185), "CURIONEST", font=font(72, True), fill=NAVY)
    multiline(d, (255, 370), "CHEMISTRY MEASUREMENT", 112, NAVY, 1010, 20, True)
    multiline(d, (255, 700), "LAB TOOLS • DENSITY • PERCENT ERROR", 58, ORANGE, 1010, 12, True)
    multiline(d, (255, 930), "Visual worksheet for U.S. Grades 8-10", 45, MUTED, 980, 8)
    photo = Image.open(ASSETS / "graduated-cylinder-public-domain.jpg").convert("RGB")
    photo.thumbnail((390, 1050), Image.Resampling.LANCZOS)
    frame = Image.new("RGB", (470, 1190), WHITE)
    fx = (frame.width - photo.width) // 2
    fy = (frame.height - photo.height) // 2
    frame.paste(photo, (fx, fy))
    canvas.paste(frame, (1420, 185))
    d.rounded_rectangle((255, 1220, 1270, 1580), 28, fill=WHITE)
    bullets = ["4 student pages", "full teacher key", "editable DOCX", "rights-cleared visuals"]
    y = 1285
    for text in bullets:
        d.ellipse((300, y + 12, 324, y + 36), fill=ORANGE)
        d.text((350, y), text, font=font(46, True), fill=INK)
        y += 75
    d.rounded_rectangle((255, 1680, 1885, 1855), 28, fill=NAVY)
    d.text((395, 1725), "PRINT-READY • US LETTER", font=font(60, True), fill=WHITE)
    canvas.resize((1200, 1200), Image.Resampling.LANCZOS).save(UPLOAD / "cover.png", quality=95)


def inside():
    canvas = Image.new("RGBA", (2000, 2000), NAVY)
    d = ImageDraw.Draw(canvas)
    d.text((120, 110), "VISUAL PRACTICE THAT TEACHES", font=font(70, True), fill=WHITE)
    d.text((120, 205), "Students use the images as evidence - not decoration.", font=font(38), fill=OCHRE)
    add_page_mockup(canvas, COMPLETE / "page-03.png", (125, 360, 760, 1200), angle=-2)
    add_page_mockup(canvas, COMPLETE / "page-04.png", (1030, 360, 760, 1200), angle=2)
    d.rounded_rectangle((120, 1650, 1880, 1875), 24, fill=CREAM)
    d.text((185, 1705), "TOOLS • UNITS • CHOICE • VISUAL EVIDENCE", font=font(54, True), fill=NAVY)
    d.text((315, 1790), "35-45 minutes • U.S. Grades 8-10", font=font(40), fill=ORANGE)
    canvas.convert("RGB").save(UPLOAD / "listing-02-inside.png", quality=95)


def teacher_ready():
    canvas = Image.new("RGBA", (2000, 2000), CREAM)
    d = ImageDraw.Draw(canvas)
    d.text((120, 105), "STUDENT + TEACHER READY", font=font(76, True), fill=NAVY)
    d.text((120, 210), "Dedicated answer areas - no writing lines behind answers.", font=font(39), fill=ORANGE)
    add_page_mockup(canvas, COMPLETE / "page-05.png", (115, 360, 760, 1170), angle=-2)
    add_page_mockup(canvas, COMPLETE / "page-09.png", (1025, 360, 760, 1170), angle=2)
    d.rounded_rectangle((115, 1640, 1885, 1880), 24, fill=NAVY)
    labels = ["FULL KEY", "TEACHER GUIDE", "EDITABLE DOCX", "SOURCE CREDITS"]
    x = 175
    for label in labels:
        d.rounded_rectangle((x, 1710, x + 360, 1815), 18, fill=WHITE)
        tw = d.textbbox((0, 0), label, font=font(34, True))[2]
        d.text((x + (360 - tw) / 2, 1740), label, font=font(34, True), fill=NAVY)
        x += 420
    canvas.convert("RGB").save(UPLOAD / "listing-03-teacher-ready.png", quality=95)


def contact_sheet():
    pages = sorted(COMPLETE.glob("page-*.png"))
    thumb_w, thumb_h = 330, 427
    cols = 3
    rows = (len(pages) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 370, rows * 475), "#ECE9E2")
    d = ImageDraw.Draw(sheet)
    for index, path in enumerate(pages):
        image = Image.open(path).convert("RGB")
        image.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        col, row = index % cols, index // cols
        x, y = col * 370 + 20, row * 475 + 25
        sheet.paste(image, (x, y))
        d.text((x, y + image.height + 6), f"Page {index + 1}", font=font(18, True), fill=INK)
    sheet.save(OUT / "qa" / "complete-contact-sheet.png", quality=92)


def main():
    UPLOAD.mkdir(parents=True, exist_ok=True)
    cover()
    inside()
    teacher_ready()
    contact_sheet()


if __name__ == "__main__":
    main()
