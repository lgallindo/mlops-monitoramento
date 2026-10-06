"""Gera (x, y) de um mercado de brinquedo e prevê ŷ com a reta do baseline."""

from __future__ import annotations

import random
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from mlops_monitoramento.jsonl import write_jsonl
from mlops_monitoramento.regressao import ajustar, faixa_yhat, prever

LOGS = Path(__file__).resolve().parent / "logs"


def _pares(n: int, x_lo: float, x_hi: float, seed: int) -> list[tuple[float, float]]:
    rng = random.Random(seed)
    out: list[tuple[float, float]] = []
    for _ in range(n):
        x = rng.uniform(x_lo, x_hi)
        y = 2.5 * x + 10.0 + rng.gauss(0.0, 3.0)
        out.append((x, y))
    return out


def _row(
    i: int, x: float, y: float, reta, extra_ms: float, erro: bool
) -> dict:
    t0 = time.perf_counter()
    yhat = prever(reta, x)
    latency = (time.perf_counter() - t0) * 1000.0 + extra_ms
    return {
        "ts": datetime.now(timezone.utc).isoformat(),
        "request_id": f"reg-{i:04d}",
        "task": "regressao_preco",
        "x": round(x, 4),
        "y_obs": round(y, 4),
        "y_hat": round(yhat, 4),
        "y_hat_bin": faixa_yhat(yhat),
        "residual": round(y - yhat, 4),
        "latency_ms": round(latency, 3),
        "error": erro,
    }


def main() -> None:
    pares_b = _pares(80, 8.0, 22.0, seed=1)
    xs = [p[0] for p in pares_b]
    ys = [p[1] for p in pares_b]
    reta = ajustar(xs, ys)

    base = [
        _row(i, x, y, reta, extra_ms=0.0, erro=False)
        for i, (x, y) in enumerate(pares_b)
    ]
    pares_r = _pares(60, 28.0, 45.0, seed=2)
    rec = []
    for i, (x, y) in enumerate(pares_r):
        extra = 15.0 if i % 6 == 0 else 0.5
        erro = i % 17 == 0
        rec.append(_row(1000 + i, x, y, reta, extra_ms=extra, erro=erro))

    write_jsonl(LOGS / "baseline.jsonl", base)
    write_jsonl(LOGS / "recente.jsonl", rec)
    print(f"reta a={reta.a:.4f} b={reta.b:.4f}")
    print(f"escrito {LOGS / 'baseline.jsonl'}")
    print(f"escrito {LOGS / 'recente.jsonl'}")


if __name__ == "__main__":
    sys.exit(main())
