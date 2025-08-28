

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

cnxn.close()