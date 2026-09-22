import unittest

from cost_mapping.geo import Point, haversine
from cost_mapping.offline import estimate_route


class OfflineTests(unittest.TestCase):
    def test_assumptions_are_visible_and_applied(self):
        a, b = Point(0, 0), Point(0, 1)
        route = estimate_route(a, b, speed_mph=30, road_factor=1.5)
        self.assertAlmostEqual(route.meters, haversine(a, b) * 1.5)
        self.assertAlmostEqual(route.seconds, route.meters / 1609.344 / 30 * 3600)
        self.assertIn("Approximation", route.source)
