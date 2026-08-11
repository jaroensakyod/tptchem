"""Build the CurioNest measurement worksheet PDF package."""

from pathlib import Path
import json
import shutil

from pypdf import PdfReader, PdfWriter
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph


HERE = Path(__file__).resolve().parent
PRODUCT = HERE.parent
ASSETS = PRODUCT / "assets"
OUT = PRODUCT / "output"
BUYER = OUT / "buyer-files"
UPLOAD = OUT / "tpt-upload"
DATA = json.loads((HERE / "source.json").read_text(encoding="utf-8"))
BRAND = DATA["brand"]
COPYRIGHT = DATA["source_policy"]["buyer_facing_copyright"]
FILE_PREFIX = "CurioNest_Measurement"

W, H = letter
INCH = 72
M = 0.55 * INCH

INK = HexColor("#202B33")
NAVY = HexColor("#203B4D")
ORANGE = HexColor("#C86543")
OCHRE = HexColor("#DDB75F")
WHITE = HexColor("#FFFEFA")
WASH = HexColor("#F8F5EE")
CREAM = HexColor("#F5EFE3")
NOTE = HexColor("#F3E5BD")
MUTED = HexColor("#6D7478")
LINE = HexColor("#D8D5CE")

FONT = "Aptos"
BOLD = "Aptos-Bold"
font_regular = Path(r"C:\Windows\Fonts\aptos.ttf")
font_bold = Path(r"C:\Windows\Fonts\aptos-bold.ttf")
if not font_regular.exists():
    font_regular = Path(r"C:\Windows\Fonts\arial.ttf")
    FONT = "ArialLocal"
if not font_bold.exists():
    font_bold = Path(r"C:\Windows\Fonts\arialbd.ttf")
    BOLD = "ArialLocal-Bold"
pdfmetrics.registerFont(TTFont(FONT, str(font_regular)))
pdfmetrics.registerFont(TTFont(BOLD, str(font_bold)))


def pstyle(name, size=10, leading=None, color=INK, bold=False, align=TA_LEFT):
    return ParagraphStyle(
        name,
        fontName=BOLD if bold else FONT,
        fontSize=size,
        leading=leading or size * 1.28,
        textColor=color,
        alignment=align,
        spaceAfter=0,
    )


BODY = pstyle("body", 9.8)
SMALL = pstyle("small", 7.6, color=MUTED)
TINY = pstyle("tiny", 6.3, color=MUTED)
LABEL = pstyle("label", 8.2, color=ORANGE, bold=True)
HEAD = pstyle("head", 18, leading=20, color=NAVY, bold=True)
SUBHEAD = pstyle("subhead", 11.3, leading=13.5, color=NAVY, bold=True)
ANSWER = pstyle("answer", 8.2, leading=10.1, color=ORANGE, bold=True)


def para(c, text, x, y_top, width, height, style=BODY):
    block = Paragraph(text, style)
    _, needed = block.wrap(width, height)
    block.drawOn(c, x, y_top - needed)
    return needed


def fit_image(c, path, x, y, width, height, border=False):
    image = ImageReader(str(path))
    iw, ih = image.getSize()
    scale = min(width / iw, height / ih)
    dw, dh = iw * scale, ih * scale
    if border:
        c.setStrokeColor(LINE)
        c.setLineWidth(0.7)
        c.rect(x, y, width, height, fill=0, stroke=1)
    c.drawImage(image, x + (width - dw) / 2, y + (height - dh) / 2, dw, dh, mask="auto")


def line(c, x1, y, x2, color=MUTED, width=0.65):
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.line(x1, y, x2, y)


def footer(c, page_num, key=False):
    line(c, M, 28, W - M, LINE, 0.45)
    c.setFont(FONT, 7)
    c.setFillColor(MUTED)
    edition = "TEACHER KEY" if key else "STUDENT WORKSHEET"
    c.drawString(M, 18, f"{COPYRIGHT}  |  {edition}")
    c.drawRightString(W - M, 18, str(page_num))


