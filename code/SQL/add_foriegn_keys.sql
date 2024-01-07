/* The delete queries in here remove rows with keys that have no match between the orders_table and the linked tables.*/
SELECT * from orders_table
WHERE  NOT EXISTS (
   SELECT FROM dim_users
   WHERE  dim_users.user_uuid = orders_table.user_uuid
   );
   
DELETE FROM orders_table
WHERE  NOT EXISTS (
   SELECT FROM dim_users
   WHERE  dim_users.user_uuid = orders_table.user_uuid
   );
   
ALTER TABLE orders_table
ADD FOREIGN KEY (user_uuid) REFERENCES dim_users(user_uuid);


   
SELECT * from dim_card_details
WHERE  NOT EXISTS (
   SELECT FROM orders_table
   WHERE  dim_card_details.card_number = orders_table.card_number
   );
   
DELETE FROM orders_table
WHERE  NOT EXISTS (
   SELECT FROM dim_card_details
   WHERE  dim_card_details.card_number = orders_table.card_number
   );

ALTER TABLE orders_table
ADD FOREIGN KEY (card_number) REFERENCES dim_card_details(card_number);



ALTER TABLE orders_table
ADD FOREIGN KEY (date_uuid) REFERENCES dim_date_times(date_uuid);



ALTER TABLE orders_table
ADD FOREIGN KEY (product_code) REFERENCES dim_products(product_code);



ALTER TABLE orders_table
ADD FOREIGN KEY (store_code) REFERENCES dim_store_details(store_code);


