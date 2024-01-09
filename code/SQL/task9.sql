
SELECT year, AVG(time_diff) AS avg_time_diff FROM
(SELECT sales_timestamp - LAG(sales_timestamp) OVER (ORDER BY sales_timestamp) AS time_diff,
	   year
FROM
(SELECT TO_TIMESTAMP(year || ' ' || LPAD(month, 2, '0') || ' ' || LPAD(day, 2, '0') || ' ' || timestamp, 
				   'YYYYMMDDHH24:MI:ss') AT TIME ZONE 'UTC' AS sales_timestamp,
	   year
FROM dim_date_times
ORDER BY sales_timestamp) AS otf1) AS otf2
GROUP BY year
ORDER BY avg_time_diff DESC
LIMIT 5
