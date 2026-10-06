"""Reta ŷ = a·x + b ajustada nos pares (x, y) do baseline (mínimos quadrados).
A janela recente usa os mesmos a e b. Muda a distribuição de x e portanto de ŷ.
KS compara as duas listas de ŷ.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Reta:
    a: float
    b: float


def ajustar(xs: list[float], ys: list[float]) -> Reta:
    n = len(xs)
    if n == 0:
        return Reta(a=0.0, b=0.0)
    mx = sum(xs) / n
    my = sum(ys) / n
    var = sum((x - mx) ** 2 for x in xs)
    if var == 0.0:
        return Reta(a=0.0, b=my)
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys, strict=True))
    a = cov / var
    b = my - a * mx
    return Reta(a=a, b=b)


def prever(reta: Reta, x: float) -> float:
    return reta.a * x + reta.b


def faixa_yhat(yhat: float) -> str:
    if yhat < 40:
        return "baixo"
    if yhat < 80:
        return "medio"
    return "alto"


def erro_absoluto_medio(rows: list[dict[str, Any]]) -> tuple[float | None, int]:
    """MAE só nos pedidos que trouxeram y_obs (rótulo). Sem rótulo, o pedido não entra."""
    erros: list[float] = []
    for row in rows:
        y_obs = row.get("y_obs")
        y_hat = row.get("y_hat")
        if y_obs is None or y_hat is None:
            continue
        erros.append(abs(float(y_obs) - float(y_hat)))
    if not erros:
        return None, 0
    return sum(erros) / len(erros), len(erros)
