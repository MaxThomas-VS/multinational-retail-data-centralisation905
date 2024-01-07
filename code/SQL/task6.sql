SELECT ROUND(CAST(SUM(orders_table.product_quantity * dim_products.price_gbp) AS NUMERIC),2) AS total_sales,
	   year, month
FROM orders_table
JOIN
	dim_date_times ON dim_date_times.date_uuid = orders_table.date_uuid	  
JOIN 
	dim_products ON orders_table.product_code = dim_products.product_code
GROUP BY year, month
ORDER BY total_sales DESC
LIMIT 10
