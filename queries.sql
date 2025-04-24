 
SELECT productTitle, sold
FROM furniture
WHERE sold > (SELECT AVG(sold) FROM furniture);
