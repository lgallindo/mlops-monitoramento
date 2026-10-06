# Contagem de tokens

Um pedido traz um texto em português. O tokenizer
`adalbertojunior/distilbert-portuguese-cased` parte o texto em IDs. O log
grava `n_tokens = len(tokenizer.encode(texto))`, a faixa
`curto` / `medio` / `longo`, a latência do `encode` e se houve erro.

A janela recente é mensagem curta (`ok`, `vlw`). O monitor calcula PSI
nessas faixas e p95 da latência.

```bash
cd ~/mlops-monitoramento
uv run python exemplos/tokens/gerar_logs.py
uv run python exemplos/tokens/monitor.py
```

Relatório: `exemplos/tokens/logs/report_tokens.json`.
A primeira execução baixa o tokenizer para `hf-cache/` na raiz do clone.
