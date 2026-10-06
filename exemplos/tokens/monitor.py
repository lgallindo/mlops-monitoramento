"""PSI nos baldes de n_tokens + p95 da latência do tokenizer."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

from mlops_monitoramento.jsonl import load_jsonl, write_report
from mlops_monitoramento.p95 import alert_p95, p95
from mlops_monitoramento.psi import alert_psi, population_stability_index

LOGS = Path(__file__).resolve().parent / "logs"
PSI_LIMIAR = 0.2
LAT_P95_LIMIAR_MS = 25.0


def main() -> int:
    base = load_jsonl(LOGS / "baseline.jsonl")
    rec = load_jsonl(LOGS / "recente.jsonl")
    if not base or not rec:
        print("Rode: just gerar", file=sys.stderr)
        return 2

    psi = population_stability_index(
        Counter(r["n_tokens_bin"] for r in base),
        Counter(r["n_tokens_bin"] for r in rec),
    )
    lat = p95([float(r["latency_ms"]) for r in rec])
    err = sum(1 for r in rec if r.get("error")) / len(rec)
    report = {
        "task": "token_count",
        "n_baseline": len(base),
        "n_recente": len(rec),
        "psi_n_tokens_bin": round(psi, 4),
        "alert_prompt_mix": alert_psi(psi, threshold=PSI_LIMIAR),
        "latency_p95_ms": round(lat, 3),
        "alert_latency": alert_p95(lat, threshold=LAT_P95_LIMIAR_MS),
        "error_rate": round(err, 4),
        "thresholds": {"psi": PSI_LIMIAR, "latency_p95_ms": LAT_P95_LIMIAR_MS},
    }
    write_report(LOGS / "report_tokens.json", report)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if report["alert_prompt_mix"] or report["alert_latency"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
