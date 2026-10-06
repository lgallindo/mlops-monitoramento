# Painel

Uma aba por modelo. Em cada aba: formulário, faixa DevOps, faixa MLOps e,
no fim, o Swagger do BentoML (`/`).

```bash
cd ~/mlops-monitoramento
just monitor || true
just painel
```

`http://127.0.0.1:3001/gui/` · Swagger `http://127.0.0.1:3001/` ·
`just swagger`. Porta 3000 nesta máquina já está com outro Bento
(`predicao-demanda`). `just painel 3000` se ela estiver livre.

POST JSON (BentoML):

- `/tokens` `{ "texto": "…" }`
- `/regressao` `{ "x": 30, "y_obs": 90 }` — `y_obs` é o valor real medido
- `/imagens` `{ "brilho": 0.2 }` (0 a 1)

CSS em `vendor/` (`vendor/PROVENIENCIA.md`).
