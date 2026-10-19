import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from globals import *

RESULTADOS = []

faixas = {
    1: "10 A 14 anos",
    2: "15 A 17 anos",
    3: "18 A 24 anos",
    4: "25 A 29 anos",
    5: "30 A 39 anos",
    6: "40 A 49 anos",
    7: "50 A 64 anos"
}

ordem_faixas = list(faixas.keys())

df_faixa_pcd = (
    DATAFRAME_PCD["Faixa Etária - Código"]
    .value_counts()
    .reindex(ordem_faixas, fill_value=0)
    .reset_index()
)

df_faixa_pcd.columns = ["faixa", "qtde"]
df_faixa_pcd["faixa"] = df_faixa_pcd["faixa"].map(faixas)

total_pcd_faixa = df_faixa_pcd["qtde"].sum()
df_faixa_pcd["percentual"] = (
    (df_faixa_pcd["qtde"] / total_pcd_faixa * 100) if total_pcd_faixa > 0 else 0.0
)

df_pcd_faixa_chart = df_faixa_pcd.copy()

df_faixa_pcd.loc[len(df_faixa_pcd)] = {
    "faixa": "Total",
    "qtde": total_pcd_faixa,
    "percentual": 100.0 if total_pcd_faixa > 0 else 0.0,
}
df_faixa_pcd["percentual"] = df_faixa_pcd["percentual"].map("{:.2f}%".format)


df_faixa_nao_pcd = (
    DATAFRAME_NAO_PCD["Faixa Etária - Código"]
    .value_counts()
    .reindex(ordem_faixas, fill_value=0)
    .reset_index()
)

df_faixa_nao_pcd.columns = ["faixa", "qtde"]
df_faixa_nao_pcd["faixa"] = df_faixa_nao_pcd["faixa"].map(faixas)

total_nao_pcd_faixa = df_faixa_nao_pcd["qtde"].sum()
df_faixa_nao_pcd["percentual"] = (
    (df_faixa_nao_pcd["qtde"] / total_nao_pcd_faixa * 100)
    if total_nao_pcd_faixa > 0
    else 0.0
)

df_nao_pcd_faixa_chart = df_faixa_nao_pcd.copy()

df_faixa_nao_pcd.loc[len(df_faixa_nao_pcd)] = {
    "faixa": "Total",
    "qtde": total_nao_pcd_faixa,
    "percentual": 100.0 if total_nao_pcd_faixa > 0 else 0.0,
}
df_faixa_nao_pcd["percentual"] = df_faixa_nao_pcd["percentual"].map("{:.2f}%".format)


RESULTADOS.append(f"Distribuição por Faixa Etária PCD:\n{df_faixa_pcd.to_string(index=False)}")
RESULTADOS.append(f"\nDistribuição por Faixa Etária Não-PCD:\n{df_faixa_nao_pcd.to_string(index=False)}")

salvar_latex("tabela_pcds_por_faixa_etaria", "Distribuição por Faixa Etária - PCD's", df_faixa_pcd)
salvar_latex("tabela_nao_pcds_por_faixa_etaria", "Distribuição por Faixa Etária - Não PCD's", df_faixa_nao_pcd)
salvar_log("distribuicao_pcds_por_faixa_etaria", RESULTADOS)


# --- PLOTAGEM DO GRÁFICO (PCDs vs. NÃO-PCDs) ---
plt.rcParams["font.sans-serif"] = "Arial"
fig, ax = plt.subplots(figsize=(8.5, 4.5), dpi=100)

categorias = df_pcd_faixa_chart["faixa"].tolist()
x = np.arange(len(categorias))
largura = 0.35

# Plotagem das barras das duas séries (Azul Marinho e Azul Claro)
rects1 = ax.bar(
    x - largura / 2,
    df_pcd_faixa_chart["percentual"],
    largura,
    label="PCDs",
    color="#1B365D",
)
rects2 = ax.bar(
    x + largura / 2,
    df_nao_pcd_faixa_chart["percentual"],
    largura,
    label="Não-PCDs",
    color="#8C9EFF",
)

# Oculta rótulos zerados (0.0%) para evitar poluição visual
labels_pcd = [f"{val:.1f}%" if val > 0 else "" for val in df_pcd_faixa_chart["percentual"]]
labels_nao_pcd = [f"{val:.1f}%" if val > 0 else "" for val in df_nao_pcd_faixa_chart["percentual"]]

ax.bar_label(rects1, labels=labels_pcd, padding=3, fontsize=8, fontweight="bold")
ax.bar_label(rects2, labels=labels_nao_pcd, padding=3, fontsize=8)

# Títulos e formatação dos eixos
ax.set_title(
    "Distribuição por Faixa Etária no Mercado Formal: PCDs vs. Não-PCDs\nArapiraca - 2025",
    fontsize=11,
    fontweight="bold",
    pad=15,
    loc="left",
)
ax.set_ylabel("Proporção (%)", fontsize=9)
ax.set_xticks(x)
ax.set_xticklabels(categorias, fontsize=8.5)
ax.legend(frameon=True, facecolor="white", edgecolor="none")

# Estilização de grid e bordas
ax.yaxis.grid(True, linestyle="--", alpha=0.5, color="#cccccc")
ax.xaxis.grid(False)
ax.set_axisbelow(True)

for spine in ["top", "right", "left", "bottom"]:
    ax.spines[spine].set_color("#dddddd")

plt.tight_layout()

# Salvando os arquivos do gráfico nas pastas de outputs
plt.savefig("outputs/figures/grafico_faixa_etaria_pcd_vs_naopcd.pdf", format="pdf", bbox_inches="tight")
plt.savefig("outputs/figures/grafico_faixa_etaria_pcd_vs_naopcd.png", format="png", dpi=300, bbox_inches="tight")
plt.show()