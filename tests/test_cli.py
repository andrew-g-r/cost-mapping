import json
import subprocess
import sys
import unittest


class CLITests(unittest.TestCase):
    def cli(self, *args):
        return subprocess.run(
            [sys.executable, "-m", "cost_mapping", *args], text=True, capture_output=True
        )

    def test_live_route_dry_run_needs_no_key(self):
        result = self.cli(
            "route",
            "--origin",
            "30,-97",
            "--destination",
            "30.1,-97.1",
            "--provider",
            "google",
            "--round-trip",
            "--dry-run",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["requests"], 2)

    def test_comparison_ranks_by_earnings(self):
        result = self.cli("compare", "examples/gigs.csv")
        self.assertEqual(result.returncode, 0, result.stderr)
        values = [row["effective_hourly"] for row in json.loads(result.stdout)]
        self.assertEqual(values, sorted(values, reverse=True))

    def test_evaluate_and_bad_input(self):
        args = ["evaluate", "--payout", "30", "--miles", "10", "--driving-minutes", "30"]
        result = self.cli(*args)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["net_earnings"], 27)
        self.assertEqual(self.cli(*args, "--tolls", "-1").returncode, 2)
