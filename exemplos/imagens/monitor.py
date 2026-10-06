"""PSI nos baldes de brilho, KS no brilho contínuo, confiança média, erros, p95."""

from __future__ import annotations

import json
import statistics
import sys
from collections import Counter
from pathlib import Path

from mlops_monitoramento.jsonl import load_jsonl, write_report
from mlops_monitoramento.ks import alert_ks, ks_two_sample
from mlops_monitoramento.p95 import alert_p95, p95
from mlops_monitoramento.psi import alert_psi, population_stability_index

LOGS = Path(__file__).resolve().parent / "logs"
PSI_LIMIAR = 0.2
KS_LIMIAR = 0.25
LAT_P95_LIMIAR_MS = 8.0
CONF_MEDIA_LIMIAR = 0.55
ERR_LIMIAR = 0.05


def main() -> int:
    base = load_jsonl(LOGS / "baseline.jsonl")
    rec = load_jsonl(LOGS / "recente.jsonl")
    if not base or not rec:
        print("Rode: just gerar", file=sys.stderr)
        return 2

    psi_in = population_stability_index(
        Counter(r["brightness_bin"] for r in base),
        Counter(r["brightness_bin"] for r in rec),
    )
    psi_pred = population_stability_index(
        Counter(r["pred_label"] for r in base),
        Counter(r["pred_label"] for r in rec),
    )
    d = ks_two_sample(
        [float(r["mean_brightness"]) for r in base],
        [float(r["mean_brightness"]) for r in rec],
    )
    lat = p95([float(r["latency_ms"]) for r in rec])
    conf = statistics.fmean(float(r["confidence"]) for r in rec)
    err = sum(1 for r in rec if r.get("error")) / len(rec)
    report = {
        "task": "image_processing",
        "n_baseline": len(base),
        "n_recente": len(rec),
        "psi_input_brightness_bin": round(psi_in, 4),
        "psi_pred_label": round(psi_pred, 4),
        "alert_input_drift": alert_psi(psi_in, threshold=PSI_LIMIAR),
        "alert_pred_drift": alert_psi(psi_pred, threshold=PSI_LIMIAR),
        "ks_mean_brightness": round(d, 4),
        "alert_ks_brightness": alert_ks(d, threshold=KS_LIMIAR),
        "latency_p95_ms": round(lat, 3),
        "alert_latency": alert_p95(lat, threshold=LAT_P95_LIMIAR_MS),
        "confidence_mean": round(conf, 4),
        "alert_low_confidence": conf < CONF_MEDIA_LIMIAR,
        "error_rate": round(err, 4),
        "alert_errors": err >= ERR_LIMIAR,
        "thresholds": {
            "psi": PSI_LIMIAR,
            "ks": KS_LIMIAR,
            "latency_p95_ms": LAT_P95_LIMIAR_MS,
            "confidence_mean_min": CONF_MEDIA_LIMIAR,
            "error_rate": ERR_LIMIAR,
        },
    }
    write_report(LOGS / "report_imagens.json", report)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    flags = (
        "alert_input_drift",
        "alert_pred_drift",
        "alert_ks_brightness",
        "alert_latency",
        "alert_low_confidence",
        "alert_errors",
    )
    return 1 if any(report[k] for k in flags) else 0


if __name__ == "__main__":
    raise SystemExit(main())
