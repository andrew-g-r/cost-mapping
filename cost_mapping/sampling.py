"""Collect offline surfaces, optionally reusing a local synthetic-data cache."""
import json
from .dataset import Surface
from .offline import estimate_route
from .units import miles, minutes

def sample_grid(grid,origin,*,speed_mph=25,road_factor=1.3,metric='miles',round_trip=False,cache=None):
    if metric not in ('miles','minutes'): raise ValueError('Metric must be miles or minutes')
    rows=[]
    for lat in grid.latitudes:
        row=[]
        for lon in grid.longitudes:
            from .geo import Point
            point=Point(lat,lon)
            key=json.dumps(['offline-v1',origin.latitude,origin.longitude,lat,lon,speed_mph,road_factor])
            route=cache.get(key) if cache else None
            if route is None:
                route=estimate_route(origin,point,speed_mph=speed_mph,road_factor=road_factor)
                if cache: cache.put(key,route)
            value=miles(route.meters,'meters') if metric=='miles' else minutes(route.seconds,'seconds')
            row.append(value*(2 if round_trip else 1))
        rows.append(row)
    source=f'Offline approximation: factor {road_factor:g}, speed {speed_mph:g} mph; '
    source+='symmetric round trip' if round_trip else 'one way'
    source+=f'; origin {origin.latitude},{origin.longitude}; no traffic or road barriers'
    return Surface(grid,rows,metric,source)
