"""Local preview server that mimics GitHub Pages SPA behavior:
unknown paths fall back to 404.html (which bounces to the app).
Usage: python3 serve.py [port]
"""
import http.server
import sys
from pathlib import Path

ROOT = Path(__file__).parent


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def send_error(self, code, *args, **kwargs):
        if code == 404:
            body = (ROOT / "404.html").read_bytes()
            self.send_response(404)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            super().send_error(code, *args, **kwargs)


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8123
    http.server.ThreadingHTTPServer(("", port), Handler).serve_forever()
