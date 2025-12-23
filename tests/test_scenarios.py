import unittest
from cost_mapping.economics import Gig
from cost_mapping.scenarios import sensitivity

class ScenarioTests(unittest.TestCase):
    def test_higher_cost_and_driving_time_reduce_hourly_earnings(self):
        rows=sensitivity(Gig('A',30,10,30))
        self.assertEqual(len(rows),9)
        self.assertGreater(rows[0]['effective_hourly'],rows[-1]['effective_hourly'])
