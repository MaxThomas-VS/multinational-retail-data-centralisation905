
SELECT MAX(LENGTH(month)) AS max_m,
       MAX(LENGTH(year)) AS max_y,
       MAX(LENGTH(day)) AS max_d,
       MAX(LENGTH(time_period)) AS max_tp
FROM dim_date_times;
	
ALTER TABLE dim_date_times
	ALTER COLUMN month TYPE VARCHAR(2),
	ALTER COLUMN year TYPE VARCHAR(4),
	ALTER COLUMN day TYPE VARCHAR(2),
	ALTER COLUMN time_period TYPE VARCHAR(10),
	ALTER COLUMN date_uuid TYPE UUID USING date_uuid::uuid;
