
-- Quais são os 10 clientes mais valiosos (maior receita total) e em quais cidades eles estão localizados?

SELECT TOP 10
    dc.EnglishEducation,
    dc.EnglishOccupation,
    dc.EmailAddress,
    dc.FirstName,
    dc.LastName,
    SUM(fis.SalesAmount) AS ReceitaTotal
FROM
    dbo.FactInternetSales AS fis
JOIN
    dbo.DimCustomer AS dc ON fis.CustomerKey = dc.CustomerKey
GROUP BY
    dc.EnglishEducation,
    dc.EnglishOccupation,
    dc.EmailAddress,
    dc.FirstName,
    dc.LastName
ORDER BY
    ReceitaTotal DESC