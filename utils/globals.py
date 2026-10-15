import pandas as pd

FILEPATH = "database/rais2025_arapiraca.parquet"
COLUMNS = [
  "Sexo - Código", 
  "Idade",
  "Faixa Etária - Código",
  "Raça Cor - Código",
  "Escolaridade Após 2005 - Código",
  "Tipo Deficiência - Código",
  "Tipo Vínculo - Código",
  "CBO 2002 Ocupação - Código",
  "Vl Rem Média Nom",
  "Vl Rem Média (SM)",
  "CNAE 2.0 Classe - Código",
  "Ind Vínculo Ativo 31/12 - Código",
  "Motivo Desligamento - Código",
  "Tamanho Estabelecimento - Código"
]

def salvar_log(nome_arquivo: str, resultados: list):
  for string in resultados:
      log_filepath = f"outputs/logs/{nome_arquivo}.txt"
      with open(log_filepath, "a", encoding="utf-8") as f:
          f.write(string + "\n")

  print(f"\n[OK] Resumo salvo com sucesso em: '{log_filepath}'")

def salvar_latex(nome_arquivo: str, legenda: str, dataframe: pd.DataFrame):
    df_temp = dataframe.copy()
    
    if "Percentual(%)" in df_temp.columns:
        df_temp["Percentual(%)"] = df_temp["Percentual(%)"].astype(str).str.replace("%", "\\%", regex=False)
    
    df_temp.to_latex(
        f"outputs/tables/{nome_arquivo}.tex",
        index=False,
        escape=False,
        column_format="lcr",
        caption=f"{legenda} (Arapiraca, 2025)",
        label=f"tab:{nome_arquivo}"
    )

base = pd.read_parquet(FILEPATH)

for col in base.columns:
    if pd.api.types.is_numeric_dtype(base[col]):
        continue

    s_clean = base[col].astype(str).str.replace(",", ".", regex=False).str.strip()

    converted = pd.to_numeric(s_clean, errors="coerce")

    if converted.notna().sum() > (0.5 * len(base)):
        base[col] = converted.fillna(0)
        if (base[col] % 1 == 0).all():
            base[col] = base[col].astype(int)

DATAFRAME_PCD = base.loc[
    (base["Tipo Deficiência - Código"] > 0) & 
    (base["Ind Vínculo Ativo 31/12 - Código"] == 1),
    COLUMNS
]

DATAFRAME_NAO_PCD = base.loc[
    (base["Tipo Deficiência - Código"] == 0) & 
    (base["Ind Vínculo Ativo 31/12 - Código"] == 1),
    COLUMNS
]
