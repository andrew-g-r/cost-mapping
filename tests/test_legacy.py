import importlib
import unittest

class LegacyTests(unittest.TestCase):
    def test_legacy_modules_import_without_network_or_plotting_dependencies(self):
        self.assertTrue(callable(importlib.import_module('cost_gmaps_request_data').main))
        self.assertTrue(callable(importlib.import_module('cost_map_renderer').main))
