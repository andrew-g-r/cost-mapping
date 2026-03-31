import json
import subprocess
import sys
import unittest

class CLITests(unittest.TestCase):
    def cli(self,*args):
        return subprocess.run([sys.executable,'-m','cost_mapping',*args],text=True,capture_output=True)
    def test_evaluate_and_bad_input(self):
        args=['evaluate','--payout','30','--miles','10','--driving-minutes','30']
        result=self.cli(*args)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(json.loads(result.stdout)['net_earnings'],27)
        self.assertEqual(self.cli(*args,'--tolls','-1').returncode,2)
