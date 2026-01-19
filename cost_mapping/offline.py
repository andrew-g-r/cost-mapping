"""Transparent geographic approximations; not road-network routing."""
from .geo import haversine, finite
from .routes import Route

def estimate_route(origin,destination,*,speed_mph=25,road_factor=1.3):
    finite(speed_mph,'average speed',minimum=.1,maximum=200)
    finite(road_factor,'road distance factor',minimum=1,maximum=10)
    meters=haversine(origin,destination)*road_factor
    seconds=meters/1609.344/speed_mph*3600
    return Route(meters,seconds,f'Approximation: great-circle × {road_factor:g}, {speed_mph:g} mph; no traffic or road barriers')
