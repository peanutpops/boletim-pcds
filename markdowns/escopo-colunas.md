# Lista de colunas totais da tabela
Bairros SP - Código
Bairros Fortaleza - Código
Bairros RJ - Código
Causa Afastamento 1 - Código
Causa Afastamento 2 - Código
Causa Afastamento 3 - Código
**Motivo Desligamento - Código**
**CBO 2002 Ocupação - Código**
**CNAE 2.0 Classe - Código**
CNAE 95 Classe - Código
Distritos SP - Código
**Ind Vínculo Ativo 31/12 - Código**
**Faixa Etária - Código**
Faixa Rem Média (SM) - Código
Faixa Hora Contrat - Código
Faixa Rem Dez (SM) - Código
Faixa Tempo Emprego - Código
**Escolaridade Após 2005 - Código**
Qtd Hora Contr
**Idade**
Ind CEI Vinculado - Código
Ind Estabelecimento Participante SIMPLES - Código
Mês Admissão - Código
Mês Desligamento - Código
Município Trab - Código
**Município - Código**
Nacionalidade - Código
**Natureza Jurídica - Código**
**Ind Portador Defic - Código**
Qtd Dias Afastamento
**Raça Cor - Código**
Região Adm DF - Código
Vl Rem Dezembro Nom
Vl Rem Dezembro (SM)
**Vl Rem Média Nom**
**Vl Rem Média (SM)**
**CNAE 2.0 Subclasse - Codigo**
**Sexo - Código**
**Tamanho Estabelecimento - Código**
Tempo Emprego
Tipo Admissão Trabalhador - Código
Tipo Estabelecimento - Código
Tipo Estabelecimento - Nome
**Tipo Deficiência - Código**
**Tipo Vínculo - Código**
IBGE Subsetor - Código
Vl Rem Janeiro SC
Vl Rem Fevereiro SC
Vl Rem Março SC
Vl Rem Abril SC
Vl Rem Maio SC
Vl Rem Junho SC
Vl Rem Julho SC
Vl Rem Agosto SC
Vl Rem Setembro SC
Vl Rem Outubro SC
Vl Rem Novembro SC
Ano Chegada Brasil
Ind Trabalho Intermitente - Código
Ind Trabalho Parcial - Código
Ind Vínculo Abandonado - Código
Categoria Trabalhador - Código

# Lista de Colunas em ordem de Escopo

## Intuitivas
- **Ind Portador Defic - Código**
- **Município - Código**

## De análise
- **Sexo - Código**
- **Idade**
- **Faixa Etária - Código**
- **Raça Cor - Código** 
- **Escolaridade Após 2005 - Código**
- **Tipo Deficiência - Código**
- **Tipo Vínculo - Código**
- **CBO 2002 Ocupação - Código** (O código de 6 dígitos que identifica a função/cargo exato exercido pelo trabalhador (ex: 422310 = Operador de Telemarketing, 411010 = Assistente Administrativo).)
- **Vl Rem Média Nom** (É o valor monetário exato em Reais (R$) da média salarial paga ao trabalhador durante os meses trabalhados em 2025.)
- **Vl Rem Média (SM)** (A remuneração média expressa em quantidade de salários mínimos vigentes no ano.)
- **CNAE 2.0 Classe - Código** (O código da atividade econômica principal do estabelecimento contratante (ex: Comércio Varejista, Serviços Hospitalares, Administração Pública).)
*Por que incluir:* Permite agrupar os trabalhadores por Setores Econômicos (Serviços, Comércio, Indústria, Construção) para ver qual setor da economia local é o mais inclusivo.
- **Ind Vínculo Ativo 31/12 - Código** (Indica se o trabalhador permanecia empregado no dia 31 de dezembro de 2025 (1 = Sim / Vínculo Ativo, 0 = Não / Desligado durante o ano).)
- **Motivo Desligamento - Código**
- **Tamanho Estabelecimento - Código** (A faixa de número de empregados do estabelecimento contratante (ex: até 4 vínculos, 10 a 19, 100 a 499, 500 ou mais).)
  *Por que incluir:* Essencial para analisar o impacto da Lei de Cotas. Permite verificar se o emprego PCD em Arapiraca está concentrado quase exclusivamente nas empresas obrigadas por lei (100+ funcionários) ou se Micro e Pequenas Empresas (MPEs) também estão contratando voluntariamente.

## A decidir
- **Natureza Jurídica - Código**
- **CNAE 2.0 Subclasse - Codigo**

```python
escopo_colunas = [
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
```