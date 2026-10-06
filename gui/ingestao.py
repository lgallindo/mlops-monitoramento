"""Acrescenta um pedido à janela recente e roda o monitor daquela pasta."""

from __future__ import annotations

import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mlops_monitoramento.imagem import brightness_bin, make_gray, predict
from mlops_monitoramento.jsonl import append_jsonl, load_jsonl
from mlops_monitoramento.regressao import ajustar, faixa_yhat, prever
from mlops_monitoramento.tokenizar import contar_tokens, faixa_n_tokens

ROOT = Path(__file__).resolve().parents[1]


def _agora() -> str:
    return datetime.now(timezone.utc).isoformat()


def _id(prefixo: str) -> str:
    return f"{prefixo}-{int(time.time() * 1000)}"


def _monitor(rel: str) -> None:
    subprocess.run(
        [sys.executable, str(ROOT / rel)],
        cwd=str(ROOT),
        check=False,
        capture_output=True,
        text=True,
    )


def pedido_tokens(texto: str) -> dict[str, Any]:
    texto = texto.strip()
    if not texto:
        raise ValueError("texto vazio")
    t0 = time.perf_counter()
    n = contar_tokens(texto)
    latency = (time.perf_counter() - t0) * 1000.0
    row = {
        "ts": _agora(),
        "request_id": _id("tok"),
        "task": "token_count",
        "text": texto,
        "n_tokens": n,
        "n_tokens_bin": faixa_n_tokens(n),
        "latency_ms": round(latency, 3),
        "error": False,
    }
    append_jsonl(ROOT / "exemplos/tokens/logs/recente.jsonl", row)
    _monitor("exemplos/tokens/monitor.py")
    return row


def pedido_regressao(x: float, y_obs: float | None) -> dict[str, Any]:
    base = load_jsonl(ROOT / "exemplos/regressao/logs/baseline.jsonl")
    if not base:
        raise ValueError("sem baseline de regressão; rode just gerar")
    reta = ajustar(
        [float(r["x"]) for r in base],
        [float(r["y_obs"]) for r in base],
    )
    t0 = time.perf_counter()
    yhat = prever(reta, x)
    latency = (time.perf_counter() - t0) * 1000.0
    row: dict[str, Any] = {
        "ts": _agora(),
        "request_id": _id("reg"),
        "task": "regressao_preco",
        "x": round(x, 4),
        "y_hat": round(yhat, 4),
        "y_hat_bin": faixa_yhat(yhat),
        "latency_ms": round(latency, 3),
        "error": False,
    }
    if y_obs is not None:
        y = float(y_obs)
        row["y_obs"] = round(y, 4)
        row["residual"] = round(y - yhat, 4)
    else:
        row["y_obs"] = None
        row["residual"] = None
    append_jsonl(ROOT / "exemplos/regressao/logs/recente.jsonl", row)
    _monitor("exemplos/regressao/monitor.py")
    return row


def pedido_imagem(brilho: float) -> dict[str, Any]:
    if brilho < 0.0 or brilho > 1.0:
        raise ValueError("brilho fora de [0, 1]")
    seed = int(time.time() * 1000) % 10_000_000
    img = make_gray(mean=brilho, seed=seed)
    pred = predict(img)
    row = {
        "ts": _agora(),
        "request_id": _id("img"),
        "task": "image_classification",
        "mean_brightness": round(pred.mean_brightness, 4),
        "brightness_bin": brightness_bin(pred.mean_brightness),
        "pred_label": pred.label,
        "confidence": round(pred.confidence, 4),
        "latency_ms": round(pred.latency_ms, 3),
        "error": False,
    }
    append_jsonl(ROOT / "exemplos/imagens/logs/recente.jsonl", row)
    _monitor("exemplos/imagens/monitor.py")
    return row
