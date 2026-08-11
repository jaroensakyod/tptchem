"""Build CurioNest complete instructional-unit PDF packages from one JSON source."""

from __future__ import annotations

from hashlib import sha256
from html import escape
from pathlib import Path
import json
import shutil
import zipfile

from pypdf import PdfReader, PdfWriter
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph

REPO_ROOT = Path(__file__).resolve().parent.parent
QUALITY_CONTRACT_PATH = REPO_ROOT / "product-lines" / "complete-unit-quality-baseline.json"
QUALITY_CONTRACT = json.loads(QUALITY_CONTRACT_PATH.read_text(encoding="utf-8"))
TYPOGRAPHY = QUALITY_CONTRACT["typography"]

PORTRAIT = letter
LANDSCAPE = landscape(letter)
PW, PH = PORTRAIT
LW, LH = LANDSCAPE
M = 42

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

FONT, BOLD = "Aptos", "Aptos-Bold"
regular = Path(r"C:\Windows\Fonts\aptos.ttf")
bold = Path(r"C:\Windows\Fonts\aptos-bold.ttf")
if not regular.exists():
    regular, FONT = Path(r"C:\Windows\Fonts\arial.ttf"), "ArialLocal"
if not bold.exists():
    bold, BOLD = Path(r"C:\Windows\Fonts\arialbd.ttf"), "ArialLocal-Bold"
pdfmetrics.registerFont(TTFont(FONT, str(regular)))
pdfmetrics.registerFont(TTFont(BOLD, str(bold)))


def st(name, size=9, leading=None, color=INK, bold=False, align=TA_LEFT):
    return ParagraphStyle(
        name,
        fontName=BOLD if bold else FONT,
        fontSize=size,
        leading=leading or size * 1.25,
        textColor=color,
        alignment=align,
        spaceAfter=0,
    )


BODY = st("body", TYPOGRAPHY["body_pt"], TYPOGRAPHY["body_leading_pt"])
SMALL = st("small", TYPOGRAPHY["small_pt"], 10.7, MUTED)
TINY = st("tiny", TYPOGRAPHY["tiny_pt"], 9.0, MUTED)
LABEL = st("label", TYPOGRAPHY["label_pt"], 10.0, ORANGE, True)


def safe(text):
    return escape(str(text)).replace("\n", "<br/>")


def para(c, text, x, top, width, height, style=BODY):
    p = Paragraph(safe(text), style)
    _, needed = p.wrap(width, height)
    p.drawOn(c, x, top - needed)
    return needed


def fit_image(c, path, x, y, width, height, border=False):
    im = ImageReader(str(path))
    iw, ih = im.getSize()
    scale = min(width / iw, height / ih)
    dw, dh = iw * scale, ih * scale
    if border:
        c.setStrokeColor(LINE)
        c.setLineWidth(0.6)
        c.rect(x, y, width, height, fill=0, stroke=1)
    c.drawImage(im, x + (width - dw) / 2, y + (height - dh) / 2, dw, dh, mask="auto")


def footer(c, width, page, edition, copyright_line):
    c.setStrokeColor(LINE)
    c.setLineWidth(0.45)
    c.line(M, 29, width - M, 29)
    c.setFillColor(MUTED)
    c.setFont(FONT, TYPOGRAPHY["footer_pt"])
    c.drawString(M, 17, f"{copyright_line}  |  {edition}")
    c.drawRightString(width - M, 17, str(page))


