/* total_sales = sum( product_price * product_quantity )*/

SELECT ROUND(CAST(SUM(orders_table.product_quantity * dim_products.price_gbp) AS NUMERIC), 2) AS total_sales,
	   dim_date_times.month
FROM orders_table
JOIN 
	dim_products ON dim_products.product_code = orders_table.product_code
JOIN 
	dim_date_times ON dim_date_times.date_uuid = orders_table.date_uuid
GROUP BY
	dim_date_times.month
ORDER BY total_sales DESC, month
