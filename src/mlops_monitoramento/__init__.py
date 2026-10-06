"""Monitoramento de modelos: PSI, KS, p95, tokens, imagem."""

from mlops_monitoramento.ks import alert_ks, ks_two_sample
from mlops_monitoramento.p95 import alert_p95, p95
from mlops_monitoramento.psi import alert_psi, population_stability_index

__all__ = [
    "alert_ks",
    "alert_p95",
    "alert_psi",
    "ks_two_sample",
    "p95",
    "population_stability_index",
]


def main() -> None:
    print("Use: just setup   (ver README.md)")
