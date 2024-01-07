
SELECT MAX(LENGTH(CAST(card_number AS VARCHAR(99)))) AS max_cn,
       MAX(LENGTH(expiry_date)) AS max_ed,
       MAX(LENGTH(CAST(date_payment_confirmed AS VARCHAR(99)))) AS max_dpc
FROM dim_card_details;
	
ALTER TABLE dim_card_details
	ALTER COLUMN card_number TYPE VARCHAR(22),
	ALTER COLUMN expiry_date TYPE VARCHAR(5),
	ALTER COLUMN date_payment_confirmed TYPE DATE;

