# Regressão e KS

Um número `x` entra; a reta `ŷ = a·x + b` (ajustada só no baseline)
devolve um preço previsto. O log grava `x`, `y_obs`, `ŷ`, a faixa
`baixo` / `medio` / `alto`, o resíduo, a latência e se houve erro.

A janela recente manda `x` maior. A reta é a mesma; os `ŷ` ficam maiores.
O monitor calcula KS sobre `ŷ` e PSI sobre as faixas.

```bash
cd ~/mlops-monitoramento
uv run python exemplos/regressao/gerar_logs.py
uv run python exemplos/regressao/monitor.py
```

Relatório: `exemplos/regressao/logs/report_regressao.json`.
