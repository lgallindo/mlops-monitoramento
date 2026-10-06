/* Abas, GET dos relatórios, POST, cartões DevOps / MLOps. */

const F_JANELA =
  "# n_base — pedidos no baseline.jsonl (passado de referência)\n" +
  "# n_rec  — pedidos no recente.jsonl (o que chegou agora)\n" +
  "n_base = |baseline|\n" +
  "n_rec  = |recente|";

const F_P95 =
  "# tempos — latency_ms da recente, já ordenados do menor para o maior\n" +
  "# n_rec  — quantos tempos existem\n" +
  "# k      — posição 95% nessa lista\n" +
  "k ← inteiro(0,95 × (n_rec − 1))\n" +
  "p95 ← tempos[k]\n" +
  "# 95 em cada 100 pedidos foram mais rápidos que este valor.";

const F_ERR =
  "# falhas — pedidos com error = true (crash, timeout, 5xx)\n" +
  "# n_rec  — total de pedidos na recente\n" +
  "taxa_de_falha ← falhas / n_rec\n" +
  "# Mede o serviço. O modelo pode errar a resposta e isto continuar 0.";

const F_PSI =
  "# peso_antigo — fração desta fatia no baseline (ex.: 80 curtos / 100 = 0,80)\n" +
  "# peso_novo   — fração da mesma fatia na recente (ex.: 20 / 100 = 0,20)\n" +
  "# parcela     — (peso_novo − peso_antigo) × ln(peso_novo / peso_antigo)\n" +
  "# PSI         — soma das parcelas de todas as fatias\n" +
  "peso_antigo ← 80/100 = 0,80\n" +
  "peso_novo   ← 20/100 = 0,20\n" +
  "parcela     ← (0,20 − 0,80) × ln(0,20/0,80) ≈ 0,83\n" +
  "PSI         ← parcela_curto + parcela_médio + parcela_longo\n" +
  "# Alerta se PSI ≥ 0,2: a mistura de fatias mudou.";

const F_KS =
  "# F_antigo(t) — fração do baseline com valor ≤ t\n" +
  "# F_novo(t)   — fração da recente com valor ≤ t\n" +
  "# KS          — maior vão vertical entre as duas escadas\n" +
  "KS ← máximo |F_antigo(t) − F_novo(t)|\n" +
  "# 0 = mesma forma. Alerta se KS ≥ 0,25.";

const F_CONF =
  "# confidence_i — número em [0, 1] gravado no log\n" +
  "# n_rec        — pedidos na recente\n" +
  "confiança_média ← (soma de confidence_i) / n_rec";

const F_MAE =
  "# y_obs — valor real medido (só existe se o formulário trouxe o rótulo)\n" +
  "# y_hat — valor previsto pela reta ŷ = a·x + b\n" +
  "# n_rotulo — pedidos recentes com y_obs preenchido\n" +
  "# MAE — média de |y_obs − ŷ| nesses pedidos\n" +
  "MAE ← ( |11−10| + |10−12| ) / 2 = 1,5\n" +
  "# no exemplo: reais 11 e 10, previstos 10 e 12\n" +
  "# Sem y_obs no pedido, a linha não entra. Alerta se MAE ≥ 8.";

