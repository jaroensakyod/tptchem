"""Build the rebuilt CurioNest Chapter 2 complete instructional unit."""

from pathlib import Path
import sys

PRODUCT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PRODUCT.parent.parent / "tools"))

from curionest_complete_unit import build_product


if __name__ == "__main__":
    result = build_product(PRODUCT)
    for path in result["files"].values():
        print(path)
