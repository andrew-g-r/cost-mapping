"""Coordinates are latitude/longitude; GeoJSON output reverses this order."""

import math
from dataclasses import dataclass


def finite(value, name, *, minimum=None, maximum=None):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number")
    if minimum is not None and value < minimum or maximum is not None and value > maximum:
        raise ValueError(f"{name} is outside the supported range")
    return float(value)


@dataclass(frozen=True)
class Point:
    latitude: float
    longitude: float

    def __post_init__(self):
        finite(self.latitude, "latitude", minimum=-90, maximum=90)
        finite(self.longitude, "longitude", minimum=-180, maximum=180)

    @classmethod
    def parse(cls, value):
        try:
            lat, lon = map(float, value.split(","))
            return cls(lat, lon)
        except (ValueError, AttributeError) as error:
            raise ValueError("Coordinates must be latitude,longitude") from error

    def geojson(self):
        return [self.longitude, self.latitude]


def haversine(a, b):
    lat1, lat2 = map(math.radians, [a.latitude, b.latitude])
    dlat, dlon = lat2 - lat1, math.radians(b.longitude - a.longitude)
    value = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 6371008.8 * 2 * math.asin(math.sqrt(min(1.0, max(0.0, value))))
