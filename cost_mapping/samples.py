"""Packaged demonstration data, independent of the working directory."""

from pathlib import Path

from .dataset import load_surface


def sample_surface():
    return load_surface(Path(__file__).with_name("data") / "austin-legacy.json")
