/* Painel: lê os três report_*.json e preenche as colunas. */

const FONTES = {
  tokens: {
    url: "/exemplos/tokens/logs/report_tokens.json",
    corpo: "corpo-tokens",
    estado: "estado-tokens",
    linhas: (r) => [
      ["n baseline", r.n_baseline, false],
      ["n recente", r.n_recente, false],
      ["PSI n_tokens", r.psi_n_tokens_bin, r.alert_prompt_mix],
      ["p95 ms", r.latency_p95_ms, r.alert_latency],
      ["error_rate", r.error_rate, false],
    ],
  },
  regressao: {
    url: "/exemplos/regressao/logs/report_regressao.json",
    corpo: "corpo-regressao",
    estado: "estado-regressao",
    linhas: (r) => [
      ["n baseline", r.n_baseline, false],
      ["n recente", r.n_recente, false],
      ["KS ŷ", r.ks_y_hat, r.alert_ks_y_hat],
      ["PSI ŷ", r.psi_y_hat_bin, r.alert_psi_y_hat],
      ["p95 ms", r.latency_p95_ms, r.alert_latency],
      ["error_rate", r.error_rate, r.alert_errors],
    ],
  },
  imagens: {
    url: "/exemplos/imagens/logs/report_imagens.json",
    corpo: "corpo-imagens",
    estado: "estado-imagens",
    linhas: (r) => [
      ["n baseline", r.n_baseline, false],
      ["n recente", r.n_recente, false],
      ["PSI brilho", r.psi_input_brightness_bin, r.alert_input_drift],
      ["PSI rótulo", r.psi_pred_label, r.alert_pred_drift],
      ["KS brilho", r.ks_mean_brightness, r.alert_ks_brightness],
      ["p95 ms", r.latency_p95_ms, r.alert_latency],
      ["confiança média", r.confidence_mean, r.alert_low_confidence],
      ["error_rate", r.error_rate, r.alert_errors],
    ],
  },
};

function celula(texto) {
  const td = document.createElement("td");
  td.textContent = texto;
  return td;
}

function preencher(chave, dados, erro) {
  const cfg = FONTES[chave];
  const estado = document.getElementById(cfg.estado);
  const corpo = document.getElementById(cfg.corpo);
  corpo.replaceChildren();
  if (erro || !dados) {
    estado.textContent = "Sem relatório. Rode just monitor e recarregue.";
    estado.className = "estado ausente";
    return;
  }
  estado.textContent = "task " + String(dados.task);
  estado.className = "estado ok";
  for (const [nome, valor, alerta] of cfg.linhas(dados)) {
    const tr = document.createElement("tr");
    if (alerta) {
      tr.className = "alerta";
    }
    tr.append(celula(nome), celula(String(valor)), celula(alerta ? "sim" : "não"));
    corpo.append(tr);
  }
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

document.addEventListener("DOMContentLoaded", () => {
  const botao = document.querySelector('[data-acao="recarregar"]');
  botao.addEventListener("click", () => {
    carregarTodas();
  });
  carregarTodas();
  setInterval(carregarTodas, 5000);
});
