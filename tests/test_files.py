import tempfile
from pathlib import Path
import unittest
from cost_mapping.files import save

class FileTests(unittest.TestCase):
    def test_no_overwrite_by_default(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'report.json'
            save(path,'first')
            with self.assertRaises(FileExistsError): save(path,'second')
            self.assertEqual(path.read_text(),'first\n')
            save(path,'second',force=True)
            self.assertEqual(path.read_text(),'second\n')
