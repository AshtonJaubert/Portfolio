-- This SQL Provides insight of Yearly Imports and Exports of Over 100 different Countries From 1960 to 2021
-- Source: https://ourworldindata.org/trade-and-globalization 
-- Before I can ask questions about the data, I want to combine the Imports and Exports tables. And then Create a balance of Trade table.
SELECT Exports.Entity,imports.Year,imports.Imports,exports.Exports
FROM imports
LEFT JOIN exports ON imports.Entity = exports.Entity 
AND imports.Year = exports.Year; 

SELECT Entity,Year,Exports,Imports ,(Exports - Imports) as 'Balance Of Trade'
FROM totaltrade;

-- What are the top 10 Countries that have the highest Exports in total from 1960-2021? (have to exclude region values for more accurate results)
SELECT Entity, SUM(Exports)
FROM balanceoftrade
WHERE Entity NOT IN ('World','High-income Countries','Europe and Central Asia (WB)','European Union (27)','East Asia and Pacific (WB)','Middle-income countries','Upper-middle-income countries','North America (WB)','Lower-middle-income countries','Middle East and North Africa (WB)','Latin America and Caribbean (WB)','South Asia (WB)')
GROUP BY Entity
ORDER BY SUM(Exports) DESC
Limit 10;

-- What are the 10 Countries have the highest Balance of Trade in 1988?
SELECT Entity, Year, MAX(BalanceOfTrade) as 'Balance Of Trade'
FROM balanceoftrade
Where Year = '1988'
AND Entity NOT IN ('World','High-income Countries','Europe and Central Asia (WB)','European Union (27)','East Asia and Pacific (WB)','Middle-income countries','Upper-middle-income countries','North America (WB)','Lower-middle-income countries','Middle East and North Africa (WB)','Latin America and Caribbean (WB)','South Asia (WB)','Sub-Saharan Africa (WB)')
GROUP BY Entity
ORDER BY MAX(BalanceOfTrade) DESC
Limit 10;

-- What 5 Countries had the lowest Imports from 2010-2015?
SELECT Entity, SUM(Imports) as 'Balance Of Trade'
FROM balanceoftrade
WHERE Entity NOT IN ('World','High-income Countries','Europe and Central Asia (WB)','European Union (27)','East Asia and Pacific (WB)','Middle-income countries','Upper-middle-income countries','North America (WB)','Lower-middle-income countries','Middle East and North Africa (WB)','Latin America and Caribbean (WB)','South Asia (WB)','Sub-Saharan Africa (WB)','low-income countries')
AND YEAR IN ('2010','2011','2012','2013','2014','2015')
GROUP BY Entity
ORDER BY 'Balance Of Trade' ASC
Limit 5;

-- What is the total imports,exports,and overall Balance Of Trade From each country from 1960-2021?
SELECT Entity, SUM(Imports) as Imports,SUM(Exports) as Exports, SUM(BalanceOfTrade) as BalanceOfTrade
FROM balanceoftrade
Where Entity NOT IN ('World','High-income Countries','Europe and Central Asia (WB)','European Union (27)','East Asia and Pacific (WB)','Middle-income countries','Upper-middle-income countries','North America (WB)','Lower-middle-income countries','Middle East and North Africa (WB)','Latin America and Caribbean (WB)','South Asia (WB)','Sub-Saharan Africa (WB)','low-income countries')
GROUP BY Entity
ORDER BY Entity ASC;

-- What was the total Global Exports in 1976?
SELECT Year,SUM(Exports) as Total_Exports
FROM balanceoftrade
WHERE Entity NOT IN ('World','High-income Countries','Europe and Central Asia (WB)','European Union (27)','East Asia and Pacific (WB)','Middle-income countries','Upper-middle-income countries','North America (WB)','Lower-middle-income countries','Middle East and North Africa (WB)','Latin America and Caribbean (WB)','South Asia (WB)','Sub-Saharan Africa (WB)','low-income countries')
AND Year = '1976';

-- what World Region has the worst trade Deficit in 2021?
SELECT Entity,Year, SUM(BalanceOfTrade) as BalanceOfTrade
FROM balanceoftrade
Where Entity IN ('Europe and Central Asia (WB)','East Asia and Pacific (WB)','North America (WB)','Middle East and North Africa (WB)','Latin America and Caribbean (WB)','South Asia (WB)','Sub-Saharan Africa (WB)')
AND Year = '2021'
GROUP BY Entity
ORDER BY SUM(BalanceOfTrade) ASC
Limit 1;
-- What Countries or Regions have a Average Balance Of Trade value that is negative?
SELECT Entity, AVG(BalanceOfTrade) as BalanceOfTrade
FROM balanceoftrade
WHERE BalanceOfTrade < -1
AND Entity NOT IN ('World','High-income Countries','Low-income Countries','Middle-income Countries')
Group by Entity;
-- In What Years did USA and China Exceed more than 1 Trillion Imports?
SELECT Entity, Year,Imports
FROM balanceoftrade
WHERE Entity IN ('China','United States')
AND Exports > 1000000000000
ORDER BY Imports;

-- What is the Average Balance Of Trade From the three Classes of Countries(High,Low,Middle-Income)
SELECT Entity,AVG(BalanceOfTrade) as 'AVG BOT'
FROM balanceoftrade
WHERE Entity IN ('High-income Countries','Low-income Countries','Middle-income Countries')
GROUP BY Entity
ORDER BY AVG(BalanceOfTrade) DESC;

