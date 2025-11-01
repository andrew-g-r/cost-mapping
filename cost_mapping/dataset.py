"""Versioned cost surfaces with explicit units and axis metadata."""
from dataclasses import dataclass, asdict
import json
from pathlib import Path
from .geo import finite
from .grid import Grid

@dataclass(frozen=True)
class Surface:
    grid: Grid
    values: list[list[float]]
    unit: str = 'miles'
    source: str = 'user supplied'
    def __post_init__(self):
        if self.unit not in ('miles','meters','minutes','seconds','currency'):
            raise ValueError('Unknown surface unit')
        if not isinstance(self.source,str) or not self.source.strip():
            raise ValueError('A source description is required')
        if len(self.values) != self.grid.rows or any(len(row) != self.grid.columns for row in self.values):
            raise ValueError('Surface shape must match latitude rows and longitude columns')
        for row in self.values:
            for value in row:
                finite(value,'surface value',minimum=0)
    def to_dict(self):
        return {'schema_version':1,'grid':asdict(self.grid),'values':self.values,'unit':self.unit,'source':self.source}
    @classmethod
    def from_dict(cls, raw):
        try:
            if raw['schema_version'] != 1:
                raise ValueError('Unsupported surface version')
            return cls(Grid(**raw['grid']),raw['values'],raw['unit'],raw['source'])
        except (KeyError,TypeError) as error:
            raise ValueError(f'Invalid surface: {error}') from error

def load_surface(path):
    path=Path(path)
    if path.stat().st_size > 20_000_000:
        raise ValueError('Surface file exceeds 20 MB')
    return Surface.from_dict(json.loads(path.read_text(encoding='utf-8')))
