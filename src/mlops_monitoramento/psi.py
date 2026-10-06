"""Population Stability Index: dois histogramas, um número."""

from __future__ import annotations

import math
from collections import Counter
from typing import Iterable


def as_counter(values: Iterable[str]) -> Counter[str]:
    return Counter(values)


def population_stability_index(
    baseline: Counter[str],
    recent: Counter[str],
    *,
    eps: float = 1e-6,
) -> float:
    keys = sorted(set(baseline) | set(recent))
    if not keys:
        return 0.0
    b_tot = sum(baseline.values()) or 1
    r_tot = sum(recent.values()) or 1
    psi = 0.0
    for k in keys:
        pb = (baseline.get(k, 0) + eps) / (b_tot + eps * len(keys))
        pr = (recent.get(k, 0) + eps) / (r_tot + eps * len(keys))
        psi += (pr - pb) * math.log(pr / pb)
    return float(psi)


def alert_psi(psi: float, *, threshold: float = 0.2) -> bool:
    return psi >= threshold
