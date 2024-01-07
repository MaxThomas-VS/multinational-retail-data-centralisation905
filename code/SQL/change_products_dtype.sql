ALTER TABLE dim_products
ADD weight_class VARCHAR(255);

UPDATE dim_products
SET weight_class = 
    CASE 
        WHEN weight_kg < 2 THEN 'Light'
        WHEN weight_kg >= 2 AND weight_kg < 40 THEN 'Mid_Sized'
        WHEN weight_kg >= 40 AND weight_kg < 140 THEN 'Heavy'
        WHEN weight_kg >= 140 THEN 'Truck_Required'
    END;
	
SELECT MAX(LENGTH(product_code)) AS max_pc,
       MAX(LENGTH(ean)) AS max_ean,
       MAX(LENGTH(weight_class)) AS max_wc
FROM dim_products;
	
ALTER TABLE dim_products
	ALTER COLUMN price_gbp TYPE FLOAT,
	ALTER COLUMN product_name TYPE VARCHAR(255),
	ALTER COLUMN weight_kg TYPE FLOAT,
	ALTER COLUMN ean TYPE VARCHAR(17),
	ALTER COLUMN product_code TYPE VARCHAR(11),
	ALTER COLUMN date_added TYPE DATE,
	ALTER COLUMN uuid TYPE UUID USING uuid::uuid,
	ALTER COLUMN still_available TYPE BOOL USING still_available::boolean,
	ALTER COLUMN weight_class TYPE VARCHAR(14)

