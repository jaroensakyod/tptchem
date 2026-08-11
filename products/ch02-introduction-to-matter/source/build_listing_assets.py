"""Build verified Chapter 2 TPT listing images."""

from pathlib import Path
import sys

PRODUCT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PRODUCT.parent.parent / "tools"))

from curionest_complete_unit_listing import build


if __name__ == "__main__":
    for output in build(PRODUCT):
        print(output)
