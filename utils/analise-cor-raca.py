import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from globals import *

RESULTADOS = []

# distribuição por sexo e raça entre pcds e não pcds
# por sexo
# pcds
sexos = {
    1: "Masculino",
    2: "Feminino"
}

contagem_sexo_pcd = DATAFRAME_PCD["Sexo - Código"].value_counts()

pcd_homens = contagem_sexo_pcd.get(1, 0)
pcd_mulheres = contagem_sexo_pcd.get(2, 0)

RESULTADOS.append(f"Homens PCD: {pcd_homens}")
RESULTADOS.append(f"Mulheres PCD: {pcd_mulheres}")
RESULTADOS.append(f"Porcentagens: Homens: {(pcd_homens * 100) / len(DATAFRAME_PCD):.2f}%. Mulheres: {(pcd_mulheres * 100) / len(DATAFRAME_PCD):.2f}%")

# não pcds
contagem_sexo_nao_pcd = DATAFRAME_NAO_PCD["Sexo - Código"].value_counts()

nao_pcd_homens = contagem_sexo_nao_pcd.get(1, 0)
nao_pcd_mulheres = contagem_sexo_nao_pcd.get(2, 0)

RESULTADOS.append(f"Homens não PCD's: {nao_pcd_homens}")
RESULTADOS.append(f"Mulheres não PCD's: {nao_pcd_mulheres}")
RESULTADOS.append(f"Porcentagens: Homens: {(nao_pcd_homens * 100) / len(DATAFRAME_NAO_PCD):.2f}%. Mulheres: {(nao_pcd_mulheres * 100) / len(DATAFRAME_NAO_PCD):.2f}%")

# por raça
racas = {
    8: "Parda",
    2: "Branca",
    4: "Preta",
    6: "Amarela",
    1: "Indígena",
    9: "Não identificado"
}

# pcds
df_racas_pcds = (
    DATAFRAME_PCD["Raça Cor - Código"]
    .value_counts()
    .reindex(racas.keys())
    .rename(index=racas)
    .rename("Total por Raça/Cor - PCD's")
)

# não pcds
df_racas_nao_pcds = (
    DATAFRAME_NAO_PCD["Raça Cor - Código"]
    .value_counts()
    .reindex(racas.keys())
    .rename(index=racas)
    .rename("Total por Raça/Cor - Não PCD's")
)

df_racas_pcds = (
    DATAFRAME_PCD["Raça Cor - Código"]
    .value_counts()
    .reindex(racas.keys(), fill_value=0)
    .reset_index()
)

df_racas_pcds.columns = ["Raça", "Qtde"]
df_racas_pcds["Raça"] = df_racas_pcds["Raça"].map(racas)

total_pcds_raca = df_racas_pcds["Qtde"].sum()
df_racas_pcds["Percentual(%)"] = (
    (df_racas_pcds["Qtde"] / total_pcds_raca * 100) if total_pcds_raca > 0 else 0.0
)

df_racas_pcds.loc[len(df_racas_pcds)] = {
    "Raça": "Total",
    "Qtde": total_pcds_raca,
    "Percentual(%)": 100.0 if total_pcds_raca > 0 else 0.0,
}

df_racas_pcds["Percentual(%)"] = df_racas_pcds["Percentual(%)"].map("{:.2f}%".format)


# tabelas
# --- TABELA DE RAÇA/COR (PCDs) ---
ordem_racas = [1, 2, 4, 6, 8, 9]

df_racas_pcds = (
    DATAFRAME_PCD["Raça Cor - Código"]
    .value_counts()
    .reindex(ordem_racas, fill_value=0)
    .reset_index()
)

df_racas_pcds.columns = ["raça", "qtde"]
df_racas_pcds["raça"] = df_racas_pcds["raça"].map(racas)

total_pcds_raca = df_racas_pcds["qtde"].sum()
df_racas_pcds["percentual"] = (
    (df_racas_pcds["qtde"] / total_pcds_raca * 100) if total_pcds_raca > 0 else 0.0
)

# Cria cópia dos dados sem o 'Total' para alimentar o gráfico
df_pcd_chart = df_racas_pcds.copy()

