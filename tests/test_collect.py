import unittest

from cost_mapping.collect import RequestBudget, round_trip
from cost_mapping.routes import Route


class CollectionTests(unittest.TestCase):
    def test_round_trip_uses_both_directions(self):
        calls = []

        def provider(a, b):
            calls.append((a, b))
            return Route(10 if a == "home" else 20, 30, "test")

        result = round_trip("home", "job", provider, budget=RequestBudget(2))
        self.assertEqual(calls, [("home", "job"), ("job", "home")])
        self.assertEqual(result.meters, 30)

    def test_round_trip_rejects_insufficient_budget_before_any_call(self):
        calls = []
        budget = RequestBudget(1)
        with self.assertRaises(ValueError):
            round_trip("home", "job", lambda *args: calls.append(args), budget=budget)
        self.assertEqual(calls, [])
        self.assertEqual(budget.used, 0)

    def test_failed_requests_also_count_toward_budget(self):
        budget = RequestBudget(1)

        def fail():
            raise OSError("test")

        with self.assertRaises(OSError):
            budget.call(fail)
        with self.assertRaisesRegex(ValueError, "exhausted"):
            budget.call(fail)
