"""Percentil 95 — o valor que 95% da lista não ultrapassa."""

from __future__ import annotations


def p95(xs: list[float]) -> float:
    if not xs:
        return 0.0
    ys = sorted(xs)
    k = int(0.95 * (len(ys) - 1))
    return float(ys[k])


def alert_p95(value: float, *, threshold: float) -> bool:
    return value >= threshold
