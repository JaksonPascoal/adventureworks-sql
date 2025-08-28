

import pyodbc
import pandas as pd
import matplotlib.pyplot as plt

# Conexao
server = 'JAKSONPASCOAL\SQLEXPRESS'
database = 'AdventureWorksDW2019'

cnxn_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

cnxn = pyodbc.connect(cnxn_string)

print("Conexão estabelecida com sucesso!")

# Query em uma variável de texto
query_top_produtos = """
SELECT TOP 5
    dp.EnglishProductName,
    dps.EnglishProductSubcategoryName,
    SUM(fis.OrderQuantity) AS QuantidadeVendida,
    SUM(fis.SalesAmount) AS ReceitaTotal
FROM
    dbo.FactInternetSales AS fis
JOIN
    dbo.DimProduct AS dp ON fis.ProductKey = dp.ProductKey
JOIN
    dbo.DimProductSubcategory AS dps ON dp.ProductSubcategoryKey = dps.ProductSubcategoryKey
GROUP BY
    dp.EnglishProductName,
    dps.EnglishProductSubcategoryName
ORDER BY
    ReceitaTotal DESC
"""

# Executar a query e criar o DataFrame
df_top_produtos = pd.read_sql(query_top_produtos, cnxn)
print("\nDataFrame criado com sucesso!")

# Exibir o início do DataFrame e fechar a conexão
print(df_top_produtos.head())

# Cria um gráfico de barras com os dados do DataFrame
plt.figure(figsize=(12, 8)) # Define o tamanho da figura
plt.barh(df_top_produtos['EnglishProductName'], df_top_produtos['ReceitaTotal'])

# Adiciona título e rótulos
plt.title('Top 5 Produtos por Receita', fontsize=16)
plt.xlabel('Receita Total', fontsize=12)
plt.ylabel('Produto', fontsize=12)

# Salvar e exibir o gráfico
plt.savefig('images/top_5_produtos.png')
plt.show()

# --- Análise 2: Top 10 Clientes ---

# 1. Query para os 10 clientes mais valiosos
query_top_clientes = """
SELECT TOP 10
    dc.FirstName + ' ' + dc.LastName AS NomeCompleto,
    SUM(fis.SalesAmount) AS ReceitaTotal
FROM
    dbo.FactInternetSales AS fis
JOIN
    dbo.DimCustomer AS dc ON fis.CustomerKey = dc.CustomerKey
GROUP BY
    dc.FirstName, dc.LastName
ORDER BY
    ReceitaTotal DESC
"""

# 2. Carregar os dados em um novo DataFrame
df_top_clientes = pd.read_sql(query_top_clientes, cnxn)
print("\nDataFrame com os 10 clientes mais valiosos criado com sucesso!")
print(df_top_clientes.head())

# 3. Criar o gráfico de barras
plt.figure(figsize=(12, 8))
plt.barh(df_top_clientes['NomeCompleto'], df_top_clientes['ReceitaTotal'])
plt.title('Top 10 Clientes por Receita', fontsize=16)
plt.xlabel('Receita Total', fontsize=12)
plt.ylabel('Cliente', fontsize=12)

# 4. Salvar o gráfico
plt.savefig('images/top_10_clientes.png')
plt.show()

# --- Análise 3: Vendas Mensais ---

# 1. Query para as vendas mensais
query_vendas_mensais = """
SELECT
    dd.EnglishMonthName,
    SUM(fis.SalesAmount) AS ReceitaMensal
FROM
    dbo.FactInternetSales AS fis
JOIN
    dbo.DimDate AS dd ON fis.OrderDateKey = dd.DateKey
WHERE
    dd.CalendarYear = 2013
GROUP BY
    dd.EnglishMonthName
ORDER BY
    dd.EnglishMonthName
"""

# 2. Carregar os dados em um novo DataFrame
df_vendas_mensais = pd.read_sql(query_vendas_mensais, cnxn)
print("\nDataFrame com as vendas mensais criado com sucesso!")
print(df_vendas_mensais.head())

# 3. Criar o gráfico de linhas
plt.figure(figsize=(12, 8))
plt.plot(df_vendas_mensais['EnglishMonthName'], df_vendas_mensais['ReceitaMensal'])
plt.title('Vendas Mensais (2013)', fontsize=16)
plt.xlabel('Mês', fontsize=12)
plt.ylabel('Receita Total', fontsize=12)

# 4. Salvar o gráfico
plt.savefig('images/vendas_mensais.png')
plt.show()

cnxn.close()