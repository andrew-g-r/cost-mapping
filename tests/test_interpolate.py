import unittest
from cost_mapping.dataset import Surface
from cost_mapping.grid import Grid
from cost_mapping.geo import Point
from cost_mapping.interpolate import interpolate, resample

class InterpolationTests(unittest.TestCase):
    def test_plane_and_corners(self):
        surface=Surface(Grid(0,0,2,4,2,2),[[0,4],[2,6]])
        self.assertEqual(interpolate(surface,Point(1,2)),3)
        self.assertEqual(interpolate(surface,Point(2,4)),6)
        self.assertEqual(interpolate(surface,Point(0,0)),0)
    def test_resampling_preserves_plane_and_endpoints(self):
        source=Surface(Grid(0,0,2,4,2,2),[[0,4],[2,6]])
        fine=resample(source,3,5)
        self.assertEqual(fine.values,[[0,1,2,3,4],[1,2,3,4,5],[2,3,4,5,6]])
    def test_out_of_bounds_is_not_extrapolated(self):
        surface=Surface(Grid(0,0,1,1,2,2),[[0,1],[1,2]])
        with self.assertRaises(ValueError): interpolate(surface,Point(2,0))
