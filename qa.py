#!/usr/bin/env python3
"""Repository-level QA for the CurioNest production pipeline.

This command intentionally uses only the Python standard library so the source,
catalog, and packaged artifacts can be checked before optional build dependencies
are installed.

Usage:
    python qa.py all
    python qa.py python
    python qa.py json
    python qa.py catalog
    python qa.py attribution
    python qa.py all --strict
"""

import argparse
import ast
import io
import json
import re
import struct
import sys
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent

MIRROR_KINDS = {
    "header", "learning_objectives", "concept", "practice", "vocabulary",
    "figure", "assess_yourself", "lesson", "fill_blank", "data_table",
    "regents_practice", "review", "answer_key",
}
QUIZ_KINDS = {"header", "instructions", "quiz", "answer_key"}
HUNT_KINDS = {"header", "setup", "stations", "answer_sheet", "answer_key"}
ITEM_KINDS = {
    "learning_objectives", "practice", "vocabulary", "assess_yourself",
    "fill_blank", "regents_practice", "review", "instructions", "quiz",
    "setup", "stations",
}


class Results(object):
    def __init__(self):
        self.passes = 0
        self.warnings = []
        self.failures = []

    def ok(self, message):
        self.passes += 1
        print("PASS  " + message)

    def warn(self, message):
        self.warnings.append(message)
        print("WARN  " + message)

    def fail(self, message):
        self.failures.append(message)
        print("FAIL  " + message)


def load_json(path, results):
    try:
        with path.open("r", encoding="utf-8") as stream:
            return json.load(stream)
    except (OSError, ValueError) as exc:
        results.fail("{}: {}".format(path.relative_to(ROOT), exc))
        return None


def check_python(results):
    print("\n== Python source ==")
    for path in sorted(ROOT.glob("*.py")):
        try:
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source, str(path))
        except (OSError, SyntaxError) as exc:
            results.fail("{}: {}".format(path.name, exc))
            continue

        names = {}
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                names.setdefault(node.name, []).append(node.lineno)
        duplicates = {name: lines for name, lines in names.items() if len(lines) > 1}
        if duplicates:
            results.fail("{}: duplicate top-level definitions {}".format(path.name, duplicates))
        else:
            results.ok("{} parses and has no duplicate top-level definitions".format(path.name))


def product_family(path):
    if path.name.startswith("quiz-"):
        return "quiz", QUIZ_KINDS, {"header", "quiz", "answer_key"}
    if path.name.startswith("hunt-"):
        return "hunt", HUNT_KINDS, {"header", "stations", "answer_sheet", "answer_key"}
    return "mirror", MIRROR_KINDS, {"header", "answer_key"}


def has_answer(item):
    return isinstance(item, dict) and item.get("answer") not in (None, "")


def validate_question(path, label, item, results):
    if not isinstance(item, dict):
        results.fail("{} {} is not an object".format(path.name, label))
        return
    if not has_answer(item):
        results.fail("{} {} has no answer".format(path.name, label))
    if item.get("type") == "mc":
        choices = item.get("choices")
        if not isinstance(choices, list) or len(choices) != 4:
            results.fail("{} {} MC item must have exactly four choices".format(path.name, label))


