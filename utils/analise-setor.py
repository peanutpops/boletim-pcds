import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from globals import *

def mapear_grande_setor_cnae(codigo):
    cod_str = str(codigo).zfill(5)
    divisao = int(cod_str[:2]) if cod_str[:2].isdigit() else 0
    
    if 1 <= divisao <= 3:
        return "Agricultura, Pecuária e Serviços Relacionados"
    elif 5 <= divisao <= 9:
        return "Indústrias Extrativas"
    elif 10 <= divisao <= 33:
        return "Indústrias de Transformação"
    elif divisao == 35:
        return "Eletricidade e Gás"
    elif 36 <= divisao <= 39:
        return "Água, Esgoto e Gestão de Resíduos"
    elif 41 <= divisao <= 43:
        return "Construção Civil"
    elif 45 <= divisao <= 47:
        return "Comércio e Reparação de Veículos"
    elif 49 <= divisao <= 53:
        return "Transporte, Armazenamento e Correio"
    elif 55 <= divisao <= 56:
        return "Alojamento e Alimentação"
    elif 58 <= divisao <= 63:
        return "Informação e Comunicação"
    elif 64 <= divisao <= 66:
        return "Atividades Financeiras e Seguros"
    elif divisao == 68:
        return "Atividades Imobiliárias"
    elif 69 <= divisao <= 75:
        return "Atividades Profissionais e Científicas"
    elif 77 <= divisao <= 82:
        return "Serviços Administrativos e Complementares"
    elif divisao == 84:
        return "Administração Pública, Defesa e Seguridade Social"
    elif divisao == 85:
        return "Educação"
    elif 86 <= divisao <= 88:
        return "Saúde Humana e Serviços Sociais"
    elif 90 <= divisao <= 93:
        return "Artes, Cultura, Esporte e Recreação"
    elif 94 <= divisao <= 96:
        return "Outras Atividades de Serviços"
    elif divisao == 97:
        return "Serviços Domésticos"
    else:
        return "Outros / Não Identificado"

DATAFRAME_PCD["Setor Econômico"] = DATAFRAME_PCD["CNAE 2.0 Classe - Código"].apply(mapear_grande_setor_cnae)

df_setor_pcd = (
    DATAFRAME_PCD["Setor Econômico"]
    .value_counts()
    .reset_index()
)
df_setor_pcd.columns = ["Setor Econômico", "Qtde"]

df_setor_pcd = df_setor_pcd[df_setor_pcd["Qtde"] > 0].reset_index(drop=True)

total_pcd_setor = df_setor_pcd["Qtde"].sum()
df_setor_pcd["Percentual(%)"] = (
    (df_setor_pcd["Qtde"] / total_pcd_setor * 100) if total_pcd_setor > 0 else 0.0
)

df_chart = df_setor_pcd.sort_values(by="Percentual(%)", ascending=True).reset_index(drop=True)


# --- PLOTAGEM DO GRÁFICO DE DISPERSÃO (DOT PLOT / CLEVELAND) ---
plt.rcParams["font.sans-serif"] = "Arial"
fig, ax = plt.subplots(figsize=(9, 5.5), dpi=100)

y = np.arange(len(df_chart))

# Linhas horizontais de referência (da origem x=0 até o ponto)
ax.hlines(
    y=y, 
    xmin=0, 
    xmax=df_chart["Percentual(%)"], 
    color="#cccccc", 
    linestyle="--", 
    linewidth=1.2, 
    zorder=1
)

# Pontos da dispersão (Scatter Plot) na cor azul marinho institucional (#1B365D)
ax.scatter(
    df_chart["Percentual(%)"], 
    y, 
    color="#1B365D", 
    s=85, 
    zorder=2, 
    label="PCDs"
)

# Rótulos com o % e a quantidade absoluta ao lado de cada ponto
for i, (pct, val) in enumerate(zip(df_chart["Percentual(%)"], df_chart["Qtde"])):
    ax.text(
        pct + 0.6, 
        i, 
        f"{pct:.1f}% ({val})", 
        va="center", 
        fontsize=8.5, 
        fontweight="bold", 
        color="#1B365D"
    )

# Estilização dos eixos e títulos
ax.set_yticks(y)
ax.set_yticklabels(df_chart["Setor Econômico"], fontsize=8.5)
ax.set_title(
    "Distribuição do Emprego de PCDs por Setor Econômico (CNAE 2.0)\nArapiraca - 2025", 
    fontsize=11, 
    fontweight="bold", 
    pad=15, 
    loc="left"
)
ax.set_xlabel("Proporção de Trabalhadores PCDs (%)", fontsize=9)
ax.set_xlim(0, max(df_chart["Percentual(%)"].max() * 1.25, 10))

# Ajuste de linhas de grade
ax.xaxis.grid(True, linestyle="--", alpha=0.5, color="#cccccc")
ax.yaxis.grid(False)
ax.set_axisbelow(True)

for spine in ["top", "right", "left", "bottom"]:
    ax.spines[spine].set_color("#dddddd")

plt.tight_layout()

# Salva os arquivos do gráfico nas pastas do projeto
plt.savefig("outputs/figures/grafico_dispersao_setores_pcd.pdf", format="pdf", bbox_inches="tight")
plt.savefig("outputs/figures/grafico_dispersao_setores_pcd.png", format="png", dpi=300, bbox_inches="tight")
plt.show()