"""Render every final CurioNest PDF page and verify component/complete parity."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess

from PIL import Image, ImageChops, ImageStat
from pypdf import PdfReader

REPO_ROOT = Path(__file__).resolve().parent.parent
QUALITY_CONTRACT_PATH = REPO_ROOT / "product-lines" / "complete-unit-quality-baseline.json"
QUALITY_CONTRACT = json.loads(QUALITY_CONTRACT_PATH.read_text(encoding="utf-8"))


def natural_key(path: Path):
    return [int(part) if part.isdigit() else part for part in re.split(r"(\d+)", path.stem)]


def rendered_pages(folder: Path) -> list[Path]:
    return sorted(folder.glob("page-*.png"), key=natural_key)


def render(pdf: Path, folder: Path, pdftoppm: Path, dpi: int) -> list[Path]:
    folder.mkdir(parents=True, exist_ok=False)
    subprocess.run(
        [str(pdftoppm), "-png", "-r", str(dpi), str(pdf), str(folder / "page")],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    pages = rendered_pages(folder)
    expected = len(PdfReader(pdf).pages)
    if len(pages) != expected:
        raise RuntimeError(f"{pdf.name}: rendered {len(pages)} pages, expected {expected}")
    return pages


def difference_score(left: Path, right: Path) -> float:
    a = Image.open(left).convert("RGB")
    b = Image.open(right).convert("RGB")
    if a.size != b.size:
        return float("inf")
    return sum(ImageStat.Stat(ImageChops.difference(a, b)).mean) / 3


def run(product: Path, pdftoppm: Path, dpi: int, replace: bool) -> Path:
    product = product.resolve()
    data = json.loads((product / "source" / "source.json").read_text(encoding="utf-8"))
    if data.get("quality_contract_version") != QUALITY_CONTRACT["version"]:
        raise ValueError(
            f"Source quality_contract_version must be {QUALITY_CONTRACT['version']}; "
            f"found {data.get('quality_contract_version', 'missing')}"
        )
    prefix = data["file_prefix"]
    buyer = product / "output" / "buyer-files"
    upload = product / "output" / "tpt-upload"
    out = product / "output" / "qa" / "final-renders"
    if out.exists():
        if not replace:
            raise FileExistsError(f"Render folder already exists: {out}")
        shutil.rmtree(out)
    out.mkdir(parents=True)

    filenames = [
        f"{prefix}_Complete.pdf",
        f"{prefix}_Lesson_Slides.pdf",
        f"{prefix}_Student_Guided_Notes_and_Practice.pdf",
        f"{prefix}_Unit_Test_A.pdf",
        f"{prefix}_Unit_Test_B.pdf",
        f"{prefix}_Teacher_Guide_and_Answer_Key.pdf",
        f"{prefix}_Rights_and_Sources.pdf",
    ]
    rendered: dict[str, list[Path]] = {}
    records: dict[str, dict[str, int | str]] = {}
    for filename in filenames:
        pdf = buyer / filename
        if not pdf.exists():
            raise FileNotFoundError(pdf)
        pages = render(pdf, out / pdf.stem, pdftoppm, dpi)
        rendered[filename] = pages
        records[filename] = {"pdf_pages": len(PdfReader(pdf).pages), "rendered_pages": len(pages)}

    preview_name = f"{prefix}_Preview.pdf"
    preview = upload / preview_name
    preview_pages = render(preview, out / preview.stem, pdftoppm, dpi)
    records[preview_name] = {"pdf_pages": len(PdfReader(preview).pages), "rendered_pages": len(preview_pages)}

    complete = rendered[f"{prefix}_Complete.pdf"]
    mappings = {
        f"{prefix}_Lesson_Slides.pdf": list(range(4, 19)),
        f"{prefix}_Student_Guided_Notes_and_Practice.pdf": list(range(19, 31)),
        f"{prefix}_Unit_Test_A.pdf": list(range(31, 35)),
        f"{prefix}_Unit_Test_B.pdf": list(range(35, 39)),
        f"{prefix}_Teacher_Guide_and_Answer_Key.pdf": [2, 3, *range(39, 50)],
        f"{prefix}_Rights_and_Sources.pdf": [50, 51],
    }
    comparisons: dict[str, dict[str, float | int | str]] = {}
    for filename, complete_numbers in mappings.items():
        component_pages = rendered[filename]
        if len(component_pages) != len(complete_numbers):
            raise RuntimeError(f"Mapping count mismatch for {filename}")
        scores = [
            difference_score(component, complete[number - 1])
            for component, number in zip(component_pages, complete_numbers)
        ]
        maximum = max(scores, default=0.0)
        # Poppler output should be pixel-identical because the component pages are
        # the same page objects used in the complete file. A tiny tolerance allows
        # harmless rasterizer rounding while still catching a wrong page.
        if maximum > 0.02:
            raise RuntimeError(f"Component/complete mismatch for {filename}: {maximum:.6f}")
        comparisons[filename] = {
            "compared_pages": len(scores),
            "maximum_mean_pixel_difference": round(maximum, 8),
            "result": "PASS",
        }

    manifest = {
        "product_id": data["product_id"],
        "quality_contract_version": data["quality_contract_version"],
        "dpi": dpi,
        "files": records,
        "total_pdf_pages_rendered": sum(int(record["rendered_pages"]) for record in records.values()),
        "component_to_complete_comparison": comparisons,
        "result": "PASS",
    }
    manifest_path = out / "render-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"PASS: {manifest['total_pdf_pages_rendered']} pages rendered for {data['product_id']}")
    print(manifest_path)
    return manifest_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("product_dir")
    parser.add_argument("--pdftoppm", required=True)
    parser.add_argument("--dpi", type=int, default=120)
    parser.add_argument("--replace", action="store_true")
    args = parser.parse_args()
    run(Path(args.product_dir), Path(args.pdftoppm), args.dpi, args.replace)


if __name__ == "__main__":
    main()
