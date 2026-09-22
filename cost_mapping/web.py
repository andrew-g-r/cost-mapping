"""Loopback calculator API; never sends browser data to a routing service."""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from socketserver import TCPServer
from urllib.parse import urlsplit

from .economics import Assumptions, Gig, evaluate
from .scenarios import sensitivity

ASSETS = Path(__file__).with_name("web")


class LocalServer(ThreadingHTTPServer):
    def server_bind(self):
        TCPServer.server_bind(self)
        self.server_name = "localhost"
        self.server_port = self.server_address[1]


def make_server(port=8766):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def respond(self, status, data, mime="application/json; charset=utf-8"):
            content = (
                data if isinstance(data, bytes) else json.dumps(data, allow_nan=False).encode()
            )
            self.send_response(status)
            self.send_header("Content-Type", mime)
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header(
                "Content-Security-Policy",
                "default-src 'self'; object-src 'none'; frame-ancestors 'none'; base-uri 'none'",
            )
            self.end_headers()
            self.wfile.write(content)

        def local(self):
            return self.headers.get("Host", "").split(":")[0] in ("localhost", "127.0.0.1")

        def do_GET(self):
            if not self.local():
                return self.respond(403, {"error": "Local access only"})
            path = urlsplit(self.path).path
            assets = {
                "/": ("index.html", "text/html"),
                "/app.js": ("app.js", "text/javascript"),
                "/style.css": ("style.css", "text/css"),
            }
            if path == "/api/health":
                return self.respond(200, {"status": "ok", "routing": "offline only"})
            if path not in assets:
                return self.respond(404, {"error": "Not found"})
            name, mime = assets[path]
            try:
                self.respond(200, (ASSETS / name).read_bytes(), mime + "; charset=utf-8")
            except OSError:
                self.respond(404, {"error": "Asset not found"})

        def do_POST(self):
            if not self.local():
                return self.respond(403, {"error": "Local access only"})
            if self.headers.get("Origin") not in (
                None,
                f"http://127.0.0.1:{self.server.server_port}",
                f"http://localhost:{self.server.server_port}",
            ):
                return self.respond(403, {"error": "Cross-origin requests are not supported"})
            if self.path not in ("/api/evaluate", "/api/scenarios"):
                return self.respond(404, {"error": "Not found"})
            try:
                size = int(self.headers.get("Content-Length", "0"))
                if not 0 < size <= 16384:
                    raise ValueError("Request body must be 1–16384 bytes")
                if self.headers.get("Content-Type", "").split(";")[0] != "application/json":
                    raise ValueError("Send application/json")
                self.connection.settimeout(5)
                payload = json.loads(self.rfile.read(size))
                if not isinstance(payload, dict) or set(payload) - {"gig", "assumptions"}:
                    raise ValueError("Expected gig and assumptions objects")
                gig = Gig(**payload["gig"])
                assumptions = Assumptions(**payload.get("assumptions", {}))
                result = (
                    evaluate(gig, assumptions)
                    if self.path == "/api/evaluate"
                    else sensitivity(gig, assumptions)
                )
                self.respond(200, result)
            except (ValueError, TypeError, KeyError, TimeoutError) as error:
                self.respond(400, {"error": str(error)})

    return LocalServer(("127.0.0.1", port), Handler)


def serve(port=8766):
    with make_server(port) as server:
        print(f"Cost mapping: http://127.0.0.1:{server.server_port}", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
