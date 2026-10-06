"""Kolmogorov–Smirnov de duas amostras: duas listas de números, um vão."""

from __future__ import annotations


def ks_two_sample(a: list[float], b: list[float]) -> float:
    """Maior distância vertical entre as duas funções de distribuição empírica.

    Variáveis:
    a, b — listas de números (baseline e recente)
    sa, sb — as mesmas listas, ordenadas
    n, m — tamanhos
    valores — união ordenada dos números distintos
    i, j — quantos pontos de cada amostra são ≤ o valor corrente
    d — máximo de |i/n − j/m|
    """
    if not a or not b:
        return 0.0
    sa = sorted(a)
    sb = sorted(b)
    n = len(sa)
    m = len(sb)
    i = 0
    j = 0
    d = 0.0
    # Em cada valor distinto, consome os empates dos dois lados antes de medir o vão.
    valores = sorted(set(sa) | set(sb))
    for x in valores:
        while i < n and sa[i] <= x:
            i += 1
        while j < m and sb[j] <= x:
            j += 1
        d = max(d, abs(i / n - j / m))
    return float(d)


def alert_ks(d: float, *, threshold: float = 0.25) -> bool:
    return d >= threshold
