#%% 
import db_utils as dbu
import data_cleaning as dc
import data_extraction as de

#%%
connection = dbu.DatabaseConnector('local_credentials')

#%%
users = dc.clean_user_data()
print(users.info())
connection.upload_table(users, 'dim_users')

#%%
cards = dc.clean_credit_card_data()
print(cards.info())
connection.upload_table(cards, 'dim_card_details')

#%%
stores = dc.clean_stores_data()
print(stores.info())
connection.upload_table(stores, 'dim_store_details')

#%%
products = dc.clean_product_data()  
print(products.info())
connection.upload_table(products, 'dim_products')

#%%
orders = dc.clean_order_data()
print(orders.info())
connection.upload_table(orders, 'orders_table')

#%%
dates = dc.clean_dates()
print(dates.info())
connection.upload_table(dates, 'dim_date_times')

#%%
print(connection.list_db_tables())


# %%
