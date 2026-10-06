# ADR 0002 — Painel HTML lado a lado

- Status: superseded
- Superseded-by: ADR 0003
- Date: 2026-10-06T12:04:13Z
- Deciders: Lucas Gallindo

## Context

`monitor.py` em cada exemplo grava `report_*.json`. Faltava uma tela que
mostrasse tokens, regressão e imagens ao mesmo tempo.

## Decision

Uma página `gui/index.html` em três colunas, servida por
`gui/servidor.py` (`http.server` na raiz do clone, porta 8765). A página
lê os três `report_*.json`. CSS de terceiros: Simple.css 2.3.7 em
`gui/vendor/` (WEB-011, reuso dos bytes já assinados no CESAR). JS do
painel: `gui/painel.js`, sem CDN.

## Consequences

`just painel` sobe o servidor. Sem os JSON (`just monitor`), cada coluna
mostra ausência. Grafana, Prometheus e três páginas distintas ficam de
fora deste clone.
