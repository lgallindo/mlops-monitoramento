"""PSI, KS, p95 — testes sem Hugging Face."""

from __future__ import annotations

from collections import Counter

from mlops_monitoramento.ks import alert_ks, ks_two_sample
from mlops_monitoramento.p95 import p95
from mlops_monitoramento.psi import alert_psi, population_stability_index
from mlops_monitoramento.regressao import ajustar, prever
from mlops_monitoramento.tokenizar import contar_tokens, faixa_n_tokens


def test_psi_identical_near_zero():
    h = Counter({"a": 10, "b": 10})
    assert population_stability_index(h, h) < 1e-9


def test_psi_shift_alerts():
    b = Counter({"claro": 80, "escuro": 20})
    r = Counter({"claro": 10, "escuro": 90})
    psi = population_stability_index(b, r)
    assert psi > 0.2
    assert alert_psi(psi)


def test_ks_identical_is_zero():
    xs = [1.0, 2.0, 3.0, 4.0]
    assert ks_two_sample(xs, xs) == 0.0


def test_ks_shift_alerts():
    a = [1.0, 2.0, 3.0, 4.0, 5.0]
    b = [20.0, 21.0, 22.0, 23.0, 24.0]
    d = ks_two_sample(a, b)
    assert d >= 0.25
    assert alert_ks(d)


def test_p95_sorted_order():
    xs = [float(i) for i in range(100)]
    assert p95(xs) == 94.0


def test_reta_recupera_inclinacao():
    xs = [1.0, 2.0, 3.0, 4.0]
    ys = [5.0, 7.0, 9.0, 11.0]
    reta = ajustar(xs, ys)
    assert abs(reta.a - 2.0) < 1e-9
    assert abs(reta.b - 3.0) < 1e-9
    assert abs(prever(reta, 10.0) - 23.0) < 1e-9


class _FakeTok:
    def encode(self, text: str, add_special_tokens: bool = True) -> list[int]:
        palavras = text.split()
        ids = list(range(len(palavras)))
        if add_special_tokens:
            return [101, *ids, 102]
        return ids


def test_contar_tokens_com_tokenizer_falso():
    n = contar_tokens("um dois tres", tokenizer=_FakeTok(), special=True)
    assert n == 5
    assert faixa_n_tokens(5) == "curto"
    assert faixa_n_tokens(20) == "medio"
    assert faixa_n_tokens(40) == "longo"
