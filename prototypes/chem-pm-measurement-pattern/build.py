"""Build a four-page CurioNest measurement worksheet pattern proof."""

from pathlib import Path
import json

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ASSETS = HERE / "assets"
OUTPUT = HERE / "output" / "pdf"
DATA = json.loads((HERE / "source.json").read_text(encoding="utf-8"))

PAGE_W, PAGE_H = A4
MM = 72 / 25.4
MARGIN = 15 * MM

INK = HexColor("#202B33")
NAVY = HexColor("#203B4D")
ORANGE = HexColor("#C86543")
OCHRE = HexColor("#DDB75F")
WHITE = HexColor("#FFFEFA")
WASH = HexColor("#F8F5EE")
CREAM = HexColor("#F5EFE3")
NOTE = HexColor("#F3E5BD")
MUTED = HexColor("#6D7478")

FONT_REGULAR = "TahomaThai"
FONT_BOLD = "TahomaThai-Bold"
pdfmetrics.registerFont(TTFont(FONT_REGULAR, r"C:\Windows\Fonts\Tahoma.ttf"))
pdfmetrics.registerFont(TTFont(FONT_BOLD, r"C:\Windows\Fonts\Tahomabd.ttf"))


def style(name, size=10.2, leading=None, color=INK, bold=False, align=TA_LEFT):
    return ParagraphStyle(
        name,
        fontName=FONT_BOLD if bold else FONT_REGULAR,
        fontSize=size,
        leading=leading or size * 1.35,
        textColor=color,
        alignment=align,
        wordWrap="CJK",
        spaceAfter=0,
    )


BODY = style("body", 10.2)
SMALL = style("small", 8.0, color=MUTED)
LABEL = style("label", 8.4, color=ORANGE, bold=True)
TITLE = style("title", 24, leading=29, color=NAVY, bold=True)
SECTION = style("section", 15, leading=18, color=NAVY, bold=True)
ANSWER = style("answer", 9.2, leading=12, color=ORANGE, bold=True)


def para(canvas, text, x, y_top, width, height, paragraph_style=BODY):
    block = Paragraph(text, paragraph_style)
    _, needed = block.wrap(width, height)
    block.drawOn(canvas, x, y_top - needed)
    return needed


def footer(canvas, page_number, tutor):
    canvas.setStrokeColor(HexColor("#D8D5CE"))
    canvas.setLineWidth(0.4)
    canvas.line(MARGIN, 12 * MM, PAGE_W - MARGIN, 12 * MM)
    canvas.setFont(FONT_REGULAR, 7.3)
    canvas.setFillColor(MUTED)
    label = "แนวสอนครู" if tutor else "แบบฝึกสำหรับผู้เรียน"
    canvas.drawString(MARGIN, 8 * MM, f"© 2026 CurioNest · For classroom use only  |  {label}")
    canvas.drawRightString(PAGE_W - MARGIN, 8 * MM, str(page_number))


