"""Compatibility entry point for explicit route requests.

Example: python cost_gmaps_request_data.py --origin 30,-97 --destination 30.1,-97.1
Use --provider google to make a live request; the default is offline.
"""
from cost_mapping.cli import main

if __name__ == '__main__':
    import sys
    raise SystemExit(main(['route', *sys.argv[1:]]))
