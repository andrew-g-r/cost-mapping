import csv
import io
import unittest
from cost_mapping.dataset import Surface
from cost_mapping.grid import Grid
from cost_mapping.export import csv_surface, geojson_surface

class ExportTests(unittest.TestCase):
    def test_geojson_uses_longitude_first(self):
        surface=Surface(Grid(10,20,11,21,2,2),[[1,2],[3,4]])
        data=geojson_surface(surface)
        self.assertEqual(data['features'][0]['geometry']['coordinates'],[20,10])
        self.assertEqual(data['features'][-1]['properties']['value'],4)
        self.assertEqual(len(list(csv.DictReader(io.StringIO(csv_surface(surface))))),4)