def check_json(results):
    print("\n== Product JSON ==")
    schema = ROOT / "schemas" / "product.schema.json"
    if schema.exists():
        load_json(schema, results)
        results.ok("schemas/product.schema.json is present and valid JSON")
    else:
        results.fail("schemas/product.schema.json is missing")

    for path in sorted((ROOT / "mirror-json").glob("*.json")):
        data = load_json(path, results)
        if data is None:
            continue
        family, allowed, required = product_family(path)
        title = data.get("title")
        meta = data.get("meta")
        sections = data.get("sections")
        if not isinstance(title, str) or not title.strip():
            results.fail("{} has no title".format(path.name))
        if not isinstance(meta, dict) or not meta.get("file_stem"):
            results.fail("{} has no meta.file_stem".format(path.name))
        if not isinstance(sections, list) or not sections:
            results.fail("{} has no sections".format(path.name))
            continue

        kinds = [section.get("kind") for section in sections if isinstance(section, dict)]
        unknown = sorted(set(kinds) - allowed)
        missing = sorted(required - set(kinds))
        if unknown:
            results.fail("{} has unsupported {} sections: {}".format(path.name, family, unknown))
        if missing:
            results.fail("{} is missing required sections: {}".format(path.name, missing))
        if kinds.count("header") != 1:
            results.fail("{} must contain exactly one header".format(path.name))
        if kinds.count("answer_key") != 1:
            results.fail("{} must contain exactly one answer_key".format(path.name))

        question_count = 0
        for index, section in enumerate(sections, 1):
            if not isinstance(section, dict):
                results.fail("{} section {} is not an object".format(path.name, index))
                continue
            kind = section.get("kind")
            if kind in ITEM_KINDS and not isinstance(section.get("items"), list):
                results.fail("{} section {} ({}) must have an items array".format(path.name, index, kind))
            if kind == "figure":
                image = section.get("image")
                if not image or not (ROOT / image).is_file():
                    results.fail("{} section {} references missing image {}".format(path.name, index, image))
            if kind in {"practice", "quiz", "review", "regents_practice", "stations"}:
                for item_index, item in enumerate(section.get("items", []), 1):
                    question_count += 1
                    validate_question(path, "{} item {}".format(kind, item_index), item, results)
            if kind == "lesson":
                practice = section.get("practice", [])
                if not isinstance(practice, list):
                    results.fail("{} lesson {} practice must be an array".format(path.name, index))
                else:
                    for item_index, item in enumerate(practice, 1):
                        question_count += 1
                        validate_question(path, "lesson {} practice {}".format(index, item_index), item, results)

        if not any(message.startswith(path.name) for message in results.failures):
            results.ok("{} ({}, {} sections, {} answered items)".format(
                path.name, family, len(sections), question_count))


def pdf_page_count(path):
    data = path.read_bytes()
    if not data.startswith(b"%PDF"):
        return None
    counts = [int(match) for match in re.findall(br"/Count\s+(\d+)", data)]
    return max(counts) if counts else None


def png_dimensions(path):
    with path.open("rb") as stream:
        header = stream.read(24)
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", header[16:24])


def valid_docx(path):
    try:
        with zipfile.ZipFile(str(path)) as archive:
            return "word/document.xml" in archive.namelist()
    except (OSError, zipfile.BadZipFile):
        return False


def check_catalog(results):
    print("\n== Catalog and packages ==")
    catalog_path = ROOT / "catalog.json"
    catalog = load_json(catalog_path, results)
    if catalog is None:
        return
    active = catalog.get("active_products")
    if not isinstance(active, list) or not active:
        results.fail("catalog.json has no active_products")
        return

    catalog_dirs = set()
    for product in active:
        pid = product.get("id", "<missing-id>")
        source = ROOT / product.get("source", "")
        package_dir = ROOT / product.get("package_dir", "")
        catalog_dirs.add(package_dir.resolve())
        if not source.is_file():
            results.fail("{} source is missing: {}".format(pid, source.relative_to(ROOT)))
        if not package_dir.is_dir():
            results.fail("{} package directory is missing: {}".format(pid, package_dir.relative_to(ROOT)))
            continue
        for name in product.get("required_files", []):
            if not (package_dir / name).is_file():
                results.fail("{} package is missing {}".format(pid, name))

        product_pdf = package_dir / "product.pdf"
        preview_pdf = package_dir / "preview.pdf"
        cover = package_dir / "cover.png"
        editable = package_dir / "product-editable.docx"
        product_pages = pdf_page_count(product_pdf) if product_pdf.is_file() else None
        preview_pages = pdf_page_count(preview_pdf) if preview_pdf.is_file() else None
        dimensions = png_dimensions(cover) if cover.is_file() else None
        if product_pages is None or product_pages < 4:
            results.fail("{} product.pdf has an invalid page count: {}".format(pid, product_pages))
        if preview_pages != 3:
            results.fail("{} preview.pdf must contain exactly 3 pages (found {})".format(pid, preview_pages))
        if product_pages and preview_pages and preview_pages >= product_pages:
            results.fail("{} preview must be shorter than the product".format(pid))
        if dimensions != (1200, 1200):
            results.fail("{} cover must be 1200x1200 PNG (found {})".format(pid, dimensions))
        if not editable.is_file() or not valid_docx(editable):
            results.fail("{} editable DOCX is missing or invalid".format(pid))
        if product.get("status") != "certified":
            results.warn("{} is {} and must not be published yet".format(pid, product.get("status")))

        product_failures = [message for message in results.failures if message.startswith(pid)]
        if not product_failures:
            results.ok("{} package structure is valid ({} product pages, {} preview pages)".format(
                pid, product_pages, preview_pages))

    actual_dirs = {path.resolve() for path in (ROOT / "products").iterdir() if path.is_dir()}
    extras = sorted(str(path.relative_to(ROOT)) for path in actual_dirs - catalog_dirs)
    if extras:
        results.warn("product directories not listed in catalog.json: {}".format(extras))


