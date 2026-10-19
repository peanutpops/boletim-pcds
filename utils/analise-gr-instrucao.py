import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from globals import *

RESULTADOS = []

df_layout = pd.read_excel("database/layout/RAIS_vinculos_layout2020.xls", skiprows=3)
df_gr_layout = df_layout.loc[81:91, ["Categorias", "Valor na Fonte"]].dropna()

graus = dict(
    zip(
        df_gr_layout["Valor na Fonte"].astype(int),
        df_gr_layout["Categorias"].astype(str).str.strip()
    )
)

graus_filtrados = {k: v for k, v in graus.items() if v not in ["MESTRADO", "DOUTORADO"]}
ordem_graus = list(graus_filtrados.keys())


df_gr_pcd = (
    DATAFRAME_PCD["Escolaridade Após 2005 - Código"]
    .astype(int)
    .value_counts()
    .reindex(ordem_graus, fill_value=0)
    .reset_index()
)

df_gr_pcd.columns = ["escolaridade", "qtde"]
df_gr_pcd["escolaridade"] = df_gr_pcd["escolaridade"].map(graus_filtrados)

total_pcd_gr = df_gr_pcd["qtde"].sum()
df_gr_pcd["percentual"] = (
    (df_gr_pcd["qtde"] / total_pcd_gr * 100) if total_pcd_gr > 0 else 0.0
)

df_pcd_gr_chart = df_gr_pcd.copy()

df_gr_pcd.loc[len(df_gr_pcd)] = {
    "escolaridade": "Total",
    "qtde": total_pcd_gr,
    "percentual": 100.0 if total_pcd_gr > 0 else 0.0,
}
df_gr_pcd["percentual"] = df_gr_pcd["percentual"].map("{:.2f}%".format)


df_gr_nao_pcd = (
    DATAFRAME_NAO_PCD["Escolaridade Após 2005 - Código"]
    .astype(int)
    .value_counts()
    .reindex(ordem_graus, fill_value=0)
    .reset_index()
)

df_gr_nao_pcd.columns = ["escolaridade", "qtde"]
df_gr_nao_pcd["escolaridade"] = df_gr_nao_pcd["escolaridade"].map(graus_filtrados)

total_nao_pcd_gr = df_gr_nao_pcd["qtde"].sum()
df_gr_nao_pcd["percentual"] = (
    (df_gr_nao_pcd["qtde"] / total_nao_pcd_gr * 100)
    if total_nao_pcd_gr > 0
    else 0.0
)

df_nao_pcd_gr_chart = df_gr_nao_pcd.copy()

df_gr_nao_pcd.loc[len(df_gr_nao_pcd)] = {
    "escolaridade": "Total",
    "qtde": total_nao_pcd_gr,
    "percentual": 100.0 if total_nao_pcd_gr > 0 else 0.0,
}
df_gr_nao_pcd["percentual"] = df_gr_nao_pcd["percentual"].map("{:.2f}%".format)


RESULTADOS.append(f"Distribuição por Escolaridade PCD:\n{df_gr_pcd.to_string(index=False)}")
RESULTADOS.append(f"\nDistribuição por Escolaridade Não-PCD:\n{df_gr_nao_pcd.to_string(index=False)}")

salvar_latex("tabela_pcds_por_grau_instrucao", "Distribuição por Grau de Instrução - PcD's", df_gr_pcd)
salvar_latex("tabela_nao_pcds_por_grau_instrucao", "Distribuição por Grau de Instrução - Não PcD's", df_gr_nao_pcd)
salvar_log("distribuicao_pcds_por_grau_instrucao", RESULTADOS)


df_chart = pd.merge(
    df_pcd_gr_chart[["escolaridade", "percentual"]],
    df_nao_pcd_gr_chart[["escolaridade", "percentual"]],
    on="escolaridade",
    suffixes=("_PCD", "_NAO_PCD")
)


# --- PLOTAGEM DO GRÁFICO DE BARRAS HORIZONTAIS AGRUPADAS ---
plt.rcParams["font.sans-serif"] = "Arial"
fig, ax = plt.subplots(figsize=(9, 5), dpi=100)

y = np.arange(len(df_chart))
altura = 0.38

rects1 = ax.barh(
    y - altura / 2,
    df_chart["percentual_PCD"],
    altura,
    label="PCDs",
    color="#1B365D"
)
rects2 = ax.barh(
    y + altura / 2,
    df_chart["percentual_NAO_PCD"],
    altura,
    label="Não-PCDs",
    color="#8C9EFF"
)

# Oculta rótulos zerados (0.0%)
labels_pcd = [f"{val:.1f}%" if val > 0 else "" for val in df_chart["percentual_PCD"]]
labels_nao_pcd = [f"{val:.1f}%" if val > 0 else "" for val in df_chart["percentual_NAO_PCD"]]

ax.bar_label(rects1, labels=labels_pcd, padding=3, fontsize=8, fontweight="bold")
ax.bar_label(rects2, labels=labels_nao_pcd, padding=3, fontsize=8)

# Títulos e Eixos
ax.set_title(
    "Distribuição por Grau de Instrução: PCDs vs. Não-PCDs\nArapiraca - 2025",
    fontsize=11,
    fontweight="bold",
    pad=15,
    loc="left"
)
ax.set_xlabel("Proporção (%)", fontsize=9)
ax.set_yticks(y)
ax.set_yticklabels(df_chart["escolaridade"], fontsize=8.5)
ax.invert_yaxis()  # Mantém do nível Analfabeto no topo até Superior Completo abaixo
ax.set_xlim(0, max(df_chart["percentual_PCD"].max(), df_chart["percentual_NAO_PCD"].max()) * 1.15)
ax.legend(frameon=True, facecolor="white", edgecolor="none", loc="lower right")

# Estilização de grid e bordas
ax.xaxis.grid(True, linestyle="--", alpha=0.5, color="#cccccc")
ax.yaxis.grid(False)
ax.set_axisbelow(True)

for spine in ["top", "right", "left", "bottom"]:
    ax.spines[spine].set_color("#dddddd")

plt.tight_layout()

# Salvando os arquivos do gráfico nas pastas do projeto
plt.savefig("outputs/figures/grafico_escolaridade_pcd_vs_naopcd.pdf", format="pdf", bbox_inches="tight")
plt.savefig("outputs/figures/grafico_escolaridade_pcd_vs_naopcd.png", format="png", dpi=300, bbox_inches="tight")
plt.show()