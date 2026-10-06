"""Classificador de brilho: média dos pixels em [0, 1] vira
{escuro, medio, claro}.
"""

from __future__ import annotations

import time
from dataclasses import dataclass

import numpy as np
from PIL import Image

CLASSES: tuple[str, ...] = ("escuro", "medio", "claro")
B_LO: float = 1.0 / 3.0
B_HI: float = 2.0 / 3.0


@dataclass(frozen=True)
class Predicao:
    label: str
    confidence: float
    mean_brightness: float
    latency_ms: float


def brightness(img: Image.Image) -> float:
    arr = np.asarray(img.convert("L"), dtype=np.float32)
    return float(arr.mean() / 255.0)


def _label_and_confidence(b: float) -> tuple[str, float]:
    if b < B_LO:
        return "escuro", 0.55 + (B_LO - b)
    if b < B_HI:
        return "medio", 0.60 + abs(0.5 - b)
    return "claro", 0.55 + (b - B_HI)


def predict(img: Image.Image) -> Predicao:
    t0 = time.perf_counter()
    b = brightness(img)
    label, conf = _label_and_confidence(b)
    conf = float(min(0.99, conf))
    latency_ms = (time.perf_counter() - t0) * 1000.0
    return Predicao(
        label=label,
        confidence=conf,
        mean_brightness=b,
        latency_ms=latency_ms,
    )


def brightness_bin(b: float) -> str:
    if b < B_LO:
        return "b0"
    if b < B_HI:
        return "b1"
    return "b2"
