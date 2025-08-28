-- Objetivo: Identificar os 5 produtos mais vendidos por quantidade e receita.
-- Usaremos JOINs para conectar as tabelas de vendas, detalhes do produto e subcategoria.
-- Usaremos ORDER BY para ranquear os produtos.

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