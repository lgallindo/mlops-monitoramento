# Regressão e KS

Um número `x` entra; a reta `ŷ = a·x + b` (ajustada só no baseline)
devolve um preço previsto. O log grava `x`, `y_obs`, `ŷ`, a faixa
`baixo` / `medio` / `alto`, o resíduo, a latência e se houve erro.

A janela recente deste material manda `x` maior. A reta é a mesma; os
`ŷ` ficam maiores. O monitor calcula KS sobre `ŷ`, PSI sobre as faixas,
e MAE (média de `|y_obs − ŷ|`) só nas linhas que têm `y_obs`.

A taxa de falha conta `error = true` no log: o processo quebrou. O MAE
conta o desvio da reta quando existe rótulo. Sem `y_obs` no pedido, o
painel deixa `y_obs` e `residual` nulos e o MAE ignora a linha.

Estudo: raiz do clone, [`README.md`](../../README.md) (aba Regressão).
Enviar `x = 35`; `y observado` opcional para o MAE.

Na raiz do clone, se quiser só este par de logs:

```bash
uv run python exemplos/regressao/gerar_logs.py
uv run python exemplos/regressao/monitor.py
```

Relatório: `exemplos/regressao/logs/report_regressao.json`.
