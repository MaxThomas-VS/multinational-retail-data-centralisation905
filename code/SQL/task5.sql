SELECT store_type,
	   SUM(orders_table.product_quantity * dim_products.price_gbp) AS total_sales,
	   SUM(orders_table.product_quantity * dim_products.price_gbp) / 
	   (SELECT SUM(orders_table.product_quantity * dim_products.price_gbp)
		FROM orders_table
		JOIN
			dim_products ON orders_table.product_code = dim_products.product_code) AS pct_total
FROM orders_table
JOIN
	dim_store_details ON dim_store_details.store_code = orders_table.store_code	  
JOIN 
	dim_products ON orders_table.product_code = dim_products.product_code
GROUP BY store_type
ORDER BY total_sales DESC
	