# Imagem e brilho

Uma imagem entra. O serviço lê o brilho médio dos pixels (escala 0–1) e
grava o balde `b0` / `b1` / `b2`, o rótulo `escuro` / `medio` / `claro`,
uma confiança, a latência e se houve erro.

A janela recente é mais escura. O monitor calcula PSI nos baldes e nos
rótulos, e KS no brilho contínuo.

```bash
cd ~/mlops-monitoramento
uv run python exemplos/imagens/gerar_logs.py
uv run python exemplos/imagens/monitor.py
```

Relatório: `exemplos/imagens/logs/report_imagens.json`.
