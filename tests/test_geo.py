import unittest
from cost_mapping.geo import Point, haversine

class GeoTests(unittest.TestCase):
    def test_distance_symmetry_and_antimeridian(self):
        a, b = Point(0,179.9), Point(0,-179.9)
        self.assertAlmostEqual(haversine(a,b), haversine(b,a))
        self.assertLess(haversine(a,b), 23000)
        self.assertEqual(haversine(a,a), 0)
        self.assertAlmostEqual(haversine(Point(0,0),Point(0,1)),111195,delta=1)
    def test_bad_coordinates(self):
        for value in ['nan,0','91,0','0,181','0','one,two']:
            with self.assertRaises(ValueError): Point.parse(value)
