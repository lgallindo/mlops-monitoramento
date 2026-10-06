setup:
    uv sync --group dev
    just gerar
    just monitor || true
    just test

gerar:
    uv run python exemplos/tokens/gerar_logs.py
    uv run python exemplos/regressao/gerar_logs.py
    uv run python exemplos/imagens/gerar_logs.py

monitor:
    uv run python exemplos/tokens/monitor.py || true
    uv run python exemplos/regressao/monitor.py || true
    uv run python exemplos/imagens/monitor.py || true

test:
    uv run pytest -q

painel porta="3001":
    uv run bentoml serve service:Painel --host 127.0.0.1 --port {{porta}}

swagger porta="3001":
    @echo "http://127.0.0.1:{{porta}}/"
    xdg-open http://127.0.0.1:{{porta}}/ >/dev/null 2>&1 || true
