import unittest

from cost_mapping.units import miles, minutes


class UnitTests(unittest.TestCase):
    def test_exact_conversions(self):
        self.assertAlmostEqual(miles(1609.344, "meters"), 1)
        self.assertAlmostEqual(miles(1.609344, "km"), 1)
        self.assertEqual(minutes(3600, "seconds"), 60)
        self.assertEqual(minutes(2, "hours"), 120)
