import unittest

from cost_mapping.economics import Assumptions, Gig, evaluate


class EconomicsTests(unittest.TestCase):
    def test_known_cost_and_hourly_result(self):
        result = evaluate(
            Gig("Delivery", 30, 10, 20, work_minutes=10, tolls=2, parking=1), Assumptions(0.5, 20)
        )
        self.assertEqual(result["cash_cost"], 8)
        self.assertEqual(result["net_earnings"], 22)
        self.assertEqual(result["effective_hourly"], 44)
        self.assertEqual(result["minimum_payout"], 18)
        self.assertTrue(result["meets_target"])

    def test_waiting_time_changes_earnings_not_cash_cost(self):
        first = evaluate(Gig("A", 20, 5, 30))
        second = evaluate(Gig("A", 20, 5, 30, waiting_minutes=30))
        self.assertEqual(first["cash_cost"], second["cash_cost"])
        self.assertEqual(first["effective_hourly"] / 2, second["effective_hourly"])

    def test_underflow_and_combined_cost_overflow_are_rejected(self):
        with self.assertRaises(ValueError):
            evaluate(Gig("Tiny", 1, 1, 5e-324))
        with self.assertRaises(ValueError):
            evaluate(Gig("Huge", 1e308, 1, 60), Assumptions(1e308, 1e308))

    def test_overflow_is_reported_instead_of_serialized(self):
        with self.assertRaises(ValueError):
            evaluate(Gig("Huge", 1, 1e308, 1), Assumptions(1e308, 20))

    def test_zero_time_negative_values_and_nan(self):
        for args in [("A", 10, 1, 0), ("A", 10, -1, 1), ("A", float("nan"), 1, 1)]:
            with self.assertRaises(ValueError):
                Gig(*args)
