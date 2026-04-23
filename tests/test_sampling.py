import unittest
from cost_mapping.sampling import sample_grid
from cost_mapping.grid import Grid
from cost_mapping.geo import Point

class SamplingTests(unittest.TestCase):
    def test_round_trip_and_origin_cell(self):
        grid=Grid(0,0,1,1,2,2)
        single=sample_grid(grid,Point(0,0))
        double=sample_grid(grid,Point(0,0),round_trip=True)
        self.assertEqual(single.values[0][0],0)
        self.assertAlmostEqual(double.values[1][1],2*single.values[1][1])
