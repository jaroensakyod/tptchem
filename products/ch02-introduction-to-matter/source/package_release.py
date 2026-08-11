"""Package the rebuilt CurioNest Chapter 2 buyer files."""

from pathlib import Path
import sys

PRODUCT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PRODUCT.parent.parent / "tools"))

from curionest_complete_unit import package_product


if __name__ == "__main__":
    package, digest = package_product(PRODUCT)
    print(package)
    print(digest)
