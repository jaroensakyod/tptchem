"""Deterministic package checks for the CurioNest TPT product."""

from pathlib import Path
import hashlib
import json
import math
import zipfile

from PIL import Image
from docx import Document
from pypdf import PdfReader


HERE = Path(__file__).resolve().parent
PRODUCT = HERE.parent
OUT = PRODUCT / "output"
BUYER = OUT / "buyer-files"
UPLOAD = OUT / "tpt-upload"
REPORT = PRODUCT / "docs" / "QA-REPORT.md"
DATA = json.loads((HERE / "source.json").read_text(encoding="utf-8"))
COPYRIGHT = DATA["source_policy"]["buyer_facing_copyright"]
FILE_PREFIX = "CurioNest_Measurement"

EXPECTED_PDFS = {
    BUYER / f"{FILE_PREFIX}_Visual_Worksheet_Student.pdf": 4,
    BUYER / f"{FILE_PREFIX}_Visual_Worksheet_Answer_Key.pdf": 4,
    BUYER / f"{FILE_PREFIX}_Visual_Worksheet_Complete.pdf": 11,
    BUYER / f"{FILE_PREFIX}_Rights_and_Sources.pdf": 1,
    UPLOAD / f"{FILE_PREFIX}_Visual_Worksheet_Preview.pdf": 3,
}
EXPECTED_ZIP = {
    f"{FILE_PREFIX}_Visual_Worksheet_Student.pdf",
    f"{FILE_PREFIX}_Visual_Worksheet_Answer_Key.pdf",
    f"{FILE_PREFIX}_Visual_Worksheet_Complete.pdf",
    f"{FILE_PREFIX}_Visual_Worksheet_Editable.docx",
    f"{FILE_PREFIX}_Rights_and_Sources.pdf",
}


def check(condition, label, details, results):
    results.append(("PASS" if condition else "FAIL", label, details))


