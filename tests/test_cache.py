import tempfile
import unittest
from pathlib import Path

from cost_mapping.cache import RouteCache
from cost_mapping.routes import Route


class CacheTests(unittest.TestCase):
    def test_ttl_and_replacement(self):
        with tempfile.TemporaryDirectory() as folder:
            now = [100]
            cache = RouteCache(Path(folder) / "cache.sqlite3", ttl=10, clock=lambda: now[0])
            cache.put("a", Route(1, 2, "synthetic"))
            self.assertEqual(cache.get("a").meters, 1)
            now[0] = 110
            self.assertIsNone(cache.get("a"))
            self.assertEqual(cache.clear_expired(), 1)

    def test_google_data_is_not_persisted(self):
        with tempfile.TemporaryDirectory() as folder:
            cache = RouteCache(Path(folder) / "cache.sqlite3")
            with self.assertRaises(ValueError):
                cache.put("a", Route(1, 2, "Google Routes API"))
