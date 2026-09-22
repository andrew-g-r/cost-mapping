import unittest

from cost_mapping.grid import Grid


class GridTests(unittest.TestCase):
    def test_rectangular_grid_includes_bounds(self):
        grid = Grid(0, 10, 2, 14, 3, 5)
        self.assertEqual(grid.latitudes, [0, 1, 2])
        self.assertEqual(grid.longitudes, [10, 11, 12, 13, 14])
        self.assertEqual(len(grid.points()), 15)

    def test_invalid_dimensions(self):
        for args in [(0, 0, 0, 1), (0, 0, 1, 1, 1, 2), (0, 0, 1, 1, 1000, 1000)]:
            with self.assertRaises(ValueError):
                Grid(*args)
