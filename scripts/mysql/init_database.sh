#!/bin/bash
# MySQL Database Initialization Script
# This script helps verify and manage the beer database

set -e

MYSQL_HOST=${MYSQL_HOST:-mysql}
MYSQL_USER=${MYSQL_USER:-student}
MYSQL_PASSWORD=${MYSQL_PASSWORD:-student123}
MYSQL_DATABASE=${MYSQL_DATABASE:-beer_db}

echo "Waiting for MySQL to be ready..."
until mysql -h"$MYSQL_HOST" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" -e "SELECT 1" > /dev/null 2>&1; do
    sleep 2
done

echo "MySQL is ready!"

echo "Checking database tables..."
mysql -h"$MYSQL_HOST" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" <<-EOSQL
    SHOW TABLES;
    
    SELECT 'Beers count:' AS info, COUNT(*) AS count FROM beers;
    SELECT 'Breweries count:' AS info, COUNT(*) AS count FROM breweries;
    SELECT 'Categories count:' AS info, COUNT(*) AS count FROM categories;
    SELECT 'Styles count:' AS info, COUNT(*) AS count FROM styles;
EOSQL

echo "Database initialization complete!"

