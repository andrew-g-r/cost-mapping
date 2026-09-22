"""Strict, line-numbered imports for user-supplied gig data."""

import csv
from pathlib import Path

from .economics import Gig


def load_gigs(path):
    path = Path(path)
    if path.stat().st_size > 10_000_000:
        raise ValueError("CSV input exceeds 10 MB")
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        required = {"name", "payout", "miles", "driving_minutes"}
        allowed = set(Gig.__dataclass_fields__)
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError("CSV requires name,payout,miles,driving_minutes")
        if (
            len(reader.fieldnames) != len(set(reader.fieldnames))
            or set(reader.fieldnames) - allowed
        ):
            raise ValueError("CSV has duplicate or unsupported columns")
        result = []
        for line, row in enumerate(reader, 2):
            if len(result) >= 10000:
                raise ValueError("CSV contains more than 10000 gigs")
            try:
                if None in row or any(value is None for value in row.values()):
                    raise ValueError("Column count differs from the header")
                data = {
                    key: float(value) if key != "name" else value
                    for key, value in row.items()
                    if value != ""
                }
                result.append(Gig(**data))
            except (ValueError, TypeError) as error:
                raise ValueError(f"CSV line {line}: {error}") from error
        if not result:
            raise ValueError("CSV contains no gigs")
        return result
