import unittest
from cost_mapping.dataset import Surface
from cost_mapping.grid import Grid

class DatasetTests(unittest.TestCase):
    def test_roundtrip_preserves_axes_and_units(self):
        surface=Surface(Grid(0,0,1,2,2,3),[[1,2,3],[4,5,6]])
        self.assertEqual(Surface.from_dict(surface.to_dict()),surface)
    def test_nonfinite_and_mismatched_data_rejected(self):
        for data in [[[1,2]],[[1,2],[3,float('nan')]]]:
            with self.assertRaises(ValueError): Surface(Grid(0,0,1,1,2,2),data)