def check_attribution(results):
    print("\n== Asset attribution ==")
    manifest = load_json(ROOT / "assets-manifest.json", results)
    if manifest is None:
        return
    assets = manifest.get("assets", [])
    if not assets:
        results.fail("assets-manifest.json has no assets")
        return
    for item in assets:
        pattern = item.get("path_glob", "")
        matches = list(ROOT.glob(pattern)) if pattern else []
        if not matches:
            results.fail("asset manifest pattern has no matches: {}".format(pattern))
        if item.get("verification_status") != "verified":
            results.warn("{}: attribution status is {}".format(pattern, item.get("verification_status")))
        if not item.get("license"):
            results.fail("{}: license is missing".format(pattern))
    if not (ROOT / "ATTRIBUTION.md").is_file():
        results.fail("ATTRIBUTION.md is missing")
    else:
        results.ok("asset manifest covers {} asset groups".format(len(assets)))


def check_environment(results):
    print("\n== Reproducible environment ==")
    required = ["pyproject.toml", "requirements.txt", "package.json", "package-lock.json"]
    for name in required:
        if not (ROOT / name).is_file():
            results.fail("{} is missing".format(name))
    package = load_json(ROOT / "package.json", results)
    lock = load_json(ROOT / "package-lock.json", results)
    if package is not None and lock is not None:
        expected = package.get("dependencies", {}).get("pptxgenjs")
        locked = lock.get("packages", {}).get("node_modules/pptxgenjs", {}).get("version")
        if expected != locked:
            results.fail("pptxgenjs package/lock mismatch: {} != {}".format(expected, locked))
        else:
            results.ok("Node dependency is locked at pptxgenjs {}".format(locked))
        image_size = lock.get("packages", {}).get("node_modules/image-size", {}).get("version")
        if image_size and tuple(int(part) for part in image_size.split(".")[:3]) <= (2, 0, 2):
            results.warn("image-size {} has a known DoS advisory; enforce SECURITY.md asset restrictions".format(image_size))
    if sys.version_info < (3, 10):
        results.warn("QA runtime is Python {}; builders require Python >=3.10".format(
            ".".join(str(value) for value in sys.version_info[:3])))
    else:
        results.ok("Python runtime satisfies >=3.10")
    if not (ROOT / "SECURITY.md").is_file():
        results.fail("SECURITY.md is missing")


def check_tests(results):
    print("\n== Regression tests ==")
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
    stream = io.StringIO()
    outcome = unittest.TextTestRunner(stream=stream, verbosity=1).run(suite)
    if outcome.wasSuccessful():
        results.ok("{} regression tests passed".format(outcome.testsRun))
    else:
        details = stream.getvalue().strip().replace("\n", " | ")
        results.fail("regression tests failed: {}".format(details))


def summarize(results, strict=False):
    print("\n== Summary ==")
    print("PASS={}  WARN={}  FAIL={}".format(
        results.passes, len(results.warnings), len(results.failures)))
    if results.failures:
        return 1
    if strict and results.warnings:
        return 2
    return 0


def main():
    parser = argparse.ArgumentParser(description="CurioNest repository QA")
    parser.add_argument("scope", nargs="?", default="all",
                        choices=["all", "python", "json", "catalog", "attribution", "environment", "tests"])
    parser.add_argument("--strict", action="store_true",
                        help="return a non-zero status when warnings remain")
    args = parser.parse_args()
    results = Results()
    checks = {
        "python": check_python,
        "json": check_json,
        "catalog": check_catalog,
        "attribution": check_attribution,
        "environment": check_environment,
        "tests": check_tests,
    }
    if args.scope == "all":
        for name in ("python", "json", "catalog", "attribution", "environment", "tests"):
            checks[name](results)
    else:
        checks[args.scope](results)
    sys.exit(summarize(results, strict=args.strict))


if __name__ == "__main__":
    main()
