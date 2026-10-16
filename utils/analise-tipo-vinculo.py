import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from globals import *

# 1. Leitura e mapeamento de Tipos de Vínculo
df_layout = pd.read_excel("database/layout/RAIS_vinculos_layout2020.xls", skiprows=3)
df_layout_filtrado = df_layout.loc[288:306, ["Categorias", "Valor na Fonte"]].dropna()

tipos = dict(
    zip(
        df_layout_filtrado["Valor na Fonte"].astype(int),
        df_layout_filtrado["Categorias"].astype(str).str.strip()
    )
)

# 2. Contagens numéricas puras (SEM string / SEM Total)
df_pcd_vinc = (
    DATAFRAME_PCD["Tipo Vínculo - Código"]
    .astype(int)
    .value_counts()
    .reset_index()
)
df_pcd_vinc.columns = ["Tipo de Vínculo", "Qtde"]
df_pcd_vinc["Tipo de Vínculo"] = df_pcd_vinc["Tipo de Vínculo"].map(tipos)

total_pcd_vinc = df_pcd_vinc["Qtde"].sum()
df_pcd_vinc["Percentual(%)"] = (df_pcd_vinc["Qtde"] / total_pcd_vinc * 100) if total_pcd_vinc > 0 else 0.0


df_nao_pcd_vinc = (
    DATAFRAME_NAO_PCD["Tipo Vínculo - Código"]
    .astype(int)
    .value_counts()
    .reset_index()
)
df_nao_pcd_vinc.columns = ["Tipo de Vínculo", "Qtde"]
df_nao_pcd_vinc["Tipo de Vínculo"] = df_nao_pcd_vinc["Tipo de Vínculo"].map(tipos)

total_nao_pcd_vinc = df_nao_pcd_vinc["Qtde"].sum()
df_nao_pcd_vinc["Percentual(%)"] = (df_nao_pcd_vinc["Qtde"] / total_nao_pcd_vinc * 100) if total_nao_pcd_vinc > 0 else 0.0


# 3. MERGE NUMÉRICO APENAS DAS CATEGORIAS EXISTENTES (Outer Join)
df_merged_chart = pd.merge(
    df_pcd_vinc[["Tipo de Vínculo", "Percentual(%)"]],
    df_nao_pcd_vinc[["Tipo de Vínculo", "Percentual(%)"]],
    on="Tipo de Vínculo",
    how="outer",
    suffixes=("_PCD", "_NAO_PCD")
).fillna(0.0)

# 4. FILTRO ESTRITO: Elimina categoricamente qualquer linha onde AMBOS sejam 0.0%
df_merged_chart = df_merged_chart[
    (df_merged_chart["Percentual(%)_PCD"] > 0) | 
    (df_merged_chart["Percentual(%)_NAO_PCD"] > 0)
].reset_index(drop=True)

# Opcional: Filtra categorias irrelevantes (< 0.1% em ambos) para um gráfico super limpo
df_chart_final = df_merged_chart[
    (df_merged_chart["Percentual(%)_PCD"] >= 0.1) | 
    (df_merged_chart["Percentual(%)_NAO_PCD"] >= 0.1)
].sort_values(by="Percentual(%)_PCD", ascending=True).reset_index(drop=True)


# --- FORMATANDO AS TABELAS LATEX (ADICIONA O TOTAL APENAS AQUI) ---
df_pcd_vinc_tex = df_pcd_vinc.copy()
df_pcd_vinc_tex.loc[len(df_pcd_vinc_tex)] = {"Tipo de Vínculo": "Total", "Qtde": total_pcd_vinc, "Percentual(%)": 100.0}
df_pcd_vinc_tex["Percentual(%)"] = df_pcd_vinc_tex["Percentual(%)"].map("{:.2f}%".format)

df_nao_pcd_vinc_tex = df_nao_pcd_vinc.copy()
df_nao_pcd_vinc_tex.loc[len(df_nao_pcd_vinc_tex)] = {"Tipo de Vínculo": "Total", "Qtde": total_nao_pcd_vinc, "Percentual(%)": 100.0}
df_nao_pcd_vinc_tex["Percentual(%)"] = df_nao_pcd_vinc_tex["Percentual(%)"].map("{:.2f}%".format)

salvar_latex("tabela_pcds_por_tipo_vinculo", "Distribuição dos Vínculos Ativos por Tipo de Vínculo - PCDs", df_pcd_vinc_tex)
salvar_latex("tabela_nao_pcds_por_tipo_vinculo", "Distribuição dos Vínculos Ativos por Tipo de Vínculo - Não-PCDs", df_nao_pcd_vinc_tex)


# --- PLOTAGEM DO GRÁFICO LIMPO ---
plt.rcParams["font.sans-serif"] = "Arial"
fig, ax = plt.subplots(figsize=(9, 4.5), dpi=100)

y = np.arange(len(df_chart_final))
altura = 0.38

rects1 = ax.barh(y - altura / 2, df_chart_final["Percentual(%)_PCD"], altura, label="PCDs", color="#1B365D")
rects2 = ax.barh(y + altura / 2, df_chart_final["Percentual(%)_NAO_PCD"], altura, label="Não-PCDs", color="#8C9EFF")

# Esconde rótulos se o valor for exatamente 0 ou menor que 0.1%
labels_pcd = [f"{val:.1f}%" if val >= 0.1 else "" for val in df_chart_final["Percentual(%)_PCD"]]
labels_nao_pcd = [f"{val:.1f}%" if val >= 0.1 else "" for val in df_chart_final["Percentual(%)_NAO_PCD"]]

ax.bar_label(rects1, labels=labels_pcd, padding=3, fontsize=8, fontweight="bold")
ax.bar_label(rects2, labels=labels_nao_pcd, padding=3, fontsize=8)

ax.set_title("Distribuição por Tipo de Vínculo Empregatício: PCDs vs. Não-PCDs\nArapiraca - 2025", fontsize=11, fontweight="bold", pad=15, loc="left")
ax.set_xlabel("Proporção (%)", fontsize=9)
ax.set_yticks(y)
ax.set_yticklabels(df_chart_final["Tipo de Vínculo"], fontsize=9)
ax.set_xlim(0, max(df_chart_final["Percentual(%)_PCD"].max(), df_chart_final["Percentual(%)_NAO_PCD"].max()) * 1.15)
ax.legend(frameon=True, facecolor="white", edgecolor="none", loc="lower right")

ax.xaxis.grid(True, linestyle="--", alpha=0.5, color="#cccccc")
ax.yaxis.grid(False)
ax.set_axisbelow(True)

for spine in ["top", "right", "left", "bottom"]:
    ax.spines[spine].set_color("#dddddd")

plt.tight_layout()

plt.savefig("outputs/figures/grafico_tipo_vinculo_pcd_vs_naopcd.pdf", format="pdf", bbox_inches="tight")
plt.savefig("outputs/figures/grafico_tipo_vinculo_pcd_vs_naopcd.png", format="png", dpi=300, bbox_inches="tight")
plt.show()