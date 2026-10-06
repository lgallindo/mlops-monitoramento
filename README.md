# Monitoramento de modelos — um repositório, três exemplos

Um pedido chega. O serviço responde. O log guarda **o que entrou**, **o que saiu**,
**quanto demorou** e **se quebrou**. Na semana seguinte você abre duas janelas
desse log — a de quando o modelo merecia confiança, e a de agora — e pergunta
se o mundo na frente do modelo ainda é o mesmo.

Este repositório ensina essa pergunta com quatro instrumentos:

| Instrumento | Olha para | Em uma frase |
| --- | --- | --- |
| **Latência** | tempo de cada pedido | “Quanto o usuário esperou?” |
| **p95** | a fila ordenada desses tempos | “95% dos pedidos terminaram até este valor; o resto é a cauda lenta.” |
| **PSI** | coisas que caem em **baldes** (escuro/médio/claro, prompt curto/longo) | “A fatia de cada balde mudou de uma janela para a outra?” |
| **KS** | coisas que são um **número contínuo** (preço previsto, brilho médio) | “As duas pilhas de números têm forma parecida?” |

Os quatro existem porque um único resumo mente. A média de tempo esconde os
cinco pedidos presos. A acurácia de ontem esconde que hoje a câmera escureceu.
O gráfico bonito da semana de treino esconde que o texto que chega agora é
só “ok” e “vlw”.

## Estatística do tamanho de um copo

Você **não** precisa lembrar da prova do teorema. Precisa saber **ordenar**,
**contar fatias** e **comparar duas listas**.

**Latência** é o relógio: `t_fim − t_início`, em milissegundos. Cada linha do
log tem a sua.

**p95** (percentil 95):

```text
# Variáveis:
# xs — lista de latency_ms da janela recente
# ys — xs ordenada do menor para o maior
# k  — posição a 95% do caminho nessa lista

ys ← ordenar(xs)
k  ← inteiro(0.95 × (tamanho(ys) − 1))
p95 ← ys[k]
```

Se o p95 sobe, a experiência ruim já chegou para muita gente, mesmo quando a
média ainda parece educada. O limiar (8 ms, 25 ms…) é **política da squad**,
combinada no `monitor.py`.

**PSI** (Population Stability Index — índice de estabilidade da população).
Nasceu em crédito: “a mistura de clientes mudou?”. Aqui: você parte o mundo
em baldes, conta a fração de cada balde no *baseline* (`pb`) e na janela
*recente* (`pr`), e soma:

```text
# Variáveis:
# pb — fração do balde no baseline
# pr — fração do mesmo balde na janela recente
# psi — soma sobre todos os baldes

psi ← Σ (pr − pb) × ln(pr / pb)
```

Mistura igual → PSI perto de 0. Mistura outra → PSI cresce. Neste repo o
alerta dispara em **0,2**. De novo: política, não lei da física.

**KS** (Kolmogorov–Smirnov de duas amostras). PSI precisa de baldes que
alguém inventou. KS trabalha com o número cru. Imagine duas escadas: cada
observação sobe um degrau de altura `1/n`. KS é o **maior vão vertical**
entre as duas escadas.

```text
# Variáveis:
# a, b — números do baseline e da janela recente
# sa, sb — as mesmas listas, ordenadas
# i, j — quantos pontos de cada lado já foram “passados”
# d — maior |i/n − j/m|

sa ← ordenar(a); sb ← ordenar(b)
n ← tamanho(sa); m ← tamanho(sb)
i ← 0; j ← 0; d ← 0
para cada valor distinto x na união das duas listas:
    avance i e j até cobrir todos os pontos ≤ x
    d ← máximo(d, |i/n − j/m|)
```

`d = 0` → as duas nuvens coincidem. `d` grande → uma nuvem mora noutro
pedaço da reta (preços previstos todos mais altos; imagens todas mais
escuras). Aqui o alerta dispara em **0,25**.

PSI e KS no mesmo log: PSI pergunta “os rótulos que inventamos mudaram de
proporção?”; KS pergunta “os números por baixo desses rótulos se
empurraram?”. Os dois podem acender juntos. Isso é didático, não um erro.

## O que o aluno já sabe é suficiente

- **ML lembrado pela metade:** um modelo é uma função `entrada → saída`
  que alguém congelou. Monitorar é olhar o **diário** dessa função, não
  retreinar na hora.
- **Classificação:** saída = nome de balde (`escuro`). Confiança neste
  material = um número heurístico no log, **não** uma probabilidade
  calibrada de prova.
- **Regressão:** saída = número (`ŷ` = preço previsto). KS entra aqui
  porque `ŷ` já vive numa reta.
- **Texto / LLM:** o modelo (e a fatura) fala em **tokens**, não em
  palavras. Contar tokens é o primeiro número honesto do log de NLP.

## Três exemplos no mesmo hábito

O hábito é sempre: gerar duas janelas JSONL → `monitor.py` imprime um
relatório → código de saída 1 se algum alerta acendeu.

### 1. Contagem de tokens (`exemplos/tokens/`)

Textos em português passam pelo tokenizer
`adalbertojunior/distilbert-portuguese-cased` (DistilBERT destilado do
BERTimbau, ~66M parâmetros — o menor encoder pt_BR estável que usamos
aqui). **Só o tokenizer é baixado**; a rede inteira fica de fora.

`n_tokens = len(tokenizer.encode(texto))`. O campo no JSONL copia o
formato de `teaching/mlops-cc02173-aula8/log_predict.py` (`n_tokens` por
pedido). A aula 8 contava pares CRF; aqui o número é o do WordPiece.

Janela recente vira mensagem curta (`ok`, `vlw`). PSI nos baldes
`curto/medio/longo` acende. p95 da latência do `encode` também entra no
relatório.

### 2. KS numa regressão (`exemplos/regressao/`)

`ŷ = a·x + b`, ajustado **só** no baseline (metragem → preço de
brinquedo). A janela recente manda `x` bem maior. A reta é a mesma; a
nuvem de `ŷ` caminha para a direita. **KS compara as duas nuvens de `ŷ`**.
PSI nos baldes `baixo/medio/alto` acompanha. Há linhas com `"error": true`
para o `error_rate` aparecer de verdade.

### 3. Drift em quem recebe imagem (`exemplos/imagens/`)

Imagem sintética → brilho médio → `{escuro, medio, claro}`. Igual ao
contrato de `teaching/mlops-monitor-imagem-processamento/`. PSI nos baldes
de brilho e de rótulo; **KS no brilho contínuo** (o número 0–1, sem
balde). Confiança média e taxa de erro vão no mesmo JSON.

## Como rodar

```bash
cd ~/mlops-monitoramento
just setup
```

`just setup` sincroniza o ambiente, gera os três pares de log, roda os
três monitores (código 1 = alerta, esperado nas janelas “doentes”) e os
testes.

Primeira vez em `exemplos/tokens/`: o tokenizer baixa para `hf-cache/`
(alguns megabytes de vocabulário, não os 66M da rede). Rede necessária
nessa etapa.

```bash
just gerar      # só os JSONL
just monitor    # só os relatórios em exemplos/*/logs/report_*.json
just test       # pytest, sem Hugging Face
```

Python 3.11+, [uv](https://docs.astral.sh/uv/), `just`.
