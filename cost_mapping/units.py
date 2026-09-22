"""Convert user-facing distance and time values into canonical units."""

from .geo import finite

METERS_PER_MILE = 1609.344


def miles(value, unit="miles"):
    finite(value, "distance", minimum=0)
    factors = {"miles": 1.0, "km": 1000 / METERS_PER_MILE, "meters": 1 / METERS_PER_MILE}
    if unit not in factors:
        raise ValueError("Distance units: miles, km, meters")
    return value * factors[unit]


def minutes(value, unit="minutes"):
    finite(value, "duration", minimum=0)
    factors = {"minutes": 1.0, "seconds": 1 / 60, "hours": 60.0}
    if unit not in factors:
        raise ValueError("Time units: minutes, seconds, hours")
    return value * factors[unit]
