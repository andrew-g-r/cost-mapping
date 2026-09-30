import io
import json
import unittest

from cost_mapping.geo import Point
from cost_mapping.google import google_route, parse_response


class GoogleTests(unittest.TestCase):
    def test_request_field_mask_and_units(self):
        requests = []

        def opener(request, timeout):
            requests.append(request)
            return io.BytesIO(b'{"routes":[{"distanceMeters":1500,"duration":"120.5s"}]}')

        result = google_route(Point(1, 2), Point(3, 4), api_key="test-only", opener=opener)
        self.assertEqual((result.meters, result.seconds), (1500, 120.5))
        self.assertEqual(
            requests[0].get_header("X-goog-fieldmask"), "routes.distanceMeters,routes.duration"
        )
        self.assertEqual(
            json.loads(requests[0].data)["origin"]["location"]["latLng"]["latitude"], 1
        )

    def test_provider_errors_close_the_body_without_echoing_credentials(self):
        from urllib.error import HTTPError

        body = io.BytesIO(b"sensitive provider response")

        def opener(request, timeout):
            raise HTTPError(request.full_url, 429, "rate limited", {}, body)

        with self.assertRaisesRegex(ValueError, "HTTP 429") as caught:
            google_route(Point(1, 2), Point(3, 4), api_key="test-only-secret", opener=opener)
        self.assertTrue(body.closed)
        self.assertNotIn("test-only-secret", str(caught.exception))

    def test_no_routes_and_bad_durations(self):
        for value in [{"routes": []}, {"routes": [{"distanceMeters": 10, "duration": "NaNs"}]}]:
            with self.assertRaises(ValueError):
                parse_response(value)
