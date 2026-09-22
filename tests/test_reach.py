import unittest

from cost_mapping.dataset import Surface
from cost_mapping.grid import Grid
from cost_mapping.reach import describe, within_budget


class ReachTests(unittest.TestCase):
    def test_threshold_is_inclusive(self):
        surface = Surface(Grid(0, 0, 1, 1, 2, 2), [[0, 5], [10, 15]], "minutes")
        self.assertEqual(len(within_budget(surface, 5)), 2)
        self.assertEqual(describe(surface)["mean"], 7.5)