def top_rule(c, number, title, subtitle, label, width=PW, height=PH):
    c.setFillColor(WHITE)
    c.rect(0, 0, width, height, fill=1, stroke=0)
    c.setFillColor(ORANGE)
    c.circle(M + 14, height - 37, 13, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont(BOLD, 10.5)
    c.drawCentredString(M + 14, height - 41, str(number))
    para(c, title, M + 36, height - 22, width - 2 * M - 130, 26, st(f"h-{number}-{label}", TYPOGRAPHY["page_title_pt"], 21, NAVY, True))
    para(c, subtitle, M + 36, height - 50, width - 2 * M - 130, 19, SMALL)
    c.setFillColor(NOTE if "KEY" in label else WASH)
    c.roundRect(width - M - 92, height - 34, 92, 18, 4, fill=1, stroke=0)
    c.setFillColor(ORANGE if "KEY" in label else MUTED)
    c.setFont(BOLD, TYPOGRAPHY["tiny_pt"])
    c.drawCentredString(width - M - 46, height - 29, label)


def draw_cover(path, data, assets):
    c = Canvas(str(path), pagesize=PORTRAIT, pageCompression=1)
    c.setAuthor("CurioNest")
    c.setTitle(data["title"])
    c.setFillColor(CREAM)
    c.rect(0, 0, PW, PH, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.rect(0, 0, 56, PH, fill=1, stroke=0)
    c.setFillColor(ORANGE)
    c.rect(56, PH - 176, 12, 100, fill=1, stroke=0)
    para(c, "CURIONEST", 92, PH - 54, 390, 26, st("cover-brand", 16, 18, NAVY, True))
    para(c, "CHEMISTRY FOUNDATIONS", 92, PH - 98, 420, 34, st("cover-series", 23, 26, NAVY, True))
    para(c, data["short_title"].upper(), 92, PH - 149, 425, 58, st("cover-title", 21, 24, ORANGE, True))
    para(c, "Complete Instructional Unit for U.S. Grades 9-10", 92, PH - 209, 420, 20, st("cover-sub", 10.5, 12.5, MUTED))

    visual = data.get("cover_visual")
    if visual:
        fit_image(c, assets / visual, 432, 404, 122, 232, True)

    para(c, "TEACH  ->  MODEL  ->  PRACTICE  ->  ASSESS", 92, 465, 320, 30, st("cover-flow", 13.5, 17, NAVY, True))
    y = 430
    for line in data["cover_features"]:
        c.setFillColor(ORANGE)
        c.circle(101, y + 3, 3.6, fill=1, stroke=0)
        para(c, line, 115, y + 10, 292, 25, st(f"cover-feature-{y}", 9.8, 12.2))
        y -= 36

    c.setFillColor(NAVY)
    c.roundRect(92, 130, 462, 78, 6, fill=1, stroke=0)
    para(c, data["cover_claim"], 112, 183, 422, 48, st("cover-claim", 14.5, 18, WHITE, True, TA_CENTER))
    para(c, f"{data['lesson_count']} LESSONS  ·  TWO 20-ITEM TEST FORMS  ·  PDF  ·  US LETTER", 92, 101, 462, 20, st("cover-meta", 8.5, 10.4, NAVY, True, TA_CENTER))
    c.setFillColor(MUTED)
    c.setFont(FONT, TYPOGRAPHY["footer_pt"])
    c.drawRightString(PW - M, 34, data.get("cover_credit", data["copyright"]))
    c.showPage()
    c.save()


def draw_teacher_guide(path, data):
    c = Canvas(str(path), pagesize=PORTRAIT, pageCompression=1)
    c.setAuthor("CurioNest")
    c.setTitle(data["title"] + " - Teacher Guide")

    top_rule(c, "TG", "Teacher Quick Start", data["short_title"], "TEACHER GUIDE")
    para(c, "UNIT PURPOSE", M, PH - 94, 150, 15, LABEL)
    para(c, data["unit_purpose"], M, PH - 115, PW - 2 * M, 66, st("purpose", 10.0, 12.6))
    para(c, "INSTRUCTIONAL RHYTHM", M, PH - 178, 180, 15, LABEL)
    para(c, "Engage -> Teach -> Model -> Guided Practice -> Independent Practice -> Exit Ticket -> Mixed Review -> Unit Test", M, PH - 199, PW - 2 * M, 34, st("rhythm", TYPOGRAPHY["student_target_pt"], 13, NAVY, True))
    para(c, "SUGGESTED PACING", M, PH - 249, 180, 15, LABEL)
    y = PH - 271
    for row in data["pacing"]:
        c.setFillColor(ORANGE)
        c.circle(M + 8, y - 1, 7, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont(BOLD, 7.5)
        c.drawCentredString(M + 8, y - 3.5, row["day"])
        para(c, row["plan"], M + 26, y + 8, PW - 2 * M - 26, 42, st(f"pace-{row['day']}", 9.2, 11.4))
        y -= 47
    para(c, "PACKAGE MAP", M, 177, 150, 15, LABEL)
    para(c, "Projectable slides teach the lesson. Student pages provide guided notes, modeled thinking, supported practice, independent practice, and exit tickets. Tests A and B follow all instruction and review. The teacher file contains every answer and rationale.", M, 156, PW - 2 * M, 66, st("package-map", 9.3, 11.7))
    footer(c, PW, 1, "TEACHER GUIDE", data["copyright"])
    c.showPage()

    top_rule(c, "TG", "Instructional Decisions", "Support, monitor, and respond", "TEACHER GUIDE")
    y = PH - 92
    sections = [
        ("BEFORE TEACHING", data["before_teaching"]),
        ("FORMATIVE LOOK-FORS", data["look_fors"]),
        ("SUPPORT", data["support"]),
        ("EXTEND", data["extend"]),
        ("ASSESSMENT USE", "Use Form A after instruction and mixed review. Reserve Form B for retakes, an alternate class period, or test security. Do not use either test as the first exposure to a skill."),
        ("SCOPE", data["release_scope"]["standards_claim"]),
    ]
    for i, (title, body) in enumerate(sections):
        para(c, title, M, y, 140, 14, LABEL)
        used = para(c, body, M + 145, y + 2, PW - 2 * M - 145, 78, st(f"guide-section-{i}", 9.1, 11.3))
        y -= max(55, used + 18)
        if i < len(sections) - 1:
            c.setStrokeColor(LINE)
            c.setLineWidth(0.45)
            c.line(M, y + 9, PW - M, y + 9)
    footer(c, PW, 2, "TEACHER GUIDE", data["copyright"])
    c.showPage()
    c.save()


def visual_block(c, assets, visuals, x, top, width, height):
    if not visuals:
        return
    gap = 7
    box = (width - gap * (len(visuals) - 1)) / len(visuals)
    for i, visual in enumerate(visuals):
        vx = x + i * (box + gap)
        fit_image(c, assets / visual["file"], vx, top - height + 34, box, height - 34, True)
        para(c, visual["caption"], vx, top - height + 30, box, 31, st(f"visual-{visual['file']}-{top}", TYPOGRAPHY["minimum_nonfooter_pt"], 8.5, MUTED, False, TA_CENTER))


def build_slides(path, data, assets):
    c = Canvas(str(path), pagesize=LANDSCAPE, pageCompression=1)
    c.setAuthor("CurioNest")
    c.setTitle(data["title"] + " - Projectable Lesson Slides")
    slide = 0
    for lesson in data["lessons"]:
        visuals = lesson.get("visuals", [])
        slide += 1
        top_rule(c, lesson["number"], lesson["title"], "Engage and notice", "ENGAGE", LW, LH)
        para(c, "LEARNING TARGET", M, LH - 96, 170, 16, LABEL)
        para(c, lesson["target"], M, LH - 119, LW - 2 * M, 52, st(f"slide-target-{slide}", 15.5, 19.2, NAVY, True))
        c.setFillColor(CREAM)
        c.roundRect(M, 142, LW - 2 * M, 252, 8, fill=1, stroke=0)
        para(c, "NOTICE / PREDICT", M + 22, 370, 190, 18, st(f"slide-eng-label-{slide}", TYPOGRAPHY["student_target_pt"], 12, ORANGE, True))
        if visuals:
            para(c, lesson["engage"], M + 22, 334, 430, 132, st(f"slide-eng-{slide}", 21.5, 27, NAVY, True, TA_CENTER))
            visual_block(c, assets, visuals[:1], 520, 362, 206, 178)
            note_x, note_w = M + 28, 430
        else:
            para(c, lesson["engage"], M + 28, 332, LW - 2 * M - 56, 128, st(f"slide-eng-{slide}", 22.5, 28, NAVY, True, TA_CENTER))
            note_x, note_w = M + 45, LW - 2 * M - 90
        para(c, "Be ready to defend your first idea. You may revise it after the lesson.", note_x, 184, note_w, 32, st(f"slide-eng-note-{slide}", 11.5, 14.5, MUTED, False, TA_CENTER))
        footer(c, LW, slide, "PROJECTABLE SLIDE", data["copyright"])
        c.showPage()

        slide += 1
        top_rule(c, lesson["number"], lesson["title"], "Explain the idea", "TEACH", LW, LH)
        left = M
        right = 420
        if not visuals:
            c.setFillColor(WASH)
            c.roundRect(left - 10, 82, 354, 430, 8, fill=1, stroke=0)
            c.setFillColor(CREAM)
            c.roundRect(right - 10, 82, LW - right - M + 20, 430, 8, fill=1, stroke=0)
        para(c, "BIG IDEA", left, LH - 96, 120, 15, LABEL)
        para(c, lesson["big_idea"], left, LH - 120, 334, 102, st(f"slide-big-{slide}", 16.3 if not visuals else 15, 20.4 if not visuals else 19, NAVY, True))
        para(c, "ESSENTIAL TERMS", left, LH - 222, 150, 15, LABEL)
        term_text = "\n".join(f"{t['term']}: {t['definition']}" for t in lesson["terms"])
        para(c, term_text, left, LH - 246, 334, 305, st(f"slide-terms-{slide}", 12.8 if not visuals else 11.2, 16 if not visuals else 14.4))
        if visuals:
            visual_block(c, assets, visuals, right, LH - 92, LW - right - M, 230)
            notes_top = LH - 337
        else:
            notes_top = LH - 96
        para(c, "WHAT TO REMEMBER", right, notes_top, 190, 15, LABEL)
        y = notes_top - 24
        for i, point in enumerate(lesson["teach_points"]):
            c.setFillColor(ORANGE)
            c.circle(right + 7, y - 1, 3.2, fill=1, stroke=0)
            used = para(c, point, right + 18, y + 8, LW - right - M - 18, 72, st(f"slide-point-{slide}-{i}", 12.8 if not visuals else 11.3, 16 if not visuals else 14.2))
            y -= max(64 if not visuals else 47, used + (17 if not visuals else 11))
        footer(c, LW, slide, "PROJECTABLE SLIDE", data["copyright"])
        c.showPage()

        slide += 1
        top_rule(c, lesson["number"], lesson["title"], "Model the reasoning", "MODEL", LW, LH)
        para(c, "WORKED EXAMPLE", M, LH - 96, 170, 15, LABEL)
        para(c, lesson["worked_example"]["prompt"], M, LH - 121, LW - 2 * M, 68, st(f"slide-model-prompt-{slide}", 16, 20, NAVY, True))
        y = LH - 202
        for i, step in enumerate(lesson["worked_example"]["steps"], 1):
            c.setFillColor(ORANGE)
            c.circle(M + 13, y - 4, 11, fill=1, stroke=0)
            c.setFillColor(WHITE)
            c.setFont(BOLD, 9)
            c.drawCentredString(M + 13, y - 7, str(i))
            para(c, step, M + 38, y + 9, LW - 2 * M - 38, 58, st(f"slide-step-{slide}-{i}", 13.2, 16.7))
            y -= 67
        c.setFillColor(NOTE)
        c.roundRect(M, 95, LW - 2 * M, 82, 7, fill=1, stroke=0)
        para(c, "RESULT", M + 18, 155, 100, 14, LABEL)
        para(c, lesson["worked_example"]["answer"], M + 112, 157, LW - 2 * M - 130, 54, st(f"slide-answer-{slide}", 15.5, 19.5, NAVY, True))
        para(c, "CHECK: " + lesson["cfu"], M, 70, LW - 2 * M, 36, st(f"slide-cfu-{slide}", 12.4, 15.5, ORANGE, True, TA_CENTER))
        footer(c, LW, slide, "PROJECTABLE SLIDE", data["copyright"])
        c.showPage()
    c.save()


def build_student(path, data, assets):
    c = Canvas(str(path), pagesize=PORTRAIT, pageCompression=1)
    c.setAuthor("CurioNest")
    c.setTitle(data["title"] + " - Student Guided Notes and Practice")
    page = 0
    for lesson in data["lessons"]:
        page += 1
        top_rule(c, lesson["number"], lesson["title"], "Learn and model", "STUDENT LESSON")
        c.setFillColor(MUTED)
        c.setFont(FONT, 7.6)
        c.drawRightString(PW - M, PH - 73, "Name: ____________________   Date: __________   Period: _____")
        para(c, "TARGET", M, PH - 95, 70, 14, LABEL)
        para(c, lesson["target"], M + 72, PH - 93, PW - 2 * M - 72, 46, st(f"student-target-{page}", TYPOGRAPHY["student_target_pt"], 12.8, NAVY, True))
        c.setFillColor(CREAM)
        c.roundRect(M, PH - 186, PW - 2 * M, 62, 5, fill=1, stroke=0)
        para(c, "ENGAGE", M + 9, PH - 137, 70, 12, LABEL)
        para(c, lesson["engage"], M + 78, PH - 136, PW - 2 * M - 88, 50, st(f"student-engage-{page}", TYPOGRAPHY["practice_prompt_pt"], 11.8))

        para(c, "TEACH", M, PH - 204, 70, 14, LABEL)
        y = PH - 228
        points = lesson["teach_points"]
        for i, point in enumerate(points):
            c.setFillColor(ORANGE)
            c.circle(M + 5, y - 1, 2.5, fill=1, stroke=0)
            used = para(c, point, M + 14, y + 7, 298, 50, st(f"student-point-{page}-{i}", 9.3, 11.7))
            y -= max(40, used + 8)
        para(c, "TERMS", 365, PH - 204, 70, 14, LABEL)
        term_text = "\n".join(f"{t['term']}: {t['definition']}" for t in lesson["terms"])
        para(c, term_text, 365, PH - 228, PW - M - 365, 112, st(f"student-terms-{page}", TYPOGRAPHY["student_teaching_pt"], 11.2))
        visuals = lesson.get("visuals", [])
        if visuals:
            visual_block(c, assets, visuals[:2], 365, PH - 341, PW - M - 365, 118)

        c.setFillColor(WASH)
        c.roundRect(M, 56, PW - 2 * M, 274, 6, fill=1, stroke=0)
        para(c, "WORKED EXAMPLE", M + 12, 313, 150, 14, LABEL)
        para(c, lesson["worked_example"]["prompt"], M + 12, 290, PW - 2 * M - 24, 54, st(f"student-work-prompt-{page}", 10, 12.5, NAVY, True))
        yy = 232
        for i, step in enumerate(lesson["worked_example"]["steps"], 1):
            para(c, f"{i}. {step}", M + 18, yy, PW - 2 * M - 36, 43, st(f"student-work-step-{page}-{i}", 9.2, 11.5))
            yy -= 44
        c.setFillColor(NOTE)
        c.roundRect(M + 12, 68, PW - 2 * M - 24, 47, 4, fill=1, stroke=0)
        para(c, "RESULT: " + lesson["worked_example"]["answer"], M + 22, 102, PW - 2 * M - 44, 35, st(f"student-work-answer-{page}", 9.7, 12.1, NAVY, True))
        footer(c, PW, page, "STUDENT LESSON", data["copyright"])
        c.showPage()

        page += 1
        top_rule(c, lesson["number"], lesson["title"], "Practice and check", "STUDENT PRACTICE")
        c.setFillColor(MUTED)
        c.setFont(FONT, 7.6)
        c.drawRightString(PW - M, PH - 73, "Name: ____________________   Date: __________   Period: _____")
        items = lesson["practice"]
        y = PH - 96
        heights = [118, 108, 108, 108, 98]
        labels = ["GUIDED PRACTICE", "INDEPENDENT", "INDEPENDENT", "INDEPENDENT", "EXIT TICKET"]
        for i, (item, h, label) in enumerate(zip(items, heights, labels)):
            para(c, label, M, y, 108, 14, st(f"practice-label-{page}-{i}", 7.8, 9.5, ORANGE, True))
            para(c, item["id"] + ". " + item["prompt"], M + 110, y + 1, PW - 2 * M - 110, 52, st(f"practice-prompt-{page}-{i}", 9.3, 11.7, INK, True))
            if i == 0:
                para(c, "Scaffold: " + item["scaffold"], M + 18, y - 52, PW - 2 * M - 36, 30, st(f"practice-scaffold-{page}", 8.3, 10.4, MUTED))
            line_y = y - h + 22
            c.setStrokeColor(LINE)
            c.setLineWidth(0.5)
            c.line(M + 18, line_y, PW - M, line_y)
            if h >= 104:
                c.line(M + 18, line_y + 18, PW - M, line_y + 18)
            y -= h + 7
        footer(c, PW, page, "STUDENT PRACTICE", data["copyright"])
        c.showPage()

    for review_page in range(2):
        page += 1
        top_rule(c, "R", "Cumulative Mixed Review", "Use ideas from every lesson", "STUDENT REVIEW")
        c.setFillColor(MUTED)
        c.setFont(FONT, 7.6)
        c.drawRightString(PW - M, PH - 73, "Name: ____________________   Date: __________   Period: _____")
        subset = data["review"][review_page * 5 : review_page * 5 + 5]
        y = PH - 98
        for i, item in enumerate(subset):
            h = 118
            para(c, item["id"] + ". " + item["prompt"], M, y, PW - 2 * M, 58, st(f"review-prompt-{page}-{i}", TYPOGRAPHY["practice_prompt_pt"], 11.8, INK, True))
            c.setStrokeColor(LINE)
            c.line(M + 10, y - h + 24, PW - M, y - h + 24)
            c.line(M + 10, y - h + 44, PW - M, y - h + 44)
            y -= h + 8
        footer(c, PW, page, "STUDENT REVIEW", data["copyright"])
        c.showPage()
    c.save()


def build_test(path, data, form):
    c = Canvas(str(path), pagesize=PORTRAIT, pageCompression=1)
    c.setAuthor("CurioNest")
    c.setTitle(data["title"] + f" - Unit Test {form}")
    items = data["tests"][form]
    for page in range(4):
        top_rule(c, form, f"Unit Test - Form {form}", data["short_title"], "STUDENT ASSESSMENT")
        c.setFillColor(MUTED)
        c.setFont(FONT, 7.6)
        c.drawRightString(PW - M, PH - 73, "Name: ____________________   Date: __________   Period: _____")
        if page == 0:
            para(c, "Directions: Select the best answer for each question. Mark one choice only. Complete this test after all lessons and the cumulative review.", M, PH - 94, PW - 2 * M, 42, st(f"directions-{form}", TYPOGRAPHY["test_choice_pt"], 10.7, MUTED))
            y = PH - 139
        else:
            y = PH - 98
        subset = items[page * 5 : page * 5 + 5]
        available = y - 46
        h = available / 5
        for i, item in enumerate(subset):
            qn = page * 5 + i + 1
            para(c, f"{qn}. {item['stem']}", M, y, PW - 2 * M, 48, st(f"test-stem-{form}-{qn}", TYPOGRAPHY["test_stem_pt"], 11.7, INK, True))
            choice_y = y - 45
            for j, choice in enumerate(item["choices"]):
                used = para(c, f"{chr(65+j)}. {choice}", M + 15, choice_y, PW - 2 * M - 15, 27, st(f"test-choice-{form}-{qn}-{j}", TYPOGRAPHY["test_choice_pt"], 10.4))
                choice_y -= max(18, used + 2)
            c.setStrokeColor(LINE)
            c.setLineWidth(0.4)
            c.line(M, y - h + 7, PW - M, y - h + 7)
            y -= h
        footer(c, PW, page + 1, f"UNIT TEST {form}", data["copyright"])
        c.showPage()
    c.save()


def build_keys(path, data):
    c = Canvas(str(path), pagesize=PORTRAIT, pageCompression=1)
    c.setAuthor("CurioNest")
    c.setTitle(data["title"] + " - Answer Key")
    page = 0
    for lesson in data["lessons"]:
        page += 1
        top_rule(c, lesson["number"], lesson["title"], "Practice answers and repair moves", "TEACHER KEY")
        y = PH - 94
        for i, item in enumerate(lesson["practice"]):
            para(c, item["id"] + ". " + item["prompt"], M, y, PW - 2 * M, 50, st(f"key-prompt-{page}-{i}", 8.9, 11.1, INK, True))
            c.setFillColor(NOTE)
            c.roundRect(M, y - 91, PW - 2 * M, 50, 4, fill=1, stroke=0)
            para(c, "ANSWER: " + item["answer"], M + 10, y - 50, PW - 2 * M - 20, 42, st(f"key-answer-{page}-{i}", 8.7, 10.8, NAVY, True))
            y -= 101
        c.setFillColor(CREAM)
        c.roundRect(M, 50, PW - 2 * M, 93, 5, fill=1, stroke=0)
        para(c, "MISCONCEPTION", M + 10, 130, 105, 12, LABEL)
        para(c, lesson["misconception"], M + 122, 133, PW - 2 * M - 132, 35, st(f"misconception-{page}", 8.3, 10.3))
        para(c, "REPAIR", M + 10, 91, 105, 12, LABEL)
        para(c, lesson["repair"], M + 122, 94, PW - 2 * M - 132, 35, st(f"repair-{page}", 8.3, 10.3, NAVY, True))
        footer(c, PW, page, "TEACHER KEY", data["copyright"])
        c.showPage()

    for review_page in range(2):
        page += 1
        top_rule(c, "R", "Cumulative Review Key", "Answers from all lessons", "TEACHER KEY")
        y = PH - 95
        subset = data["review"][review_page * 5 : review_page * 5 + 5]
        for i, item in enumerate(subset):
            para(c, item["id"] + ". " + item["prompt"], M, y, PW - 2 * M, 50, st(f"review-key-prompt-{page}-{i}", 8.9, 11.1, INK, True))
            c.setFillColor(NOTE)
            c.roundRect(M, y - 96, PW - 2 * M, 54, 4, fill=1, stroke=0)
            para(c, "ANSWER: " + item["answer"], M + 10, y - 52, PW - 2 * M - 20, 45, st(f"review-key-answer-{page}-{i}", TYPOGRAPHY["small_pt"], 10.7, NAVY, True))
            y -= 110
        footer(c, PW, page, "TEACHER KEY", data["copyright"])
        c.showPage()

    for form in ("A", "B"):
        items = data["tests"][form]
        for chunk in range(2):
            page += 1
            top_rule(c, form, f"Unit Test {form} - Rationale Key", "Ten items per page", "TEACHER KEY")
            y = PH - 95
            subset = items[chunk * 10 : chunk * 10 + 10]
            for i, item in enumerate(subset):
                qn = chunk * 10 + i + 1
                letter = chr(65 + item["answer"])
                para(c, f"{qn}. {letter} - {item['choices'][item['answer']]}", M, y, PW - 2 * M, 24, st(f"test-key-head-{form}-{qn}", 9.1, 11.2, ORANGE, True))
                para(c, item["rationale"], M + 18, y - 24, PW - 2 * M - 18, 39, st(f"test-key-rationale-{form}-{qn}", TYPOGRAPHY["small_pt"], 10.7, NAVY, True))
                y -= 61
            footer(c, PW, page, f"UNIT TEST {form} KEY", data["copyright"])
            c.showPage()
    c.save()


def draw_rights(path, data, manifest):
    c = Canvas(str(path), pagesize=PORTRAIT, pageCompression=1)
    c.setAuthor("CurioNest")
    c.setTitle(data["title"] + " - Rights and Sources")
    top_rule(c, "R", "Terms and Instructional Sources", data["short_title"], "RIGHTS & SOURCES")
    c.setFillColor(NOTE)
    c.roundRect(M, PH - 176, PW - 2 * M, 84, 6, fill=1, stroke=0)
    para(c, "LICENSE", M + 10, PH - 107, 95, 13, LABEL)
    para(c, "One educator may use this resource with that educator's own students, including inside a password-protected LMS. Do not share, resell, redistribute, post publicly, or remove credits.", M + 105, PH - 106, PW - 2 * M - 115, 64, st("license", 9.1, 11.4))
    para(c, "INSTRUCTIONAL REFERENCES", M, PH - 204, PW - 2 * M, 15, st("rights-head", TYPOGRAPHY["student_target_pt"], 12.5, NAVY, True))
    y = PH - 228
    for i, src in enumerate(data["sources"]):
        used = para(c, f"{src['organization']} - {src['title']}\n{src['url']}", M + 8, y, PW - 2 * M - 16, 46, st(f"rights-source-{i}", 8.0, 9.8))
        y -= used + 8
    c.setFillColor(WASH)
    c.roundRect(M, 62, PW - 2 * M, 148, 6, fill=1, stroke=0)
    para(c, "SOURCE BOUNDARIES", M + 12, 194, PW - 2 * M - 24, 14, LABEL)
    blocked_text = "\n".join([
        "• No third-party worksheet questions, answers, images, layouts, or packet sequence were used.",
        "• No local textbook text or exercise was adapted for this commercial resource.",
        "• No retired publisher branding appears in buyer-facing files.",
    ])
    para(c, "References verify terminology, science scope, and instructional practice; source exercises and wording are not reproduced.\n" + blocked_text, M + 12, 170, PW - 2 * M - 24, 98, st("reference-note", 8.4, 10.5, NAVY, True))
    footer(c, PW, 1, "RIGHTS & SOURCES", data["copyright"])
    c.showPage()

    top_rule(c, "R", "Visual Credits and Originality", data["short_title"], "RIGHTS & SOURCES")
    para(c, "DOCUMENTED INSTRUCTIONAL VISUALS", M, PH - 96, PW - 2 * M, 15, st("visual-credit-head", TYPOGRAPHY["student_target_pt"], 12.5, NAVY, True))
    y = PH - 121
    for i, item in enumerate(manifest["assets"]):
        text = f"{item['credit']} | {item['license']} | {item.get('source_page', item.get('source', ''))}"
        used = para(c, text, M + 8, y, PW - 2 * M - 16, 43, st(f"rights-visual-{i}", 7.8, 9.6))
        y -= used + 7
    originality_top = max(220, min(420, y - 35))
    originality_bottom = originality_top - 150
    c.setFillColor(CREAM)
    c.roundRect(M, originality_bottom, PW - 2 * M, 150, 6, fill=1, stroke=0)
    para(c, "ORIGINALITY AND EXCLUSIONS", M + 12, originality_top - 17, PW - 2 * M - 24, 14, LABEL)
    para(c, "All lesson text, examples, practice, test items, choices, rationales, and page composition are original to CurioNest. External references verify terminology and U.S. classroom scope only. No third-party worksheet wording, answer, screenshot, logo, distinctive layout, or packet sequence is reproduced or adapted. No AI-generated or code-drawn instructional image is used.", M + 12, originality_top - 41, PW - 2 * M - 24, 101, st("originality", TYPOGRAPHY["student_teaching_pt"], 11.1, NAVY, True))
    footer(c, PW, 2, "RIGHTS & SOURCES", data["copyright"])
    c.showPage()
    c.save()


def combine(output, inputs, title, copyright_line):
    writer = PdfWriter()
    for inp in inputs:
        for page in PdfReader(inp).pages:
            writer.add_page(page)
    writer.add_metadata({"/Title": title, "/Author": "CurioNest", "/Creator": "CurioNest", "/Subject": copyright_line})
    with output.open("wb") as stream:
        writer.write(stream)


def select_pages(output, selections, title, copyright_line):
    writer = PdfWriter()
    for inp, indexes in selections:
        reader = PdfReader(inp)
        for index in indexes:
            writer.add_page(reader.pages[index])
    writer.add_metadata({"/Title": title, "/Author": "CurioNest", "/Creator": "CurioNest", "/Subject": copyright_line})
    with output.open("wb") as stream:
        writer.write(stream)


def build_product(product_dir):
    product = Path(product_dir).resolve()
    source = product / "source"
    assets = product / "assets"
    buyer = product / "output" / "buyer-files"
    upload = product / "output" / "tpt-upload"
    qa = product / "output" / "qa" / "pdf"
    for folder in (buyer, upload, qa):
        folder.mkdir(parents=True, exist_ok=True)
    data = json.loads((source / "source.json").read_text(encoding="utf-8"))
    if data.get("quality_contract_version") != QUALITY_CONTRACT["version"]:
        raise ValueError(
            f"Source quality_contract_version must be {QUALITY_CONTRACT['version']}; "
            f"found {data.get('quality_contract_version', 'missing')}"
        )
    manifest = json.loads((assets / "manifest.json").read_text(encoding="utf-8"))
    prefix = data["file_prefix"]

    cover = qa / "cover.pdf"
    guide = qa / "teacher-guide.pdf"
    keys_only = qa / "keys-only.pdf"
    slides = buyer / f"{prefix}_Lesson_Slides.pdf"
    student = buyer / f"{prefix}_Student_Guided_Notes_and_Practice.pdf"
    test_a = buyer / f"{prefix}_Unit_Test_A.pdf"
    test_b = buyer / f"{prefix}_Unit_Test_B.pdf"
    teacher = buyer / f"{prefix}_Teacher_Guide_and_Answer_Key.pdf"
    rights = buyer / f"{prefix}_Rights_and_Sources.pdf"
    complete = buyer / f"{prefix}_Complete.pdf"
    preview = upload / f"{prefix}_Preview.pdf"

    draw_cover(cover, data, assets)
    draw_teacher_guide(guide, data)
    build_slides(slides, data, assets)
    build_student(student, data, assets)
    build_test(test_a, data, "A")
    build_test(test_b, data, "B")
    build_keys(keys_only, data)
    combine(teacher, [guide, keys_only], data["title"] + " - Teacher Guide and Answer Key", data["copyright"])
    draw_rights(rights, data, manifest)
    combine(complete, [cover, guide, slides, student, test_a, test_b, keys_only, rights], data["title"] + " - Complete", data["copyright"])
    select_pages(
        preview,
        [(cover, [0]), (slides, [1]), (student, [0, 1]), (test_a, [0]), (keys_only, [0])],
        data["title"] + " - Preview",
        data["copyright"],
    )
    return {
        "data": data,
        "buyer": buyer,
        "upload": upload,
        "qa": qa,
        "files": {
            "complete": complete,
            "slides": slides,
            "student": student,
            "test_a": test_a,
            "test_b": test_b,
            "teacher": teacher,
            "rights": rights,
            "preview": preview,
        },
    }


def package_product(product_dir):
    product = Path(product_dir).resolve()
    data = json.loads((product / "source" / "source.json").read_text(encoding="utf-8"))
    if data.get("quality_contract_version") != QUALITY_CONTRACT["version"]:
        raise ValueError(
            f"Source quality_contract_version must be {QUALITY_CONTRACT['version']}; "
            f"found {data.get('quality_contract_version', 'missing')}"
        )
    prefix = data["file_prefix"]
    buyer = product / "output" / "buyer-files"
    upload = product / "output" / "tpt-upload"
    docs = product / "docs"
    names = [
        f"{prefix}_Complete.pdf",
        f"{prefix}_Lesson_Slides.pdf",
        f"{prefix}_Student_Guided_Notes_and_Practice.pdf",
        f"{prefix}_Unit_Test_A.pdf",
        f"{prefix}_Unit_Test_B.pdf",
        f"{prefix}_Teacher_Guide_and_Answer_Key.pdf",
        f"{prefix}_Rights_and_Sources.pdf",
    ]
    package = upload / f"{prefix}_TPT_Package.zip"
    with zipfile.ZipFile(package, "w", zipfile.ZIP_DEFLATED) as archive:
        for name in names:
            archive.write(buyer / name, name)
    for name in ("TPT-LISTING-COPY.md", "TPT-UPLOAD-CHECKLIST.md", "RELEASE-EVIDENCE.md", "QA-REPORT.md", "DEFENDER-SCAN.txt"):
        path = docs / name
        if path.exists():
            shutil.copy2(path, upload / name)
    digest = sha256(package.read_bytes()).hexdigest()
    manifest = {
        "product_id": data["product_id"],
        "quality_contract_version": data["quality_contract_version"],
        "package": package.name,
        "sha256": digest,
        "buyer_files": names,
        "format": "PDF only; no editable file advertised or delivered",
    }
    (upload / "UPLOAD-MANIFEST.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return package, digest
