"""Compatibility entry point for current cost-surface plotting.

Example: python cost_map_renderer.py sample.json --output map.png
"""
from cost_mapping.cli import main

if __name__ == '__main__':
    import sys
    raise SystemExit(main(['plot', *sys.argv[1:]]))
