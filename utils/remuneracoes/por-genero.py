import matplotlib.pyplot as plt
import numpy as np
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from globals import *

RESULTADOS = []

nominais_homens_pcds = DATAFRAME_PCD.loc[
    (DATAFRAME_PCD["Vl Rem Média Nom"] > 0) & (DATAFRAME_PCD["Sexo - Código"] == 1),
    "Vl Rem Média Nom"
]
nominais_mulheres_pcds = DATAFRAME_PCD.loc[
    (DATAFRAME_PCD["Vl Rem Média Nom"] > 0) & (DATAFRAME_PCD["Sexo - Código"] == 2),
    "Vl Rem Média Nom"
]

media_nominais_homens_pcds = nominais_homens_pcds.mean()
mediana_nominais_homens_pcds = nominais_homens_pcds.median()
media_nominais_mulheres_pcds = nominais_mulheres_pcds.mean()
mediana_nominais_mulheres_pcds = nominais_mulheres_pcds.median()

# Salários Mínimos
sm_homens_pcds = DATAFRAME_PCD.loc[
    (DATAFRAME_PCD["Vl Rem Média (SM)"] > 0) & (DATAFRAME_PCD["Sexo - Código"] == 1),
    "Vl Rem Média (SM)"
]
sm_mulheres_pcds = DATAFRAME_PCD.loc[
    (DATAFRAME_PCD["Vl Rem Média (SM)"] > 0) & (DATAFRAME_PCD["Sexo - Código"] == 2),
    "Vl Rem Média (SM)"
]

media_sm_homens_pcds = sm_homens_pcds.mean()
mediana_sm_homens_pcds = sm_homens_pcds.median()
media_sm_mulheres_pcds = sm_mulheres_pcds.mean()
mediana_sm_mulheres_pcds = sm_mulheres_pcds.median()


# --- SALÁRIOS NÃO-PCDs ---
# Nominais
nominais_homens_nao_pcds = DATAFRAME_NAO_PCD.loc[
    (DATAFRAME_NAO_PCD["Vl Rem Média Nom"] > 0) & (DATAFRAME_NAO_PCD["Sexo - Código"] == 1),
    "Vl Rem Média Nom"
]
nominais_mulheres_nao_pcds = DATAFRAME_NAO_PCD.loc[
    (DATAFRAME_NAO_PCD["Vl Rem Média Nom"] > 0) & (DATAFRAME_NAO_PCD["Sexo - Código"] == 2),
    "Vl Rem Média Nom"
]

media_nominais_homens_nao_pcds = nominais_homens_nao_pcds.mean()
mediana_nominais_homens_nao_pcds = nominais_homens_nao_pcds.median()
media_nominais_mulheres_nao_pcds = nominais_mulheres_nao_pcds.mean()
mediana_nominais_mulheres_nao_pcds = nominais_mulheres_nao_pcds.median()

# Salários Mínimos
sm_homens_nao_pcds = DATAFRAME_NAO_PCD.loc[
    (DATAFRAME_NAO_PCD["Vl Rem Média (SM)"] > 0) & (DATAFRAME_NAO_PCD["Sexo - Código"] == 1),
    "Vl Rem Média (SM)"
]
sm_mulheres_nao_pcds = DATAFRAME_NAO_PCD.loc[
    (DATAFRAME_NAO_PCD["Vl Rem Média (SM)"] > 0) & (DATAFRAME_NAO_PCD["Sexo - Código"] == 2),
    "Vl Rem Média (SM)"
]

media_sm_homens_nao_pcds = sm_homens_nao_pcds.mean()
mediana_sm_homens_nao_pcds = sm_homens_nao_pcds.median()
media_sm_mulheres_nao_pcds = sm_mulheres_nao_pcds.mean()
mediana_sm_mulheres_nao_pcds = sm_mulheres_nao_pcds.median()


# --- INCLUSÃO NA LISTA DE RESULTADOS ---
RESULTADOS.append("\n--- INDICADORES SALARIAIS POR GÊNERO (PCDs) ---")
RESULTADOS.append(f"Homens PCD   -> Média Nom: R$ {media_nominais_homens_pcds:.2f} | Mediana Nom: R$ {mediana_nominais_homens_pcds:.2f}")
RESULTADOS.append(f"Homens PCD   -> Média SM:  {media_sm_homens_pcds:.2f} SM  | Mediana SM:  {mediana_sm_homens_pcds:.2f} SM")
RESULTADOS.append(f"Mulheres PCD -> Média Nom: R$ {media_nominais_mulheres_pcds:.2f} | Mediana Nom: R$ {mediana_nominais_mulheres_pcds:.2f}")
RESULTADOS.append(f"Mulheres PCD -> Média SM:  {media_sm_mulheres_pcds:.2f} SM  | Mediana SM:  {mediana_sm_mulheres_pcds:.2f} SM")