const FONTES = {
  tokens: {
    url: "/exemplos/tokens/logs/report_tokens.json",
    api: "/tokens",
    estado: "estado-tokens",
    devops: "corpo-devops-tokens",
    mlops: "corpo-mlops-tokens",
    metricas: (r) => ({
      devops: [
        {
          nome: "n baseline / n recente",
          valor: r.n_baseline + " / " + r.n_recente,
          alerta: false,
          desc: "Tamanho das duas janelas de log. Baseline = passado de referência. Recente = o que chegou agora.",
          formula: F_JANELA,
        },
        {
          nome: "p95 de latência (ms)",
          valor: r.latency_p95_ms,
          alerta: r.alert_latency,
          desc: "Depois de ordenar os tempos, o valor na posição 95%. A cauda lenta, não a média.",
          formula: F_P95,
        },
        {
          nome: "taxa de falha do serviço",
          valor: r.error_rate,
          alerta: false,
          desc: "Fração dos pedidos em que o código marcou error = true (crash, timeout). Não mede qualidade do tokenizer.",
          formula: F_ERR,
        },
      ],
      mlops: [
        {
          nome: "PSI de n_tokens",
          valor: r.psi_n_tokens_bin,
          alerta: r.alert_prompt_mix,
          desc: "Os textos novos são mais curtos ou mais longos que os do baseline? PSI alto = a mistura de fatias mudou.",
          formula: F_PSI,
        },
      ],
    }),
  },
  regressao: {
    url: "/exemplos/regressao/logs/report_regressao.json",
    api: "/regressao",
    estado: "estado-regressao",
    devops: "corpo-devops-regressao",
    mlops: "corpo-mlops-regressao",
    metricas: (r) => ({
      devops: [
        {
          nome: "n baseline / n recente",
          valor: r.n_baseline + " / " + r.n_recente,
          alerta: false,
          desc: "Tamanho das duas janelas de log.",
          formula: F_JANELA,
        },
        {
          nome: "p95 de latência (ms)",
          valor: r.latency_p95_ms,
          alerta: r.alert_latency,
          desc: "Cauda lenta da previsão. Tempo de software, não erro da reta.",
          formula: F_P95,
        },
        {
          nome: "taxa de falha do serviço",
          valor: r.error_rate,
          alerta: r.alert_errors,
          desc: "Pedidos em que o código quebrou (error = true). Se a reta errou o preço mas respondeu, isto continua baixo.",
          formula: F_ERR,
        },
      ],
      mlops: [
        {
          nome: "MAE (erro do modelo)",
          valor: r.mae == null ? "—" : r.mae,
          alerta: !!r.alert_mae,
          desc:
            "Média de |y observado − ŷ| só nos " +
            String(r.n_com_y_obs) +
            " pedidos recentes que trouxeram rótulo. Sem y observado no formulário, a linha não entra aqui.",
          formula: F_MAE,
        },
        {
          nome: "KS de ŷ",
          valor: r.ks_y_hat,
          alerta: r.alert_ks_y_hat,
          desc: "As previsões novas ainda têm a mesma forma que as do baseline? KS olha a lista inteira de ŷ, sem precisar de y observado.",
          formula: F_KS,
        },
        {
          nome: "PSI de ŷ",
          valor: r.psi_y_hat_bin,
          alerta: r.alert_psi_y_hat,
          desc: "As fatias baixo / médio / alto de ŷ mudaram de peso? PSI alto = o modelo está emitindo outra mistura de preços.",
          formula: F_PSI,
        },
      ],
    }),
  },
  imagens: {
    url: "/exemplos/imagens/logs/report_imagens.json",
    api: "/imagens",
    estado: "estado-imagens",
    devops: "corpo-devops-imagens",
    mlops: "corpo-mlops-imagens",
    metricas: (r) => ({
      devops: [
        {
          nome: "n baseline / n recente",
          valor: r.n_baseline + " / " + r.n_recente,
          alerta: false,
          desc: "Tamanho das duas janelas de log.",
          formula: F_JANELA,
        },
        {
          nome: "p95 de latência (ms)",
          valor: r.latency_p95_ms,
          alerta: r.alert_latency,
          desc: "Cauda lenta do classificador.",
          formula: F_P95,
        },
        {
          nome: "taxa de falha do serviço",
          valor: r.error_rate,
          alerta: r.alert_errors,
          desc: "Pedidos em que o código marcou error = true. Não é o erro de classificação.",
          formula: F_ERR,
        },
      ],
      mlops: [
        {
          nome: "PSI de brilho (entrada)",
          valor: r.psi_input_brightness_bin,
          alerta: r.alert_input_drift,
          desc: "As imagens novas são mais escuras ou mais claras que as do baseline?",
          formula: F_PSI,
        },
        {
          nome: "PSI de rótulo (saída)",
          valor: r.psi_pred_label,
          alerta: r.alert_pred_drift,
          desc: "O classificador passou a gritar «escuro» (ou «claro») com outra frequência?",
          formula: F_PSI,
        },
        {
          nome: "KS de brilho",
          valor: r.ks_mean_brightness,
          alerta: r.alert_ks_brightness,
          desc: "Mesma pergunta do PSI, na escala contínua 0–1, sem fatiar em baldes.",
          formula: F_KS,
        },
        {
          nome: "confiança média",
          valor: r.confidence_mean,
          alerta: r.alert_low_confidence,
          desc: "Média do campo confidence na recente. Cai quando o brilho fica no meio do caminho entre classes.",
          formula: F_CONF,
        },
      ],
    }),
  },
};

function el(tag, cls) {
  const node = document.createElement(tag);
  if (cls) {
    node.className = cls;
  }
  return node;
}

function cartao(m) {
  const art = el("article", m.alerta ? "metrica alerta" : "metrica");
  const cab = el("div", "metrica-cabeca");
  const h = el("h4");
  h.textContent = m.nome;
  const val = el("div", "valor");
  val.textContent = String(m.valor);
  cab.append(h, val);
  const selo = el("p", m.alerta ? "selo ligado" : "selo");
  selo.textContent = m.alerta ? "alerta" : "ok";
  const desc = el("p", "desc");
  desc.textContent = m.desc;
  const form = el("pre", "formula");
  form.textContent = m.formula;
  art.append(cab, selo, desc, form);
  return art;
}