def page_header(canvas, number, heading, subheading=""):
    canvas.setFillColor(ORANGE)
    canvas.circle(MARGIN + 6 * MM, PAGE_H - 18 * MM, 5.5 * MM, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont(FONT_BOLD, 13)
    canvas.drawCentredString(MARGIN + 6 * MM, PAGE_H - 20 * MM, str(number))
    para(canvas, heading, MARGIN + 16 * MM, PAGE_H - 13 * MM, PAGE_W - 2 * MARGIN - 16 * MM, 18 * MM, SECTION)
    if subheading:
        para(canvas, subheading, MARGIN + 16 * MM, PAGE_H - 22 * MM, PAGE_W - 2 * MARGIN - 16 * MM, 12 * MM, SMALL)


def image_fit(canvas, path, x, y, width, height, border=False):
    image = ImageReader(str(path))
    iw, ih = image.getSize()
    scale = min(width / iw, height / ih)
    dw, dh = iw * scale, ih * scale
    dx, dy = x + (width - dw) / 2, y + (height - dh) / 2
    if border:
        canvas.setStrokeColor(HexColor("#D8D5CE"))
        canvas.setLineWidth(0.7)
        canvas.rect(x, y, width, height, fill=0, stroke=1)
    canvas.drawImage(image, dx, dy, dw, dh, preserveAspectRatio=True, mask="auto")


def answer_overlay(canvas, text, x, y_top, width, height=25 * MM):
    canvas.saveState()
    canvas.setFillColor(NOTE)
    canvas.roundRect(x, y_top - height, width, height, 2 * MM, fill=1, stroke=0)
    para(canvas, "คำตอบครู: " + text, x + 3 * MM, y_top - 3 * MM, width - 6 * MM, height - 6 * MM, ANSWER)
    canvas.restoreState()


def draw_cover(canvas, tutor):
    canvas.setFillColor(CREAM)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, 18 * MM, PAGE_H, fill=1, stroke=0)
    canvas.setFillColor(ORANGE)
    canvas.rect(18 * MM, PAGE_H - 36 * MM, 5 * MM, 22 * MM, fill=1, stroke=0)
    canvas.setFont(FONT_BOLD, 15)
    canvas.setFillColor(NAVY)
    canvas.drawString(30 * MM, PAGE_H - 23 * MM, "CURIONEST")
    canvas.setFont(FONT_REGULAR, 8.5)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 22 * MM, DATA["level"])
    para(canvas, DATA["title"], 30 * MM, PAGE_H - 50 * MM, 100 * MM, 35 * MM, TITLE)
    para(canvas, DATA["subtitle"], 30 * MM, PAGE_H - 85 * MM, 100 * MM, 22 * MM, style("subtitle", 12.5, color=ORANGE, bold=True))
    image_fit(canvas, ASSETS / "graduated-cylinder-public-domain.jpg", 140 * MM, PAGE_H - 150 * MM, 42 * MM, 102 * MM, border=True)
    canvas.setFillColor(WASH)
    canvas.roundRect(30 * MM, 55 * MM, 102 * MM, 66 * MM, 3 * MM, fill=1, stroke=0)
    para(canvas, "สิ่งที่จะทำในชีตนี้", 36 * MM, 113 * MM, 90 * MM, 10 * MM, style("cover-head", 11.5, color=NAVY, bold=True))
    y = 100 * MM
    for index, target in enumerate(DATA["learning_targets"], 1):
        canvas.setFillColor(ORANGE)
        canvas.circle(39 * MM, y + 1.5 * MM, 3.2 * MM, fill=1, stroke=0)
        canvas.setFillColor(WHITE)
        canvas.setFont(FONT_BOLD, 8)
        canvas.drawCentredString(39 * MM, y - 0.7 * MM, str(index))
        para(canvas, target, 46 * MM, y + 5 * MM, 77 * MM, 13 * MM, BODY)
        y -= 16 * MM
    canvas.setFillColor(NOTE)
    canvas.roundRect(140 * MM, 55 * MM, 42 * MM, 26 * MM, 2 * MM, fill=1, stroke=0)
    para(canvas, "สูตรหลัก<br/><b>d = m / V</b>", 145 * MM, 74 * MM, 32 * MM, 18 * MM, style("formula", 12, leading=17, color=NAVY, bold=True, align=TA_CENTER))
    canvas.setFillColor(MUTED)
    canvas.setFont(FONT_REGULAR, 7)
    canvas.drawRightString(PAGE_W - MARGIN, 17 * MM, "ภาพกระบอกตวง: Public Domain, Wikimedia Commons")
    footer(canvas, 1, tutor)


