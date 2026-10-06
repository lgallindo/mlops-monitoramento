"""HTTP na raiz do clone: /gui/ e os report_*.json em exemplos/*/logs/."""

from __future__ import annotations

import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PORTA = int(os.environ.get("PAINEL_PORTA", "8765"))


def main() -> None:
    os.chdir(ROOT)

    class Handler(SimpleHTTPRequestHandler):
        def log_message(self, fmt: str, *args: object) -> None:
            sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    httpd = ThreadingHTTPServer(("127.0.0.1", PORTA), Handler)
    print(f"http://127.0.0.1:{PORTA}/gui/", flush=True)
    print("Ctrl+C para parar.", flush=True)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
