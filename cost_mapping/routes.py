"""Route measurements and adapters for previously exported directions."""

from dataclasses import dataclass

from .geo import finite


@dataclass(frozen=True)
class Route:
    meters: float
    seconds: float
    source: str

    def __post_init__(self):
        finite(self.meters, "route distance", minimum=0)
        finite(self.seconds, "route duration", minimum=0)
        if not isinstance(self.source, str) or not self.source:
            raise ValueError("Route source is required")


def from_legacy_directions(raw):
    try:
        legs = raw[0]["legs"]
        if not legs:
            raise ValueError("No route legs returned")
        routes = [
            Route(leg["distance"]["value"], leg["duration"]["value"], "imported directions")
            for leg in legs
        ]
        return Route(
            sum(r.meters for r in routes),
            sum(r.seconds for r in routes),
            "imported directions (all legs)",
        )
    except (KeyError, TypeError, IndexError) as error:
        raise ValueError("Directions response is missing route legs or measurements") from error
