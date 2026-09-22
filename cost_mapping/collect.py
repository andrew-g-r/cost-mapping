"""Explicit request budgets and directional round-trip aggregation."""

from .routes import Route


class RequestBudget:
    def __init__(self, limit):
        if type(limit) is not int or not 1 <= limit <= 10000:
            raise ValueError("Request limit must be between 1 and 10000")
        self.limit, self.used = limit, 0

    def call(self, provider, *args, **kwargs):
        if self.used >= self.limit:
            raise ValueError("Request budget exhausted; no additional request was sent")
        self.used += 1
        return provider(*args, **kwargs)


def round_trip(origin, destination, provider, *, budget):
    outbound = budget.call(provider, origin, destination)
    inbound = budget.call(provider, destination, origin)
    return Route(
        outbound.meters + inbound.meters,
        outbound.seconds + inbound.seconds,
        outbound.source + "; outbound + return",
    )