def draw_summary(canvas, tutor):
    canvas.setFillColor(WHITE)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    page_header(canvas, 1, "เลือกเครื่องมือให้ตรงกับข้อมูล", "เริ่มจากคำถามว่า ต้องการวัดอะไร และต้องละเอียดเพียงใด")
    left_x, right_x = MARGIN, 108 * MM
    top = PAGE_H - 38 * MM
    para(canvas, "เครื่องมือสามแบบ งานไม่เหมือนกัน", left_x, top, 82 * MM, 12 * MM, style("sub1", 11.5, color=NAVY, bold=True))
    instruments = [
        ("electronic-balance-ccby3.png", "เครื่องชั่งอิเล็กทรอนิกส์", "วัดมวล | g"),
        ("graduated-cylinder-ccby3.png", "กระบอกตวง", "วัดปริมาตรของเหลว | mL"),
        ("beaker-ccby3.png", "บีกเกอร์", "บรรจุและผสม | ไม่ใช่งานวัดละเอียด"),
    ]
    y = top - 34 * MM
    for filename, name, use in instruments:
        image_fit(canvas, ASSETS / filename, left_x, y, 25 * MM, 27 * MM)
        para(canvas, name, left_x + 30 * MM, y + 23 * MM, 50 * MM, 10 * MM, style(name, 9.5, color=NAVY, bold=True))
        para(canvas, use, left_x + 30 * MM, y + 11 * MM, 50 * MM, 10 * MM, SMALL)
        y -= 37 * MM
    para(canvas, "หนึ่งค่าการวัดต้องสื่อ 3 อย่าง", right_x, top, 77 * MM, 12 * MM, style("sub2", 11.5, color=NAVY, bold=True))
    parts = [
        ("1", "ขนาด", "ตัวเลขที่อ่านหรือคำนวณได้"),
        ("2", "หน่วย", "มาตรฐานที่ทำให้ค่ามีความหมาย"),
        ("3", "ความไม่แน่นอน", "สะท้อนขีดจำกัดของเครื่องมือและการอ่านค่า"),
    ]
    y2 = top - 17 * MM
    for number, head, body in parts:
        canvas.setFillColor(ORANGE)
        canvas.circle(right_x + 4 * MM, y2, 3.5 * MM, fill=1, stroke=0)
        canvas.setFillColor(WHITE)
        canvas.setFont(FONT_BOLD, 8)
        canvas.drawCentredString(right_x + 4 * MM, y2 - 1 * MM, number)
        para(canvas, f"<b>{head}</b><br/>{body}", right_x + 11 * MM, y2 + 6 * MM, 62 * MM, 22 * MM, BODY)
        y2 -= 27 * MM
    canvas.setFillColor(WASH)
    canvas.roundRect(right_x, 81 * MM, 77 * MM, 38 * MM, 2 * MM, fill=1, stroke=0)
    para(canvas, "ตัวอย่างนำทาง", right_x + 5 * MM, 112 * MM, 65 * MM, 10 * MM, LABEL)
    para(canvas, "มวล 36.4 g และปริมาตร 14.0 mL<br/><b>d = 36.4 / 14.0 = 2.60 g/mL</b>", right_x + 5 * MM, 102 * MM, 65 * MM, 24 * MM, BODY)
    canvas.setFillColor(NOTE)
    canvas.roundRect(right_x, 46 * MM, 77 * MM, 27 * MM, 2 * MM, fill=1, stroke=0)
    para(canvas, "ระวัง", right_x + 5 * MM, 68 * MM, 65 * MM, 8 * MM, LABEL)
    para(canvas, "บีกเกอร์มีขีดบอกปริมาตรได้ แต่ไม่ควรแทนกระบอกตวงเมื่อต้องการค่าละเอียด", right_x + 5 * MM, 59 * MM, 65 * MM, 19 * MM, SMALL)
    if tutor:
        para(canvas, "ชวนถาม: นักเรียนกำลังเลือกเครื่องมือจากชื่อ หรือจากคุณภาพของข้อมูลที่ต้องการ?", MARGIN, 34 * MM, PAGE_W - 2 * MARGIN, 11 * MM, ANSWER)
    footer(canvas, 2, tutor)


