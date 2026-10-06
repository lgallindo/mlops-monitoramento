"""Contagem de tokens com DistilBERT treinado em português.

Modelo Hugging Face: `adalbertojunior/distilbert-portuguese-cased`
(destilado do BERTimbau, cerca de 66M parâmetros). Só o tokenizer é
carregado. `n_tokens` é `len(tokenizer.encode(texto))`.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Protocol

MODELO_HF = "adalbertojunior/distilbert-portuguese-cased"


class TokenizerLike(Protocol):
    def encode(self, text: str, add_special_tokens: bool = True) -> list[int]: ...


_cache: TokenizerLike | None = None


def hf_cache_dir() -> Path:
    raw = os.environ.get("HF_HOME") or os.environ.get("TRANSFORMERS_CACHE")
    if raw:
        return Path(raw)
    return Path(__file__).resolve().parents[2] / "hf-cache"


def carregar_tokenizer() -> TokenizerLike:
    global _cache
    if _cache is not None:
        return _cache
    from transformers import AutoTokenizer

    cache = hf_cache_dir()
    cache.mkdir(parents=True, exist_ok=True)
    _cache = AutoTokenizer.from_pretrained(
        MODELO_HF,
        do_lower_case=False,
        cache_dir=str(cache),
    )
    return _cache


def contar_tokens(
    texto: str,
    tokenizer: TokenizerLike | None = None,
    *,
    special: bool = True,
) -> int:
    tok = tokenizer if tokenizer is not None else carregar_tokenizer()
    ids = tok.encode(texto, add_special_tokens=special)
    return len(ids)


def faixa_n_tokens(n: int) -> str:
    """Baldes para PSI: curto / médio / longo."""
    if n < 12:
        return "curto"
    if n < 28:
        return "medio"
    return "longo"
