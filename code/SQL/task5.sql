SELECT COUNT(orders_table.date_uuid) AS number_of_sales,
	   SUM(orders_table.product_quantity * dim_products*price_gbp) AS total_sales,
	   CASE 
	        WHEN dim_store_details.store_type = 'Web Portal' THEN 'Web'
		    ELSE 'Offline' 
	   END AS location
FROM orders_table
JOIN
	dim_store_details ON dim_store_details.store_code = orders_table.store_code
GROUP BY location
ORDER BY location DESC


+-------------+-------------+---------------------+
| store_type  | total_sales | percentage_total(%) |
+-------------+-------------+---------------------+
| Local       |  3440896.52 |               44.87 |
| Web portal  |  1726547.05 |               22.44 |
| Super Store |  1224293.65 |               15.63 |
| Mall Kiosk  |   698791.61 |                8.96 |
| Outlet      |   631804.81 |                8.10 |
+-------------+-------------+---------------------+

