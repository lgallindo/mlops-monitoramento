"""O painel sobe com BentoML (`just painel`), não com http.server."""

from __future__ import annotations

import sys

print(
    "O painel sobe com BentoML: just painel  →  http://127.0.0.1:3001/gui/",
    file=sys.stderr,
)
raise SystemExit(2)
