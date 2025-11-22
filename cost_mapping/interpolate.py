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
