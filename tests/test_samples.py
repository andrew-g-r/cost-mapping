import unittest
from cost_mapping.samples import sample_surface

class SampleTests(unittest.TestCase):
    def test_legacy_sample_orientation_and_endpoint(self):
        surface=sample_surface()
        self.assertEqual((surface.grid.rows,surface.grid.columns),(16,16))
        self.assertAlmostEqual(surface.values[1][0],36.10051325388047)
        self.assertLess(surface.grid.north,30.660661)
        self.assertIn('unverified',surface.source)
