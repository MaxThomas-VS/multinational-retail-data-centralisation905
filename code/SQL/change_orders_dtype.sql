SELECT MAX(LENGTH(CAST(card_number AS VARCHAR(99)))) AS max_card_number,
       MAX(LENGTH(store_code)) AS max_store_code,
	   MAX(LENGTH(product_code)) AS max_product_code
FROM orders_table

ALTER TABLE orders_table 
	ALTER COLUMN date_uuid TYPE UUID USING date_uuid::uuid,
    ALTER COLUMN user_uuid TYPE UUID USING user_uuid::uuid,
    ALTER COLUMN card_number TYPE VARCHAR(22),
	ALTER COLUMN store_code TYPE VARCHAR(12),
	ALTER COLUMN product_code TYPE VARCHAR(12),
	ALTER COLUMN product_quantity TYPE SMALLINT;
	