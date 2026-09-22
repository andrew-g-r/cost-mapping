import json
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from cost_mapping.web import make_server


class WebTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = make_server(0)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def request(self, value, **headers):
        return Request(
            self.url + "/api/evaluate",
            data=json.dumps(value).encode(),
            headers={"Content-Type": "application/json", **headers},
        )

    def test_known_calculation_over_http(self):
        with urlopen(
            self.request({"gig": {"name": "A", "payout": 30, "miles": 10, "driving_minutes": 30}}),
            timeout=5,
        ) as response:
            self.assertEqual(json.load(response)["net_earnings"], 27)

    def test_static_assets_are_packaged_and_served(self):
        for asset in ["/", "/app.js", "/style.css"]:
            with urlopen(self.url + asset, timeout=5) as response:
                self.assertEqual(response.status, 200)
                self.assertEqual(response.headers["X-Content-Type-Options"], "nosniff")

    def test_bad_data_and_cross_origin(self):
        for request in [self.request({"gig": {}}), self.request({}, Origin="https://evil.example")]:
            try:
                urlopen(request, timeout=5)
            except HTTPError as error:
                self.assertIn(error.code, (400, 403))
                error.close()
            else:
                self.fail("Expected rejection")