def draw_practice(canvas, tutor):
    canvas.setFillColor(WHITE)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    page_header(canvas, 2, "ลองเลือก ลองอธิบาย ลองคำนวณ", "ตอบให้ครบ: หลักฐาน - เครื่องมือ/สมการ - หน่วย")
    top = PAGE_H - 43 * MM
    para(canvas, "A  จับคู่ภาพกับงานวัด", MARGIN, top, 170 * MM, 10 * MM, style("pa", 12, color=NAVY, bold=True))
    x_positions = [MARGIN, 77 * MM, 139 * MM]
    entries = [
        ("electronic-balance-ccby3.png", "มวล / ปริมาตร / อุณหภูมิ"),
        ("graduated-cylinder-ccby3.png", "มวล / ปริมาตร / อุณหภูมิ"),
        ("beaker-ccby3.png", "งานวัดละเอียด / บรรจุและผสม"),
    ]
    for x, (filename, prompt) in zip(x_positions, entries):
        image_fit(canvas, ASSETS / filename, x, top - 42 * MM, 42 * MM, 33 * MM)
        para(canvas, prompt, x, top - 46 * MM, 48 * MM, 12 * MM, SMALL)
        canvas.setStrokeColor(MUTED)
        canvas.line(x, top - 58 * MM, x + 45 * MM, top - 58 * MM)
    if tutor:
        para(canvas, "มวล (g)", x_positions[0], top - 56 * MM, 45 * MM, 8 * MM, ANSWER)
        para(canvas, "ปริมาตร (mL)", x_positions[1], top - 56 * MM, 45 * MM, 8 * MM, ANSWER)
        para(canvas, "บรรจุและผสม", x_positions[2], top - 56 * MM, 45 * MM, 8 * MM, ANSWER)
    y = top - 72 * MM
    para(canvas, "B  เลือกเครื่องมือ", MARGIN, y, 170 * MM, 10 * MM, style("pb", 12, color=NAVY, bold=True))
    para(canvas, DATA["practice"]["choice_prompt"], MARGIN, y - 12 * MM, 170 * MM, 18 * MM, BODY)
    canvas.setStrokeColor(MUTED)
    for offset in (32, 42):
        canvas.line(MARGIN, y - offset * MM, PAGE_W - MARGIN, y - offset * MM)
    if tutor:
        answer_overlay(canvas, DATA["answers"]["choice"], MARGIN, y - 23 * MM, PAGE_W - 2 * MARGIN, 21 * MM)
    y2 = y - 58 * MM
    para(canvas, "C  คำนวณความหนาแน่น", MARGIN, y2, 170 * MM, 10 * MM, style("pc", 12, color=NAVY, bold=True))
    para(canvas, DATA["practice"]["density_prompt"], MARGIN, y2 - 12 * MM, 170 * MM, 18 * MM, BODY)
    canvas.setFillColor(WASH)
    canvas.roundRect(MARGIN, 34 * MM, PAGE_W - 2 * MARGIN, 55 * MM, 2 * MM, fill=1, stroke=0)
    para(canvas, "พื้นที่ทำโจทย์", MARGIN + 5 * MM, 83 * MM, 35 * MM, 8 * MM, SMALL)
    if tutor:
        para(canvas, DATA["answers"]["density"], MARGIN + 8 * MM, 69 * MM, PAGE_W - 2 * MARGIN - 16 * MM, 22 * MM, ANSWER)
        para(canvas, "จุดซ่อม: ถ้านักเรียนลืมหน่วย ให้ย้อนถามว่า ตัวตั้งและตัวหารบอกปริมาณใด", MARGIN + 8 * MM, 50 * MM, PAGE_W - 2 * MARGIN - 16 * MM, 15 * MM, SMALL)
    footer(canvas, 3, tutor)


