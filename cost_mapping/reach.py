"""Find sampled points within a budget, without inventing polygon boundaries."""

from .geo import finite


def within_budget(surface, budget):
    finite(budget, "budget", minimum=0)
    return [
        {"latitude": lat, "longitude": lon, "value": surface.values[i][j], "unit": surface.unit}
        for i, lat in enumerate(surface.grid.latitudes)
        for j, lon in enumerate(surface.grid.longitudes)
        if surface.values[i][j] <= budget
    ]


def describe(surface):
    values = [v for row in surface.values for v in row]
    return {
        "rows": surface.grid.rows,
        "columns": surface.grid.columns,
        "samples": len(values),
        "minimum": min(values),
        "maximum": max(values),
        "mean": sum(values) / len(values),
        "unit": surface.unit,
        "source": surface.source,
        "bounds": [surface.grid.south, surface.grid.west, surface.grid.north, surface.grid.east],
    }
