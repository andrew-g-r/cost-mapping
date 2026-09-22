"""Sensitivity analysis for uncertain trip time and operating cost."""

from dataclasses import replace

from .economics import Assumptions, evaluate
from .geo import finite


def sensitivity(gig, assumptions=None, cost_factors=(0.8, 1, 1.2), time_factors=(0.8, 1, 1.2)):
    assumptions = assumptions or Assumptions()
    if not cost_factors or not time_factors or len(cost_factors) * len(time_factors) > 1000:
        raise ValueError("Use 1–1000 sensitivity combinations")
    output = []
    for cost in cost_factors:
        finite(cost, "cost factor", minimum=0)
        for time in time_factors:
            finite(time, "time factor", minimum=0.01)
            scenario = replace(gig, driving_minutes=gig.driving_minutes * time)
            result = evaluate(
                scenario, replace(assumptions, cost_per_mile=assumptions.cost_per_mile * cost)
            )
            output.append({"cost_factor": cost, "driving_time_factor": time, **result})
    return output
