import json
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest

class WorkflowTests(unittest.TestCase):
    def cli(self,*args):
        result=subprocess.run([sys.executable,'-m','cost_mapping',*map(str,args)],capture_output=True,text=True,timeout=60 if args[0]=='plot' else 10)
        self.assertEqual(result.returncode,0,result.stderr)
        return result.stdout
    def test_collect_query_resample_and_export(self):
        with tempfile.TemporaryDirectory() as folder:
            source=Path(folder)/'area.json'
            smooth=Path(folder)/'smooth.json'
            self.cli('collect','--origin','0,0','--bounds',0,0,1,1,'--rows',3,'--columns',4,'--output',source)
            info=json.loads(self.cli('inspect',source))
            self.assertEqual(info['samples'],12)
            self.assertEqual(json.loads(self.cli('query',source,'--point','0,0'))['value'],0)
            self.cli('resample',source,'--rows',4,'--columns',6,'--output',smooth)
            features=json.loads(self.cli('export',smooth))['features']
            self.assertEqual(len(features),24)
            self.assertEqual(len(json.loads(self.cli('reach',source,'--budget',0))),1)
    def test_offline_round_trip_needs_no_external_service(self):
        result=json.loads(self.cli('route','--origin','30,-97','--destination','30.1,-97.1','--round-trip'))
        self.assertEqual(result['requests'],0)
        self.assertGreater(result['miles'],0)
    def test_optional_plot_writes_a_real_image(self):
        try: import matplotlib
        except ImportError: self.skipTest('Optional plotting extra not installed')
        with tempfile.TemporaryDirectory() as folder:
            source=Path(folder)/'sample.json';image=Path(folder)/'map.png'
            self.cli('sample','--output',source)
            self.cli('plot',source,'--output',image)
            self.assertTrue(image.read_bytes().startswith(b'\x89PNG'))
