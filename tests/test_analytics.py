import contextlib
import csv
import io
import json
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import analytics


class AnalyticsTests(unittest.TestCase):
    def test_stable_product_id_is_deterministic(self):
        first = analytics.stable_product_id("Acids and Bases Worksheet")
        second = analytics.stable_product_id("  acids AND bases worksheet  ")
        self.assertEqual(first, second)
        self.assertTrue(first.startswith("CSV-"))

    def test_import_snapshot_upserts_same_date(self):
        with tempfile.TemporaryDirectory() as temp_name:
            temp = Path(temp_name)
            data_path = temp / "kpi.json"
            csv_path = temp / "stats.csv"
            analytics.save(str(data_path), {
                "schema_version": 1, "updated": None, "products": {}
            })
            with csv_path.open("w", newline="", encoding="utf-8") as stream:
                writer = csv.DictWriter(stream, fieldnames=["Product ID", "Title", "Views", "Sales", "Earnings"])
                writer.writeheader()
                writer.writerow({"Product ID": "123", "Title": "Test Product", "Views": "10", "Sales": "2", "Earnings": "$7.00"})
            args = SimpleNamespace(file=str(csv_path), mode="snapshot", date="2026-08-10")
            with contextlib.redirect_stdout(io.StringIO()):
                analytics.cmd_import(args, str(data_path))
                analytics.cmd_import(args, str(data_path))
            data = json.loads(data_path.read_text(encoding="utf-8"))
            snapshots = data["products"]["TPT-123"]["statistics_snapshots"]
            self.assertEqual(len(snapshots), 1)
            self.assertEqual(snapshots[0]["views"], 10)

    def test_report_flags_use_each_products_own_metrics(self):
        today = date.today().isoformat()
        data = {
            "schema_version": 1,
            "updated": None,
            "products": {
                "A": {
                    "title": "A", "daily": [{"date": today, "views": 5, "sales": 0, "revenue": 0.0}],
                    "keywords": [], "ab_tests": []
                },
                "B": {
                    "title": "B", "daily": [{"date": today, "views": 10, "sales": 3, "revenue": 9.0}],
                    "keywords": [], "ab_tests": []
                }
            }
        }
        with tempfile.TemporaryDirectory() as temp_name:
            data_path = Path(temp_name) / "kpi.json"
            data_path.write_text(json.dumps(data), encoding="utf-8")
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                analytics.cmd_report(SimpleNamespace(days=7), str(data_path))
        lines = output.getvalue().splitlines()
        line_a = next(line for line in lines if line.startswith("A "))
        line_b = next(line for line in lines if line.startswith("B "))
        self.assertIn("conversion", line_a)
        self.assertNotIn("sequel", line_a)
        self.assertIn("sequel", line_b)


if __name__ == "__main__":
    unittest.main()
