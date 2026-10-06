"""Painel: três APIs BentoML + estáticos do GUI (mesmo padrão da aula 02173)."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import bentoml
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "gui"))

from ingestao import pedido_imagem, pedido_regressao, pedido_tokens  # noqa: E402

RELATORIOS = {
    "tokens": ROOT / "exemplos/tokens/logs/report_tokens.json",
    "regressao": ROOT / "exemplos/regressao/logs/report_regressao.json",
    "imagens": ROOT / "exemplos/imagens/logs/report_imagens.json",
}

_estaticos = Starlette(
    routes=[
        Mount(
            "/gui",
            app=StaticFiles(directory=str(ROOT / "gui"), html=True),
            name="gui",
        ),
        Mount(
            "/exemplos",
            app=StaticFiles(directory=str(ROOT / "exemplos")),
            name="exemplos",
        ),
    ]
)


def _relatorio(chave: str) -> dict[str, Any]:
    path = RELATORIOS[chave]
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


@bentoml.service(name="painel-monitoramento", resources={"cpu": "1"})
@bentoml.asgi_app(_estaticos, path="/")
class Painel:
    @bentoml.api
    def tokens(self, texto: str) -> dict[str, Any]:
        pedido = pedido_tokens(texto)
        return {"pedido": pedido, "relatorio": _relatorio("tokens")}

    @bentoml.api
    def regressao(self, x: float, y_obs: float | None = None) -> dict[str, Any]:
        pedido = pedido_regressao(x, y_obs)
        return {"pedido": pedido, "relatorio": _relatorio("regressao")}

    @bentoml.api
    def imagens(self, brilho: float) -> dict[str, Any]:
        pedido = pedido_imagem(brilho)
        return {"pedido": pedido, "relatorio": _relatorio("imagens")}
