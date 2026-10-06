# Imagem e brilho

Uma imagem entra. O serviço lê o brilho médio dos pixels (escala 0–1) e
grava o balde `b0` / `b1` / `b2`, o rótulo `escuro` / `medio` / `claro`,
uma confiança, a latência e se houve erro.

A janela recente deste material é mais escura. O monitor calcula PSI nos
baldes e nos rótulos, e KS no brilho contínuo.

Estudo: raiz do clone, [`README.md`](../../README.md) (aba Imagens).
Enviar brilho `0.15`; ler PSI, KS e confiança média.

Na raiz do clone, se quiser só este par de logs:

```bash
uv run python exemplos/imagens/gerar_logs.py
uv run python exemplos/imagens/monitor.py
```

Relatório: `exemplos/imagens/logs/report_imagens.json`.