RESULTADOS.append("\n--- INDICADORES SALARIAIS POR GÊNERO (NÃO-PCDs) ---")
RESULTADOS.append(f"Homens Não-PCD   -> Média Nom: R$ {media_nominais_homens_nao_pcds:.2f} | Mediana Nom: R$ {mediana_nominais_homens_nao_pcds:.2f}")
RESULTADOS.append(f"Homens Não-PCD   -> Média SM:  {media_sm_homens_nao_pcds:.2f} SM  | Mediana SM:  {mediana_sm_homens_nao_pcds:.2f} SM")
RESULTADOS.append(f"Mulheres Não-PCD -> Média Nom: R$ {media_nominais_mulheres_nao_pcds:.2f} | Mediana Nom: R$ {mediana_nominais_mulheres_nao_pcds:.2f}")
RESULTADOS.append(f"Mulheres Não-PCD -> Média SM:  {media_sm_mulheres_nao_pcds:.2f} SM  | Mediana SM:  {mediana_sm_mulheres_nao_pcds:.2f} SM")

# salvar_log("indicadores_salariais_por_genero", RESULTADOS)

plt.rcParams["font.sans-serif"] = "Arial"
fig, ax = plt.subplots(figsize=(8, 4.5), dpi=100)

categorias = ["PCDs", "Não-PCDs"]
x = np.arange(len(categorias))
largura = 0.35

# Mediana Nominal para Homens e Mulheres
medianas_homens = [
    DATAFRAME_PCD.loc[(DATAFRAME_PCD["Vl Rem Média Nom"] > 0) & (DATAFRAME_PCD["Sexo - Código"] == 1), "Vl Rem Média Nom"].median(),
    DATAFRAME_NAO_PCD.loc[(DATAFRAME_NAO_PCD["Vl Rem Média Nom"] > 0) & (DATAFRAME_NAO_PCD["Sexo - Código"] == 1), "Vl Rem Média Nom"].median()
]

medianas_mulheres = [
    DATAFRAME_PCD.loc[(DATAFRAME_PCD["Vl Rem Média Nom"] > 0) & (DATAFRAME_PCD["Sexo - Código"] == 2), "Vl Rem Média Nom"].median(),
    DATAFRAME_NAO_PCD.loc[(DATAFRAME_NAO_PCD["Vl Rem Média Nom"] > 0) & (DATAFRAME_NAO_PCD["Sexo - Código"] == 2), "Vl Rem Média Nom"].median()
]

rects1 = ax.bar(x - largura/2, medianas_homens, largura, label="Homens (Mediana)", color="#1B365D")
rects2 = ax.bar(x + largura/2, medianas_mulheres, largura, label="Mulheres (Mediana)", color="#972738")

ax.bar_label(rects1, fmt="R$ %.2f", padding=3, fontsize=8, fontweight="bold")
ax.bar_label(rects2, fmt="R$ %.2f", padding=3, fontsize=8)

ax.set_title("Mediana Salarial Nominal por Gênero: PCDs vs. Não-PCDs\nArapiraca - 2025", fontsize=11, fontweight="bold", pad=15, loc="left")
ax.set_ylabel("Mediana (R$)", fontsize=9)
ax.set_xticks(x)
ax.set_xticklabels(categorias, fontsize=9)
ax.set_ylim(0, max(max(medianas_homens), max(medianas_mulheres)) * 1.2)
ax.legend(frameon=True, facecolor="white", edgecolor="none")

ax.yaxis.grid(True, linestyle="--", alpha=0.5, color="#cccccc")
ax.xaxis.grid(False)
ax.set_axisbelow(True)

for spine in ["top", "right", "left", "bottom"]:
    ax.spines[spine].set_color("#dddddd")

plt.tight_layout()

plt.savefig("outputs/figures/grafico_remuneracao_por_genero.pdf", format="pdf", bbox_inches="tight")
plt.savefig("outputs/figures/grafico_remuneracao_por_genero.png", format="png", dpi=300, bbox_inches="tight")
plt.show()