def draw_repair(canvas, tutor):
    canvas.setFillColor(WHITE)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    page_header(canvas, 3, "อ่านภาพ แล้วซ่อมวิธีคิด", "ภาพเป็นหลักฐาน ไม่ใช่ของตกแต่ง")
    image_fit(canvas, ASSETS / "graduated-cylinder-public-domain.jpg", MARGIN, 125 * MM, 43 * MM, 108 * MM, border=True)
    right = 67 * MM
    para(canvas, "1  หลักฐานจากภาพ", right, PAGE_H - 45 * MM, 118 * MM, 9 * MM, style("r1", 11.5, color=NAVY, bold=True))
    para(canvas, DATA["practice"]["photo_prompt"], right, PAGE_H - 58 * MM, 118 * MM, 22 * MM, BODY)
    canvas.setStrokeColor(MUTED)
    canvas.line(right, PAGE_H - 83 * MM, PAGE_W - MARGIN, PAGE_H - 83 * MM)
    if tutor:
        para(canvas, DATA["answers"]["photo"], right, PAGE_H - 72 * MM, 118 * MM, 20 * MM, ANSWER)
    para(canvas, "2  เลือกจากความละเอียด", right, PAGE_H - 98 * MM, 118 * MM, 9 * MM, style("r2", 11.5, color=NAVY, bold=True))
    para(canvas, DATA["practice"]["precision_prompt"], right, PAGE_H - 111 * MM, 118 * MM, 22 * MM, BODY)
    canvas.line(right, PAGE_H - 136 * MM, PAGE_W - MARGIN, PAGE_H - 136 * MM)
    if tutor:
        para(canvas, DATA["answers"]["precision"], right, PAGE_H - 125 * MM, 118 * MM, 20 * MM, ANSWER)
    para(canvas, "3  ตรวจความคลาดเคลื่อน", MARGIN, 112 * MM, 170 * MM, 9 * MM, style("r3", 11.5, color=NAVY, bold=True))
    para(canvas, DATA["practice"]["percent_error_prompt"], MARGIN, 99 * MM, 170 * MM, 18 * MM, BODY)
    canvas.setFillColor(WASH)
    canvas.roundRect(MARGIN, 57 * MM, PAGE_W - 2 * MARGIN, 30 * MM, 2 * MM, fill=1, stroke=0)
    if tutor:
        para(canvas, DATA["answers"]["percent_error"], MARGIN + 6 * MM, 78 * MM, PAGE_W - 2 * MARGIN - 12 * MM, 15 * MM, ANSWER)
    else:
        para(canvas, "แสดงสูตร การแทนค่า และคำตอบพร้อมเครื่องหมาย %", MARGIN + 6 * MM, 78 * MM, PAGE_W - 2 * MARGIN - 12 * MM, 15 * MM, SMALL)
    canvas.setFillColor(NOTE)
    canvas.roundRect(MARGIN, 23 * MM, PAGE_W - 2 * MARGIN, 27 * MM, 2 * MM, fill=1, stroke=0)
    para(canvas, "บันทึกการซ่อม", MARGIN + 5 * MM, 45 * MM, 35 * MM, 8 * MM, LABEL)
    repair = "ข้อที่พลาด: ________   แนวคิดที่ทำให้พลาด: ____________________   ครั้งหน้าจะซ่อมโดย: ____________________"
    if tutor:
        repair = "วินิจฉัย: แยกให้ชัดว่าพลาดจากการเลือกเครื่องมือ การอ่านหลักฐาน หน่วย หรือเลขนัยสำคัญ แล้วกำหนดการฝึกซ้ำหนึ่งอย่าง"
    para(canvas, repair, MARGIN + 5 * MM, 36 * MM, PAGE_W - 2 * MARGIN - 10 * MM, 15 * MM, SMALL if not tutor else ANSWER)
    canvas.setFillColor(MUTED)
    canvas.setFont(FONT_REGULAR, 5.8)
    canvas.drawString(MARGIN, 15 * MM, "Sources: OpenStax Chemistry 2e Ch.1 (scope); Chem Pride Unit 1 (workflow benchmark only).")
    canvas.drawRightString(PAGE_W - MARGIN, 15 * MM, "Image: Public Domain; icons: Servier/Bioicons CC BY 3.0")
    footer(canvas, 4, tutor)


def build(path, tutor=False):
    canvas = Canvas(str(path), pagesize=A4, pageCompression=1)
    canvas.setTitle(DATA["title"])
    canvas.setAuthor("CurioNest")
    for draw in (draw_cover, draw_summary, draw_practice, draw_repair):
        draw(canvas, tutor)
        canvas.showPage()
    canvas.save()


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    build(OUTPUT / "curionest-measurement-pattern-student.pdf", tutor=False)
    build(OUTPUT / "curionest-measurement-pattern-tutor.pdf", tutor=True)
    print(OUTPUT)


if __name__ == "__main__":
    main()
