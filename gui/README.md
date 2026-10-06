# Painel lado a lado

Uma página. Três colunas: tokens, regressão, imagens. Lê
`exemplos/*/logs/report_*.json` gerados por `just monitor`.

```bash
cd ~/mlops-monitoramento
just monitor || true
just painel
```

Abre `http://127.0.0.1:8765/gui/`. Porta: `PAINEL_PORTA` (padrão 8765).

Sem os JSON, cada coluna pede `just monitor`. Recarrega sozinho a cada 5 s.
CSS/JS de terceiros estão em `vendor/` (ver `vendor/PROVENIENCIA.md`).
