import tempfile
import unittest
from pathlib import Path

from cost_mapping.imports import load_gigs


class ImportTests(unittest.TestCase):
    def test_example_loads(self):
        self.assertEqual(len(load_gigs(Path(__file__).parents[1] / "examples/gigs.csv")), 3)

    def test_bad_rows_report_line_number(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "gigs.csv"
            path.write_text("name,payout,miles,driving_minutes\nA,nope,1,3\n")
            with self.assertRaisesRegex(ValueError, "line 2"):
                load_gigs(path)
