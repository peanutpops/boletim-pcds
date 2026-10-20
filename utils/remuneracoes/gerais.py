import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from globals import *

RESULTADOS = []

df_nominal_pcd = DATAFRAME_PCD.loc[
    DATAFRAME_PCD["Vl Rem Média Nom"] > 0, "Vl Rem Média Nom"
]
df_sm_pcd = DATAFRAME_PCD.loc[
    DATAFRAME_PCD["Vl Rem Média (SM)"] > 0, "Vl Rem Média (SM)"
]

media_nominal_pcd = df_nominal_pcd.mean()
mediana_nominal_pcd = df_nominal_pcd.median()
media_sm_pcd = df_sm_pcd.mean()
mediana_sm_pcd = df_sm_pcd.median()


df_nominal_nao_pcd = DATAFRAME_NAO_PCD.loc[
    DATAFRAME_NAO_PCD["Vl Rem Média Nom"] > 0, "Vl Rem Média Nom"
]
df_sm_nao_pcd = DATAFRAME_NAO_PCD.loc[
    DATAFRAME_NAO_PCD["Vl Rem Média (SM)"] > 0, "Vl Rem Média (SM)"
]

media_nominal_nao_pcd = df_nominal_nao_pcd.mean()
mediana_nominal_nao_pcd = df_nominal_nao_pcd.median()
media_sm_nao_pcd = df_sm_nao_pcd.mean()
mediana_sm_nao_pcd = df_sm_nao_pcd.median()


RESULTADOS.append("--- INDICADORES SALARIAIS GERAIS ---")
RESULTADOS.append(
    f"PCDs     -> Média Nom: R$ {media_nominal_pcd:.2f} | Mediana Nom: R$ {mediana_nominal_pcd:.2f}"
)
RESULTADOS.append(
    f"PCDs     -> Média SM:  {media_sm_pcd:.2f} SM  | Mediana SM:  {mediana_sm_pcd:.2f} SM"
)
RESULTADOS.append(
    f"Não-PCDs -> Média Nom: R$ {media_nominal_nao_pcd:.2f} | Mediana Nom: R$ {mediana_nominal_nao_pcd:.2f}"
)
RESULTADOS.append(
    f"Não-PCDs -> Média SM:  {media_sm_nao_pcd:.2f} SM  | Mediana SM:  {mediana_sm_nao_pcd:.2f} SM"
)

df_rendimento = pd.DataFrame({
    "Métrica Salarial": [
        "Média Nominal (R$)",
        "Mediana Nominal (R$)",
        "Média (Salários Mínimos)",
        "Mediana (Salários Mínimos)"
    ],
    "PCDs": [
        f"R$ {media_nominal_pcd:.2f}",
        f"R$ {mediana_nominal_pcd:.2f}",
        f"{media_sm_pcd:.2f} SM",
        f"{mediana_sm_pcd:.2f} SM"
    ],
    "Não-PCDs": [
        f"R$ {media_nominal_nao_pcd:.2f}",
        f"R$ {mediana_nominal_nao_pcd:.2f}",
        f"{media_sm_nao_pcd:.2f} SM",
        f"{mediana_sm_nao_pcd:.2f} SM"
    ]
})

'''salvar_log("indicadores_salariais_gerais", RESULTADOS)
salvar_latex("tabela_indicadores_salariais", "Indicadores de Rendimento Médio e Mediano: PCDs vs. Não-PCDs", df_rendimento)'''

df_nom_pcd = DATAFRAME_PCD.loc[DATAFRAME_PCD["Vl Rem Média Nom"] > 0, "Vl Rem Média Nom"]
df_sm_pcd = DATAFRAME_PCD.loc[DATAFRAME_PCD["Vl Rem Média (SM)"] > 0, "Vl Rem Média (SM)"]

df_nom_nao_pcd = DATAFRAME_NAO_PCD.loc[DATAFRAME_NAO_PCD["Vl Rem Média Nom"] > 0, "Vl Rem Média Nom"]
df_sm_nao_pcd = DATAFRAME_NAO_PCD.loc[DATAFRAME_NAO_PCD["Vl Rem Média (SM)"] > 0, "Vl Rem Média (SM)"]

# Métrica
medias_nom = [df_nom_pcd.mean(), df_nom_nao_pcd.mean()]
medianas_nom = [df_nom_pcd.median(), df_nom_nao_pcd.median()]

medias_sm = [df_sm_pcd.mean(), df_sm_nao_pcd.mean()]
medianas_sm = [df_sm_pcd.median(), df_sm_nao_pcd.median()]

# --- PLOTAGEM ---
plt.rcParams["font.sans-serif"] = "Arial"
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5), dpi=100)

grupos = ["PCDs", "Não-PCDs"]
x = np.arange(len(grupos))
largura = 0.35

# Subplot 1: Rendimento Nominal (R$)
rects1 = ax1.bar(x - largura/2, medias_nom, largura, label="Média (R$)", color="#1B365D")
rects2 = ax1.bar(x + largura/2, medianas_nom, largura, label="Mediana (R$)", color="#8C9EFF")

ax1.bar_label(rects1, fmt="R$ %.2f", padding=3, fontsize=8, fontweight="bold")
ax1.bar_label(rects2, fmt="R$ %.2f", padding=3, fontsize=8)

ax1.set_title("Rendimento Média e Mediana Nominal (R$)", fontsize=10, fontweight="bold", pad=12, loc="left")
ax1.set_xticks(x)
ax1.set_xticklabels(grupos, fontsize=9)
ax1.set_ylabel("Valor (R$)", fontsize=9)
ax1.set_ylim(0, max(medias_nom) * 1.25)
ax1.legend(frameon=True, facecolor="white", edgecolor="none")
ax1.yaxis.grid(True, linestyle="--", alpha=0.5, color="#cccccc")

# Subplot 2: Rendimento em Salários Mínimos (SM)
rects3 = ax2.bar(x - largura/2, medias_sm, largura, label="Média (SM)", color="#1B365D")
rects4 = ax2.bar(x + largura/2, medianas_sm, largura, label="Mediana (SM)", color="#8C9EFF")

ax2.bar_label(rects3, fmt="%.2f SM", padding=3, fontsize=8, fontweight="bold")
ax2.bar_label(rects4, fmt="%.2f SM", padding=3, fontsize=8)

ax2.set_title("Rendimento em Salários Mínimos (SM)", fontsize=10, fontweight="bold", pad=12, loc="left")
ax2.set_xticks(x)
ax2.set_xticklabels(grupos, fontsize=9)
ax2.set_ylabel("Salários Mínimos (SM)", fontsize=9)
ax2.set_ylim(0, max(medias_sm) * 1.25)
ax2.legend(frameon=True, facecolor="white", edgecolor="none")
ax2.yaxis.grid(True, linestyle="--", alpha=0.5, color="#cccccc")

for ax in [ax1, ax2]:
    ax.xaxis.grid(False)
    ax.set_axisbelow(True)
    for spine in ["top", "right", "left", "bottom"]:
        ax.spines[spine].set_color("#dddddd")

plt.suptitle("Comparativo de Rendimento do Trabalho Formal: PCDs vs. Não-PCDs\nArapiraca - 2025", fontsize=11, fontweight="bold", y=1.03, x=0.08, ha="left")
plt.tight_layout()

# Salvando
plt.savefig("outputs/figures/grafico_remuneracao_geral_pcd_vs_naopcd.pdf", format="pdf", bbox_inches="tight")
plt.savefig("outputs/figures/grafico_remuneracao_geral_pcd_vs_naopcd.png", format="png", dpi=300, bbox_inches="tight")
plt.show()