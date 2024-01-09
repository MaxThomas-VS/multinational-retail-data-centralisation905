
/* Setup dim_date_times table */
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

/* Setup dim_card_details table */
SELECT MAX(LENGTH(CAST(card_number AS VARCHAR(99)))) AS max_cn,
       MAX(LENGTH(expiry_date)) AS max_ed,
       MAX(LENGTH(CAST(date_payment_confirmed AS VARCHAR(99)))) AS max_dpc
FROM dim_card_details;
	
ALTER TABLE dim_card_details
	ALTER COLUMN card_number TYPE VARCHAR(22),
	ALTER COLUMN expiry_date TYPE VARCHAR(5),
	ALTER COLUMN date_payment_confirmed TYPE DATE;

/* Setup orders_table table */
SELECT MAX(LENGTH(CAST(card_number AS VARCHAR(99)))) AS max_card_number,
       MAX(LENGTH(store_code)) AS max_store_code,
	   MAX(LENGTH(product_code)) AS max_product_code
FROM orders_table;

ALTER TABLE orders_table 
	ALTER COLUMN date_uuid TYPE UUID USING date_uuid::uuid,
    ALTER COLUMN user_uuid TYPE UUID USING user_uuid::uuid,
    ALTER COLUMN card_number TYPE VARCHAR(22),
	ALTER COLUMN store_code TYPE VARCHAR(12),
	ALTER COLUMN product_code TYPE VARCHAR(12),
	ALTER COLUMN product_quantity TYPE SMALLINT;

/* Setup dim_users table */
SELECT MAX(LENGTH(country_code)) AS max_country_code
FROM dim_users;

ALTER TABLE dim_users
	ALTER COLUMN first_name TYPE VARCHAR(255),
	ALTER COLUMN last_name TYPE VARCHAR(255),
	ALTER COLUMN date_of_birth TYPE DATE,
	ALTER COLUMN country_code TYPE VARCHAR(255),
	ALTER COLUMN user_uuid TYPE UUID USING user_uuid::uuid,
	ALTER COLUMN join_date TYPE DATE;

/* Setup dim_stores table */
SELECT MAX(LENGTH(store_code)) AS max_store_code,
       MAX(LENGTH(country_code)) AS max_country_code
FROM dim_store_details;

UPDATE dim_store_details
SET longitude = NULL, locality = 'Web', country_code = NULL
WHERE longitude = 'N/A';


ALTER TABLE dim_store_details
	ALTER COLUMN longitude TYPE FLOAT USING longitude::double precision,
	ALTER COLUMN latitude TYPE FLOAT USING latitude::double precision,
	ALTER COLUMN store_code TYPE VARCHAR(12),
	ALTER COLUMN staff_numbers TYPE SMALLINT USING staff_numbers::smallint,
	ALTER COLUMN opening_date TYPE DATE USING opening_date::date,
	ALTER COLUMN store_type TYPE VARCHAR(255),
	ALTER COLUMN store_type DROP NOT NULL,
	ALTER COLUMN country_code TYPE VARCHAR(2),
	ALTER COLUMN continent TYPE VARCHAR(255);

/* Setup dim_products table */
SELECT MAX(LENGTH(store_code)) AS max_store_code,
       MAX(LENGTH(country_code)) AS max_country_code
FROM dim_store_details;

UPDATE dim_store_details
SET longitude = NULL, locality = 'Web', country_code = NULL
WHERE address = 'N/A';

ALTER TABLE dim_store_details
	ALTER COLUMN longitude TYPE FLOAT USING longitude::double precision,
	ALTER COLUMN latitude TYPE FLOAT USING latitude::double precision,
	ALTER COLUMN store_code TYPE VARCHAR(12),
	ALTER COLUMN staff_numbers TYPE SMALLINT USING staff_numbers::smallint,
	ALTER COLUMN opening_date TYPE DATE USING opening_date::date,
	ALTER COLUMN store_type TYPE VARCHAR(255),
	ALTER COLUMN store_type DROP NOT NULL,
	ALTER COLUMN country_code TYPE VARCHAR(2),
	ALTER COLUMN continent TYPE VARCHAR(255);

/* Adds primary keys to all tables */
ALTER TABLE dim_card_details ADD PRIMARY KEY (card_number);

ALTER TABLE dim_date_times ADD PRIMARY KEY (date_uuid);

ALTER TABLE dim_products ADD PRIMARY KEY (product_code);

ALTER TABLE dim_store_details ADD PRIMARY KEY (store_code);

ALTER TABLE dim_users ADD PRIMARY KEY (user_uuid);

/* Adds foreign keys to orders_table */
/* The delete queries in here remove rows with keys that have no match between the orders_table and the linked tables.*/
DELETE FROM orders_table
WHERE  NOT EXISTS (
   SELECT FROM dim_users
   WHERE  dim_users.user_uuid = orders_table.user_uuid
   );
  
DELETE FROM orders_table
WHERE  NOT EXISTS (
   SELECT FROM dim_card_details
   WHERE  dim_card_details.card_number = orders_table.card_number
   );
 
ALTER TABLE orders_table
ADD FOREIGN KEY (user_uuid) REFERENCES dim_users(user_uuid);

ALTER TABLE orders_table
ADD FOREIGN KEY (card_number) REFERENCES dim_card_details(card_number);

ALTER TABLE orders_table
ADD FOREIGN KEY (date_uuid) REFERENCES dim_date_times(date_uuid);

ALTER TABLE orders_table
ADD FOREIGN KEY (product_code) REFERENCES dim_products(product_code);

ALTER TABLE orders_table
ADD FOREIGN KEY (store_code) REFERENCES dim_store_details(store_code);


