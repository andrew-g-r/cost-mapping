import unittest

from cost_mapping.routes import from_legacy_directions


class RouteTests(unittest.TestCase):
    def test_all_legs_are_summed(self):
        route = from_legacy_directions(
            [
                {
                    "legs": [
                        {"distance": {"value": 100}, "duration": {"value": 20}},
                        {"distance": {"value": 300}, "duration": {"value": 50}},
                    ]
                }
            ]
        )
        self.assertEqual((route.meters, route.seconds), (400, 70))

    def test_missing_route_is_actionable(self):
        with self.assertRaises(ValueError):
            from_legacy_directions([])
