SELECT country_code, count(country_code) AS total_no_stores
FROM dim_store_details
WHERE NOT address = 'N/A'
GROUP BY country_code
ORDER BY total_no_stores;
