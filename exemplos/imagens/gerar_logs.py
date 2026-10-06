"""Imagens sintéticas + logs: PSI de brilho e KS no brilho contínuo."""

from __future__ import annotations

import random
import sys
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image

from mlops_monitoramento.imagem import brightness_bin, predict
from mlops_monitoramento.jsonl import write_jsonl

LOGS = Path(__file__).resolve().parent / "logs"


def make_image(*, mean: float, seed: int, size: int = 64) -> Image.Image:
    rng = random.Random(seed)
    base = int(max(0, min(255, mean * 255)))
    pixels = bytes(
        max(0, min(255, base + rng.randint(-20, 20))) for _ in range(size * size)
    )
    return Image.frombytes("L", (size, size), pixels)


def write_window(
    path: Path,
    *,
    n: int,
    mean_lo: float,
    mean_hi: float,
    seed0: int,
    inject_error: bool,
) -> None:
    rows = []
    for i in range(n):
        mean = mean_lo + (mean_hi - mean_lo) * (i / max(n - 1, 1))
        img = make_image(mean=mean, seed=seed0 + i)
        pred = predict(img)
        latency = pred.latency_ms + (12.0 if mean < 0.25 and i % 7 == 0 else 0.0)
        erro = bool(inject_error and i % 11 == 0)
        rows.append(
            {
                "ts": datetime.now(timezone.utc).isoformat(),
                "request_id": f"img-{seed0}-{i:04d}",
                "task": "image_classification",
                "mean_brightness": round(pred.mean_brightness, 4),
                "brightness_bin": brightness_bin(pred.mean_brightness),
                "pred_label": pred.label,
                "confidence": round(pred.confidence, 4),
                "latency_ms": round(latency, 3),
                "error": erro,
            }
        )
    write_jsonl(path, rows)


def main() -> None:
    write_window(
        LOGS / "baseline.jsonl",
        n=120,
        mean_lo=0.15,
        mean_hi=0.85,
        seed0=1000,
        inject_error=False,
    )
    write_window(
        LOGS / "recente.jsonl",
        n=80,
        mean_lo=0.05,
        mean_hi=0.40,
        seed0=2000,
        inject_error=True,
    )
    print(f"escrito {LOGS / 'baseline.jsonl'}")
    print(f"escrito {LOGS / 'recente.jsonl'}")


if __name__ == "__main__":
    sys.exit(main())
