"""Arquivos do painel existem e o HTML não aponta para CDN."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUI = ROOT / "gui"


def test_vendor_simple_css_present():
    css = GUI / "vendor" / "simple-2.3.7.css"
    assert css.is_file()
    assert css.stat().st_size > 1000


def test_html_abas_e_api():
    html = (GUI / "index.html").read_text(encoding="utf-8")
    assert "vendor/simple-2.3.7.css" in html
    assert "cdn." not in html
    assert "unpkg" not in html
    assert "jsdelivr" not in html
    assert html.count('role="tab"') == 3
    assert "faixa-devops" in html
    assert "faixa-mlops" in html
    assert 'class="swagger"' in html
    assert "/tokens" in html
    assert 'swagger-vivo' in html
    js = (GUI / "painel.js").read_text(encoding="utf-8")
    assert "formula" in js
    assert '"/tokens"' in js or "api: \"/tokens\"" in js
    assert "/api/tokens" not in js
    assert "MAE" in js
    servico = (ROOT / "service.py").read_text(encoding="utf-8")
    assert "bentoml.service" in servico
    assert "class Painel" in servico
    for nome in ("tokens.json", "regressao.json", "imagens.json"):
        spec = GUI / "openapi" / nome
        assert spec.is_file()
        assert "openapi" in spec.read_text(encoding="utf-8")


def test_append_jsonl(tmp_path):
    from mlops_monitoramento.jsonl import append_jsonl, load_jsonl

    path = tmp_path / "a.jsonl"
    append_jsonl(path, {"n": 1})
    append_jsonl(path, {"n": 2})
    rows = load_jsonl(path)
    assert [r["n"] for r in rows] == [1, 2]
