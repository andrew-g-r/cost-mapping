"""Google Routes API v2 adapter; requests require an explicit key."""

import json
import os
import re
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .geo import finite
from .routes import Route

ENDPOINT = "https://routes.googleapis.com/directions/v2:computeRoutes"


def parse_response(raw):
    try:
        route = raw["routes"][0]
        duration = route["duration"]
        if not isinstance(duration, str) or not re.fullmatch(r"\d+(?:\.\d+)?s", duration):
            raise ValueError("Invalid Routes API duration")
        return Route(
            route["distanceMeters"], float(duration[:-1]), "Google Routes API; traffic unaware"
        )
    except (KeyError, IndexError, TypeError) as error:
        raise ValueError("No usable route returned by Google Routes API") from error


def google_route(
    origin, destination, *, api_key=None, timeout=15, avoid_tolls=False, opener=urlopen
):
    key = api_key or os.environ.get("GOOGLE_MAPS_API_KEY")
    if not key:
        raise ValueError("Set GOOGLE_MAPS_API_KEY to use live routing")
    finite(timeout, "request timeout", minimum=0.1, maximum=120)

    def waypoint(point):
        return {"location": {"latLng": {"latitude": point.latitude, "longitude": point.longitude}}}

    data = {
        "origin": waypoint(origin),
        "destination": waypoint(destination),
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_UNAWARE",
        "routeModifiers": {"avoidTolls": bool(avoid_tolls)},
    }
    request = Request(
        ENDPOINT,
        data=json.dumps(data).encode(),
        headers={
            "Content-Type": "application/json",
            "X-Goog-Api-Key": key,
            "X-Goog-FieldMask": "routes.distanceMeters,routes.duration",
        },
    )
    try:
        with opener(request, timeout=timeout) as response:
            payload = response.read(2_000_001)
            if len(payload) > 2_000_000:
                raise ValueError("Routing response exceeds 2 MB")
            return parse_response(json.loads(payload))
    except HTTPError as error:
        error.close()
        raise ValueError(
            f"Google Routes returned HTTP {error.code}; check API access, billing and quota"
        ) from None
    except (URLError, TimeoutError):
        raise ValueError(
            "Google Routes request failed or timed out; no estimate was substituted"
        ) from None