def header(c, number, title, subtitle, key=False):
    c.setFillColor(WHITE)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(ORANGE)
    c.circle(M + 15, H - 39, 14, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont(BOLD, 12)
    c.drawCentredString(M + 15, H - 43, str(number))
    para(c, title, M + 38, H - 27, W - 2 * M - 38, 24, HEAD)
    para(c, subtitle, M + 38, H - 52, W - 2 * M - 38, 18, SMALL)
    if key:
        c.setFillColor(NOTE)
        c.roundRect(W - M - 80, H - 27, 80, 17, 4, fill=1, stroke=0)
        c.setFillColor(ORANGE)
        c.setFont(BOLD, 7.5)
        c.drawCentredString(W - M - 40, H - 22, "TEACHER KEY")
    else:
        c.setFillColor(MUTED)
        c.setFont(FONT, 7.5)
        c.drawRightString(W - M, H - 72, "Name: ____________________   Date: __________   Class Period: ______")


def answer_box(c, text, x, y, width, height):
    c.setFillColor(NOTE)
    c.roundRect(x, y, width, height, 5, fill=1, stroke=0)
    para(c, text, x + 6, y + height - 5, width - 12, height - 10, ANSWER)


def draw_student_page_1(c, key=False):
    header(c, 1, "Measurement Ready", "Use the tool, scale, unit, and calculation as one evidence chain.", key)
    c.setFillColor(WASH)
    c.roundRect(M, H - 133, W - 2 * M, 48, 7, fill=1, stroke=0)
    para(c, "LEARNING TARGETS", M + 10, H - 95, 110, 12, LABEL)
    targets = " • ".join(DATA["learning_targets"][:3])
    para(c, targets, M + 10, H - 108, W - 2 * M - 20, 31, pstyle("targets", 8.1, leading=10.2))

    para(c, "Three tools, three different jobs", M, H - 154, W - 2 * M, 16, SUBHEAD)
    xs = [M, M + 181, M + 362]
    entries = [
        ("electronic-balance-ccby3.png", "Electronic balance", "Measures mass", "Typical unit: g"),
        ("graduated-cylinder-ccby3.png", "Graduated cylinder", "Measures liquid volume", "Typical unit: mL"),
        ("beaker-ccby3.png", "Beaker", "Holds and mixes", "Volume is approximate"),
    ]
    for x, (filename, name, job, unit) in zip(xs, entries):
        fit_image(c, ASSETS / filename, x + 18, H - 290, 105, 105)
        para(c, name, x, H - 299, 145, 14, pstyle(name, 9.3, color=NAVY, bold=True, align=TA_CENTER))
        para(c, f"{job}<br/>{unit}", x, H - 316, 145, 28, pstyle(name + "2", 7.8, leading=10, color=MUTED, align=TA_CENTER))

    para(c, "Measurement rules that prevent avoidable errors", M, H - 363, W - 2 * M, 16, SUBHEAD)
    rules = [
        ("1", "Record the value and the unit together."),
        ("2", "For an analog scale, record all certain digits plus one estimated digit."),
        ("3", "Read a concave liquid meniscus at eye level from its lowest point."),
        ("4", "Keep units through every calculation and round only the final result."),
    ]
    y = H - 392
    for number, text in rules:
        c.setFillColor(ORANGE)
        c.circle(M + 10, y + 2, 8, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont(BOLD, 8)
        c.drawCentredString(M + 10, y - 1, number)
        para(c, text, M + 26, y + 8, W - 2 * M - 28, 19, BODY)
        y -= 30

    c.setFillColor(NOTE)
    c.roundRect(M, 120, W - 2 * M, 93, 7, fill=1, stroke=0)
    para(c, "FORMULA TOOLBOX", M + 11, 201, 110, 12, LABEL)
    para(c, "<b>density = mass / volume</b><br/><br/><b>percent error =</b><br/><b>|experimental - accepted| / accepted × 100</b>", M + 11, 183, 330, 62, pstyle("formula", 9.8, leading=13, color=NAVY, bold=True))
    para(c, "Units tell the story", M + 365, 188, 125, 13, pstyle("units", 9.2, color=NAVY, bold=True))
    para(c, "mass: g<br/>liquid volume: mL<br/>density: g/mL", M + 365, 170, 125, 45, pstyle("units2", 9, leading=13))
    footer(c, 1, key)


def draw_student_page_2(c, key=False):
    header(c, 2, "Choose the Tool", "Name what you see, then use visible features to justify the choice.", key)
    para(c, "A. Identify each instrument", M, H - 89, 240, 16, SUBHEAD)
    xs = [M, M + 181, M + 362]
    entries = [
        ("electronic-balance-ccby3.png", "1"),
        ("graduated-cylinder-ccby3.png", "2"),
        ("beaker-ccby3.png", "3"),
    ]
    for x, (filename, number) in zip(xs, entries):
        fit_image(c, ASSETS / filename, x + 17, H - 229, 110, 103)
        c.setFillColor(ORANGE)
        c.circle(x + 10, H - 126, 9, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont(BOLD, 8)
        c.drawCentredString(x + 10, H - 129, number)
        if not key:
            para(c, "Instrument: __________________", x, H - 239, 150, 13, pstyle("inst" + number, 7.9))
            para(c, "Quantity/job: ________________", x, H - 258, 150, 13, pstyle("job" + number, 7.9))
            para(c, "Unit (if measured): __________", x, H - 277, 150, 13, pstyle("unit" + number, 7.9))
    if key:
        answers = [DATA["answers"]["tool_1"], DATA["answers"]["tool_2"], DATA["answers"]["tool_3"]]
        for x, text in zip(xs, answers):
            answer_box(c, text.replace(" - ", "<br/>"), x, H - 304, 150, 55)

    para(c, "B. Select and justify", M, H - 333, 220, 16, SUBHEAD)
    para(c, "4. You need 18.6 mL of water. Choose a beaker or a graduated cylinder. Explain which visible design features support your choice.", M, H - 354, W - 2 * M, 31, BODY)
    if key:
        answer_box(c, DATA["answers"]["choice_1"], M, H - 434, W - 2 * M, 48)
    else:
        line(c, M, H - 395, W - M)
        line(c, M, H - 414, W - M)

    para(c, "5. You need about 125 mL of solution and room to stir. Choose a beaker or a graduated cylinder. Explain.", M, H - 449, W - 2 * M, 26, BODY)
    if key:
        answer_box(c, DATA["answers"]["choice_2"], M, H - 519, W - 2 * M, 43)
    else:
        line(c, M, H - 486, W - M)
        line(c, M, H - 505, W - M)

    para(c, "C. Read visual evidence", M, H - 543, 220, 16, SUBHEAD)
    fit_image(c, ASSETS / "graduated-cylinder-public-domain.jpg", M, 55, 88, 178, border=True)
    para(c, "6. Identify two visible features that show this vessel was designed to measure liquid volume.", M + 110, H - 568, W - 2 * M - 110, 29, BODY)
    if key:
        answer_box(c, DATA["answers"]["photo_evidence"], M + 110, 71, W - 2 * M - 110, 68)
    else:
        line(c, M + 110, H - 610, W - M)
        line(c, M + 110, H - 631, W - M)
    para(c, "Photo: Darrien / Haltopub, Public Domain, Wikimedia Commons", M, 49, 180, 11, TINY)
    footer(c, 2, key)


def draw_student_page_3(c, key=False):
    header(c, 3, "Calculate with Units", "Show the formula, substitute values with units, and round only the final answer.", key)
    c.setFillColor(WASH)
    c.roundRect(M, H - 151, W - 2 * M, 61, 7, fill=1, stroke=0)
    para(c, "GUIDED EXAMPLE", M + 10, H - 101, 120, 12, LABEL)
    para(c, "A sample has a mass of 36.4 g and a volume of 14.0 mL.<br/><b>d = m / V = 36.4 g / 14.0 mL = 2.60 g/mL</b>", M + 10, H - 118, W - 2 * M - 20, 42, pstyle("guided", 10.1, leading=14))

    tasks = [
        ("7", "A liquid sample has a mass of 27.0 g and a density of 2.70 g/mL. Calculate its volume.", "volume_2"),
        ("8", "A liquid has a density of 0.789 g/mL and a volume of 25.0 mL. Calculate its mass.", "mass_3"),
        ("9", "A student measures 2.58 g/mL. The accepted value is 2.70 g/mL. Calculate percent error.", "percent_error_4"),
    ]
    y = H - 178
    for num, prompt, answer_key in tasks:
        para(c, f"<b>{num}.</b> {prompt}", M, y, W - 2 * M, 28, BODY)
        if key:
            answer_box(c, DATA["answers"][answer_key], M, y - 76, W - 2 * M, 57)
        else:
            c.setFillColor(WASH)
            c.roundRect(M, y - 76, W - 2 * M, 57, 5, fill=1, stroke=0)
            para(c, "Work space", M + 8, y - 25, 70, 10, SMALL)
        y -= 112

    para(c, "10. Accuracy and precision", M, y + 2, 220, 16, SUBHEAD)
    para(c, "Accepted density: 2.70 g/mL", M, y - 17, 180, 14, BODY)
    c.setStrokeColor(LINE)
    c.setFillColor(WASH)
    c.rect(M, y - 100, W - 2 * M, 70, fill=1, stroke=1)
    c.setFillColor(NAVY)
    c.setFont(BOLD, 8.5)
    c.drawString(M + 12, y - 48, "Set A")
    c.drawString(M + 12, y - 77, "Set B")
    c.setFillColor(INK)
    c.setFont(FONT, 9)
    c.drawString(M + 80, y - 48, "2.70, 2.71, 2.69 g/mL")
    c.drawString(M + 80, y - 77, "2.42, 2.41, 2.42 g/mL")
    para(c, "Which set is accurate? Which is precise? Explain using the pattern in the data.", M, y - 115, W - 2 * M, 22, BODY)
    if key:
        answer_box(c, DATA["answers"]["dataset"], M, y - 178, W - 2 * M, 38)
    else:
        line(c, M, y - 152, W - M)
    footer(c, 3, key)


def draw_student_page_4(c, key=False):
    header(c, 4, "Reason from Evidence", "Use the data to build a claim, diagnose the error, and plan a repair.", key)
    para(c, "LAB CASE: UNKNOWN LIQUID", M, H - 89, 250, 16, SUBHEAD)
    c.setFillColor(WASH)
    c.roundRect(M, H - 223, W - 2 * M, 113, 7, fill=1, stroke=0)
    para(c, "A student uses an electronic balance and a graduated cylinder. The empty container has a mass of 42.31 g. The container plus liquid has a mass of 67.19 g. The liquid volume is 20.0 mL. The accepted density is 1.25 g/mL.", M + 11, H - 124, W - 2 * M - 22, 52, BODY)
    if key:
        para(c, f"<b>11. Mass of liquid:</b> <font color='#C86543'><b>{DATA['answers']['case_mass']}</b></font>", M + 11, H - 182, 230, 14, BODY)
        para(c, f"<b>12. Experimental density:</b> <font color='#C86543'><b>{DATA['answers']['case_density']}</b></font>", M + 275, H - 182, 230, 14, BODY)
        para(c, f"<b>13. Percent error:</b> <font color='#C86543'><b>{DATA['answers']['case_percent_error']}</b></font>", M + 11, H - 207, 270, 14, BODY)
    else:
        para(c, "11. Mass of liquid: ____________________", M + 11, H - 182, 230, 14, BODY)
        para(c, "12. Experimental density: ____________________", M + 275, H - 182, 230, 14, BODY)
        para(c, "13. Percent error: ____________________", M + 11, H - 207, 230, 14, BODY)

    para(c, "14. Claim - Evidence - Reasoning", M, H - 252, 270, 16, SUBHEAD)
    para(c, "Claim: Is the experimental result close to the accepted value?", M, H - 274, W - 2 * M, 18, BODY)
    para(c, "Evidence: Cite at least two numbers from the case.", M, H - 327, W - 2 * M, 18, BODY)
    para(c, "Reasoning: Explain what percent error tells you and what it does not tell you about precision.", M, H - 380, W - 2 * M, 26, BODY)
    if key:
        answer_box(c, DATA["answers"]["case_claim"] + " Evidence: 1.244 g/mL before final rounding vs. 1.25 g/mL and 0.48% error.", M, H - 461, W - 2 * M, 52)
    else:
        line(c, M, H - 307, W - M)
        line(c, M, H - 360, W - M)
        line(c, M, H - 420, W - M)
        line(c, M, H - 439, W - M)

    para(c, "15. Error diagnosis", M, H - 476, 220, 16, SUBHEAD)
    para(c, "Another student reads the liquid above eye level, rounds every intermediate value, and omits units. Name two problems and one exact repair action.", M, H - 499, W - 2 * M, 31, BODY)
    if key:
        answer_box(c, DATA["answers"]["repair"], M, H - 574, W - 2 * M, 45)
    else:
        line(c, M, H - 543, W - M)
        line(c, M, H - 563, W - M)

    c.setFillColor(NOTE)
    c.roundRect(M, 57, W - 2 * M, 78, 7, fill=1, stroke=0)
    para(c, "REPAIR LOG", M + 10, 125, 90, 12, LABEL)
    para(c, "Item/skill to repair: ____________________________", M + 10, 107, 250, 13, pstyle("repair1", 8.4))
    para(c, "Incorrect idea or step: __________________________", M + 10, 88, 250, 13, pstyle("repair2", 8.4))
    para(c, "Next action: ____________________________________", M + 285, 107, 230, 13, pstyle("repair3", 8.4))
    para(c, "When I will retry: ______________________________", M + 285, 88, 230, 13, pstyle("repair4", 8.4))
    footer(c, 4, key)


STUDENT_DRAWERS = [draw_student_page_1, draw_student_page_2, draw_student_page_3, draw_student_page_4]


def build_student_or_key(path, key=False):
    c = Canvas(str(path), pagesize=letter, pageCompression=1)
    c.setTitle(DATA["title"] + (" - Answer Key" if key else " - Student"))
    c.setAuthor(BRAND)
    for drawer in STUDENT_DRAWERS:
        drawer(c, key)
        c.showPage()
    c.save()


def draw_marketing_cover(c):
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.rect(0, 0, 54, H, fill=1, stroke=0)
    c.setFillColor(ORANGE)
    c.rect(54, H - 130, 12, 75, fill=1, stroke=0)
    c.setFont(BOLD, 17)
    c.setFillColor(NAVY)
    c.drawString(92, H - 70, BRAND.upper())
    para(c, "CHEMISTRY MEASUREMENT", 92, H - 132, 330, 40, pstyle("cover-title", 25, leading=28, color=NAVY, bold=True))
    para(c, "Lab Tools, Density & Percent Error", 92, H - 190, 335, 50, pstyle("cover-sub", 16, leading=20, color=ORANGE, bold=True))
    para(c, "Visual worksheet for U.S. Grades 8-10", 92, H - 236, 320, 22, pstyle("cover-meta", 10.5, color=MUTED))
    fit_image(c, ASSETS / "graduated-cylinder-public-domain.jpg", 445, H - 365, 105, 260, border=True)
    c.setFillColor(WASH)
    c.roundRect(92, 310, 315, 165, 8, fill=1, stroke=0)
    para(c, "STUDENTS WILL", 110, 454, 120, 12, LABEL)
    items = [
        "identify common measurement tools",
        "justify equipment choices with visual evidence",
        "calculate density and percent error",
        "compare accuracy and precision",
        "repair a measurement misconception",
    ]
    y = 429
    for text in items:
        c.setFillColor(ORANGE)
        c.circle(116, y + 2, 4, fill=1, stroke=0)
        para(c, text, 128, y + 8, 255, 16, pstyle("cover-item" + text, 9.5))
        y -= 25
    c.setFillColor(NOTE)
    c.roundRect(445, 310, 105, 82, 7, fill=1, stroke=0)
    para(c, "4 student pages<br/>4-page full key<br/>Editable DOCX", 455, 378, 85, 58, pstyle("cover-inc", 9.4, leading=15, color=NAVY, bold=True, align=TA_CENTER))
    para(c, "PRINT-READY • US LETTER", 92, 242, 315, 15, pstyle("cover-tag", 10, color=NAVY, bold=True, align=TA_CENTER))
    c.setFillColor(NAVY)
    c.roundRect(92, 145, 458, 70, 7, fill=1, stroke=0)
    para(c, "density = mass / volume", 110, 191, 420, 35, pstyle("cover-formula", 18, leading=23, color=WHITE, bold=True, align=TA_CENTER))
    c.setFont(FONT, 6.4)
    c.setFillColor(MUTED)
    c.drawRightString(W - M, 34, "Photo: Darrien / Haltopub, Public Domain, Wikimedia Commons")


def draw_teacher_guide(c):
    c.setFillColor(WHITE)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    para(c, "TEACHER QUICK START", M, H - 48, W - 2 * M, 30, pstyle("tg-title", 22, color=NAVY, bold=True))
    para(c, DATA["title"], M, H - 80, W - 2 * M, 24, pstyle("tg-sub", 12, color=ORANGE, bold=True))
    c.setFillColor(WASH)
    c.roundRect(M, H - 178, W - 2 * M, 70, 7, fill=1, stroke=0)
    para(c, "AT A GLANCE", M + 10, H - 121, 100, 12, LABEL)
    para(c, "U.S. Grades 8-10  |  35-45 minutes  |  Individual, pairs, or intervention  |  No lab materials required", M + 10, H - 143, W - 2 * M - 20, 32, pstyle("atglance", 10.2, leading=14, color=NAVY, bold=True))
    sections = [
        ("Purpose", "Students connect visible equipment features to measurement choices, then apply the resulting data to density, percent error, accuracy, and precision."),
        ("Suggested pacing", "5 min quick reference; 10 min tool selection; 15 min calculations; 10 min lab case and repair; 5 min review."),
        ("Before class", "Print pages 1-4. Decide whether students may use calculators. Review local expectations for significant figures and liquid-volume reading."),
        ("Differentiation", "Support: allow the formula toolbox and a unit bank. Core: complete as written. Extension: ask students to design one additional measurement trial that would improve confidence in precision."),
        ("Look-fors", "Students name the measured quantity, not only the tool; carry units through calculations; use the accepted value in the percent-error denominator; avoid claiming precision from a single trial."),
        ("Safety note", "This is a paper-based readiness task. Local laboratory rules, teacher directions, SDS information, and equipment-specific procedures always take priority."),
    ]
    y = H - 212
    for title, body in sections:
        para(c, title, M, y, 125, 16, pstyle("tg" + title, 11, color=NAVY, bold=True))
        para(c, body, M + 130, y, W - 2 * M - 130, 48, pstyle("tgb" + title, 9.2, leading=12.2))
        y -= 72 if title in ("Differentiation", "Look-fors") else 59
    c.setFillColor(NOTE)
    c.roundRect(M, 55, W - 2 * M, 72, 7, fill=1, stroke=0)
    para(c, "Fast formative check", M + 10, 115, 150, 13, LABEL)
    para(c, "Ask: “What makes a measurement trustworthy?” A complete response should connect the right tool, readable scale, unit, repeated trials, and transparent calculation.", M + 10, 96, W - 2 * M - 20, 38, pstyle("fast", 9.3, leading=12.5))
    footer(c, 2, True)


def draw_terms(c):
    c.setFillColor(WHITE)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    para(c, "TERMS, CREDITS & SOURCES", M, H - 48, W - 2 * M, 30, pstyle("terms-title", 20, color=NAVY, bold=True))
    para(c, COPYRIGHT, M, H - 86, W - 2 * M, 20, pstyle("thanks", 11, color=ORANGE, bold=True))
    para(c, "TERMS OF USE", M, H - 127, 180, 15, SUBHEAD)
    terms = [
        "Purchase grants one educator a license for use with that educator's own students.",
        "You may print copies and post the files inside a password-protected learning system for your own students.",
        "Do not share files with colleagues, post publicly online, resell, redistribute, or remove credits.",
        "Contact the seller for additional educator licenses or school-wide use.",
    ]
    y = H - 153
    for item in terms:
        c.setFillColor(ORANGE)
        c.circle(M + 5, y + 2, 3.5, fill=1, stroke=0)
        para(c, item, M + 17, y + 8, W - 2 * M - 17, 26, pstyle("term" + item, 9.1, leading=12))
        y -= 38
    para(c, "IMAGE CREDITS", M, y - 4, 180, 15, SUBHEAD)
    credits = (
        "Graduated-cylinder photograph: Darrien / Haltopub, Public Domain, Wikimedia Commons, "
        "commons.wikimedia.org/wiki/File:Graduated_cylinder.jpg.<br/><br/>"
        "Electronic balance, graduated cylinder, and beaker icons: Servier via Bioicons, "
        "CC BY 3.0 Unported.<br/>Bioicons: bioicons.com &nbsp;&nbsp; "
        "License: creativecommons.org/licenses/by/3.0/"
    )
    para(c, credits, M, y - 27, W - 2 * M, 95, pstyle("credits", 8.5, leading=11.5))
    y -= 132
    para(c, "CONTENT SOURCES", M, y, 180, 15, SUBHEAD)
    sources = (
        "<b>NIST SP 811 - Guide for the Use of the International System of Units (SI)</b><br/>"
        "nist.gov/publications/guide-use-international-system-units-si<br/><br/>"
        "<b>American Chemical Society</b><br/>"
        "2025 Guidelines and Recommendations for Teaching Middle and High School Chemistry:<br/>"
        "acs.org/education/policies/middle-and-high-school-chemistry.html<br/>"
        "Lab and Safety Equipment: acs.org/education/policies/middle-and-high-school-chemistry/"
        "classroom-and-lab-facilities/safety-equipment.html<br/>"
        "The Importance of the Laboratory Experience: acs.org/education/policies/middle-and-high-school-chemistry/"
        "teaching-and-assessment/lab-experience.html<br/>"
        "Density of Water: acs.org/middleschoolchemistry/lessonplans/chapter3/lesson2.html<br/><br/>"
        "<b>Next Generation Science Standards practice - Using Mathematics and Computational Thinking</b><br/>"
        "nextgenscience.org/practice/using-mathematics-and-computational-thinking<br/><br/>"
        "These sources verify terminology and U.S. classroom scope. No source text or activity was copied."
    )
    para(c, sources, M, y - 24, W - 2 * M, 198, pstyle("sources", 7.15, leading=9.2))
    c.setFillColor(NOTE)
    c.roundRect(M, 62, W - 2 * M, 58, 7, fill=1, stroke=0)
    para(c, f"{COPYRIGHT}. Original questions and page composition are owned by CurioNest. Instructional visuals are separately licensed as credited above.", M + 10, 102, W - 2 * M - 20, 36, pstyle("copyright", 9.1, leading=12, color=NAVY, bold=True, align=TA_CENTER))
    footer(c, 11, True)


def build_front(path):
    c = Canvas(str(path), pagesize=letter, pageCompression=1)
    c.setTitle(DATA["title"])
    c.setAuthor(BRAND)
    draw_marketing_cover(c)
    c.showPage()
    draw_teacher_guide(c)
    c.showPage()
    c.save()


def build_terms(path):
    c = Canvas(str(path), pagesize=letter, pageCompression=1)
    c.setTitle("Terms, Credits & Sources")
    c.setAuthor(BRAND)
    draw_terms(c)
    c.showPage()
    c.save()


def combine(output, *inputs):
    writer = PdfWriter()
    for input_path in inputs:
        reader = PdfReader(input_path)
        for page in reader.pages:
            writer.add_page(page)
    writer.add_metadata(
        {
            "/Title": DATA["title"],
            "/Author": BRAND,
            "/Creator": BRAND,
            "/Subject": COPYRIGHT,
        }
    )
    with output.open("wb") as stream:
        writer.write(stream)


def combine_selected(output, selections):
    writer = PdfWriter()
    for input_path, page_indexes in selections:
        reader = PdfReader(input_path)
        for index in page_indexes:
            writer.add_page(reader.pages[index])
    writer.add_metadata(
        {
            "/Title": f"{DATA['title']} - Preview",
            "/Author": BRAND,
            "/Creator": BRAND,
            "/Subject": COPYRIGHT,
        }
    )
    with output.open("wb") as stream:
        writer.write(stream)


def build_preview_info(path):
    c = Canvas(str(path), pagesize=letter, pageCompression=1)
    c.setFillColor(WHITE)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    para(c, "WHAT'S INCLUDED", M, H - 55, W - 2 * M, 36, pstyle("pi-title", 25, color=NAVY, bold=True, align=TA_CENTER))
    para(c, "A complete, low-prep measurement lesson", M, H - 93, W - 2 * M, 20, pstyle("pi-sub", 12, color=ORANGE, bold=True, align=TA_CENTER))
    features = [
        ("4", "student pages", "reference, visual choices, calculations, CER + repair"),
        ("4", "answer-key pages", "dedicated answer areas with teacher guidance"),
        ("1", "editable DOCX", "adapt wording and pacing for your students"),
        ("4", "rights-cleared visuals", "real photo plus attributed Servier science icons"),
    ]
    y = H - 150
    for number, label, detail in features:
        c.setFillColor(ORANGE)
        c.circle(M + 30, y - 6, 23, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont(BOLD, 16)
        c.drawCentredString(M + 30, y - 12, number)
        para(c, label, M + 68, y + 6, 170, 18, pstyle("pil" + label, 12, color=NAVY, bold=True))
        para(c, detail, M + 68, y - 16, W - 2 * M - 80, 28, pstyle("pid" + label, 9.3))
        y -= 92
    c.setFillColor(NOTE)
    c.roundRect(M, 112, W - 2 * M, 87, 7, fill=1, stroke=0)
    para(c, "BEST FOR", M + 12, 186, 90, 12, LABEL)
    para(c, "Beginning-of-course chemistry • pre-lab readiness • physical science review • intervention • make-up work", M + 12, 162, W - 2 * M - 24, 40, pstyle("best", 10.3, leading=14, color=NAVY, bold=True, align=TA_CENTER))
    para(c, "Preview pages follow. One key page is shown so you can evaluate answer quality; the full key is included in the purchase.", M, 82, W - 2 * M, 35, pstyle("preview-note", 8.5, leading=11.5, color=MUTED, align=TA_CENTER))
    c.showPage()
    c.save()


def main():
    BUYER.mkdir(parents=True, exist_ok=True)
    UPLOAD.mkdir(parents=True, exist_ok=True)
    temp = OUT / "qa" / "pdf"
    temp.mkdir(parents=True, exist_ok=True)

    student = BUYER / f"{FILE_PREFIX}_Visual_Worksheet_Student.pdf"
    key = BUYER / f"{FILE_PREFIX}_Visual_Worksheet_Answer_Key.pdf"
    combined = BUYER / f"{FILE_PREFIX}_Visual_Worksheet_Complete.pdf"
    front = temp / "front.pdf"
    terms = temp / "terms.pdf"
    preview_info = temp / "preview-info.pdf"
    preview = UPLOAD / f"{FILE_PREFIX}_Visual_Worksheet_Preview.pdf"

    build_student_or_key(student, key=False)
    build_student_or_key(key, key=True)
    build_front(front)
    build_terms(terms)
    shutil.copy2(terms, BUYER / f"{FILE_PREFIX}_Rights_and_Sources.pdf")
    combine(combined, front, student, key, terms)

    build_preview_info(preview_info)
    preview_cover = temp / "preview-cover.pdf"
    c = Canvas(str(preview_cover), pagesize=letter, pageCompression=1)
    draw_marketing_cover(c)
    c.showPage()
    c.save()
    combine_selected(
        preview,
        [
            (preview_cover, [0]),
            (student, [1]),
            (key, [2]),
        ],
    )
    print(combined)


if __name__ == "__main__":
    main()
