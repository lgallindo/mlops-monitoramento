"""KS (e PSI auxiliar) sobre ŷ da regressão; p95 da latência."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

from mlops_monitoramento.jsonl import load_jsonl, write_report
from mlops_monitoramento.ks import alert_ks, ks_two_sample
from mlops_monitoramento.p95 import alert_p95, p95
from mlops_monitoramento.psi import alert_psi, population_stability_index

LOGS = Path(__file__).resolve().parent / "logs"
KS_LIMIAR = 0.25
PSI_LIMIAR = 0.2
LAT_P95_LIMIAR_MS = 8.0
ERR_LIMIAR = 0.05


def main() -> int:
    base = load_jsonl(LOGS / "baseline.jsonl")
    rec = load_jsonl(LOGS / "recente.jsonl")
    if not base or not rec:
        print("Rode: just gerar", file=sys.stderr)
        return 2

    yh_b = [float(r["y_hat"]) for r in base]
    yh_r = [float(r["y_hat"]) for r in rec]
    d = ks_two_sample(yh_b, yh_r)
    psi = population_stability_index(
        Counter(r["y_hat_bin"] for r in base),
        Counter(r["y_hat_bin"] for r in rec),
    )
    lat = p95([float(r["latency_ms"]) for r in rec])
    err = sum(1 for r in rec if r.get("error")) / len(rec)
    report = {
        "task": "regressao_preco",
        "n_baseline": len(base),
        "n_recente": len(rec),
        "ks_y_hat": round(d, 4),
        "alert_ks_y_hat": alert_ks(d, threshold=KS_LIMIAR),
        "psi_y_hat_bin": round(psi, 4),
        "alert_psi_y_hat": alert_psi(psi, threshold=PSI_LIMIAR),
        "latency_p95_ms": round(lat, 3),
        "alert_latency": alert_p95(lat, threshold=LAT_P95_LIMIAR_MS),
        "error_rate": round(err, 4),
        "alert_errors": err >= ERR_LIMIAR,
        "thresholds": {
            "ks": KS_LIMIAR,
            "psi": PSI_LIMIAR,
            "latency_p95_ms": LAT_P95_LIMIAR_MS,
            "error_rate": ERR_LIMIAR,
        },
    }
    write_report(LOGS / "report_regressao.json", report)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    flags = (
        "alert_ks_y_hat",
        "alert_psi_y_hat",
        "alert_latency",
        "alert_errors",
    )
    return 1 if any(report[k] for k in flags) else 0


if __name__ == "__main__":
    raise SystemExit(main())