function preencherGrupo(id, lista) {
  const caixa = document.getElementById(id);
  caixa.replaceChildren();
  for (const m of lista) {
    caixa.append(cartao(m));
  }
}

function preencher(chave, dados, erro, extra) {
  const cfg = FONTES[chave];
  const estado = document.getElementById(cfg.estado);
  if (erro || !dados || !dados.task) {
    estado.textContent = "Sem relatório. Rode just monitor.";
    estado.className = "estado ausente";
    document.getElementById(cfg.devops).replaceChildren();
    document.getElementById(cfg.mlops).replaceChildren();
    return;
  }
  let msg = "task " + String(dados.task);
  if (extra) {
    msg = extra + " · " + msg;
  }
  estado.textContent = msg;
  estado.className = "estado ok";
  const grupos = cfg.metricas(dados);
  preencherGrupo(cfg.devops, grupos.devops);
  preencherGrupo(cfg.mlops, grupos.mlops);
}

function mostrarUltimoRegressao(pedido) {
  const caixa = document.getElementById("ultimo-regressao");
  if (!caixa || !pedido) {
    return;
  }
  const yObs = pedido.y_obs;
  const temRotulo = yObs !== null && yObs !== undefined;
  const partes = [
    "último pedido " + pedido.request_id,
    "x = " + String(pedido.x),
    "ŷ previsto = " + String(pedido.y_hat),
  ];
  if (temRotulo) {
    partes.push("y observado = " + String(yObs));
    partes.push("resíduo y−ŷ = " + String(pedido.residual));
  } else {
    partes.push("y observado ausente → esta linha não entra no MAE");
  }
  caixa.hidden = false;
  caixa.textContent = partes.join(" · ");
}

async function carregarUma(chave) {
  const cfg = FONTES[chave];
  try {
    const resp = await fetch(cfg.url, { cache: "no-store" });
    if (!resp.ok) {
      preencher(chave, null, true);
      return;
    }
    preencher(chave, await resp.json(), false);
  } catch (_e) {
    preencher(chave, null, true);
  }
}

async function carregarTodas() {
  const stamp = document.getElementById("status-carga");
  stamp.textContent = "lendo…";
  await Promise.all(["tokens", "regressao", "imagens"].map(carregarUma));
  stamp.textContent = "atualizado " + new Date().toISOString();
}

function mostrarAba(chave) {
  document.querySelectorAll('[role="tab"]').forEach((btn) => {
    const on = btn.getAttribute("data-aba") === chave;
    btn.setAttribute("aria-selected", on ? "true" : "false");
  });
  document.querySelectorAll('[role="tabpanel"]').forEach((painel) => {
    painel.hidden = painel.id !== "painel-" + chave;
  });
}

async function enviar(chave, corpo) {
  const stamp = document.getElementById("status-carga");
  stamp.textContent = "enviando…";
  const resp = await fetch(FONTES[chave].api, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(corpo),
  });
  const dados = await resp.json();
  if (!resp.ok) {
    stamp.textContent = "erro: " + String(dados.erro || resp.status);
    return;
  }
  const rid = dados.pedido && dados.pedido.request_id;
  preencher(chave, dados.relatorio, false, rid ? "pedido " + rid : "");
  if (chave === "regressao") {
    mostrarUltimoRegressao(dados.pedido);
  }
  stamp.textContent = "atualizado " + new Date().toISOString();
}

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll('[role="tab"]').forEach((btn) => {
    btn.addEventListener("click", () => {
      mostrarAba(btn.getAttribute("data-aba"));
    });
  });

  document.getElementById("form-tokens").addEventListener("submit", (ev) => {
    ev.preventDefault();
    enviar("tokens", { texto: document.getElementById("campo-texto").value });
  });
  document.getElementById("form-regressao").addEventListener("submit", (ev) => {
    ev.preventDefault();
    const x = document.getElementById("campo-x").value;
    const y = document.getElementById("campo-y").value;
    const corpo = { x: Number(x) };
    if (y !== "") {
      corpo.y_obs = Number(y);
    }
    enviar("regressao", corpo);
  });
  document.getElementById("form-imagens").addEventListener("submit", (ev) => {
    ev.preventDefault();
    enviar("imagens", {
      brilho: Number(document.getElementById("campo-brilho").value),
    });
  });

  carregarTodas();
  setInterval(carregarTodas, 5000);
});
