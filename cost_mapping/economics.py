"""Trip economics: cash costs and the value of time stay separate."""
from dataclasses import dataclass, asdict
from .geo import finite

@dataclass(frozen=True)
class Assumptions:
    cost_per_mile: float = 0.30
    target_hourly: float = 20.0
    def __post_init__(self):
        finite(self.cost_per_mile,'cost per mile',minimum=0)
        finite(self.target_hourly,'target hourly earnings',minimum=0)

@dataclass(frozen=True)
class Gig:
    name: str
    payout: float
    miles: float
    driving_minutes: float
    work_minutes: float = 0
    waiting_minutes: float = 0
    tolls: float = 0
    parking: float = 0
    def __post_init__(self):
        if not isinstance(self.name,str) or not self.name.strip() or len(self.name)>200:
            raise ValueError('Gig name must contain 1–200 characters')
        for key,value in asdict(self).items():
            if key != 'name': finite(value,key,minimum=0)
        if self.driving_minutes+self.work_minutes+self.waiting_minutes <= 0:
            raise ValueError('Total trip and work time must be positive')

def evaluate(gig, assumptions=None):
    assumptions=assumptions or Assumptions()
    minutes=gig.driving_minutes+gig.work_minutes+gig.waiting_minutes
    vehicle=gig.miles*assumptions.cost_per_mile
    expenses=vehicle+gig.tolls+gig.parking
    net=gig.payout-expenses
    time_value=minutes/60*assumptions.target_hourly
    for label,value in [('total time',minutes),('cash cost',expenses),('net earnings',net),('time value',time_value),('hourly earnings',net/(minutes/60))]:
        finite(value,label)
    return {'name':gig.name,'payout':gig.payout,'miles':gig.miles,'total_minutes':minutes,
            'vehicle_cost':vehicle,'cash_cost':expenses,'net_earnings':net,
            'effective_hourly':net/(minutes/60),'target_time_value':time_value,
            'minimum_payout':expenses+time_value,'surplus':net-time_value,
            'meets_target':net>=time_value}
