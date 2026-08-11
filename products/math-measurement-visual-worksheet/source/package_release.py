"""Create the seller upload folder and deterministic CurioNest buyer ZIP."""

from hashlib import sha256
from pathlib import Path
import shutil
import zipfile


HERE = Path(__file__).resolve().parent
PRODUCT = HERE.parent
BUYER = PRODUCT / "output" / "buyer-files"
UPLOAD = PRODUCT / "output" / "tpt-upload"
DOCS = PRODUCT / "docs"
PREFIX = "CurioNest_Measurement"

BUYER_FILES = [
    f"{PREFIX}_Visual_Worksheet_Student.pdf",
    f"{PREFIX}_Visual_Worksheet_Answer_Key.pdf",
    f"{PREFIX}_Visual_Worksheet_Complete.pdf",
    f"{PREFIX}_Visual_Worksheet_Editable.docx",
    f"{PREFIX}_Rights_and_Sources.pdf",
]


def main():
    UPLOAD.mkdir(parents=True, exist_ok=True)
    for name in BUYER_FILES:
        path = BUYER / name
        if not path.is_file():
            raise FileNotFoundError(path)

    for name in ("TPT-LISTING-COPY.md", "TPT-UPLOAD-CHECKLIST.md", "RELEASE-EVIDENCE.md"):
        shutil.copy2(DOCS / name, UPLOAD / name)

    zip_path = UPLOAD / f"{PREFIX}_Visual_Worksheet_TPT.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name in sorted(BUYER_FILES):
            archive.write(BUYER / name, arcname=name)

    digest = sha256(zip_path.read_bytes()).hexdigest()
    evidence = UPLOAD / "UPLOAD-EVIDENCE.txt"
    evidence.write_text(
        "CurioNest Measurement Visual Worksheet\n"
        "Automated package build: 2026-08-11\n"
        f"Buyer ZIP: {zip_path.name}\n"
        f"SHA-256: {digest}\n"
        "Release status: BLOCKED - human review gates pending\n"
        "Copyright: © 2026 CurioNest · For classroom use only\n"
        "Review RELEASE-EVIDENCE.md before Make Listing Active.\n",
        encoding="utf-8",
    )
    print(zip_path)
    print(digest)


if __name__ == "__main__":
    main()
