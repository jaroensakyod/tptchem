"""Automated instructional, content-structure, package, and file QA for CurioNest units."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from pathlib import Path
import json
import re
import zipfile

import pdfplumber
from PIL import Image, ImageStat
from pypdf import PdfReader

REPO_ROOT = Path(__file__).resolve().parent.parent
QUALITY_CONTRACT_PATH = REPO_ROOT / "product-lines" / "complete-unit-quality-baseline.json"
QUALITY_CONTRACT = json.loads(QUALITY_CONTRACT_PATH.read_text(encoding="utf-8"))


def pdf_text(path):
    return "\n".join((page.extract_text() or "") for page in PdfReader(path).pages)


def minimum_nonfooter_font_size(path):
    sizes = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            sizes.extend(
                float(char["size"])
                for char in page.chars
                if char.get("text", "").strip() and float(char["top"]) < float(page.height) - 35
            )
    return min(sizes, default=0.0)


def normalized(text):
    return re.sub(r"\s+", " ", text.strip().lower())


def max_run(values):
    best = current = 0
    prior = object()
    for value in values:
        current = current + 1 if value == prior else 1
        best = max(best, current)
        prior = value
    return best


def keyed_choice(data, form, stem_fragment):
    matches = [item for item in data["tests"][form] if stem_fragment.lower() in item["stem"].lower()]
    if len(matches) != 1:
        raise ValueError(f"Expected one {form} item containing {stem_fragment!r}; found {len(matches)}")
    item = matches[0]
    return item["choices"][item["answer"]]


def by_id(items, item_id):
    matches = [item for item in items if item.get("id") == item_id]
    if len(matches) != 1:
        raise ValueError(f"Expected one item {item_id!r}; found {len(matches)}")
    return matches[0]


def run_qa(product_dir):
    product = Path(product_dir).resolve()
    source_path = product / "source" / "source.json"
    data = json.loads(source_path.read_text(encoding="utf-8"))
    assets = product / "assets"
    buyer = product / "output" / "buyer-files"
    upload = product / "output" / "tpt-upload"
    docs = product / "docs"
    prefix = data["file_prefix"]
    contract = QUALITY_CONTRACT
    identity = contract["identity"]
    instruction = contract["instruction"]
    package_contract = contract["package"]
    typography = contract["typography"]
    visual_contract = contract["visuals"]
    results = []

    def check(ok, name, evidence):
        results.append((bool(ok), name, str(evidence)))

    check(contract.get("locked_minimum") is True, "Quality contract is locked", contract.get("locked_minimum"))
    check(data.get("quality_contract_version") == contract["version"], "Active quality-contract version", data.get("quality_contract_version", "missing"))
    check(data["brand"] == identity["brand"], "Exact product brand", data["brand"])
    check(data["copyright"] == identity["copyright"], "Exact copyright source line", data["copyright"])
    check(data["target"] == identity["target"], "U.S. target is explicit", data["target"])
    check(data["lesson_count"] == instruction["lesson_count"] and len(data["lessons"]) == instruction["lesson_count"], "Five-lesson instructional sequence", len(data["lessons"]))
    source_visible_text = json.dumps(data, ensure_ascii=False)
    check(not re.search(r"[\u0E00-\u0E7F]", source_visible_text), "American-English source contains no Thai script", "clear")
    check("\ufffd" not in source_visible_text, "Source contains no Unicode replacement characters", "clear")

    all_prompts = []
    for lesson in data["lessons"]:
        number = lesson["number"]
        check(bool(lesson["target"] and lesson["engage"] and lesson["big_idea"]), f"Lesson {number}: target, engage, and big idea", "present")
        check(len(lesson["terms"]) >= instruction["minimum_terms_per_lesson"], f"Lesson {number}: essential vocabulary", len(lesson["terms"]))
        check(len(lesson["teach_points"]) >= instruction["minimum_teach_points_per_lesson"], f"Lesson {number}: explicit teaching points", len(lesson["teach_points"]))
        worked = lesson["worked_example"]
        check(bool(worked["prompt"] and worked["answer"]) and len(worked["steps"]) >= 3, f"Lesson {number}: complete worked example", len(worked["steps"]))
        check(bool(lesson["cfu"]), f"Lesson {number}: check for understanding", "present")
        check(len(lesson["practice"]) == instruction["practice_items_per_lesson"], f"Lesson {number}: guided, independent, and exit sequence", len(lesson["practice"]))
        check(bool(lesson["practice"][0].get("scaffold")), f"Lesson {number}: guided scaffold", lesson["practice"][0].get("scaffold", "missing"))
        check(all(item.get("answer", "").strip() for item in lesson["practice"]), f"Lesson {number}: every practice item keyed", len(lesson["practice"]))
        check(bool(lesson["misconception"] and lesson["repair"]), f"Lesson {number}: misconception and repair move", "present")
        all_prompts.extend(item["prompt"] for item in lesson["practice"])

    check(len(data["review"]) == instruction["mixed_review_items"], "Ten-item cumulative mixed review", len(data["review"]))
    check(all(item.get("answer", "").strip() for item in data["review"]), "Every review item keyed", len(data["review"]))
    all_prompts.extend(item["prompt"] for item in data["review"])

    test_stems = {}
    for form in ("A", "B"):
        items = data["tests"][form]
        blueprint = data["assessment_blueprint"][form]
        check(len(items) == instruction["test_items_per_form"], f"Test {form}: 20 items", len(items))
        check(len(blueprint) == instruction["test_items_per_form"], f"Test {form}: 20-item blueprint", len(blueprint))
        expected_lessons = set(range(1, instruction["lesson_count"] + 1))
        check(set(blueprint) == expected_lessons and min(Counter(blueprint).values()) >= instruction["minimum_assessment_items_per_lesson_per_form"], f"Test {form}: every lesson assessed at least three times", dict(Counter(blueprint)))
        check(all(len(item["choices"]) == instruction["choices_per_test_item"] for item in items), f"Test {form}: exactly four choices per item", "20/20")
        check(all(isinstance(item["answer"], int) and 0 <= item["answer"] <= 3 for item in items), f"Test {form}: exactly one keyed index per item", "20/20")
        check(all(item.get("rationale", "").strip() for item in items), f"Test {form}: rationale for every item", "20/20")
        check(all(len(item.get("rationale", "").strip()) >= 25 for item in items), f"Test {form}: rationales are substantive", "20/20")
        answers = [item["answer"] for item in items]
        counts = Counter(answers)
        check(max_run(answers) <= 3, f"Test {form}: no answer-position run longer than three", max_run(answers))
        check(set(counts) == {0, 1, 2, 3} and max(counts.values()) - min(counts.values()) <= 3, f"Test {form}: balanced answer positions", dict(counts))
        stems = [normalized(item["stem"]) for item in items]
        check(len(stems) == len(set(stems)), f"Test {form}: unique stems", len(set(stems)))
        # Choice case can be scientifically meaningful (for example, g versus G),
        # so preserve capitalization while normalizing only whitespace here.
        check(all(len(set(re.sub(r"\s+", " ", choice.strip()) for choice in item["choices"])) == 4 for item in items), f"Test {form}: unique choices within each item", "20/20")
        test_stems[form] = set(stems)
        all_prompts.extend(item["stem"] for item in items)
    check(not (test_stems["A"] & test_stems["B"]), "No verbatim stem reuse between Forms A and B", len(test_stems["A"] & test_stems["B"]))
    normalized_prompts = [normalized(prompt) for prompt in all_prompts]
    check(len(normalized_prompts) == len(set(normalized_prompts)), "No exact scored-prompt duplication inside product", len(normalized_prompts) - len(set(normalized_prompts)))

    # Independent product-specific spot checks recompute the highest-risk values
    # and assert core classifications. Human teacher review still solves all items.
    if data["product_id"] == "CN-CH01-MATH":
        lesson_2 = data["lessons"][1]
        lesson_4 = data["lessons"][3]
        lesson_5 = data["lessons"][4]
        percent_error = abs(12.4 - 12.0) / 12.0 * 100
        mean = (1.247 + 1.249 + 1.248) / 3
        mean_error = abs(mean - 1.200) / 1.200 * 100
        check(abs(12.4 * 3.20 - 39.68) < 1e-12 and lesson_2["worked_example"]["answer"] == "39.7", "Science audit: multiplication and significant figures", lesson_2["worked_example"]["answer"])
        check("3.33%" in by_id(lesson_4["practice"], "L4-4")["answer"] and abs(percent_error - 3.3333333333) < 1e-8, "Science audit: percent-error calculation", f"{percent_error:.6f}%")
        worked_steps = " ".join(lesson_5["worked_example"]["steps"])
        check("1.248 g/mL" in worked_steps and "4.00%" in worked_steps and abs(mean_error - 4.0) < 1e-10, "Science audit: mean, accuracy, and precision example", f"mean={mean:.3f}; error={mean_error:.2f}%")
        numeric_keys = [
            ("A", "0.0825 L", "82.5 mL"),
            ("A", "12.4 x 3.20", "39.7"),
            ("A", "90.0 km/h", "25.0 m/s"),
            ("A", "mass 57.0 g", "2.85 g/mL"),
            ("A", "density 1.24 g/mL", "31.6 g"),
            ("A", "accepted density is 12.0", "3.33%"),
            ("B", "7400 micrograms", "7.4 mg"),
            ("B", "45.60 / 2.5", "18"),
            ("B", "100.0 - 0.37", "99.6"),
            ("B", "3.60 days", "86.4 h"),
            ("B", "18.0 m/s", "64.8 km/h"),
            ("B", "mass 44.7 g", "2.98 g/mL"),
            ("B", "density 2.50 g/cm^3", "5.96 cm^3"),
            ("B", "accepted mass is 25.0", "4.00%"),
        ]
        for form, fragment, expected_choice in numeric_keys:
            actual = keyed_choice(data, form, fragment)
            check(actual == expected_choice, f"Assessment calculation audit {form}: {fragment}", actual)
    elif data["product_id"] == "CN-CH02-MATTER":
        recovery = (92.0 + 27.6) / 120.0 * 100
        review_answer = by_id(data["review"], "R9")["answer"]
        check("99.7%" in review_answer and abs(recovery - 99.6666666667) < 1e-8, "Science audit: percent recovery", f"{recovery:.6f}%")
        concept_keys = [
            ("A", "Which sample is matter", "Air in a sealed syringe"),
            ("A", "evenly distributed", "Homogeneous mixture"),
            ("A", "clean copper wire", "Element"),
            ("A", "pure water", "Compound"),
            ("A", "physical and intensive", "Density"),
            ("A", "decisive evidence", "New substances with different compositions form."),
            ("A", "insoluble sand", "Filtration"),
            ("A", "120.0 g sample", "99.7%"),
            ("B", "not evidence that something is matter", "It is visible."),
            ("B", "identical particles made of two different atom types", "Compound"),
            ("B", "two physical properties", "Density and conductivity"),
            ("B", "Which property is extensive", "Volume"),
            ("B", "observation alone is insufficient", "Bubbles appear."),
            ("B", "immiscible liquid layers", "Decantation or a separatory funnel"),
            ("B", "central to distillation", "Volatility or boiling behavior"),
            ("B", "correctly applies conservation", "Gas products count even if they leave an open container."),
        ]
        for form, fragment, expected_choice in concept_keys:
            actual = keyed_choice(data, form, fragment)
            check(actual == expected_choice, f"Assessment concept audit {form}: {fragment}", actual)

    manifest = json.loads((assets / "manifest.json").read_text(encoding="utf-8"))
    lesson_visual_files = {
        visual["file"]
        for lesson in data["lessons"]
        for visual in lesson.get("visuals", [])
    }
    lessons_with_visuals = sum(bool(lesson.get("visuals")) for lesson in data["lessons"])
    manifest_files = {item["file"] for item in manifest["assets"]}
    used_visual_files = lesson_visual_files | {data["cover_visual"]}
    check(len(manifest["assets"]) >= visual_contract["minimum_unique_assets_per_unit"], "Quality baseline: minimum documented instructional visuals", len(manifest["assets"]))
    check(lessons_with_visuals >= visual_contract["minimum_lessons_with_instructional_visuals"], "Quality baseline: lessons with instructional visuals", lessons_with_visuals)
    check(used_visual_files <= manifest_files, "Every placed or cover visual is documented in the manifest", sorted(used_visual_files - manifest_files) or "complete")
    check(manifest_files <= used_visual_files, "Every manifest visual has a product placement", sorted(manifest_files - used_visual_files) or "complete")
    allowed = set(visual_contract["allowed_licenses"])
    for item in manifest["assets"]:
        path = assets / item["file"]
        check(path.exists() and path.stat().st_size > 10_000, f"Visual exists: {item['file']}", path.stat().st_size if path.exists() else 0)
        check(item["license"] in allowed, f"Commercial-use-compatible visual license: {item['file']}", item["license"])
        source_url = item.get("source_page", item.get("source", ""))
        check(source_url.startswith("https://"), f"HTTPS visual provenance: {item['file']}", source_url)
        check(bool(item.get("credit", "").strip()), f"Visual credit recorded: {item['file']}", item.get("credit", "missing"))

    page_contract = package_contract["pages"]
    expected = {
        f"{prefix}_Complete.pdf": page_contract["complete"],
        f"{prefix}_Lesson_Slides.pdf": page_contract["lesson_slides"],
        f"{prefix}_Student_Guided_Notes_and_Practice.pdf": page_contract["student_guided_notes_and_practice"],
        f"{prefix}_Unit_Test_A.pdf": page_contract["unit_test_a"],
        f"{prefix}_Unit_Test_B.pdf": page_contract["unit_test_b"],
        f"{prefix}_Teacher_Guide_and_Answer_Key.pdf": page_contract["teacher_guide_and_answer_key"],
        f"{prefix}_Rights_and_Sources.pdf": page_contract["rights_and_sources"],
    }
    texts = {}
    for name, pages in expected.items():
        path = buyer / name
        check(path.exists(), f"Buyer file exists: {name}", path)
        if not path.exists():
            continue
        reader = PdfReader(path)
        text = pdf_text(path)
        texts[name] = text
        check(len(reader.pages) == pages, f"Page count: {name}", len(reader.pages))
        check(path.stat().st_size > 50_000, f"Nontrivial PDF size: {name}", path.stat().st_size)
        min_font = minimum_nonfooter_font_size(path)
        check(min_font >= typography["minimum_nonfooter_pt"] - 0.01, f"No nonfooter text below {typography['minimum_nonfooter_pt']} pt: {name}", round(min_font, 2))
        check(reader.metadata.get("/Author") == "CurioNest", f"Author metadata: {name}", reader.metadata.get("/Author"))
        check(data["copyright"] in text, f"Exact copyright in: {name}", data["copyright"])
        sizes = {(round(float(p.mediabox.width)), round(float(p.mediabox.height))) for p in reader.pages}
        check(sizes <= {(612, 792), (792, 612)}, f"US Letter portrait/landscape only: {name}", sorted(sizes))
        low = text.lower()
        check("chem p'm" not in low and "chem_pm" not in low and "publisher:" not in low, f"No retired brand/publisher in: {name}", "clear")
        check("chempride" not in low and "openstax" not in low and "chemistry 2e" not in low, f"No blocked authoring source named in: {name}", "clear")
        check(not re.search(r"[\u0E00-\u0E7F]", text), f"American-English buyer PDF contains no Thai script: {name}", "clear")
        check("\ufffd" not in text, f"Buyer PDF contains no Unicode replacement character: {name}", "clear")

    actual_buyer_files = {path.name for path in buyer.iterdir() if path.is_file()}
    check(actual_buyer_files == set(expected), "Buyer folder contains exactly seven current PDFs", sorted(actual_buyer_files))

    student_text = texts.get(f"{prefix}_Student_Guided_Notes_and_Practice.pdf", "")
    slides_text = texts.get(f"{prefix}_Lesson_Slides.pdf", "")
    teacher_text = texts.get(f"{prefix}_Teacher_Guide_and_Answer_Key.pdf", "")
    test_a_text = texts.get(f"{prefix}_Unit_Test_A.pdf", "")
    test_b_text = texts.get(f"{prefix}_Unit_Test_B.pdf", "")
    for phrase in ("TARGET", "ENGAGE", "TEACH", "WORKED EXAMPLE", "GUIDED PRACTICE", "INDEPENDENT", "EXIT TICKET", "CUMULATIVE MIXED REVIEW"):
        check(phrase in student_text.upper(), f"Student sequence includes: {phrase}", "present")
    for phrase in ("ENGAGE", "TEACH", "MODEL", "WORKED EXAMPLE", "CHECK:"):
        check(phrase in slides_text, f"Slides include: {phrase}", "present")
    check("ANSWER:" not in student_text, "Student lesson file contains no answer labels", "clear")
    check("ANSWER:" not in test_a_text and "ANSWER:" not in test_b_text, "Student tests contain no answer labels", "clear")
    check(teacher_text.count("ANSWER:") == 35, "Teacher key contains 25 practice and 10 review answers", teacher_text.count("ANSWER:"))
    check("MISCONCEPTION" in teacher_text and "REPAIR" in teacher_text, "Teacher key includes misconception repair", "present")
    check("UNIT TEST A - RATIONALE KEY" in teacher_text.upper() and "UNIT TEST B - RATIONALE KEY" in teacher_text.upper(), "Teacher file includes both rationale keys", "present")

    preview = upload / f"{prefix}_Preview.pdf"
    check(preview.exists() and len(PdfReader(preview).pages) == page_contract["preview"], "Six-page truthful preview", len(PdfReader(preview).pages) if preview.exists() else 0)
    if preview.exists():
        preview_text = pdf_text(preview)
        check("WORKED EXAMPLE" in preview_text and "GUIDED PRACTICE" in preview_text and "ANSWER:" in preview_text, "Preview demonstrates teaching, practice, and answer support", "present")
        preview_reader = PdfReader(preview)
        check(preview_reader.metadata.get("/Author") == "CurioNest", "Preview author metadata", preview_reader.metadata.get("/Author"))
        check(not re.search(r"[\u0E00-\u0E7F]", preview_text) and "\ufffd" not in preview_text, "American-English preview text is clean", "clear")

    listing_names = ("listing-01-cover.png", "listing-02-teach-practice.png", "listing-03-assessment-key.png")
    check(len(listing_names) == package_contract["listing_images"]["count"], "Quality baseline: listing-image count", len(listing_names))
    for name in listing_names:
        path = upload / name
        check(path.exists(), f"Listing image exists: {name}", path)
        if path.exists():
            image = Image.open(path).convert("RGB")
            expected_listing_size = (
                package_contract["listing_images"]["width_px"],
                package_contract["listing_images"]["height_px"],
            )
            check(image.size == expected_listing_size, f"Listing image size: {name}", image.size)
            check(sum(ImageStat.Stat(image).var) > 100, f"Listing image is not blank: {name}", round(sum(ImageStat.Stat(image).var), 1))

    listing_path = docs / "TPT-LISTING-COPY.md"
    listing = listing_path.read_text(encoding="utf-8") if listing_path.exists() else ""
    for phrase in ("15 projectable lesson slides", "12 student lesson, practice, and review pages", "Unit Test A", "Unit Test B", "20 multiple-choice items per form", "PDF only", "US Letter", "American English"):
        check(phrase in listing, f"Listing exact claim: {phrase}", "present" if phrase in listing else "missing")
    check("does not claim formal NGSS alignment" in listing, "Listing avoids unverified NGSS alignment", "present" if "does not claim formal NGSS alignment" in listing else "missing")
    check("Editable" not in listing and "editable" not in listing, "Listing does not advertise an editable file", "clear")
    listing_low = listing.lower()
    check(not any(term in listing_low for term in ("chempride", "chem p'm", "chem_pm", "openstax", "chemistry 2e")), "Listing contains no blocked-source or retired-brand name", "clear")
    check(not re.search(r"[\u0E00-\u0E7F]", listing) and "\ufffd" not in listing, "American-English listing text is clean", "clear")

    package = upload / f"{prefix}_TPT_Package.zip"
    wanted = set(expected)
    check(package.exists(), "Buyer ZIP exists", package)
    if package.exists():
        with zipfile.ZipFile(package) as archive:
            names = set(archive.namelist())
            bad = archive.testzip()
        check(names == wanted, "ZIP contains exactly seven verified buyer PDFs", sorted(names))
        check(bad is None, "ZIP integrity", bad or "PASS")
        digest = sha256(package.read_bytes()).hexdigest()
        upload_manifest_path = upload / "UPLOAD-MANIFEST.json"
        upload_manifest = json.loads(upload_manifest_path.read_text(encoding="utf-8")) if upload_manifest_path.exists() else {}
        check(upload_manifest.get("sha256") == digest, "Manifest SHA-256 matches buyer ZIP", digest)
        check(upload_manifest.get("quality_contract_version") == contract["version"], "Manifest quality-contract version", upload_manifest.get("quality_contract_version", "missing"))
        check(upload_manifest.get("buyer_files") == list(expected), "Manifest inventory matches buyer files", upload_manifest.get("buyer_files", []))
        check(package.stat().st_size < 50 * 1024 * 1024, "Buyer ZIP is below 50 MB", package.stat().st_size)

    rights_path = docs / "RIGHTS-AND-SOURCES.md"
    rights_text = rights_path.read_text(encoding="utf-8").lower() if rights_path.exists() else ""
    check("no ai-generated" in rights_text and "no code-drawn" in rights_text, "Rights record excludes generated/drawn instructional images", "present" if rights_text else "missing")
    release_path = docs / "RELEASE-EVIDENCE.md"
    release_text = release_path.read_text(encoding="utf-8") if release_path.exists() else ""
    check("BLOCKED - HUMAN REVIEW PENDING" in release_text, "Three human gates block publication", "blocked")
    defender_path = docs / "DEFENDER-SCAN.txt"
    defender_text = defender_path.read_text(encoding="utf-8") if defender_path.exists() else ""
    check("no threats found" in defender_text.lower(), "Exact final ZIP has a recorded no-threat result", "present" if defender_text else "missing")
    if package.exists():
        digest = sha256(package.read_bytes()).hexdigest()
        check(digest in defender_text, "Defender record names the exact final ZIP SHA-256", digest)
        check(digest in release_text, "Release evidence names the exact final ZIP SHA-256", digest)

    render_manifest_path = product / "output" / "qa" / "final-renders" / "render-manifest.json"
    render_manifest = json.loads(render_manifest_path.read_text(encoding="utf-8")) if render_manifest_path.exists() else {}
    check(render_manifest.get("quality_contract_version") == contract["version"], "Render manifest quality-contract version", render_manifest.get("quality_contract_version", "missing"))
    check(render_manifest.get("result") == "PASS", "Every final PDF has a completed render manifest", render_manifest.get("result", "missing"))
    check(render_manifest.get("total_pdf_pages_rendered") == package_contract["total_final_pdf_pages"], "All 107 final PDF pages rendered", render_manifest.get("total_pdf_pages_rendered", 0))
    comparisons = render_manifest.get("component_to_complete_comparison", {})
    check(len(comparisons) == 6 and all(item.get("result") == "PASS" for item in comparisons.values()), "All six component PDFs match the complete unit", len(comparisons))

    obsolete_uploads = {"listing-02-student-pages.png", "listing-03-answer-key.png", "preview-cover.pdf"}
    check(not any((upload / name).exists() for name in obsolete_uploads), "Obsolete upload artifacts removed", "clear")

    passed = sum(ok for ok, _, _ in results)
    total = len(results)
    report = [
        f"# Automated QA Report - {data['product_id']}",
        "",
        f"**Result:** {'PASS' if passed == total else 'FAIL'} ({passed}/{total})",
        "",
        "> Automated PASS does not authorize publication. Native-English, U.S. chemistry-teacher, and classroom dry-run gates remain mandatory.",
        "",
        f"Source SHA-256: `{sha256(source_path.read_bytes()).hexdigest()}`",
        f"Quality contract: `{contract['contract_id']} {contract['version']}`",
        "",
    ]
    for ok, name, evidence in results:
        report.append(f"- [{'x' if ok else ' '}] {name} - `{evidence}`")
    (docs / "QA-REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"{'PASS' if passed == total else 'FAIL'} {passed}/{total}")
    if passed != total:
        for ok, name, evidence in results:
            if not ok:
                print("FAIL", name, evidence)
        raise SystemExit(1)
    return passed, total
