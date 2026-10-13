import pandas as pd
from pathlib import Path

ARQ = Path(r"database\RAIS_VINC_PUB_NORDESTE\RAIS_VINC_PUB_NORDESTE.COMT")
SEP, ENC = ",", "latin-1"
COL_MUN = "Município - Código"
COD_ARAPIRACA = "270030"

arapiraca = []
total = 0
for i, chunk in enumerate(pd.read_csv(ARQ, sep=SEP, encoding=ENC, dtype=str, chunksize=500_000)):
    mun = chunk[COL_MUN].str.strip()
    arap = chunk[mun == COD_ARAPIRACA]
    arapiraca.append(arap)
    total += len(chunk)
    print(f"bloco {i}: {total:,} linhas lidas | Arapiraca: {len(arap)}")

arap = pd.concat(arapiraca, ignore_index=True)
print(len(arap))

arap.to_parquet("rais2025_arapiraca.parquet", index=False)