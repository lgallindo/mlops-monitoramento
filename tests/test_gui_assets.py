"""Arquivos do painel existem e o HTML não aponta para CDN."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUI = ROOT / "gui"


def test_vendor_simple_css_present():
    css = GUI / "vendor" / "simple-2.3.7.css"
    assert css.is_file()
    assert css.stat().st_size > 1000


def test_html_usa_vendor_local():
    html = (GUI / "index.html").read_text(encoding="utf-8")
    assert "vendor/simple-2.3.7.css" in html
    assert "cdn." not in html
    assert "unpkg" not in html
    assert "jsdelivr" not in html
