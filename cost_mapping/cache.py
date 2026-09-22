"""TTL cache for user-owned or synthetic route data, not Google responses."""

import json
import sqlite3
import time
from contextlib import closing, contextmanager
from pathlib import Path

from .geo import finite
from .routes import Route


class RouteCache:
    def __init__(self, path, *, ttl=86400, clock=time.time):
        finite(ttl, "cache TTL", minimum=0)
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.ttl, self.clock = ttl, clock
        with self.connect() as db:
            db.execute(
                "CREATE TABLE IF NOT EXISTS routes (key TEXT PRIMARY KEY, created REAL NOT NULL, value TEXT NOT NULL)"
            )

    @contextmanager
    def connect(self):
        with closing(sqlite3.connect(self.path, timeout=5)) as db:
            with db:
                yield db

    def get(self, key):
        with self.connect() as db:
            row = db.execute("SELECT created,value FROM routes WHERE key=?", (key,)).fetchone()
        if not row or not 0 <= self.clock() - row[0] < self.ttl:
            return None
        return Route(**json.loads(row[1]))

    def put(self, key, route):
        if route.source.startswith("Google"):
            raise ValueError("Google route responses are not persisted by this cache")
        from dataclasses import asdict

        with self.connect() as db:
            db.execute(
                "INSERT OR REPLACE INTO routes VALUES (?,?,?)",
                (key, self.clock(), json.dumps(asdict(route))),
            )

    def clear_expired(self):
        with self.connect() as db:
            cursor = db.execute(
                "DELETE FROM routes WHERE created<=? OR created>?",
                (self.clock() - self.ttl, self.clock()),
            )
            return cursor.rowcount
