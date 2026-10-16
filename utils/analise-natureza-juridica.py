import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from globals import *

df_layout = pd.read_excel("database/layout/RAIS_vinculos_layout2020.xls", skiprows=3)
df_nat_layout = df_layout.loc[152:226, ["Categorias", "Valor na Fonte"]].dropna()

def categorizar_nat(cod):
    cod_str = str(cod).strip()
    if cod_str.startswith("1"):
        return "Administração Pública"
    elif cod_str.startswith("2"):
        return "Setor Privado Empresarial"
    elif cod_str.startswith("3"):
        return "Terceiro Setor / Sem Fins Lucrativos"
    elif cod_str.startswith("4"):
        return "Pessoas Físicas / Autônomos"
    else:
        return "Outros / Não Informado"

nat_map = dict(
    zip(
        df_nat_layout["Valor na Fonte"].astype(str).str.strip(),
        df_nat_layout["Valor na Fonte"].apply(categorizar_nat)
    )
)

categorias_ordem = [
    "Administração Pública",
    "Setor Privado Empresarial",
    "Terceiro Setor / Sem Fins Lucrativos",
    "Pessoas Físicas / Autônomos",
    "Outros / Não Informado"
]

RESULTADOS = []

serie_pcd_nat = (
    base.loc[(base["Tipo Deficiência - Código"] > 0) & (base["Ind Vínculo Ativo 31/12 - Código"] == 1), "Natureza Jurídica - Código"]
    .astype(str)
    .str.strip()
    .map(nat_map)
    .fillna("Outros / Não Informado")
)

serie_nao_pcd_nat = (
    base.loc[(base["Tipo Deficiência - Código"] == 0) & (base["Ind Vínculo Ativo 31/12 - Código"] == 1), "Natureza Jurídica - Código"]
    .astype(str)
    .str.strip()
    .map(nat_map)
    .fillna("Outros / Não Informado")
)

df_nat_pcds = (
    serie_pcd_nat.value_counts()
    .reindex(categorias_ordem, fill_value=0)
    .reset_index()
)
df_nat_pcds.columns = ["Natureza Jurídica", "Qtde"]

total_pcds_nat = df_nat_pcds["Qtde"].sum()
df_nat_pcds["Percentual(%)"] = (
    (df_nat_pcds["Qtde"] / total_pcds_nat * 100) if total_pcds_nat > 0 else 0.0
)

df_pcd_nat_chart = df_nat_pcds.copy()

df_nat_pcds.loc[len(df_nat_pcds)] = {
    "Natureza Jurídica": "Total",
    "Qtde": total_pcds_nat,
    "Percentual(%)": 100.0 if total_pcds_nat > 0 else 0.0,
}
df_nat_pcds["Percentual(%)"] = df_nat_pcds["Percentual(%)"].map("{:.2f}%".format)


df_nat_nao_pcds = (
    serie_nao_pcd_nat.value_counts()
    .reindex(categorias_ordem, fill_value=0)
    .reset_index()
)
df_nat_nao_pcds.columns = ["Natureza Jurídica", "Qtde"]

total_nao_pcds_nat = df_nat_nao_pcds["Qtde"].sum()
df_nat_nao_pcds["Percentual(%)"] = (
    (df_nat_nao_pcds["Qtde"] / total_nao_pcds_nat * 100)
    if total_nao_pcds_nat > 0
    else 0.0
)

df_nao_pcd_nat_chart = df_nat_nao_pcds.copy()

df_nat_nao_pcds.loc[len(df_nat_nao_pcds)] = {
    "Natureza Jurídica": "Total",
    "Qtde": total_nao_pcds_nat,
    "Percentual(%)": 100.0 if total_nao_pcds_nat > 0 else 0.0,
}
df_nat_nao_pcds["Percentual(%)"] = df_nat_nao_pcds["Percentual(%)"].map(
    "{:.2f}%".format
)

RESULTADOS.append(f"Total PCDs ativos por Natureza Jurídica:\n{df_nat_pcds.to_string(index=False)}")
RESULTADOS.append(f"\nTotal Não-PCDs ativos por Natureza Jurídica:\n{df_nat_nao_pcds.to_string(index=False)}")

salvar_latex("tabela_pcds_por_natureza_juridica", "Distribuição dos Vínculos Ativos de PCDs por Natureza Jurídica", df_nat_pcds)
salvar_latex("tabela_nao_pcds_por_natureza_juridica", "Distribuição dos Vínculos Ativos de Não-PCDs por Natureza Jurídica", df_nat_nao_pcds)
salvar_log("distribuicao_pcds_por_natureza_juridica", RESULTADOS)


plt.rcParams["font.sans-serif"] = "Arial"
fig, ax = plt.subplots(figsize=(9, 5), dpi=100)

categorias = df_pcd_nat_chart["Natureza Jurídica"].tolist()
x = np.arange(len(categorias))
largura = 0.35

rects1 = ax.bar(
    x - largura / 2,
    df_pcd_nat_chart["Percentual(%)"],
    largura,
    label="PCDs",
    color="#1B365D",
)
rects2 = ax.bar(
    x + largura / 2,
    df_nao_pcd_nat_chart["Percentual(%)"],
    largura,
    label="Não-PCDs",
    color="#8C9EFF",
)

ax.bar_label(rects1, fmt="%.1f%%", padding=3, fontsize=8, fontweight="bold")
ax.bar_label(rects2, fmt="%.1f%%", padding=3, fontsize=8)

ax.set_title(
    "Distribuição por Natureza Jurídica do Empregador: PCDs vs. Não-PCDs\nArapiraca - 2025",
    fontsize=11,
    fontweight="bold",
    pad=15,
    loc="left",
)
ax.set_ylabel("Proporção (%)", fontsize=9)
ax.set_xticks(x)
ax.set_xticklabels(categorias, fontsize=8, rotation=15, ha="right")
ax.legend(frameon=True, facecolor="white", edgecolor="none")

ax.yaxis.grid(True, linestyle="--", alpha=0.5, color="#cccccc")
ax.xaxis.grid(False)
ax.set_axisbelow(True)

for spine in ["top", "right", "left", "bottom"]:
    ax.spines[spine].set_color("#dddddd")

plt.tight_layout()

plt.savefig("outputs/figures/grafico_natureza_juridica_pcd_vs_naopcd.pdf", format="pdf", bbox_inches="tight")
plt.savefig("outputs/figures/grafico_natureza_juridica_pcd_vs_naopcd.png", format="png", dpi=300, bbox_inches="tight")
plt.show()