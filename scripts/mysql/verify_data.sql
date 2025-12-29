-- Verification script for beer database
-- Run this to check if data is loaded correctly

USE beer_db;

-- Show all tables
SHOW TABLES;

-- Count records in each table
SELECT 'beers' AS table_name, COUNT(*) AS record_count FROM beers
UNION ALL
SELECT 'breweries', COUNT(*) FROM breweries
UNION ALL
SELECT 'categories', COUNT(*) FROM categories
UNION ALL
SELECT 'styles', COUNT(*) FROM styles
UNION ALL
SELECT 'geocodes', COUNT(*) FROM geocodes;

-- Sample queries
SELECT 
    b.name AS beer_name,
    br.name AS brewery_name,
    c.cat_name AS category,
    s.style_name AS style,
    b.abv
FROM beers b
LEFT JOIN breweries br ON b.brewery_id = br.id
LEFT JOIN categories c ON b.cat_id = c.id
LEFT JOIN styles s ON b.style_id = s.id
LIMIT 10;

-- Statistics
SELECT 
    AVG(abv) AS avg_abv,
    MIN(abv) AS min_abv,
    MAX(abv) AS max_abv,
    COUNT(*) AS total_beers
FROM beers
WHERE abv > 0;

