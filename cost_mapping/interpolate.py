"""Bilinear interpolation without the removed SciPy interp2d dependency."""
import math
from .geo import Point

def interpolate(surface, point):
    grid=surface.grid
    if not grid.south <= point.latitude <= grid.north or not grid.west <= point.longitude <= grid.east:
        raise ValueError('Point is outside the sampled area; extrapolation is disabled')
    y=(point.latitude-grid.south)/(grid.north-grid.south)*(grid.rows-1)
    x=(point.longitude-grid.west)/(grid.east-grid.west)*(grid.columns-1)
    row=min(math.floor(y),grid.rows-2)
    column=min(math.floor(x),grid.columns-2)
    dy,dx=y-row,x-column
    a,b=surface.values[row][column:column+2]
    c,d=surface.values[row+1][column:column+2]
    return (1-dy)*((1-dx)*a+dx*b)+dy*((1-dx)*c+dx*d)


def resample(surface, rows=48, columns=48):
    from .grid import Grid
    from .dataset import Surface
    old=surface.grid
    grid=Grid(old.south,old.west,old.north,old.east,rows,columns)
    values=[[interpolate(surface,Point(lat,lon)) for lon in grid.longitudes] for lat in grid.latitudes]
    return Surface(grid,values,surface.unit,surface.source+'; bilinear resampling (not additional observations)')
