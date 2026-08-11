"""Run complete-unit QA for CurioNest Chapter 1."""

from pathlib import Path
import sys

PRODUCT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PRODUCT.parent.parent / "tools"))

from curionest_complete_unit_qa import run_qa


if __name__ == "__main__":
    run_qa(PRODUCT)