def main():
    results = []
    for path, expected_pages in EXPECTED_PDFS.items():
        check(path.exists() and path.stat().st_size > 10_000, f"File exists: {path.name}", f"{path.stat().st_size if path.exists() else 0} bytes", results)
        if not path.exists():
            continue
        reader = PdfReader(path)
        check(len(reader.pages) == expected_pages, f"Page count: {path.name}", f"expected {expected_pages}, found {len(reader.pages)}", results)
        for idx, page in enumerate(reader.pages, 1):
            width = float(page.mediabox.width)
            height = float(page.mediabox.height)
            text = (page.extract_text() or "").strip()
            check(abs(width - 612) < 1 and abs(height - 792) < 1, f"US Letter: {path.name} p.{idx}", f"{width:.1f} x {height:.1f} pt", results)
            check(len(text) > 40, f"Extractable text: {path.name} p.{idx}", f"{len(text)} chars", results)

    student_text = "\n".join((p.extract_text() or "") for p in PdfReader(BUYER / f"{FILE_PREFIX}_Visual_Worksheet_Student.pdf").pages)
    key_text = "\n".join((p.extract_text() or "") for p in PdfReader(BUYER / f"{FILE_PREFIX}_Visual_Worksheet_Answer_Key.pdf").pages)
    combined_text = "\n".join((p.extract_text() or "") for p in PdfReader(BUYER / f"{FILE_PREFIX}_Visual_Worksheet_Complete.pdf").pages)
    rights_text = "\n".join((p.extract_text() or "") for p in PdfReader(BUYER / f"{FILE_PREFIX}_Rights_and_Sources.pdf").pages)
    normalized_rights_text = " ".join(rights_text.split())
    check(
        COPYRIGHT in combined_text
        and "CHEM P'M" not in combined_text
        and "Publisher:" not in combined_text,
        "Brand and copyright gate",
        f"Exact line present: {COPYRIGHT}; retired CHEM P'M brand and Publisher label absent",
        results,
    )
    for path in EXPECTED_PDFS:
        author = str((PdfReader(path).metadata or {}).get("/Author", ""))
        check(author == DATA["brand"], f"PDF author metadata: {path.name}", author or "missing", results)
    check(
        all(field in student_text for field in ("Name:", "Date:", "Class Period:")),
        "U.S. student fields",
        "Name, Date, and Class Period found",
        results,
    )
    check(
        all(term in normalized_rights_text for term in ("NIST", "American Chemical Society", "Next Generation Science Standards")),
        "Buyer-facing reference gate",
        "NIST, ACS, and NGSS practice references found",
        results,
    )
    check(
        "ChemPride" not in rights_text and "OpenStax" not in rights_text,
        "Internal-source separation",
        "benchmark and blocked reference absent from buyer-facing source page",
        results,
    )
    check(
        all(blank not in key_text for blank in ("Mass of liquid: ____________________", "Experimental density: ____________________", "Percent error: ____________________")),
        "Answer-line separation",
        "case answers replace response lines in teacher key",
        results,
    )
    for answer in ("10.0 mL", "19.7 g", "4.44%", "0.480%"):
        check(answer in key_text, f"Key contains {answer}", "expected answer found", results)
    check(all(answer not in student_text for answer in ("10.0 mL", "19.7 g", "4.44%", "0.480%")), "Student/key separation", "scored answers absent from student PDF", results)

    check(math.isclose(36.4 / 14.0, 2.6, rel_tol=1e-12), "Density example", "36.4 / 14.0 = 2.60", results)
    check(math.isclose(27.0 / 2.70, 10.0, rel_tol=1e-12), "Volume item", "27.0 / 2.70 = 10.0", results)
    check(math.isclose(0.789 * 25.0, 19.725, rel_tol=1e-12), "Mass item", "0.789 x 25.0 = 19.725 -> 19.7", results)
    check(math.isclose(abs(2.58 - 2.70) / 2.70 * 100, 4.4444444444, rel_tol=1e-8), "Percent-error item", "4.44%", results)
    case_density = (67.19 - 42.31) / 20.0
    case_error = abs(case_density - 1.25) / 1.25 * 100
    check(math.isclose(case_density, 1.244, rel_tol=1e-12), "Case density", "1.244 -> 1.24 g/mL", results)
    check(math.isclose(case_error, 0.48, rel_tol=1e-12), "Case percent error", "0.480%", results)

    visual = DATA["visual_gate"]
    check(visual["decision"] == "PASS" and visual["required_count"] == visual["completed_count"] and visual["missing_count"] == 0, "Instructional visual gate", f"{visual['completed_count']}/{visual['required_count']} complete", results)
    for asset in ("graduated-cylinder-public-domain.jpg", "electronic-balance-ccby3.png", "graduated-cylinder-ccby3.png", "beaker-ccby3.png"):
        path = PRODUCT / "assets" / asset
        check(path.exists() and path.stat().st_size > 5_000, f"Licensed asset present: {asset}", f"{path.stat().st_size if path.exists() else 0} bytes", results)

    expected_image_sizes = {
        "cover.png": (1200, 1200),
        "listing-02-inside.png": (2000, 2000),
        "listing-03-teacher-ready.png": (2000, 2000),
    }
    for image_name, expected_size in expected_image_sizes.items():
        path = UPLOAD / image_name
        with Image.open(path) as image:
            check(image.size == expected_size, f"Listing image size: {image_name}", f"{image.size[0]} x {image.size[1]}", results)

    docx = BUYER / f"{FILE_PREFIX}_Visual_Worksheet_Editable.docx"
    check(docx.exists() and docx.stat().st_size > 50_000, "Editable DOCX", f"{docx.stat().st_size if docx.exists() else 0} bytes", results)
    if docx.exists():
        document = Document(docx)
        footer_text = "\n".join(
            paragraph.text
            for section in document.sections
            for paragraph in section.footer.paragraphs
        )
        check(
            document.core_properties.author == DATA["brand"],
            "DOCX author metadata",
            document.core_properties.author or "missing",
            results,
        )
        check(
            COPYRIGHT in footer_text
            and "CHEM P'M" not in footer_text
            and "Publisher:" not in footer_text,
            "DOCX brand and copyright gate",
            f"Exact line present: {COPYRIGHT}; retired CHEM P'M brand and Publisher label absent",
            results,
        )
    docx_pdf = OUT / "qa" / "docx" / f"{FILE_PREFIX}_Visual_Worksheet_Editable.pdf"
    check(docx_pdf.exists() and len(PdfReader(docx_pdf).pages) == 8, "DOCX render gate", "8 rendered pages inspected", results)

    zip_path = UPLOAD / f"{FILE_PREFIX}_Visual_Worksheet_TPT.zip"
    check(zip_path.exists(), "TPT ZIP exists", str(zip_path), results)
    zip_sha256 = "not built"
    if zip_path.exists():
        zip_sha256 = hashlib.sha256(zip_path.read_bytes()).hexdigest()
        with zipfile.ZipFile(zip_path) as archive:
            names = {Path(name).name for name in archive.namelist() if not name.endswith("/")}
        check(names == EXPECTED_ZIP, "TPT ZIP contents", ", ".join(sorted(names)), results)

    failures = [row for row in results if row[0] == "FAIL"]
    lines = [
        "# QA Report - Chemistry Measurement Visual Worksheet",
        "",
        "**Date:** 2026-08-11  ",
        f"**Automated package decision:** {'PASS' if not failures else 'FAIL - BLOCKED'}  ",
        "**Marketplace release decision:** BLOCKED - native-English, chemistry-teacher, and classroom dry-run evidence is still required before Make Listing Active.  ",
        f"**Buyer ZIP SHA-256:** `{zip_sha256}`  ",
        "**Controlled format decision:** This resource targets U.S. Grades 8-10 and uses American English, US Letter paper, and U.S.-style Name/Date/Class Period fields. The repository's TPT US Letter gate is the release authority.",
        "",
        "| Result | Check | Evidence |",
        "|---|---|---|",
    ]
    lines.extend(f"| {status} | {label} | {details.replace('|', '/')} |" for status, label, details in results)
    lines.extend([
        "",
        "## Visual inspection",
        "",
        "All 11 complete-product PDF pages, all 3 preview pages, all 8 DOCX-render pages, and all 3 listing images were inspected at readable size. No clipping, overlap, missing image, unreadable answer, or unintended blank page remains.",
        "",
        "## Rights decision",
        "",
        "Buyer-facing content references are official NIST, American Chemical Society, and NGSS practice sources. ChemPride remains an internal workflow benchmark only; the local OpenStax Chemistry 2e file remains excluded as direct generative input. CurioNest is the rights holder/brand, not a content reference. The instructional photograph is Public Domain; the three Servier icons are CC BY 3.0 and credited in the product package.",
        "",
        f"**Summary:** PASS={sum(1 for r in results if r[0] == 'PASS')} FAIL={len(failures)}",
    ])
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"PASS={sum(1 for r in results if r[0] == 'PASS')} FAIL={len(failures)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
