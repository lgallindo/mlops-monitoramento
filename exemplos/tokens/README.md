# Contagem de tokens

Um pedido traz um texto em português. O tokenizer
`adalbertojunior/distilbert-portuguese-cased` parte o texto em IDs. O log
grava `n_tokens = len(tokenizer.encode(texto))`, a faixa
`curto` / `medio` / `longo`, a latência do `encode` e se houve erro.

A janela recente deste material é mensagem curta. O monitor calcula PSI
nessas faixas e p95 da latência.

Estudo: raiz do clone, [`README.md`](../../README.md) (aba Tokens no
painel). Enviar texto curto e depois uma frase longa; ler DevOps (p95) e
MLOps (PSI de `n_tokens`).

Na raiz do clone, se quiser só este par de logs:

```bash
uv run python exemplos/tokens/gerar_logs.py
uv run python exemplos/tokens/monitor.py
```

Relatório: `exemplos/tokens/logs/report_tokens.json`.
A primeira execução baixa o tokenizer para `hf-cache/` na raiz do clone.