# Adiciona linha de Total para exportação da Tabela
df_racas_pcds.loc[len(df_racas_pcds)] = {
    "raça": "Total",
    "qtde": total_pcds_raca,
    "percentual": 100.0 if total_pcds_raca > 0 else 0.0,
}

df_racas_pcds["percentual"] = df_racas_pcds["percentual"].map("{:.2f}%".format)


# --- TABELA DE RAÇA/COR (NÃO PCDs) ---
df_racas_nao_pcds = (
    DATAFRAME_NAO_PCD["Raça Cor - Código"]
    .value_counts()
    .reindex(ordem_racas, fill_value=0)
    .reset_index()
)

df_racas_nao_pcds.columns = ["raça", "qtde"]
df_racas_nao_pcds["raça"] = df_racas_nao_pcds["raça"].map(racas)

total_nao_pcds_raca = df_racas_nao_pcds["qtde"].sum()
df_racas_nao_pcds["percentual"] = (
    (df_racas_nao_pcds["qtde"] / total_nao_pcds_raca * 100)
    if total_nao_pcds_raca > 0
    else 0.0
)

# Cria cópia dos dados sem o 'Total' para alimentar o gráfico
df_nao_pcd_chart = df_racas_nao_pcds.copy()

# Adiciona linha de Total para exportação da Tabela
df_racas_nao_pcds.loc[len(df_racas_nao_pcds)] = {
    "raça": "Total",
    "qtde": total_nao_pcds_raca,
    "percentual": 100.0 if total_nao_pcds_raca > 0 else 0.0,
}

df_racas_nao_pcds["percentual"] = df_racas_nao_pcds["percentual"].map(
    "{:.2f}%".format
)

# Exportações de arquivos
salvar_latex("tabela_pcds_por_raca", "Distribuição dos Vínculos Ativos por Raça - PCD's", df_racas_pcds)
salvar_latex("tabela_nao_pcds_por_raca", "Distribuição dos Vínculos Ativos por Raça - Não PCD's", df_racas_nao_pcds)
salvar_log("distribuicao_pcds_por_raca_cor", RESULTADOS)


# --- PLOTAGEM DO GRÁFICO (PCDs vs. NÃO-PCDs) ---
plt.rcParams["font.sans-serif"] = "Arial"
fig, ax = plt.subplots(figsize=(8, 4.5), dpi=100)

categorias = df_pcd_chart["raça"].tolist()
x = np.arange(len(categorias))
largura = 0.35

# Plotagem das duas séries de barras
rects1 = ax.bar(
    x - largura / 2,
    df_pcd_chart["percentual"],
    largura,
    label="PCDs",
    color="#1B365D",
)
rects2 = ax.bar(
    x + largura / 2,
    df_nao_pcd_chart["percentual"],
    largura,
    label="Não-PCDs",
    color="#8C9EFF",
)

# Rótulos de porcentagem sobre cada barra
ax.bar_label(rects1, fmt="%.1f%%", padding=3, fontsize=8, fontweight="bold")
ax.bar_label(rects2, fmt="%.1f%%", padding=3, fontsize=8)

# Títulos e eixos
ax.set_title(
    "Distribuição Racial no Mercado Formal: PCDs vs. Não-PCDs\nArapiraca - 2025",
    fontsize=11,
    fontweight="bold",
    pad=15,
    loc="left",
)
ax.set_ylabel("Proporção (%)", fontsize=9)
ax.set_xticks(x)
ax.set_xticklabels(categorias, fontsize=9)
ax.legend(frameon=True, facecolor="white", edgecolor="none")

# Estilização do grid
ax.yaxis.grid(True, linestyle="--", alpha=0.5, color="#cccccc")
ax.xaxis.grid(False)
ax.set_axisbelow(True)

for spine in ["top", "right", "left", "bottom"]:
    ax.spines[spine].set_color("#dddddd")

plt.tight_layout()

# Salvando o gráfico
plt.savefig(
    "outputs/figures/grafico_raca_pcd_vs_naopcd.pdf",
    format="pdf",
    bbox_inches="tight",
)
plt.savefig(
    "outputs/figures/grafico_raca_pcd_vs_naopcd.png",
    format="png",
    dpi=300,
    bbox_inches="tight",
)
plt.show()