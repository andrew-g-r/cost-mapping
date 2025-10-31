"""Regular grids use latitude rows and longitude columns."""
from dataclasses import dataclass
from .geo import Point

@dataclass(frozen=True)
class Grid:
    south: float
    west: float
    north: float
    east: float
    rows: int = 16
    columns: int = 16
    def __post_init__(self):
        Point(self.south, self.west)
        Point(self.north, self.east)
        if self.south >= self.north or self.west >= self.east:
            raise ValueError('Bounds require south < north and west < east; split antimeridian regions')
        if any(type(n) is not int or not 2 <= n <= 1000 for n in (self.rows,self.columns)) or self.rows*self.columns > 100000:
            raise ValueError('Grid dimensions must be 2–1000 with at most 100000 cells')
    @property
    def latitudes(self):
        return [self.south + (self.north-self.south)*i/(self.rows-1) for i in range(self.rows)]
    @property
    def longitudes(self):
        return [self.west + (self.east-self.west)*i/(self.columns-1) for i in range(self.columns)]
    def points(self):
        return [Point(lat,lon) for lat in self.latitudes for lon in self.longitudes]
