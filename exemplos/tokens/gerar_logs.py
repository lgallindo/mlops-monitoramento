"""Gera JSONL de textos pt_BR com n_tokens do DistilBERT português."""

from __future__ import annotations

import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from mlops_monitoramento.jsonl import write_jsonl
from mlops_monitoramento.tokenizar import carregar_tokenizer, contar_tokens, faixa_n_tokens

LOGS = Path(__file__).resolve().parent / "logs"

BASELINE = [
    "O pedido de acesso à informação tramita na ouvidoria desde março.",
    "A turma precisa entregar o relatório de monitoramento na sexta-feira.",
    "Previsão de demanda para o SKU da região Nordeste ficou estável.",
    "O sensor da câmera registrou imagens mais escuras no turno da noite.",
    "Contrato assinado entre a prefeitura e a cooperativa de reciclagem.",
    "A API devolveu o rótulo claro com confiança média de sessenta por cento.",
    "Estudantes compararam a janela baseline com a janela recente no laboratório.",
    "O texto da LAI descreve prazos, recursos e o papel da CGU no acompanhamento.",
    "Fatura emitida em Recife com vencimento em dez dias úteis após o envio.",
    "O modelo de regressão estima o preço a partir da metragem do imóvel.",
    "ok",
    "sim, pode ser",
    "Preciso de um resumo curto do capítulo sobre latência.",
    "A fila do serviço cresceu depois do deploy da versão de quinta.",
    "Documentação interna pede para gravar n_tokens, latency_ms e error no log.",
]

RECENTE = [
    "ok",
    "sim",
    "vlw",
    "blz",
    "thx",
    "ok obrigado",
    "sim pode",
    "tá",
    "fechou",
    "show",
    "ok",
    "sim",
    "vlw demais",
    "blz então",
    "ok",
    "O sistema caiu e a fila de geração de PDF estourou o tempo limite combinado com o cliente da prefeitura.",
]


def _row(texto: str, i: int, extra_ms: float = 0.0) -> dict:
    t0 = time.perf_counter()
    n = contar_tokens(texto)
    latency = (time.perf_counter() - t0) * 1000.0 + extra_ms
    return {
        "ts": datetime.now(timezone.utc).isoformat(),
        "request_id": f"tok-{i:04d}",
        "task": "token_count",
        "text": texto,
        "n_tokens": n,
        "n_tokens_bin": faixa_n_tokens(n),
        "latency_ms": round(latency, 3),
        "error": False,
    }


def main() -> None:
    carregar_tokenizer()
    base = [_row(t, i) for i, t in enumerate(BASELINE)]
    rec = [
        _row(t, 1000 + i, extra_ms=40.0 if i % 5 == 0 else 0.0)
        for i, t in enumerate(RECENTE)
    ]
    write_jsonl(LOGS / "baseline.jsonl", base)
    write_jsonl(LOGS / "recente.jsonl", rec)
    print(f"escrito {LOGS / 'baseline.jsonl'}")
    print(f"escrito {LOGS / 'recente.jsonl'}")


if __name__ == "__main__":
    sys.exit(main())
